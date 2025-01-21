import strawberry
from typing import List, Optional
from strawberry.types import Info
from siaql.graphql.resolvers.renterd import RenterdBaseResolver
from siaql.graphql.schemas.types import (
    Account,
    MemoryResponse,
    DownloadStatsResponse,
    UploadStatsResponse,
    UploadMultipartUploadPartOptions,
    UploadMultipartUploadPartResponse,
    UploadObjectOptions,
    UploadObjectResponse,
)


@strawberry.type
class WorkerQueries(RenterdBaseResolver):
    @strawberry.field
    async def account(self, info: Info, host_key: str) -> Account:
        """Get account for a host"""
        return await RenterdBaseResolver.handle_api_call(info, "get_worker_account", host_key=host_key)

    @strawberry.field
    async def worker_id(self, info: Info) -> str:
        """Get worker ID"""
        return await RenterdBaseResolver.handle_api_call(info, "get_worker_id")

    @strawberry.field
    async def memory_state(self, info: Info) -> MemoryResponse:
        """Get memory state"""
        return await RenterdBaseResolver.handle_api_call(info, "get_memory_state")

    @strawberry.field
    async def download_stats(self, info: Info) -> DownloadStatsResponse:
        """Get download statistics"""
        return await RenterdBaseResolver.handle_api_call(info, "get_download_stats")

    @strawberry.field
    async def upload_stats(self, info: Info) -> UploadStatsResponse:
        """Get upload statistics"""
        return await RenterdBaseResolver.handle_api_call(info, "get_upload_stats")

    @strawberry.field
    async def worker_object(self, info: Info, bucket: str, key: str, opts: DownloadObjectOptions) -> GetObjectResponse:
        """Get object from worker"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_object",
            bucket=bucket,
            key=key,
            opts=opts
        )

    @strawberry.field
    async def rhp_contracts(self, info: Info) -> Dict[str, Contract]:
        """Get all contracts"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_rhp_contracts"
        )

    @strawberry.field
    async def worker_state(self, info: Info) -> WorkerStateResponse:
        """Get worker state"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_state"
        )




@strawberry.type
class WorkerMutations(RenterdBaseResolver):


    @strawberry.mutation
    async def upload_object(
        self, info: Info, bucket: str, key: str, data: str, opts: UploadObjectOptions
    ) -> UploadObjectResponse:
        """Upload an object"""
        return await RenterdBaseResolver.handle_api_call(
            info, "upload_object", bucket=bucket, key=key, data=data, opts=opts
        )

    @strawberry.mutation
    async def delete_object(self, info: Info, bucket: str, key: str) -> bool:
        """Delete an object"""
        await RenterdBaseResolver.handle_api_call(info, "delete_object", bucket=bucket, key=key)
        return True

    @strawberry.mutation
    async def upload_multipart_part(
        self,
        info: Info,
        bucket: str,
        key: str,
        upload_id: str,
        part_number: int,
        opts: UploadMultipartUploadPartOptions,
    ) -> UploadMultipartUploadPartResponse:
        """Upload part of multipart upload"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "upload_multipart_part",
            bucket=bucket,
            key=key,
            upload_id=upload_id,
            part_number=part_number,
            opts=opts,
        )
    
        @strawberry.mutation
    async def broadcast_contract(self, info: Info, contract_id: str) -> bool:
        """Broadcast contract"""
        await RenterdBaseResolver.handle_api_call(
            info,
            "broadcast_contract",
            contract_id=contract_id
        )
        return True

    @strawberry.mutation
    async def prune_contract(self, info: Info, contract_id: str, request: ContractPruneRequest) -> ContractPruneResponse:
        """Prune contract"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "prune_contract",
            contract_id=contract_id,
            request=request
        )

    @strawberry.mutation
    async def get_contract_roots(self, info: Info, contract_id: str) -> List[str]:
        """Get contract roots"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contract_roots",
            contract_id=contract_id
        )

    @strawberry.mutation
    async def form_contract(self, info: Info, request: ContractFormRequest) -> ContractMetadata:
        """Form a new contract"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "form_contract",
            request=request
        )

    @strawberry.mutation
    async def fund_contract(self, info: Info, request: RHPFundRequest) -> bool:
        """Fund a contract"""
        await RenterdBaseResolver.handle_api_call(
            info,
            "fund_contract",
            request=request
        )
        return True

    @strawberry.mutation
    async def renew_contract(self, info: Info, request: ContractRenewRequest) -> ContractMetadata:
        """Renew a contract"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "renew_contract",
            request=request
        )

    @strawberry.mutation
    async def scan_host(self, info: Info, request: HostScanRequest) -> HostScanResponse:
        """Scan a host"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "scan_host",
            request=request
        )

    @strawberry.mutation
    async def sync_contract(self, info: Info, request: RHPSyncRequest) -> bool:
        """Sync a contract"""
        await RenterdBaseResolver.handle_api_call(
            info,
            "sync_contract",
            request=request
        )
        return True

    @strawberry.mutation
    async def migrate_slab(self, info: Info, request: MigrationSlabsRequest) -> SlabsForMigrationResponse:
        """Migrate a slab"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "migrate_slab",
            request=request
        )
