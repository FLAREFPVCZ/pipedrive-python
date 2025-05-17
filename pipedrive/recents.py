class Recents:
    def __init__(self, client):
        self._client = client

    async def get_recent_changes(self, params=None, **kwargs):
        url = "recents"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
