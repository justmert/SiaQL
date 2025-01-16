from typing import List, Optional, Union
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver

from siaql.graphql.schemas.types import (
    Event,
    BlockIndex,
    MinerEventData,
    V1TransactionEventData,
    SiacoinElement,
    SiafundElement,
    SiacoinOutput,
    SiafundOutput
)

@strawberry.type
class EventQueries(WalletdBaseResolver):
    @strawberry.field
    async def event(self, info: Info, id: str) -> Event:
        """Gets a specific event by ID"""
        def transform_event(event: dict) -> Event:
            # Transform BlockIndex
            block_index = BlockIndex(
                height=event["index"]["height"],
                id=event["index"]["id"]
            )

            # Transform event data based on type
            event_data = None
            if event["type"] == "miner":
                siacoin_element = SiacoinElement(
                    id=event["data"]["siacoinElement"]["id"],
                    leaf_index=event["data"]["siacoinElement"]["leafIndex"],
                    merkle_proof=event["data"]["siacoinElement"].get("merkleProof"),
                    siacoin_output=SiacoinOutput(
                        value=event["data"]["siacoinElement"]["siacoinOutput"]["value"],
                        address=event["data"]["siacoinElement"]["siacoinOutput"]["address"]
                    ),
                    maturity_height=event["data"]["siacoinElement"]["maturityHeight"]
                )
                event_data = MinerEventData(siacoin_element=siacoin_element)
            elif event["type"] == "v1Transaction":
                # Transform spent elements
                spent_siacoin_elements = None
                if "spentSiacoinElements" in event["data"]:
                    spent_siacoin_elements = [
                        SiacoinElement(
                            id=elem["id"],
                            leaf_index=elem["leafIndex"],
                            merkle_proof=elem.get("merkleProof"),
                            siacoin_output=SiacoinOutput(
                                value=elem["siacoinOutput"]["value"],
                                address=elem["siacoinOutput"]["address"]
                            ),
                            maturity_height=elem["maturityHeight"]
                        )
                        for elem in event["data"]["spentSiacoinElements"]
                    ]

                spent_siafund_elements = None
                if "spentSiafundElements" in event["data"]:
                    spent_siafund_elements = [
                        SiafundElement(
                            id=elem["id"],
                            leaf_index=elem["leafIndex"],
                            merkle_proof=elem.get("merkleProof"),
                            siafund_output=SiafundOutput(
                                value=elem["siafundOutput"]["value"],
                                address=elem["siafundOutput"]["address"],
                                claim_start=elem["siafundOutput"].get("claimStart", "0")
                            ),
                            claim_start=elem["claimStart"]
                        )
                        for elem in event["data"]["spentSiafundElements"]
                    ]

                event_data = V1TransactionEventData(
                    transaction=event["data"]["transaction"],
                    spent_siacoin_elements=spent_siacoin_elements,
                    spent_siafund_elements=spent_siafund_elements
                )

            return Event(
                id=event["id"],
                index=block_index,
                timestamp=datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00')),
                maturity_height=event["maturityHeight"],
                type=event["type"],
                data=event_data,
                relevant=event.get("relevant")
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_event",
            transform_func=transform_event,
            event_id=id
        )
        return data
