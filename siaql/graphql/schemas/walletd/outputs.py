import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import SiacoinElement, SiafundElement

from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput
from typing import Optional


@strawberry.type
class OutputsQueries:
    @strawberry.field
    async def walletd_get_siacoin_output(
        self,
        info: Info,
        id: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> SiacoinElement:
        """Get rescan status"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_siacoin_output",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
        return data

    @strawberry.field
    async def walletd_get_siafund_output(
        self,
        info: Info,
        id: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> SiafundElement:
        """Start rescan from height"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_siafund_output",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
