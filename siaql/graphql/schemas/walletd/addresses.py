from typing import List, Optional, Dict
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import (
    WalletEvent,
    SiacoinElement,     # Changed from types.SiacoinElement to just SiacoinElement
    SiafundElement,     # Changed from types.SiafundElement to just SiafundElement
    BalanceResponse    # Changed from types.UnlockConditions to just UnlockConditions

)

@strawberry.type
class AddressQueries:

    @strawberry.field
    async def address_balance(self, info: Info, address: str) -> BalanceResponse:
        """Get balance for address"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_balance",
            address=address
        )
        return data


    @strawberry.field
    async def address_events(
        self, 
        info: Info, 
        address: str,
        offset: int = 0,
        limit: int = 500
    ) -> List[WalletEvent]:
        """Get events for an address"""

        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_events",
            address=address,
            offset=offset,
            limit=limit
        )

    @strawberry.field
    async def address_unconfirmed_events(
        self, 
        info: Info, 
        address: str
    ) -> List[WalletEvent]:
        """Get unconfirmed events for an address"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_unconfirmed_events",
            address=address
        )

    @strawberry.field
    async def address_siacoin_outputs(
        self,
        info: Info,
        address: str,
        offset: int = 0,
        limit: int = 1000
    ) -> List[SiacoinElement]:
        """Get siacoin outputs for an address"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_siacoin_outputs",
            address=address,
            offset=offset,
            limit=limit
        )

    @strawberry.field
    async def address_siafund_outputs(
        self,
        info: Info,
        address: str,
        offset: int = 0,
        limit: int = 1000
    ) -> List[SiafundElement]:
        """Get siafund outputs for an address"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_siafund_outputs",
            address=address,
            offset=offset,
            limit=limit
        )
