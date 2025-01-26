import strawberry
from typing import List, Optional
from strawberry.types import Info

from siaql.graphql.schemas.types import Alert, Hash256
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput

from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class AlertQueries:
    @strawberry.field
    async def hostd_alerts(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Alert]:
        """Get active alerts"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_alerts", filter_input=filter, sort_input=sort, pagination_input=pagination
        )


@strawberry.type
class AlertMutations:
    @strawberry.mutation
    async def hostd_dismiss_alerts(self, info: Info, ids: List[Hash256]) -> bool:
        """Dismiss specified alerts"""
        await HostdBaseResolver.handle_api_call(info, "post_alerts_dismiss", ids=ids)
        return True
