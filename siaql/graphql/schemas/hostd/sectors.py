import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import Hash256, VerifySectorResponse
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class SectorQueries:
    @strawberry.field
    async def verify_sector(self, info: Info, root: Hash256) -> VerifySectorResponse:
        """Verify a sector"""
        return await HostdBaseResolver.handle_api_call(info, "get_verify_sector", root=root)


@strawberry.type
class SectorMutations:
    @strawberry.mutation
    async def delete_sector(self, info: Info, root: Hash256) -> bool:
        """Delete a sector"""
        await HostdBaseResolver.handle_api_call(info, "delete_sector", root=root)
        return True
