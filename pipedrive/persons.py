class Persons:
    def __init__(self, client):
        self._client = client

    async def get_person(self, person_id, **kwargs):
        url = "persons/{}".format(person_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_persons(self, params=None, **kwargs):
        url = "persons"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def search_persons(self, params=None, **kwargs):
        url = "persons/search"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def create_person(self, data, **kwargs):
        url = "persons"
        return await self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    async def update_person(self, person_id, data, **kwargs):
        url = "persons/{}".format(person_id)
        return await self._client._put(self._client.BASE_URL + url, json=data, **kwargs)

    async def delete_person(self, person_id, **kwargs):
        url = "persons/{}".format(person_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)

    async def get_person_deals(self, person_id, **kwargs):
        url = "persons/{}/deals".format(person_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_person_fields(self, params=None, **kwargs):
        url = "personFields"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def get_person_activities(self, person_id, **kwargs):
        url = "persons/{}/activities".format(person_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)
    
    async def add_follower_to_person(self, person_id, user_id, **kwargs):
        url = "persons/{}/followers".format(person_id)
        data = {"user_id": user_id}
        return await self._client._post(self._client.BASE_URL+url, json=data, **kwargs)
