class Notes:
    def __init__(self, client):
        self._client = client

    async def get_note(self, note_id, **kwargs):
        url = "notes/{}".format(note_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_notes(self, params=None, **kwargs):
        url = "notes"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    async def create_note(self, data, **kwargs):
        url = "notes"
        return await self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    async def update_note(self, note_id, data, **kwargs):
        url = "notes/{}".format(note_id)
        return await self._client._put(self._client.BASE_URL + url, json=data, **kwargs)

    async def delete_note(self, note_id, **kwargs):
        url = "notes/{}".format(note_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)

    async def get_note_fields(self, params=None, **kwargs):
        url = "noteFields"
        return await self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
