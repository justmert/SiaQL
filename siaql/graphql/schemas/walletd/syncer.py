# siaql/graphql/schemas/walletd/syncer.py
from typing import List, Optional
from datetime import datetime
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import GatewayPeer, Block
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class SyncerQueries:
    @strawberry.field
    async def syncer_peers(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[GatewayPeer]:
        """Get list of connected peers"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_syncer_peers",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )


@strawberry.type
class SyncerMutations:
    @strawberry.mutation
    async def syncer_connect(self, info: Info, addr: str) -> bool:
        """Connect to a peer"""
        await WalletdBaseResolver.handle_api_call(info, "post_syncer_connect", addr=addr)
        return True

    @strawberry.mutation
    async def syncer_broadcast_block(self, info: Info, block: Block.Input) -> bool:
        """Broadcast a block to all peers"""
        await WalletdBaseResolver.handle_api_call(info, "post_syncer_broadcast_block", block=block)
        return True
