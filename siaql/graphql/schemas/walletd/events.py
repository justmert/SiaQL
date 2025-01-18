from typing import List, Optional, Union
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import Event

@strawberry.type
class EventQueries:
    @strawberry.field
    async def event(self, info: Info, event_id: str) -> Event:
        """Get a specific event"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_event",
            event_id=event_id
        )
