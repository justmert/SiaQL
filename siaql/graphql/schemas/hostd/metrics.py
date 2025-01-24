import strawberry
from typing import List, Optional
from datetime import datetime
from strawberry.types import Info

from siaql.graphql.schemas.types import Metrics, MetricsInterval
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class MetricsQueries(HostdBaseResolver):
    @strawberry.field
    async def metrics(self, info: Info, timestamp: Optional[datetime] = None) -> Metrics:
        """Get metrics at specified timestamp"""
        return await self.handle_api_call(info, "get_metrics", timestamp=timestamp)

    @strawberry.field
    async def period_metrics(
        self, info: Info, start: datetime, periods: int, interval: MetricsInterval
    ) -> List[Metrics]:
        """Get metrics for multiple periods"""
        return await self.handle_api_call(info, "get_period_metrics", start=start, periods=periods, interval=interval)
