import strawberry
from typing import List, Optional
from strawberry.types import Info

from siaql.graphql.schemas.types import (
    Contract,
    ContractFilter,
    FileContractID,
    HostdContractsResponse,
    IntegrityCheckResult,
)
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput

from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class ContractQueries:
    @strawberry.field
    async def hostd_contracts(
        self,
        info: Info,
        filter: ContractFilter.Input,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> HostdContractsResponse:
        """Get contracts matching the filter"""
        return await HostdBaseResolver.handle_api_call(
            info, "post_contracts", filter=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def hostd_contract(
        self,
        info: Info,
        id: FileContractID,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Contract:
        """Get a specific contract by ID"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_contract", id=id, filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def hostd_contract_integrity(
        self,
        info: Info,
        id: FileContractID,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Optional[IntegrityCheckResult]:
        """Get integrity check result for a contract"""
        return await HostdBaseResolver.handle_api_call(
            info, "get_contract_integrity", id=id, filter_input=filter, sort_input=sort, pagination_input=pagination
        )


@strawberry.type
class ContractMutations:
    @strawberry.mutation
    async def hostd_check_contract_integrity(self, info: Info, id: FileContractID) -> bool:
        """Start integrity check for a contract"""
        await HostdBaseResolver.handle_api_call(info, "put_contract_integrity", id=id)
        return True

    @strawberry.mutation
    async def hostd_delete_contract_integrity(self, info: Info, id: FileContractID) -> bool:
        """Delete integrity check result for a contract"""
        await HostdBaseResolver.handle_api_call(info, "delete_contract_integrity", id=id)
        return True
