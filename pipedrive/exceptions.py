class BaseError(Exception):
    def __init__(self, message, response, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.response = response


class ApiError(BaseError):
    """Base class for all API errors"""
    pass


class ConnectionError(ApiError):
    """Error when connecting to the API"""
    pass


class TimeoutError(ApiError):
    """Request timed out"""
    pass


class BadRequestError(ApiError):
    pass


class UnauthorizedError(ApiError):
    pass


class ForbiddenError(ApiError):
    pass


class NotFoundError(ApiError):
    pass


class GoneError(ApiError):
    pass


class UnsupportedMediaTypeError(ApiError):
    pass


class UnprocessableEntityError(ApiError):
    pass


class TooManyRequestsError(ApiError):
    pass


class InternalServerError(ApiError):
    pass


class NotImplementedError(ApiError):
    pass


class ServiceUnavailableError(ApiError):
    pass


class UnknownError(ApiError):
    pass
