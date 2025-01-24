import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import Currency
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class TPoolQueries:
    @strawberry.field
    async def tpool_fee(self, info: Info) -> Currency:
        """Get recommended transaction fee"""
        return await HostdBaseResolver.handle_api_call(info, "get_tpool_fee")
