import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import Alert, Hash256
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class AlertQueries(HostdBaseResolver):
    @strawberry.field
    async def alerts(self, info: Info) -> List[Alert]:
        """Get active alerts"""
        return await self.handle_api_call(info, "get_alerts")


@strawberry.type
class AlertMutations(HostdBaseResolver):
    @strawberry.mutation
    async def dismiss_alerts(self, info: Info, ids: List[Hash256]) -> bool:
        """Dismiss specified alerts"""
        await self.handle_api_call(info, "post_alerts_dismiss", ids=ids)
        return True
