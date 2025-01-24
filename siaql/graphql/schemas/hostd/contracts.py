import strawberry
from typing import List, Optional
from strawberry.types import Info

from siaql.graphql.schemas.types import (
    Contract,
    ContractFilter,
    FileContractID,
    ContractsResponse,
    IntegrityCheckResult,
)
from siaql.graphql.resolvers.hostd import HostdBaseResolver


@strawberry.type
class ContractQueries:
    @strawberry.field
    async def contracts(self, info: Info, filter: ContractFilter.Input) -> ContractsResponse:
        """Get contracts matching the filter"""
        return await HostdBaseResolver.handle_api_call(info, "post_contracts", filter=filter)

    @strawberry.field
    async def contract(self, info: Info, id: FileContractID) -> Contract:
        """Get a specific contract by ID"""
        return await HostdBaseResolver.handle_api_call(info, "get_contract", id=id)

    @strawberry.field
    async def contract_integrity(self, info: Info, id: FileContractID) -> Optional[IntegrityCheckResult]:
        """Get integrity check result for a contract"""
        return await HostdBaseResolver.handle_api_call(info, "get_contract_integrity", id=id)


@strawberry.type
class ContractMutations:
    @strawberry.mutation
    async def check_contract_integrity(self, info: Info, id: FileContractID) -> bool:
        """Start integrity check for a contract"""
        await HostdBaseResolver.handle_api_call(info, "put_contract_integrity", id=id)
        return True

    @strawberry.mutation
    async def delete_contract_integrity(self, info: Info, id: FileContractID) -> bool:
        """Delete integrity check result for a contract"""
        await HostdBaseResolver.handle_api_call(info, "delete_contract_integrity", id=id)
        return True
