class Organizations:
    def __init__(self, client):
        self._client = client

    async def get_organization(self, organization_id, **kwargs):
        url = "organizations/{}".format(organization_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_organizations(self, params=None, **kwargs):
        url = "organizations"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def create_organization(self, data, **kwargs):
        url = "organizations"
        return await self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    async def update_organization(self, organization_id, data, **kwargs):
        url = "organizations/{}".format(organization_id)
        return await self._client._put(self._client.BASE_URL + url, json=data, **kwargs)

    async def delete_organization(self, organization_id, **kwargs):
        url = "organizations/{}".format(organization_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)

    async def get_organization_fields(self, params=None, **kwargs):
        url = "organizationFields"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def search_organizations(self, params=None, **kwargs):
        url = "organizations/search"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def get_organization_persons(self, organization_id, params=None, **kwargs):
        url = "organizations/{}/persons".format(organization_id)
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
    
    async def add_follower_to_organization(self, org_id, user_id, **kwargs):
        url = "organizations/{}/followers".format(org_id)
        data = {"user_id": user_id}
        return await self._client._post(self._client.BASE_URL+url, json=data, **kwargs)
