# siaql/siaql/graphql/schemas/consensus.py
from typing import List, Optional, Union
from datetime import datetime
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import (
    ChainIndex,
    ConsensusState,
    ConsensusUpdatesResponse,  # From consensus.State
    Network,  # From consensus.Network
    ApplyUpdate,  # From consensus.ApplyUpdate
    RevertUpdate,  # From consensus.RevertUpdate
)
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class ConsensusQueries(WalletdBaseResolver):
    @strawberry.field
    async def walletd_consensus_network(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Network:
        """Get the consensus network information"""
        return await WalletdBaseResolver.handle_api_call(
            info, "get_consensus_network", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def walletd_consensus_tip(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ChainIndex:
        """Get the current consensus tip"""
        return await WalletdBaseResolver.handle_api_call(
            info, "get_consensus_tip", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def walletd_consensus_tip_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ConsensusState:
        """Get the current consensus tip state"""
        return await WalletdBaseResolver.handle_api_call(
            info, "get_consensus_tip_state", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def walletd_consensus_index(
        self,
        info: Info,
        height: int,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ChainIndex:
        """Get consensus index at specified height"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_index",
            height=height,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_consensus_updates(
        self,
        info: Info,
        index: ChainIndex.Input,
        limit: int = 10,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ConsensusUpdatesResponse:
        """Get consensus updates since specified index"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_updates",
            index=index,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
