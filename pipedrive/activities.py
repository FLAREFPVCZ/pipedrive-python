class Activities:
    def __init__(self, client):
        self._client = client

    async def get_activity(self, activity_id, **kwargs):
        url = "activities/{}".format(activity_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_activities(self, params=None, **kwargs):
        url = "activities"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def create_activity(self, data, **kwargs):
        url = "activities"
        return await self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    async def update_activity(self, activity_id, data, **kwargs):
        url = "activities/{}".format(activity_id)
        return await self._client._put(self._client.BASE_URL + url, json=data, **kwargs)

    async def delete_activity(self, activity_id, **kwargs):
        url = "activities/{}".format(activity_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)

    async def get_activity_fields(self, params=None, **kwargs):
        url = "activityFields"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
