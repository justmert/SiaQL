import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import ChainIndex
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class IndexQueries(HostdBaseResolver):
    @strawberry.field
    async def index_tip(self, info: Info) -> ChainIndex:
        """Get the current index tip"""
        return await self.handle_api_call(info, "get_index_tip")
