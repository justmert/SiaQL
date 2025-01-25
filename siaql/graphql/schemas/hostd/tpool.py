import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import Currency
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput

from typing import Optional


@strawberry.type
class TPoolQueries:
    @strawberry.field
    async def tpool_fee(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Currency:
        """Get recommended transaction fee"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_tpool_fee", filter_input=filter, sort_input=sort, pagination_input=pagination
        )
