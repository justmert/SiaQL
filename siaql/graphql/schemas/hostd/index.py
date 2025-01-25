import strawberry
from typing import Optional
from strawberry.types import Info

from siaql.graphql.schemas.types import ChainIndex
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class IndexQueries:
    @strawberry.field
    async def index_tip(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ChainIndex:
        """Get the current index tip"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_index_tip", filter_input=filter, sort_input=sort, pagination_input=pagination
        )
