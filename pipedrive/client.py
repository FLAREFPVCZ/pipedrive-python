from urllib.parse import urlencode
import asyncio
import random
import time
from typing import Optional, Dict, Any, List, Tuple, Union

import aiohttp
from aiohttp.client_exceptions import ClientError, ServerTimeoutError, ClientConnectorError

from pipedrive import exceptions
from pipedrive.activities import Activities
from pipedrive.deals import Deals
from pipedrive.filters import Filters
from pipedrive.leads import Leads
from pipedrive.items import Items
from pipedrive.notes import Notes
from pipedrive.organizations import Organizations
from pipedrive.persons import Persons
from pipedrive.pipelines import Pipelines
from pipedrive.products import Products
from pipedrive.stages import Stages
from pipedrive.recents import Recents
from pipedrive.subscriptions import Subscriptions
from pipedrive.users import Users
from pipedrive.webhooks import Webhooks


class Client:
    BASE_URL = "https://api.pipedrive.com/api/v2/"
    
    # Default request timeout in seconds
    DEFAULT_TIMEOUT = 30
    
    # Default concurrency limit for batch operations
    DEFAULT_CONCURRENCY_LIMIT = 5
    
    # Default retry settings
    MAX_RETRIES = 3
    MIN_RETRY_DELAY = 0.1
    MAX_RETRY_DELAY = 10.0
    RETRY_FACTOR = 2.0
    RETRY_STATUS_CODES = {408, 429, 500, 502, 503, 504}
    
    # Methods that are safe to retry
    IDEMPOTENT_METHODS = {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}

    def __init__(
        self, 
        api_token=None,
        domain=None,
        timeout: Union[int, float, Tuple[int, int]] = DEFAULT_TIMEOUT,
        concurrency_limit: int = DEFAULT_CONCURRENCY_LIMIT,
        max_retries: int = MAX_RETRIES,
        tcp_connector_limit: Optional[int] = 100,
        tcp_connector_limit_per_host: Optional[int] = 0,  # 0 means no limit
    ):
        """
        Initialize the Pipedrive API client.
        
        Args:
            api_token: Pipedrive API token for authentication
            domain: Custom domain for API endpoint
            timeout: Request timeout in seconds (can be a tuple of (connect_timeout, read_timeout))
            concurrency_limit: Maximum number of concurrent requests for batch operations
            max_retries: Maximum number of retry attempts for failed requests
            tcp_connector_limit: Maximum number of connections (overall)
            tcp_connector_limit_per_host: Maximum number of connections per host
        """
        self.api_token = api_token
        self.session = None
        self.timeout = timeout
        self.concurrency_limit = concurrency_limit
        self.max_retries = max_retries
        self.tcp_connector_limit = tcp_connector_limit
        self.tcp_connector_limit_per_host = tcp_connector_limit_per_host
        self._semaphore = None  # Will be initialized in __aenter__
        
        # Initialize resource classes
        self.activities = Activities(self)
        self.deals = Deals(self)
        self.filters = Filters(self)
        self.leads = Leads(self)
        self.items = Items(self)
        self.notes = Notes(self)
        self.organizations = Organizations(self)
        self.persons = Persons(self)
        self.pipelines = Pipelines(self)
        self.products = Products(self)
        self.subscriptions = Subscriptions(self)
        self.recents = Recents(self)
        self.stages = Stages(self)
        self.users = Users(self)
        self.webhooks = Webhooks(self)

        if domain:
            if not domain.endswith("/"):
                domain += "/"
            self.BASE_URL = domain + "api/v2/"

    async def __aenter__(self):
        """Set up the client session when entering the context manager."""
        # Create a TCP connector with connection pooling
        connector = aiohttp.TCPConnector(
            limit=self.tcp_connector_limit,
            limit_per_host=self.tcp_connector_limit_per_host,
            enable_cleanup_closed=True,
        )
        
        # Create the client session with default headers and timeout
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers={
                "User-Agent": "pipedrive-python/1.0",
                "Accept": "application/json",
            },
        )
        
        # Initialize the semaphore for concurrency control
        self._semaphore = asyncio.Semaphore(self.concurrency_limit)
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the context manager."""
        if self.session:
            await self.session.close()
            self.session = None
        self._semaphore = None

    def set_api_token(self, api_token):
        """Set the API token for authentication."""
        self.api_token = api_token

    async def _get(self, url, params=None, **kwargs):
        """Send a GET request."""
        return await self._request("get", url, params=params, **kwargs)

    async def _post(self, url, **kwargs):
        """Send a POST request."""
        return await self._request("post", url, **kwargs)

    async def _put(self, url, **kwargs):
        """Send a PUT request."""
        return await self._request("put", url, **kwargs)

    async def _patch(self, url, **kwargs):
        """Send a PATCH request."""
        return await self._request("patch", url, **kwargs)

    async def _delete(self, url, **kwargs):
        """Send a DELETE request."""
        return await self._request("delete", url, **kwargs)

    async def batch_get(self, urls: List[str], params_list: Optional[List[Dict]] = None, **kwargs):
        """
        Execute multiple GET requests in parallel with concurrency control.
        
        Args:
            urls: List of URLs to request
            params_list: List of query parameters for each URL (optional)
            **kwargs: Additional arguments to pass to each request
            
        Returns:
            List of responses in the same order as the input URLs
        """
        if params_list is None:
            params_list = [None] * len(urls)
        
        if len(params_list) != len(urls):
            raise ValueError("params_list length must match urls length")
        
        # Create tasks for each request
        tasks = []
        for i, url in enumerate(urls):
            tasks.append(self._get(url, params=params_list[i], **kwargs))
        
        # Execute requests with gather for concurrency
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def paginate(self, url, params=None, limit_key="limit", start_key="start", 
                      items_key="data", total_key="additional_data.pagination.total_count", 
                      page_size=100, max_items=None, **kwargs):
        """
        Automatically handle pagination for GET requests.
        
        Args:
            url: Base URL to request
            params: Query parameters
            limit_key: Parameter name for page size
            start_key: Parameter name for offset/start
            items_key: Response key containing items
            total_key: Response key containing total count (dot notation for nested keys)
            page_size: Number of items per page
            max_items: Maximum number of items to retrieve (None for all)
            **kwargs: Additional arguments to pass to each request
            
        Returns:
            List of all items across pages
        """
        if params is None:
            params = {}
        
        all_items = []
        start = 0
        params[limit_key] = page_size
        
        while True:
            params[start_key] = start
            response = await self._get(url, params=params, **kwargs)
            
            # Extract items using the items_key
            items = response.get(items_key, [])
            if not items:
                break
                
            all_items.extend(items)
            
            # Check if we've reached the maximum number of items
            if max_items is not None and len(all_items) >= max_items:
                all_items = all_items[:max_items]
                break
                
            # Get total count using dot notation
            total = response
            for key in total_key.split('.'):
                if isinstance(total, dict):
                    total = total.get(key, {})
                else:
                    total = 0
                    break
            
            # If we've retrieved all items or there's no pagination info, break
            if not isinstance(total, (int, float)) or len(all_items) >= total:
                break
                
            start += len(items)
            
        return all_items

    async def _request(self, method, url, headers=None, params=None, retry_count=0, **kwargs):
        """
        Send an HTTP request with retry logic, error handling, and concurrency control.
        
        Args:
            method: HTTP method (get, post, put, delete, etc.)
            url: URL to request
            headers: Request headers
            params: Query parameters
            retry_count: Current retry attempt (used internally)
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Parsed response data
        """
        method = method.upper()
        _headers = {}
        _params = {}
        
        # Set up authentication with API token
        if self.api_token:
            _params["api_token"] = self.api_token
            
        # Merge with provided headers and params
        if headers:
            _headers.update(headers)
        if params:
            _params.update(params)
        
        # Create session if it doesn't exist (should only happen outside context manager)
        if not self.session:
            connector = aiohttp.TCPConnector(
                limit=self.tcp_connector_limit,
                limit_per_host=self.tcp_connector_limit_per_host,
            )
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            )
            
        try:
            # Use semaphore for concurrency control if available
            if self._semaphore:
                async with self._semaphore:
                    async with self.session.request(
                        method, url, headers=_headers, params=_params, **kwargs
                    ) as response:
                        return await self._parse(response, method, url, _headers, _params, retry_count, **kwargs)
            else:
                # Fallback if semaphore is not available (outside context manager)
                async with self.session.request(
                    method, url, headers=_headers, params=_params, **kwargs
                ) as response:
                    return await self._parse(response, method, url, _headers, _params, retry_count, **kwargs)
                    
        except (ClientError, asyncio.TimeoutError, ServerTimeoutError, ClientConnectorError) as e:
            # Handle network-related errors with retry logic
            if retry_count < self.max_retries and (method in self.IDEMPOTENT_METHODS or retry_count == 0):
                return await self._retry_request(method, url, headers, params, retry_count, e, **kwargs)
            
            # If we've exhausted retries or it's not safe to retry, raise appropriate exception
            if isinstance(e, asyncio.TimeoutError) or isinstance(e, ServerTimeoutError):
                raise exceptions.TimeoutError(f"Request timed out: {url}", None) from e
            elif isinstance(e, ClientConnectorError):
                raise exceptions.ConnectionError(f"Connection error: {url}", None) from e
            else:
                raise exceptions.ApiError(f"API request failed: {url}", None) from e

    async def _retry_request(self, method, url, headers, params, retry_count, exception, **kwargs):
        """
        Implement retry logic with exponential backoff.
        
        Args:
            method: HTTP method
            url: URL to request
            headers: Request headers
            params: Query parameters
            retry_count: Current retry attempt
            exception: The exception that triggered the retry
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Result of the retried request
        """
        retry_count += 1
        
        # Calculate backoff delay with jitter
        delay = min(
            self.MAX_RETRY_DELAY,
            self.MIN_RETRY_DELAY * (self.RETRY_FACTOR ** (retry_count - 1))
        )
        # Add jitter (±30%)
        jitter = delay * 0.3
        delay = delay + random.uniform(-jitter, jitter)
        
        # Log the retry (in a real implementation, use a proper logger)
        print(f"Retrying request to {url} after {delay:.2f}s (attempt {retry_count}/{self.max_retries})")
        
        # Wait before retrying
        await asyncio.sleep(delay)
        
        # Retry the request
        return await self._request(method, url, headers, params, retry_count, **kwargs)

    async def _parse(self, response, method, url, headers, params, retry_count, **kwargs):
        """
        Parse the response and handle errors.
        
        Args:
            response: aiohttp response object
            method: HTTP method used
            url: URL requested
            headers: Request headers
            params: Query parameters
            retry_count: Current retry attempt
            **kwargs: Additional arguments passed to the request
            
        Returns:
            Parsed response data
        """
        status_code = response.status
        content_type = response.headers.get("Content-Type", "")
        
        # Check if we should retry based on status code
        if status_code in self.RETRY_STATUS_CODES and retry_count < self.max_retries and method in self.IDEMPOTENT_METHODS:
            return await self._retry_request(method, url, headers, params, retry_count, None, **kwargs)
        
        # Parse response based on content type
        if "application/json" in content_type:
            r = await response.json()
        else:
            r = await response.text()
            return r

        # Handle error responses
        if not response.ok:
            error = None
            if isinstance(r, dict) and "error" in r:
                error = r["error"]
                
            # Map status codes to appropriate exceptions
            if status_code == 400:
                raise exceptions.BadRequestError(error, response)
            elif status_code == 401:
                raise exceptions.UnauthorizedError(error, response)
            elif status_code == 403:
                raise exceptions.ForbiddenError(error, response)
            elif status_code == 404:
                raise exceptions.NotFoundError(error, response)
            elif status_code == 408:
                raise exceptions.TimeoutError(error, response)
            elif status_code == 410:
                raise exceptions.GoneError(error, response)
            elif status_code == 415:
                raise exceptions.UnsupportedMediaTypeError(error, response)
            elif status_code == 422:
                raise exceptions.UnprocessableEntityError(error, response)
            elif status_code == 429:
                raise exceptions.TooManyRequestsError(error, response)
            elif status_code == 500:
                raise exceptions.InternalServerError(error, response)
            elif status_code == 501:
                raise exceptions.NotImplementedError(error, response)
            elif status_code == 503:
                raise exceptions.ServiceUnavailableError(error, response)
            else:
                raise exceptions.UnknownError(error, response)

        return r
