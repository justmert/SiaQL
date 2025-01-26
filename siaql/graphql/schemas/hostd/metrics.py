import strawberry
from typing import List, Optional
from datetime import datetime
from strawberry.types import Info

from siaql.graphql.schemas.types import Metrics, MetricsInterval
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class MetricsQueries:
    @strawberry.field
    async def hostd_metrics(
        self,
        info: Info,
        timestamp: Optional[datetime] = None,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Metrics:
        """Get metrics at specified timestamp"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_metrics", timestamp=timestamp, filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def hostd_period_metrics(
        self,
        info: Info,
        start: datetime,
        periods: int,
        interval: MetricsInterval,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Metrics]:
        """Get metrics for multiple periods"""
        return await HostdBaseResolver.handle_api_call(
            info,
            "get_period_metrics",
            start=start,
            periods=periods,
            interval=interval,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
