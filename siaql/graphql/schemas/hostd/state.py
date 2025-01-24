import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import HostdState
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class StateQueries:
    @strawberry.field
    async def state(self, info: Info) -> HostdState:
        """Get current host state"""
        return await HostdBaseResolver.handle_api_call(info, "get_state")
