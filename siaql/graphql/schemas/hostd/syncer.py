import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import Peer
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class SyncerQueries(HostdBaseResolver):
    @strawberry.field
    async def syncer_address(self, info: Info) -> str:
        """Get syncer address"""
        return await self.handle_api_call(info, "get_syncer_address")

    @strawberry.field
    async def syncer_peers(self, info: Info) -> List[Peer]:
        """Get list of connected peers"""
        return await self.handle_api_call(info, "get_syncer_peers")


@strawberry.type
class SyncerMutations(HostdBaseResolver):
    @strawberry.mutation
    async def connect_peer(self, info: Info, address: str) -> bool:
        """Connect to a peer"""
        await self.handle_api_call(info, "put_syncer_peer", address=address)
        return True
