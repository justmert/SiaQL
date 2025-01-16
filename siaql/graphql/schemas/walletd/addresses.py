from typing import List, Optional, Dict
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.schemas.walletd.events import Event, BlockIndex, MinerEventData, V1TransactionEventData
from siaql.graphql.resolvers.walletd import WalletdBaseResolver

from siaql.graphql.schemas.types import (
    AddressBalance,
    SiacoinElement,
    SiacoinOutput,
    SiafundElement,
    SiafundOutput
)

@strawberry.type
class AddressQueries:
    @strawberry.field
    async def address_balance(self, info: Info, address: str) -> AddressBalance:
        """Gets the balance of an individual address"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_balance",
            lambda d: AddressBalance(
                siacoins=d["siacoins"],
                immature_siacoins=d["immatureSiacoins"],
                siafunds=d["siafunds"]
            ),
            address=address
        )
        return data

    @strawberry.field
    async def address_events(
        self, 
        info: Info,
        address: str, 
        limit: Optional[int] = 100, 
        offset: Optional[int] = 0
    ) -> List[Event]:
        """Gets events for a specific address"""
        def transform_event(event: Dict) -> Event:
            # Transform BlockIndex
            block_index = BlockIndex(
                height=event["index"]["height"],
                id=event["index"]["id"]
            )

            # Transform event data based on type
            event_data = None
            if event["type"] == "miner" and "siacoinElement" in event["data"]:
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
                                claim_start=elem["siafundOutput"]["claimStart"]
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
            "get_address_events",
            transform_func=lambda events: [transform_event(event) for event in events],
            address=address,
            limit=limit,
            offset=offset
        )
        return data

    @strawberry.field
    async def address_unconfirmed_events(
        self, 
        info: Info,
        address: str, 
        limit: Optional[int] = 100, 
        offset: Optional[int] = 0
    ) -> List[Event]:
        """Gets unconfirmed events for a specific address"""
        def transform_event(event: Dict) -> Event:
            # Transform BlockIndex
            block_index = BlockIndex(
                height=event["index"]["height"],
                id=event["index"]["id"]
            )

            # Transform event data based on type
            event_data = None
            if event["type"] == "v1Transaction":
                # Transform transaction data
                transaction = event["data"]["transaction"]
                
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
                                claim_start=elem["siafundOutput"]["claimStart"]
                            ),
                            claim_start=elem["claimStart"]
                        )
                        for elem in event["data"]["spentSiafundElements"]
                    ]

                event_data = V1TransactionEventData(
                    transaction=transaction,
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
            "get_address_unconfirmed_events",
            transform_func=lambda events: [transform_event(event) for event in events],
            address=address,
            limit=limit,
            offset=offset
        )
        return data

    @strawberry.field
    async def address_siacoin_outputs(
        self, 
        info: Info,
        address: str, 
        limit: Optional[int] = 100, 
        offset: Optional[int] = 0
    ) -> List[SiacoinElement]:
        """Gets Siacoin UTXOs owned by the address"""
        def transform_output(output: Dict) -> SiacoinElement:
            return SiacoinElement(
                id=output["id"],
                leaf_index=output["leafIndex"],
                merkle_proof=output.get("merkleProof"),
                siacoin_output=SiacoinOutput(
                    value=output["siacoinOutput"]["value"],
                    address=output["siacoinOutput"]["address"]
                ),
                maturity_height=output["maturityHeight"]
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_siacoin_outputs",
            transform_func=lambda outputs: [transform_output(output) for output in outputs],
            address=address,
            limit=limit,
            offset=offset
        )
        return data

    @strawberry.field
    async def address_siafund_outputs(
        self,
        info: Info, 
        address: str, 
        limit: Optional[int] = 10, 
        offset: Optional[int] = 0
    ) -> List[SiafundElement]:
        """Gets Siafund UTXOs owned by the address"""
        def transform_output(output: Dict) -> SiafundElement:
            return SiafundElement(
                id=output["id"],
                leaf_index=output["leafIndex"],
                merkle_proof=output.get("merkleProof"),
                siafund_output=SiafundOutput(
                    value=output["siafundOutput"]["value"],
                    address=output["siafundOutput"]["address"],
                    claim_start=output["siafundOutput"].get("claimStart", "0")
                ),
                claim_start=output["claimStart"]
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_siafund_outputs",
            transform_func=lambda outputs: [transform_output(output) for output in outputs],
            address=address,
            limit=limit,
            offset=offset
        )
        return data