# siaql/siaql/graphql/schemas/consensus.py
from typing import List, Optional, Union
from datetime import datetime
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import (
    ChainIndex,
    ConsensusState,        # From consensus.State 
    Network,      # From consensus.Network
    ApplyUpdate,  # From consensus.ApplyUpdate
    RevertUpdate,  # From consensus.RevertUpdate
    Block,
)

@strawberry.type
class ConsensusQueries(WalletdBaseResolver):
    @strawberry.field
    async def consensus_network(self, info: Info) -> Network:
        """Get the consensus network information"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_network"
        )

    @strawberry.field
    async def consensus_tip(self, info: Info) -> ChainIndex:
        """Get the current consensus tip"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_tip"
        )

    @strawberry.field
    async def consensus_tip_state(self, info: Info) -> ConsensusState:
        """Get the current consensus tip state"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_tip_state"
        )

    @strawberry.field
    async def consensus_index(self, info: Info, height: int) -> ChainIndex:
        """Get consensus index at specified height"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_index",
            height=height
        )

    @strawberry.field
    async def consensus_updates(
        self, 
        info: Info, 
        index: ChainIndex.Input, 
        limit: int = 10
    ) -> List[Union[ApplyUpdate, RevertUpdate]]:
        """Get consensus updates since specified index"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_updates",
            index=index,
            limit=limit
        )
