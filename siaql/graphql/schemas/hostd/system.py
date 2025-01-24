import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import SystemDirResponse
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class SystemQueries:
    @strawberry.field
    async def system_dir(self, info: Info, path: str) -> SystemDirResponse:
        """Get directory contents"""
        return await HostdBaseResolver.handle_api_call(info, "get_system_dir", path=path)


@strawberry.type
class SystemMutations:
    @strawberry.mutation
    async def create_dir(self, info: Info, path: str) -> bool:
        """Create a directory"""
        await HostdBaseResolver.handle_api_call(info, "put_system_dir", path=path)
        return True

    @strawberry.mutation
    async def backup_sqlite3(self, info: Info, path: str) -> bool:
        """Create a backup of the SQLite3 database"""
        await HostdBaseResolver.handle_api_call(info, "post_system_sqlite3_backup", path=path)
        return True
