import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import SystemDirResponse
from siaql.graphql.resolvers.hostd import HostdBaseResolver
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput
from typing import Optional


@strawberry.type
class SystemQueries:
    @strawberry.field
    async def hostd_system_dir(
        self,
        info: Info,
        path: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> SystemDirResponse:
        """Get directory contents"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_system_dir", path=path, filter_input=filter, sort_input=sort, pagination_input=pagination
        )


@strawberry.type
class SystemMutations:
    @strawberry.mutation
    async def hostd_create_dir(self, info: Info, path: str) -> bool:
        """Create a directory"""
        await HostdBaseResolver.handle_api_call(info, "put_system_dir", path=path)
        return True

    @strawberry.mutation
    async def hostd_backup_sqlite3(self, info: Info, path: str) -> bool:
        """Create a backup of the SQLite3 database"""
        await HostdBaseResolver.handle_api_call(info, "post_system_sqlite3_backup", path=path)
        return True
