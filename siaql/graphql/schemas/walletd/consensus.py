# siaql/siaql/graphql/schemas/consensus.py
from typing import List, Optional
from datetime import datetime
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver

from siaql.graphql.schemas.types import (
    NetworkInfo,
    HardforkDevAddr,
    HardforkTax,
    HardforkStorageProof,
    HardforkOak,
    HardforkASIC,
    HardforkFoundation,
    HardforkV2,
    ChainIndex,
    TipState,
    ElementsInfo
)


@strawberry.type
class ConsensusQueries(WalletdBaseResolver):
    @strawberry.field
    async def network(self, info: Info) -> NetworkInfo:
        """Returns the current network parameters"""
        def transform_network(network: dict) -> NetworkInfo:
            return NetworkInfo(
                name=network["name"],
                initial_coinbase=network["initialCoinbase"],
                minimum_coinbase=network["minimumCoinbase"],
                initial_target=network["initialTarget"],
                hardfork_dev_addr=HardforkDevAddr(
                    height=network["hardforkDevAddr"]["height"],
                    old_address=network["hardforkDevAddr"]["oldAddress"],
                    new_address=network["hardforkDevAddr"]["newAddress"]
                ),
                hardfork_tax=HardforkTax(
                    height=network["hardforkTax"]["height"]
                ),
                hardfork_storage_proof=HardforkStorageProof(
                    height=network["hardforkStorageProof"]["height"]
                ),
                hardfork_oak=HardforkOak(
                    height=network["hardforkOak"]["height"],
                    fix_height=network["hardforkOak"]["fixHeight"],
                    genesis_timestamp=datetime.fromisoformat(network["hardforkOak"]["genesisTimestamp"].replace('Z', '+00:00'))
                ),
                hardfork_asic=HardforkASIC(
                    height=network["hardforkASIC"]["height"],
                    oak_time=network["hardforkASIC"]["oakTime"],
                    oak_target=network["hardforkASIC"]["oakTarget"]
                ),
                hardfork_foundation=HardforkFoundation(
                    height=network["hardforkFoundation"]["height"],
                    primary_address=network["hardforkFoundation"]["primaryAddress"],
                    failsafe_address=network["hardforkFoundation"]["failsafeAddress"]
                ),
                hardfork_v2=HardforkV2(
                    allow_height=network["hardforkV2"]["allowHeight"],
                    require_height=network["hardforkV2"]["requireHeight"]
                )
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_network",
            transform_func=transform_network
        )
        return data

    @strawberry.field
    async def tip(self, info: Info) -> ChainIndex:
        """Returns the height and ID of the current block"""
        def transform_tip(tip: dict) -> ChainIndex:
            return ChainIndex(
                height=tip["height"],
                id=tip["ID"]
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_tip",
            transform_func=transform_tip
        )
        return data

    @strawberry.field
    async def tip_state(self, info: Info) -> TipState:
        """Returns the current consensus state"""
        def transform_tipstate(tipstate: dict) -> TipState:
            return TipState(
                index=ChainIndex(
                    height=tipstate["index"]["height"],
                    id=tipstate["index"]["id"]
                ),
                prev_timestamps=[
                    datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    for ts in tipstate["prevTimestamps"]
                ],
                depth=tipstate["depth"],
                child_target=tipstate["childTarget"],
                siafund_pool=tipstate["siafundPool"],
                oak_time=tipstate["oakTime"],
                oak_target=tipstate["oakTarget"],
                foundation_primary_address=tipstate["foundationPrimaryAddress"],
                foundation_failsafe_address=tipstate["foundationFailsafeAddress"],
                total_work=tipstate["totalWork"],
                difficulty=tipstate["difficulty"],
                oak_work=tipstate["oakWork"],
                elements=ElementsInfo(
                    num_leaves=tipstate["elements"]["numLeaves"],
                    trees=tipstate["elements"]["trees"]
                ),
                attestations=tipstate["attestations"]
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_tipstate",
            transform_func=transform_tipstate
        )
        return data

    @strawberry.field
    async def index(self, info: Info, height: int) -> ChainIndex:
        """Returns the chain index at a specified height"""
        def transform_index(index: dict) -> ChainIndex:
            return ChainIndex(
                height=index["height"],
                id=index["id"]
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_consensus_index",
            transform_func=transform_index,
            height=height
        )
        return data