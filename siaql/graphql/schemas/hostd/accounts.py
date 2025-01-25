import strawberry
from typing import List, Optional
from strawberry.types import Info

from siaql.graphql.schemas.types import FundingSource, HostdAccount
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class AccountQueries:
    @strawberry.field
    async def accounts(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[HostdAccount]:
        """Get list of accounts with pagination"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_accounts", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def account_funding(
        self,
        info: Info,
        account: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[FundingSource]:
        """Get funding sources for an account"""
        return await HostdBaseResolver.handle_api_call(
            info,
            "get_account_funding",
            account=account,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )
