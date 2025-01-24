import strawberry
from strawberry.types import Info

from siaql.graphql.schemas.types import HostSettings, PinnedSettings
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class SettingsQueries:
    @strawberry.field
    async def settings(self, info: Info) -> HostSettings:
        """Get current host settings"""
        return await HostdBaseResolver.handle_api_call(info, "get_settings")

    @strawberry.field
    async def pinned_settings(self, info: Info) -> PinnedSettings:
        """Get pinned settings"""
        return await HostdBaseResolver.handle_api_call(info, "get_pinned_settings")


@strawberry.type
class SettingsMutations:
    @strawberry.mutation
    async def update_settings(self, info: Info, settings: HostSettings.Input) -> HostSettings:
        """Update host settings"""
        return await HostdBaseResolver.handle_api_call(info, "patch_settings", settings=settings)

    @strawberry.mutation
    async def update_pinned_settings(self, info: Info, settings: PinnedSettings.Input) -> bool:
        """Update pinned settings"""
        await HostdBaseResolver.handle_api_call(info, "put_pinned_settings", settings=settings)
        return True

    @strawberry.mutation
    async def announce(self, info: Info) -> bool:
        """Announce the host"""
        await HostdBaseResolver.handle_api_call(info, "post_announce")
        return True

    @strawberry.mutation
    async def update_ddns(self, info: Info, force: bool = False) -> bool:
        """Update dynamic DNS settings"""
        await HostdBaseResolver.handle_api_call(info, "put_ddns_update", force=force)
        return True
