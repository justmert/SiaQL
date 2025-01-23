import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import HostsRequest
from siaql.graphql.resolvers.renterd import RenterdBaseResolver
from siaql.graphql.schemas.types import (
    AutopilotConfig,
    AutopilotStateResponse,
    HostResponse,
    ConfigEvaluationRequest,
    ConfigEvaluationResponse,
    PublicKey,
)
from typing import Optional


@strawberry.type
class AutopilotQueries(RenterdBaseResolver):
    @strawberry.field
    async def autopilot_config(self, info: Info) -> AutopilotConfig:
        """Get the autopilot configuration"""
        return await self.handle_api_call(info, "get_autopilot_config")

    @strawberry.field
    async def autopilot_state(self, info: Info) -> AutopilotStateResponse:
        """Get the current state of the autopilot"""
        return await self.handle_api_call(info, "get_autopilot_state")

    @strawberry.field
    async def autopilot_host(self, info: Info, host_key: PublicKey) -> HostResponse:
        """Get information about a specific host"""
        return await self.handle_api_call(info, "get_autopilot_host", host_key=host_key)

    @strawberry.field
    async def autopilot_hosts(
        self,
        info: Info,
        filter_mode: Optional[str] = None,
        usability_mode: Optional[str] = None,
        address_contains: Optional[str] = None,
        key_in: Optional[List[PublicKey]] = None,
        offset: int = 0,
        limit: int = -1,
    ) -> List[HostResponse]:
        """Get information about all hosts"""
        return await self.handle_api_call(
            info,
            "get_autopilot_hosts",
            filter_mode=filter_mode,
            usability_mode=usability_mode,
            address_contains=address_contains,
            key_in=key_in,
            offset=offset,
            limit=limit,
        )


@strawberry.type
class AutopilotMutations(RenterdBaseResolver):
    @strawberry.mutation
    async def update_autopilot_config(self, info: Info, config: AutopilotConfig) -> bool:
        """Update the autopilot configuration"""
        await self.handle_api_call(info, "update_autopilot_config", config=config)
        return True

    @strawberry.mutation
    async def trigger_autopilot(self, info: Info, force_scan: bool = False) -> bool:
        """Trigger an iteration of the autopilot's main loop"""
        response = await self.handle_api_call(info, "trigger_autopilot", force_scan=force_scan)
        return response.get("triggered", False)

    @strawberry.mutation
    async def evaluate_autopilot_config(self, info: Info, req: ConfigEvaluationRequest) -> ConfigEvaluationResponse:
        """Evaluate an autopilot configuration"""
        return await self.handle_api_call(info, "evaluate_autopilot_config", req=req)
