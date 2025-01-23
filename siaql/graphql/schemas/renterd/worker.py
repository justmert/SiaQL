from typing import Any, Dict, List, Optional

import strawberry
from strawberry.types import Info

from siaql.graphql.resolvers.renterd import RenterdBaseResolver
from siaql.graphql.schemas.types import (
    Account,
    ContractsResponse,
    DeleteObjectOptions,
    DownloadStatsResponse,
    GetObjectOptions,
    GetObjectResponse,
    HeadObjectOptions,
    HeadObjectResponse,
    HostPriceTable,
    MemoryResponse,
    MigrateSlabResponse,
    MultipartAbortRequest,
    MultipartAddPartRequest,
    MultipartCompleteRequest,
    MultipartCompleteResponse,
    MultipartCreateRequest,
    MultipartCreateResponse,
    RHPPriceTableRequest,
    RHPScanRequest,
    RHPScanResponse,
    Slab,
    UploadObjectOptions,
    UploadObjectResponse,
    UploadStatsResponse,
    WebhookEvent,
    WorkerStateResponse,
)


@strawberry.type
class WorkerQueries(RenterdBaseResolver):
    @strawberry.field
    async def worker_state(self, info: Info) -> WorkerStateResponse:
        """Get the current state of the worker"""
        return await self.handle_api_call(info, "get_worker_state")

    @strawberry.field
    async def worker_memory(self, info: Info) -> MemoryResponse:
        """Get memory statistics"""
        return await self.handle_api_call(info, "get_worker_memory")

    @strawberry.field
    async def worker_id(self, info: Info) -> str:
        """Get the worker ID"""
        return await self.handle_api_call(info, "get_worker_id")

    @strawberry.field
    async def worker_accounts(self, info: Info) -> List[Account]:
        """Get all accounts"""
        return await self.handle_api_call(info, "get_worker_accounts")

    @strawberry.field
    async def worker_account(self, info: Info, host_key: str) -> Account:
        """Get account for specific host"""
        return await self.handle_api_call(info, "get_worker_account", host_key=host_key)

    @strawberry.field
    async def worker_contracts(self, info: Info, host_timeout: Optional[int] = None) -> ContractsResponse:
        """Get all contracts"""
        return await self.handle_api_call(info, "get_worker_contracts", host_timeout=host_timeout)

    @strawberry.field
    async def worker_object(self, info: Info, bucket: str, path: str, opts: GetObjectOptions) -> GetObjectResponse:
        """Get object data"""
        return await self.handle_api_call(info, "get_worker_object", bucket=bucket, path=path, opts=opts)

    @strawberry.field
    async def download_stats(self, info: Info) -> DownloadStatsResponse:
        """Get download statistics"""
        return await self.handle_api_call(info, "get_worker_downloads_stats")

    @strawberry.field
    async def upload_stats(self, info: Info) -> UploadStatsResponse:
        """Get upload statistics"""
        return await self.handle_api_call(info, "get_worker_uploads_stats")


@strawberry.type
class WorkerMutations(RenterdBaseResolver):
    @strawberry.mutation
    async def rhp_scan(self, info: Info, req: RHPScanRequest) -> RHPScanResponse:
        """Perform RHP scan"""
        return await self.handle_api_call(info, "rhp_scan", req=req)

    @strawberry.mutation
    async def rhp_price_table(self, info: Info, req: RHPPriceTableRequest) -> HostPriceTable:
        """Get host price table"""
        return await self.handle_api_call(info, "rhp_price_table", req=req)

    @strawberry.mutation
    async def upload_object(
        self, info: Info, bucket: str, path: str, data: bytes, options: UploadObjectOptions
    ) -> UploadObjectResponse:
        """Upload an object"""
        return await self.handle_api_call(info, "upload_object", bucket=bucket, path=path, data=data, options=options)

    @strawberry.mutation
    async def delete_object(self, info: Info, bucket: str, path: str, opts: DeleteObjectOptions) -> bool:
        """Delete an object"""
        await self.handle_api_call(info, "delete_worker_object", bucket=bucket, path=path, opts=opts)
        return True

    @strawberry.mutation
    async def head_object(self, info: Info, bucket: str, path: str, opts: HeadObjectOptions) -> HeadObjectResponse:
        """Get object metadata"""
        return await self.handle_api_call(info, "head_object", bucket=bucket, path=path, opts=opts)

    @strawberry.mutation
    async def multipart_create(self, info: Info, req: MultipartCreateRequest) -> MultipartCreateResponse:
        """Create multipart upload"""
        return await self.handle_api_call(info, "multipart_create", req=req)

    @strawberry.mutation
    async def multipart_abort(self, info: Info, req: MultipartAbortRequest) -> bool:
        """Abort multipart upload"""
        await self.handle_api_call(info, "multipart_abort", req=req)
        return True

    @strawberry.mutation
    async def multipart_complete(self, info: Info, req: MultipartCompleteRequest) -> MultipartCompleteResponse:
        """Complete multipart upload"""
        return await self.handle_api_call(info, "multipart_complete", req=req)

    @strawberry.mutation
    async def multipart_upload(self, info: Info, path: str, req: MultipartAddPartRequest) -> bool:
        """Upload a part in multipart upload"""
        await self.handle_api_call(info, "multipart_upload", path=path, req=req)
        return True

    @strawberry.mutation
    async def migrate_slab(self, info: Info, slab: Slab) -> MigrateSlabResponse:
        """Migrate a slab"""
        return await self.handle_api_call(info, "migrate_slab", slab=slab)

    @strawberry.mutation
    async def reset_account_drift(self, info: Info, account_id: str) -> bool:
        """Reset account drift"""
        await self.handle_api_call(info, "reset_account_drift", account_id=account_id)
        return True

    @strawberry.mutation
    async def register_worker_event(self, info: Info, event: WebhookEvent) -> bool:
        """Register a worker event"""
        await self.handle_api_call(info, "register_worker_event", event=event)
        return True
