from datetime import datetime
from typing import Any, Dict, List, Optional

import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput

from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import (
    SiacoinElement,
    SiafundElement,
    Wallet,
    Balance,
    Address,
)
from siaql.graphql.schemas.types import (
    WalletUpdateRequest,
    WalletReserveRequest,
    WalletReleaseRequest,
    WalletFundRequest,
    WalletEvent,
    WalletFundSFRequest,
    WalletFundResponse,
)


@strawberry.type
class WalletQueries:
    @strawberry.field
    async def walletd_wallets(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Wallet]:
        """Get all wallets"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_wallets",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_wallet_addresses(
        self,
        info: Info,
        wallet_id: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Address]:
        """Get addresses for a wallet"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_wallet_addresses",
            wallet_id=wallet_id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_wallet_balance(
        self,
        info: Info,
        wallet_id: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Balance:
        """Get wallet balance"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_wallet_balance",
            wallet_id=wallet_id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_wallet_events(
        self,
        info: Info,
        wallet_id: str,
        offset: int = 0,
        limit: int = 500,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[WalletEvent]:
        """Get wallet events"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_wallet_events",
            wallet_id=wallet_id,
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_wallet_unconfirmed_events(
        self,
        info: Info,
        wallet_id: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[WalletEvent]:
        """Get unconfirmed wallet events"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_wallet_unconfirmed_events",
            wallet_id=wallet_id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_wallet_siacoin_outputs(
        self,
        info: Info,
        wallet_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[SiacoinElement]:
        """Get wallet siacoin outputs"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_wallet_siacoin_outputs",
            wallet_id=wallet_id,
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
        return data

    @strawberry.field
    async def walletd_wallet_siafund_outputs(
        self,
        info: Info,
        wallet_id: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[SiafundElement]:
        """Get wallet siafund outputs"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_wallet_siafund_outputs",
            wallet_id=wallet_id,
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
        return data


@strawberry.type
class WalletMutations:
    @strawberry.mutation
    async def walletd_add_wallet(self, info: Info, wallet: WalletUpdateRequest.Input) -> Wallet:
        """Add a new wallet"""
        return await WalletdBaseResolver.handle_api_call(info, "post_add_wallet", wallet_update=wallet)

    @strawberry.mutation
    async def walletd_update_wallet(self, info: Info, wallet_id: str, wallet: WalletUpdateRequest.Input) -> Wallet:
        """Update a wallet"""
        return await WalletdBaseResolver.handle_api_call(
            info, "post_update_wallet", wallet_id=wallet_id, wallet_update=wallet
        )

    @strawberry.mutation
    async def walletd_delete_wallet(self, info: Info, wallet_id: str) -> bool:
        """Delete a wallet"""
        await WalletdBaseResolver.handle_api_call(info, "delete_wallet", wallet_id=wallet_id)
        return True

    @strawberry.mutation
    async def walletd_add_wallet_address(self, info: Info, wallet_id: str, address: Address) -> bool:
        """Add an address to a wallet"""
        await WalletdBaseResolver.handle_api_call(info, "add_wallet_address", wallet_id=wallet_id, address=address)
        return True

    @strawberry.mutation
    async def walletd_remove_wallet_address(self, info: Info, wallet_id: str, address: str) -> bool:
        """Remove an address from a wallet"""
        await WalletdBaseResolver.handle_api_call(info, "delete_wallet_address", wallet_id=wallet_id, address=address)
        return True

    @strawberry.mutation
    async def walletd_reserve_outputs(self, info: Info, wallet_id: str, request: WalletReserveRequest.Input) -> bool:
        """Reserve outputs"""
        await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_reserve", wallet_id=wallet_id, reserve_request=request
        )
        return True

    @strawberry.mutation
    async def walletd_release_outputs(self, info: Info, wallet_id: str, request: WalletReleaseRequest.Input) -> bool:
        """Release outputs"""
        await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_release", wallet_id=wallet_id, release_request=request
        )
        return True

    @strawberry.mutation
    async def walletd_fund_transaction(
        self, info: Info, wallet_id: str, request: WalletFundRequest.Input
    ) -> WalletFundResponse:
        return await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_fund", wallet_id=wallet_id, fund_request=request
        )

    @strawberry.mutation
    async def walletd_fund_siafund_transaction(
        self, info: Info, wallet_id: str, request: WalletFundSFRequest.Input
    ) -> WalletFundResponse:
        """Fund a siafund transaction"""
        return await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_fund_siafund", wallet_id=wallet_id, fund_request=request
        )
