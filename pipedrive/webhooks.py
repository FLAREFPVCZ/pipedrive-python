class Webhooks:
    def __init__(self, client):
        self._client = client

    async def get_hooks_subscription(self, **kwargs):
        url = "webhooks"
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def create_hook_subscription(self, subscription_url, event_action, event_object, **kwargs):
        url = "webhooks"
        data = {
            "subscription_url": subscription_url,
            "event_action": event_action,
            "event_object": event_object,
        }
        return await self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    async def delete_hook_subscription(self, hook_id, **kwargs):
        url = "webhooks/{}".format(hook_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)
