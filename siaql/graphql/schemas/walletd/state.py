from typing import Optional
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver

@strawberry.type
class State:
    version: str
    commit: str
    os: str
    build_time: datetime = strawberry.field(name="buildTime")
    start_time: datetime = strawberry.field(name="startTime")
    index_mode: str = strawberry.field(name="indexMode")

@strawberry.type
class StateQueries(WalletdBaseResolver):
    @strawberry.field
    async def state(self, info: Info) -> State:
        """Gets the current state of the running walletd node"""
        def transform_state(state: dict) -> State:
            return State(
                version=state["version"],
                commit=state["commit"],
                os=state["os"],
                build_time=datetime.fromisoformat(state["buildTime"].replace('Z', '+00:00')),
                start_time=datetime.fromisoformat(state["startTime"].replace('Z', '+00:00')),
                index_mode=state["indexMode"]
            )

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_state",
            transform_func=transform_state
        )
        return data