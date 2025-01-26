import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import Hash256, VerifySectorResponse
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput
from typing import Optional


@strawberry.type
class SectorQueries:
    @strawberry.field
    async def hostd_verify_sector(
        self,
        info: Info,
        root: Hash256,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> VerifySectorResponse:
        """Verify a sector"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_verify_sector", root=root, filter_input=filter, sort_input=sort, pagination_input=pagination
        )


@strawberry.type
class SectorMutations:
    @strawberry.mutation
    async def hostd_delete_sector(self, info: Info, root: Hash256) -> bool:
        """Delete a sector"""
        await HostdBaseResolver.handle_api_call(info, "delete_sector", root=root)
        return True
