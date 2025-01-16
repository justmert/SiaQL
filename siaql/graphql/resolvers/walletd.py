from typing import List, Optional
import strawberry
from strawberry.types import Info
from datetime import datetime

@strawberry.type
class BlockIndex:
    height: int
    id: str

@strawberry.type
class SiacoinOutput:
    value: str
    address: str

@strawberry.type
class SiafundOutput:
    value: int
    address: str
    claim_start: str = strawberry.field(name="claimStart")

@strawberry.type
class AddressBalance:
    siacoins: str
    immature_siacoins: str = strawberry.field(name="immatureSiacoins")
    siafunds: int

@strawberry.type
class SiacoinElement:
    id: str
    leaf_index: int = strawberry.field(name="leafIndex")
    merkle_proof: Optional[List[str]] = strawberry.field(name="merkleProof")
    siacoin_output: SiacoinOutput = strawberry.field(name="siacoinOutput")
    maturity_height: int = strawberry.field(name="maturityHeight")

@strawberry.type
class SiafundElement:
    id: str
    leaf_index: int = strawberry.field(name="leafIndex")
    merkle_proof: Optional[List[str]] = strawberry.field(name="merkleProof")
    siafund_output: SiafundOutput = strawberry.field(name="siafundOutput")
    claim_start: str = strawberry.field(name="claimStart")

@strawberry.type
class Event:
    id: str
    index: BlockIndex
    timestamp: datetime
    maturity_height: int = strawberry.field(name="maturityHeight")
    type: str
    data: Optional[str]  # We'll store JSON string for flexible event data
    relevant: Optional[List[str]]

@strawberry.type
class Query:
    @strawberry.field
    async def address_balance(self, info: Info, address: str) -> AddressBalance:
        """Gets the balance of an individual address"""
        client = info.context["walletd_client"]
        data = await client.get_address_balance(address)
        return AddressBalance(
            siacoins=data["siacoins"],
            immature_siacoins=data["immatureSiacoins"],
            siafunds=data["siafunds"]
        )

    @strawberry.field
    async def address_events(
        self, 
        address: str, 
        limit: Optional[int] = 100, 
        offset: Optional[int] = 0
    ) -> List[Event]:
        """Gets events for a specific address"""
        pass

    @strawberry.field
    async def address_unconfirmed_events(
        self, 
        address: str, 
        limit: Optional[int] = 100, 
        offset: Optional[int] = 0
    ) -> List[Event]:
        """Gets unconfirmed events for a specific address"""
        pass

    @strawberry.field
    async def address_siacoin_outputs(
        self, 
        address: str, 
        limit: Optional[int] = 100, 
        offset: Optional[int] = 0
    ) -> List[SiacoinElement]:
        """Gets Siacoin UTXOs owned by the address"""
        pass

    @strawberry.field
    async def address_siafund_outputs(
        self, 
        address: str, 
        limit: Optional[int] = 100, 
        offset: Optional[int] = 0
    ) -> List[SiafundElement]:
        """Gets Siafund UTXOs owned by the address"""
        pass

    @strawberry.field
    async def event(self, id: str) -> Event:
        """Gets a specific event by ID"""
        pass