from datetime import datetime
from typing import Any, Dict, List, Optional

import strawberry
from strawberry.types import Info

from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import (
    SiacoinElement,
    SiafundElement,
    Wallet,
    Balance,
    Address,
    Event,
)
from siaql.graphql.schemas.types import (
    WalletUpdateRequest,
    WalletReserveRequest,
    WalletReleaseRequest,
    WalletFundRequest,
    WalletEvent,
    WalletFundSFRequest,
    WalletConstructRequest,
    WalletConstructResponse,
    WalletConstructV2Response,
    WalletFundResponse,
)


@strawberry.type
class WalletQueries:
    @strawberry.field
    async def wallets(self, info: Info) -> List[Wallet]:
        """Get all wallets"""
        return await WalletdBaseResolver.handle_api_call(info, "get_wallets")

    @strawberry.field
    async def wallet_addresses(self, info: Info, wallet_id: str) -> List[Address]:
        """Get addresses for a wallet"""
        return await WalletdBaseResolver.handle_api_call(info, "get_wallet_addresses", wallet_id=wallet_id)

    @strawberry.field
    async def wallet_balance(self, info: Info, wallet_id: str) -> Balance:
        """Get wallet balance"""
        return await WalletdBaseResolver.handle_api_call(info, "get_wallet_balance", wallet_id=wallet_id)

    @strawberry.field
    async def wallet_events(self, info: Info, wallet_id: str, offset: int = 0, limit: int = 500) -> List[WalletEvent]:
        """Get wallet events"""
        return await WalletdBaseResolver.handle_api_call(
            info, "get_wallet_events", wallet_id=wallet_id, offset=offset, limit=limit
        )

    @strawberry.field
    async def wallet_unconfirmed_events(self, info: Info, wallet_id: str) -> List[Event]:
        """Get unconfirmed wallet events"""
        return await WalletdBaseResolver.handle_api_call(info, "get_wallet_unconfirmed_events", wallet_id=wallet_id)

    @strawberry.field
    async def wallet_siacoin_outputs(
        self, info: Info, wallet_id: str, offset: Optional[int] = 0, limit: Optional[int] = 1000
    ) -> List[SiacoinElement]:
        """Get wallet siacoin outputs"""
        data = await WalletdBaseResolver.handle_api_call(
            info, "get_wallet_siacoin_outputs", wallet_id=wallet_id, offset=offset, limit=limit
        )
        return data

    @strawberry.field
    async def wallet_siafund_outputs(
        self, info: Info, wallet_id: str, offset: Optional[int] = 0, limit: Optional[int] = 1000
    ) -> List[SiafundElement]:
        """Get wallet siafund outputs"""
        data = await WalletdBaseResolver.handle_api_call(
            info, "get_wallet_siafund_outputs", wallet_id=wallet_id, offset=offset, limit=limit
        )
        return data


@strawberry.type
class WalletMutations:
    @strawberry.mutation
    async def add_wallet(self, info: Info, wallet: WalletUpdateRequest.Input) -> Wallet:
        """Add a new wallet"""
        return await WalletdBaseResolver.handle_api_call(info, "post_add_wallet", wallet_update=wallet)

    @strawberry.mutation
    async def update_wallet(self, info: Info, wallet_id: str, wallet: WalletUpdateRequest.Input) -> Wallet:
        """Update a wallet"""
        return await WalletdBaseResolver.handle_api_call(
            info, "post_update_wallet", wallet_id=wallet_id, wallet_update=wallet
        )

    @strawberry.mutation
    async def delete_wallet(self, info: Info, wallet_id: str) -> bool:
        """Delete a wallet"""
        await WalletdBaseResolver.handle_api_call(info, "delete_wallet", wallet_id=wallet_id)
        return True

    @strawberry.mutation
    async def add_wallet_address(self, info: Info, wallet_id: str, address: Address) -> bool:
        """Add an address to a wallet"""
        await WalletdBaseResolver.handle_api_call(info, "put_wallet_address", wallet_id=wallet_id, address=address)
        return True

    @strawberry.mutation
    async def remove_wallet_address(self, info: Info, wallet_id: str, address: str) -> bool:
        """Remove an address from a wallet"""
        await WalletdBaseResolver.handle_api_call(info, "delete_wallet_address", wallet_id=wallet_id, address=address)
        return True

    @strawberry.mutation
    async def reserve_outputs(self, info: Info, wallet_id: str, request: WalletReserveRequest.Input) -> bool:
        """Reserve outputs"""
        await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_reserve", wallet_id=wallet_id, reserve_request=request
        )
        return True

    @strawberry.mutation
    async def release_outputs(self, info: Info, wallet_id: str, request: WalletReleaseRequest.Input) -> bool:
        """Release outputs"""
        await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_release", wallet_id=wallet_id, release_request=request
        )
        return True

    @strawberry.mutation
    async def fund_transaction(self, info: Info, wallet_id: str, request: WalletFundRequest.Input) -> WalletFundResponse:
        return await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_fund", wallet_id=wallet_id, fund_request=request
        )

    @strawberry.mutation
    async def fund_siafund_transaction(
        self, info: Info, wallet_id: str, request: WalletFundSFRequest.Input
    ) -> WalletFundResponse:
        """Fund a siafund transaction"""
        return await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_fund_siafund", wallet_id=wallet_id, fund_request=request
        )

    @strawberry.mutation
    async def construct_transaction(
        self, info: Info, wallet_id: str, request: WalletConstructRequest.Input
    ) -> WalletConstructResponse:
        """Construct a transaction"""
        return await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_construct", wallet_id=wallet_id, construct_request=request
        )

    @strawberry.mutation
    async def construct_v2_transaction(
        self, info: Info, wallet_id: str, request: WalletConstructRequest.Input
    ) -> WalletConstructV2Response:
        """Construct a v2 transaction"""
        return await WalletdBaseResolver.handle_api_call(
            info, "post_wallet_construct_v2", wallet_id=wallet_id, construct_request=request
        )
