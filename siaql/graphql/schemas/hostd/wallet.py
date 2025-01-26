import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import (
    WalletResponse,
    WalletEvent,
    Address,
    Currency,
    TransactionID,
    WalletSendSiacoinsRequest,
)
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput

from typing import Optional


@strawberry.type
class WalletQueries:
    @strawberry.field
    async def hostd_wallet(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> WalletResponse:
        """Get wallet state"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_wallet", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def hostd_wallet_events(
        self,
        info: Info,
        limit: int = 100,
        offset: int = 0,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[WalletEvent]:
        """Get wallet events with pagination"""
        return await HostdBaseResolver.handle_api_call(
            info,
            "get_wallet_events",
            limit=limit,
            offset=offset,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def hostd_wallet_pending(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[WalletEvent]:
        """Get pending wallet events"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_wallet_pending", filter_input=filter, sort_input=sort, pagination_input=pagination
        )


@strawberry.type
class WalletMutations:
    @strawberry.mutation
    async def hostd_send_siacoins(self, info: Info, req: WalletSendSiacoinsRequest.Input) -> TransactionID:
        """Send siacoins to an address"""
        return await HostdBaseResolver.handle_api_call(info, "post_wallet_send", req=req)
