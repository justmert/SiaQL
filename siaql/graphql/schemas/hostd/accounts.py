import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import FundingSource, HostdAccount
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class AccountQueries:
    @strawberry.field
    async def accounts(self, info: Info, limit: int = 100, offset: int = 0) -> List[HostdAccount]:
        """Get list of accounts with pagination"""
        return await HostdBaseResolver.handle_api_call(info, "get_accounts", limit=limit, offset=offset)

    @strawberry.field
    async def account_funding(self, info: Info, account: str) -> List[FundingSource]:
        """Get funding sources for an account"""
        return await HostdBaseResolver.handle_api_call(info, "get_account_funding", account=account)
