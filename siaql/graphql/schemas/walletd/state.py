from typing import Optional
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import StateResponse
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class StateQueries(WalletdBaseResolver):
    @strawberry.field
    async def walletd_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> StateResponse:
        """Get current state of walletd daemon"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_state",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
