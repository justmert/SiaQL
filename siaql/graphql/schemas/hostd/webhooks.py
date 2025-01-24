import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import RegisterWebHookRequest, Webhook
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class WebhookQueries:
    @strawberry.field
    async def webhooks(self, info: Info) -> List[Webhook]:
        """Get list of webhooks"""
        return await HostdBaseResolver.handle_api_call(info, "get_webhooks")


@strawberry.type
class WebhookMutations:
    @strawberry.mutation
    async def register_webhook(self, info: Info, req: RegisterWebHookRequest.Input) -> Webhook:
        """Register a new webhook"""
        return await HostdBaseResolver.handle_api_call(info, "post_webhooks", req=req)

    @strawberry.mutation
    async def update_webhook(self, info: Info, id: int, req: RegisterWebHookRequest.Input) -> Webhook:
        """Update an existing webhook"""
        return await HostdBaseResolver.handle_api_call(info, "put_webhooks", id=id, req=req)

    @strawberry.mutation
    async def delete_webhook(self, info: Info, id: int) -> bool:
        """Delete a webhook"""
        await HostdBaseResolver.handle_api_call(info, "delete_webhooks", id=id)
        return True

    @strawberry.mutation
    async def test_webhook(self, info: Info, id: int) -> bool:
        """Test a webhook"""
        await HostdBaseResolver.handle_api_call(info, "post_webhooks_test", id=id)
        return True
