import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import RegisterWebHookRequest, Webhook
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput
from typing import Optional


@strawberry.type
class WebhookQueries:
    @strawberry.field
    async def hostd_webhooks(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Webhook]:
        """Get list of webhooks"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_webhooks", filter_input=filter, sort_input=sort, pagination_input=pagination
        )


@strawberry.type
class WebhookMutations:
    @strawberry.mutation
    async def hostd_register_webhook(self, info: Info, req: RegisterWebHookRequest.Input) -> Webhook:
        """Register a new webhook"""
        return await HostdBaseResolver.handle_api_call(info, "post_webhooks", req=req)

    @strawberry.mutation
    async def hostd_update_webhook(self, info: Info, id: int, req: RegisterWebHookRequest.Input) -> Webhook:
        """Update an existing webhook"""
        return await HostdBaseResolver.handle_api_call(info, "put_webhooks", id=id, req=req)

    @strawberry.mutation
    async def hostd_delete_webhook(self, info: Info, id: int) -> bool:
        """Delete a webhook"""
        await HostdBaseResolver.handle_api_call(info, "delete_webhooks", id=id)
        return True

    @strawberry.mutation
    async def hostd_test_webhook(self, info: Info, id: int) -> bool:
        """Test a webhook"""
        await HostdBaseResolver.handle_api_call(info, "post_webhooks_test", id=id)
        return True
