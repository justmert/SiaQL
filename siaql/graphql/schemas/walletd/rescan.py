# graphql/schemas/walletd/rescan.py

import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import RescanResponse

@strawberry.type
class RescanQueries:
    @strawberry.field
    async def rescan_status(self, info: Info) -> RescanResponse:
        """Get rescan status"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_rescan_status"
        )
        return data

@strawberry.type
class RescanMutations:
    @strawberry.mutation
    async def start_rescan(self, info: Info, height: int) -> bool:
        """Start rescan from height"""
        await WalletdBaseResolver.handle_api_call(
            info,
            "start_rescan",
            height=height
        )
        return True