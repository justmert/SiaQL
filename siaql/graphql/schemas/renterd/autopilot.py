import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import HostsRequest
from siaql.graphql.resolvers.renterd import RenterdBaseResolver
from siaql.graphql.schemas.types import AutopilotConfig, AutopilotStateResponse, Host


@strawberry.type
class AutopilotQueries(RenterdBaseResolver):
    @strawberry.field
    async def autopilot_config(self, info: Info) -> AutopilotConfig:
        """Get autopilot configuration"""
        return await RenterdBaseResolver.handle_api_call(info, "get_autopilot_config")

    @strawberry.field
    async def autopilot_host(self, info: Info, host_key: str) -> Host:
        """Get host information"""
        return await RenterdBaseResolver.handle_api_call(info, "get_autopilot_host", host_key=host_key)

    @strawberry.field
    async def autopilot_state(self, info: Info) -> AutopilotStateResponse:
        """Get autopilot state"""
        return await RenterdBaseResolver.handle_api_call(info, "get_autopilot_state")

    @strawberry.field  # news
    async def autopilots(self, info: Info) -> List[AutopilotConfig]:
        """Get all autopilot configurations"""
        return await self.handle_api_call(info, "get_autopilots")

    @strawberry.field
    async def autopilot(self, info: Info, autopilot_id: str) -> AutopilotConfig:
        """Get specific autopilot configuration"""
        return await self.handle_api_call(info, "get_autopilot", autopilot_id=autopilot_id)


@strawberry.type
class AutopilotMutations(RenterdBaseResolver):
    @strawberry.mutation
    async def update_autopilot_config(self, info: Info, config: AutopilotConfig) -> bool:
        """Update autopilot configuration"""
        await RenterdBaseResolver.handle_api_call(info, "update_autopilot_config", config=config)
        return True

    @strawberry.mutation
    async def trigger_autopilot(self, info: Info, force_scan: bool = False) -> bool:
        """Trigger autopilot"""
        return await RenterdBaseResolver.handle_api_call(info, "trigger_autopilot", force_scan=force_scan)

    @strawberry.mutation
    async def autopilot_search_hosts(self, info: Info, request: HostsRequest) -> List[Host]:
        """Search hosts"""
        return await RenterdBaseResolver.handle_api_call(info, "search_hosts", request=request)

    @strawberry.mutation  # new
    async def update_autopilot(self, info: Info, autopilot_id: str, config: AutopilotConfig) -> bool:
        """Update specific autopilot configuration"""
        await self.handle_api_call(info, "update_autopilot", autopilot_id=autopilot_id, config=config)
        return True
