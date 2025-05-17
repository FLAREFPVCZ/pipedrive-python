class Subscriptions:
    def __init__(self, client):
        self._client = client

    async def get_subscription(self, subscription_id, **kwargs):
        url = "subscriptions/{}".format(subscription_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_deal_subscription(self, deal_id, **kwargs):
        url = "subscriptions/find/{}".format(deal_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def get_all_payments(self, subscription_id, **kwargs):
        url = "subscriptions/{}/payments".format(subscription_id)
        return await self._client._get(self._client.BASE_URL + url, **kwargs)

    async def add_recurring_subscription(self, data, **kwargs):
        url = "subscriptions/recurring"
        return await self._client._post(self._client.BASE_URL + url, data, **kwargs)

    async def add_installment_subscription(self, data, **kwargs):
        url = "subscriptions/installment"
        return await self._client._post(self._client.BASE_URL + url, data, **kwargs)

    async def update_recurring_subscription(self, subscription_id, data, **kwargs):
        url = "subscriptions/recurring/{}".format(subscription_id)
        return await self._client._put(self._client.BASE_URL + url, data, **kwargs)

    async def update_installment_subscription(self, subscription_id, data, **kwargs):
        url = "subscriptions/installment/{}".format(subscription_id)
        return await self._client._put(self._client.BASE_URL + url, data, **kwargs)

    async def cancel_recurring_subscription(self, subscription_id, data, **kwargs):
        url = "subscriptions/recurring/{}/cancel".format(subscription_id)
        return await self._client._put(self._client.BASE_URL + url, data, **kwargs)

    async def delete_subscription(self, subscription_id, **kwargs):
        url = "subscriptions/{}".format(subscription_id)
        return await self._client._delete(self._client.BASE_URL + url, **kwargs)
