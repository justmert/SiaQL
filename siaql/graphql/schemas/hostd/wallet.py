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


@strawberry.type
class WalletQueries:
    @strawberry.field
    async def wallet(self, info: Info) -> WalletResponse:
        """Get wallet state"""
        return await HostdBaseResolver.handle_api_call(info, "get_wallet")

    @strawberry.field
    async def wallet_events(self, info: Info, limit: int = 100, offset: int = 0) -> List[WalletEvent]:
        """Get wallet events with pagination"""
        return await HostdBaseResolver.handle_api_call(info, "get_wallet_events", limit=limit, offset=offset)

    @strawberry.field
    async def wallet_pending(self, info: Info) -> List[WalletEvent]:
        """Get pending wallet events"""
        return await HostdBaseResolver.handle_api_call(info, "get_wallet_pending")


@strawberry.type
class WalletMutations:
    @strawberry.mutation
    async def send_siacoins(self, info: Info, req: WalletSendSiacoinsRequest.Input) -> TransactionID:
        """Send siacoins to an address"""
        return await HostdBaseResolver.handle_api_call(info, "post_wallet_send", req=req)
