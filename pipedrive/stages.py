class Stages:
    def __init__(self, client):
        self._client = client

    async def get_stage(self, stage_id, **kwargs):
        url = "stages/{}".format(stage_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_stages(self, params=None, **kwargs):
        url = "stages"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def get_stage_deals(self, stage_id, **kwargs):
        url = "stages/{}/deals".format(stage_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def create_stage(self, data, **kwargs):
        url = "stages"
        return await self._client._post(self._client.BASE_URL + url, data, **kwargs)

    async def update_stage(self, stage_id, data, **kwargs):
        url = "stages/{}".format(stage_id)
        return await self._client._put(self._client.BASE_URL + url, data, **kwargs)

    async def delete_stage(self, stage_id, **kwargs):
        url = "stages/{}".format(stage_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)
