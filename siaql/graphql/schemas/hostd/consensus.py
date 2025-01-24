import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import ChainIndex, Network, ConsensusState
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class ConsensusQueries(HostdBaseResolver):
    @strawberry.field
    async def consensus_tip(self, info: Info) -> ChainIndex:
        """Get the current consensus tip"""
        return await self.handle_api_call(info, "get_consensus_tip")

    @strawberry.field
    async def consensus_tip_state(self, info: Info) -> ConsensusState:
        """Get the current consensus tip state"""
        return await self.handle_api_call(info, "get_consensus_tip_state")

    @strawberry.field
    async def consensus_network(self, info: Info) -> Network:
        """Get consensus network parameters"""
        return await self.handle_api_call(info, "get_consensus_network")
