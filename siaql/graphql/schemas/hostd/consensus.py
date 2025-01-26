import strawberry
from strawberry.types import Info
from typing import Optional

from siaql.graphql.schemas.types import ChainIndex, Network, ConsensusState
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput

from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class ConsensusQueries:
    @strawberry.field
    async def hostd_consensus_tip(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ChainIndex:
        """Get the current consensus tip"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_consensus_tip", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def hostd_consensus_tip_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ConsensusState:
        """Get the current consensus tip state"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_consensus_tip_state", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def hostd_consensus_network(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Network:
        """Get consensus network parameters"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_consensus_network", filter_input=filter, sort_input=sort, pagination_input=pagination
        )
