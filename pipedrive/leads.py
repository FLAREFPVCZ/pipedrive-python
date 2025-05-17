class Leads:
    def __init__(self, client):
        self._client = client

    async def get_lead(self, lead_id, **kwargs):
        url = "leads/{}".format(lead_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_leads(self, **kwargs):
        url = "leads"
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def create_lead(self, data, **kwargs):
        url = "leads"
        return await self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    async def update_lead(self, lead_id, data, **kwargs):
        url = "leads/{}".format(lead_id)
        return await self._client._patch(self._client.BASE_URL + url, json=data, **kwargs)

    async def delete_lead(self, lead_id, **kwargs):
        url = "leads/{}".format(lead_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)

    async def get_lead_details(self, lead_id, **kwargs):
        url = "leads/{}".format(lead_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def search_leads(self, params=None, **kwargs):
        url = "leads/search"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
