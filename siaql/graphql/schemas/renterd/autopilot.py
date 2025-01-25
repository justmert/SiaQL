import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.resolvers.renterd import RenterdBaseResolver
from siaql.graphql.schemas.types import (
    AutopilotConfig,
    AutopilotStateResponse,
    HostResponse,
    ConfigEvaluationRequest,
    ConfigEvaluationResponse,
    PublicKey,
    SearchHostsRequest,
)
from typing import Optional
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class AutopilotQueries:
    @strawberry.field
    async def autopilot_config(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> AutopilotConfig:
        """Get the autopilot configuration"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_autopilot_config",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def autopilot_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> AutopilotStateResponse:
        """Get the current state of the autopilot"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_autopilot_state",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def autopilot_host(
        self,
        info: Info,
        host_key: PublicKey,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> HostResponse:
        """Get information about a specific host"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_autopilot_host",
            host_key=host_key,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def autopilot_hosts(
        self,
        info: Info,
        opts: SearchHostsRequest.Input,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[HostResponse]:
        """Get information about all hosts"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_autopilot_hosts",
            opts=opts,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )


@strawberry.type
class AutopilotMutations(RenterdBaseResolver):
    @strawberry.mutation
    async def update_autopilot_config(self, info: Info, config: AutopilotConfig.Input) -> bool:
        """Update the autopilot configuration"""
        await RenterdBaseResolver.handle_api_call(info, "update_autopilot_config", config=config)
        return True

    @strawberry.mutation
    async def trigger_autopilot(self, info: Info, force_scan: bool = False) -> bool:
        """Trigger an iteration of the autopilot's main loop"""
        response = await RenterdBaseResolver.handle_api_call(info, "trigger_autopilot", force_scan=force_scan)
        return response.get("triggered", False)

    @strawberry.mutation
    async def evaluate_autopilot_config(
        self, info: Info, req: ConfigEvaluationRequest.Input
    ) -> ConfigEvaluationResponse:
        """Evaluate an autopilot configuration"""
        return await RenterdBaseResolver.handle_api_call(info, "evaluate_autopilot_config", req=req)
