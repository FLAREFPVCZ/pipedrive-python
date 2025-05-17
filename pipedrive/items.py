class Items:
    def __init__(self, client):
        self._client = client

    async def get_item_search(self, params=None, **kwargs):
        url = "itemSearch"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
