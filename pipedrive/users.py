class Users:
    def __init__(self, client):
        self._client = client

    async def get_user(self, user_id, **kwargs):
        url = "users/{}".format(user_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_users(self, **kwargs):
        url = "users"
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_me(self, **kwargs):
        url = "users/me"
        return await self._client._get(self._client.BASE_URL + url, **kwargs)
