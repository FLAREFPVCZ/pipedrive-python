class Products:
    def __init__(self, client):
        self._client = client

    async def get_product(self, product_id, **kwargs):
        url = "products/{}".format(product_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_products(self, **kwargs):
        url = "products"
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def search_products(self, params=None, **kwargs):
        url = "products/search"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def create_product(self, data, **kwargs):
        url = "products"
        return await self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    async def update_product(self, product_id, data, **kwargs):
        url = "products/{}".format(product_id)
        return await self._client._put(self._client.BASE_URL + url, json=data, **kwargs)

    async def delete_product(self, product_id, **kwargs):
        url = "products/{}".format(product_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)

    async def get_product_deal(self, product_id, **kwargs):
        url = "products/{}/deals".format(product_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_product_fields(self, **kwargs):
        url = "productFields"
        return await self._client._get(self._client.BASE_URL + url, **kwargs)
