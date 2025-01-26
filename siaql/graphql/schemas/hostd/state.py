import strawberry
from strawberry.types import Info
from typing import Optional

from siaql.graphql.schemas.types import HostdState
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class StateQueries:
    @strawberry.field
    async def hostd_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> HostdState:
        """Get current host state"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_state", filter_input=filter, sort_input=sort, pagination_input=pagination
        )
