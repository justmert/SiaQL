import strawberry
from typing import List, Optional
from strawberry.types import Info

from siaql.graphql.schemas.types import Peer
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class SyncerQueries:
    @strawberry.field
    async def hostd_syncer_address(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> str:
        """Get syncer address"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_syncer_address", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def hostd_syncer_peers(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Peer]:
        """Get list of connected peers"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_syncer_peers", filter_input=filter, sort_input=sort, pagination_input=pagination
        )


@strawberry.type
class SyncerMutations:
    @strawberry.mutation
    async def hostd_connect_peer(self, info: Info, address: str) -> bool:
        """Connect to a peer"""
        await HostdBaseResolver.handle_api_call(info, "put_syncer_peer", address=address)
        return True
