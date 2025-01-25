from typing import List, Optional, Dict
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import WalletEvent, SiacoinElement, SiafundElement, Balance
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class AddressQueries:
    @strawberry.field
    async def address_balance(
        self,
        info: Info,
        address: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Balance:
        """Get balance for address"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_balance",
            address=address,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
        return data

    @strawberry.field
    async def address_events(
        self,
        info: Info,
        address: str,
        offset: int = 0,
        limit: int = 500,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[WalletEvent]:
        """Get events for an address"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_events",
            address=address,
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def address_unconfirmed_events(
        self,
        info: Info,
        address: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[WalletEvent]:
        """Get unconfirmed events for an address"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_unconfirmed_events",
            address=address,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def address_siacoin_outputs(
        self,
        info: Info,
        address: str,
        offset: int = 0,
        limit: int = 1000,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[SiacoinElement]:
        """Get siacoin outputs for an address"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_siacoin_outputs",
            address=address,
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def address_siafund_outputs(
        self,
        info: Info,
        address: str,
        offset: int = 0,
        limit: int = 1000,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[SiafundElement]:
        """Get siafund outputs for an address"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_address_siafund_outputs",
            address=address,
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
