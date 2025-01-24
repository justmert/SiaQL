import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import SiacoinElement, SiafundElement


@strawberry.type
class OutputsQueries:
    @strawberry.field
    async def get_siacoin_output(self, info: Info, id: str) -> SiacoinElement:
        """Get rescan status"""
        data = await WalletdBaseResolver.handle_api_call(info, "get_siacoin_output", id=id)
        return data

    @strawberry.field
    async def get_siafund_output(self, info: Info, id: str) -> SiafundElement:
        """Start rescan from height"""
        await WalletdBaseResolver.handle_api_call(info, "get_siafund_output", id=id)
        return True
