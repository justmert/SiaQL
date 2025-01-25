# graphql/schemas/walletd/rescan.py

import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import RescanResponse
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput
from typing import Optional


@strawberry.type
class RescanQueries:
    @strawberry.field
    async def rescan_status(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> RescanResponse:
        """Get rescan status"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_rescan_status",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
        return data


@strawberry.type
class RescanMutations:
    @strawberry.mutation
    async def start_rescan(self, info: Info, height: int) -> bool:
        """Start rescan from height"""
        await WalletdBaseResolver.handle_api_call(info, "start_rescan", height=height)
        return True
