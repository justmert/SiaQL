from typing import Optional
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import StateResponse


@strawberry.type
class StateQueries(WalletdBaseResolver):
    @strawberry.field
    async def state(self, info: Info) -> StateResponse:
        """Get current state of walletd daemon"""
        return await WalletdBaseResolver.handle_api_call(info, "get_state")
