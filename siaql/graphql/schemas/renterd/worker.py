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
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class WorkerQueries:
    @strawberry.field
    async def worker_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> WorkerStateResponse:
        """Get the current state of the worker"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_state",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def worker_memory(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> MemoryResponse:
        """Get memory statistics"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_memory",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def worker_id(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> str:
        """Get the worker ID"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_id",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def worker_accounts(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Account]:
        """Get all accounts"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_accounts",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def worker_account(
        self,
        info: Info,
        host_key: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Account:
        """Get account for specific host"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_account",
            host_key=host_key,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def worker_contracts(
        self,
        info: Info,
        host_timeout: Optional[int] = None,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ContractsResponse:
        """Get all contracts"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_contracts",
            host_timeout=host_timeout,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def worker_object(
        self,
        info: Info,
        bucket: str,
        path: str,
        opts: GetObjectOptions.Input,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> GetObjectResponse:
        """Get object data"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_object",
            bucket=bucket,
            path=path,
            opts=opts,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def download_stats(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> DownloadStatsResponse:
        """Get download statistics"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_downloads_stats",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def upload_stats(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> UploadStatsResponse:
        """Get upload statistics"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_worker_uploads_stats",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )


@strawberry.type
class WorkerMutations(RenterdBaseResolver):
    @strawberry.mutation
    async def rhp_scan(self, info: Info, req: RHPScanRequest.Input) -> RHPScanResponse:
        """Perform RHP scan"""
        return await RenterdBaseResolver.handle_api_call(info, "rhp_scan", req=req)

    @strawberry.mutation
    async def rhp_price_table(self, info: Info, req: RHPPriceTableRequest.Input) -> HostPriceTable:
        """Get host price table"""
        return await RenterdBaseResolver.handle_api_call(info, "rhp_price_table", req=req)

    @strawberry.mutation
    async def upload_object(
        self, info: Info, bucket: str, path: str, data: str, options: UploadObjectOptions.Input
    ) -> UploadObjectResponse:
        """Upload an object"""
        return await RenterdBaseResolver.handle_api_call(
            info, "upload_object", bucket=bucket, path=path, data=data, options=options
        )

    @strawberry.mutation
    async def delete_object(self, info: Info, bucket: str, path: str, opts: DeleteObjectOptions.Input) -> bool:
        """Delete an object"""
        await RenterdBaseResolver.handle_api_call(info, "delete_worker_object", bucket=bucket, path=path, opts=opts)
        return True

    @strawberry.mutation
    async def head_object(
        self, info: Info, bucket: str, path: str, opts: HeadObjectOptions.Input
    ) -> HeadObjectResponse:
        """Get object metadata"""
        return await RenterdBaseResolver.handle_api_call(info, "head_object", bucket=bucket, path=path, opts=opts)

    @strawberry.mutation
    async def multipart_create(self, info: Info, req: MultipartCreateRequest.Input) -> MultipartCreateResponse:
        """Create multipart upload"""
        return await RenterdBaseResolver.handle_api_call(info, "multipart_create", req=req)

    @strawberry.mutation
    async def multipart_abort(self, info: Info, req: MultipartAbortRequest.Input) -> bool:
        """Abort multipart upload"""
        await RenterdBaseResolver.handle_api_call(info, "multipart_abort", req=req)
        return True

    @strawberry.mutation
    async def multipart_complete(self, info: Info, req: MultipartCompleteRequest.Input) -> MultipartCompleteResponse:
        """Complete multipart upload"""
        return await RenterdBaseResolver.handle_api_call(info, "multipart_complete", req=req)

    @strawberry.mutation
    async def multipart_upload(self, info: Info, path: str, req: MultipartAddPartRequest.Input) -> bool:
        """Upload a part in multipart upload"""
        await RenterdBaseResolver.handle_api_call(info, "multipart_upload", path=path, req=req)
        return True

    @strawberry.mutation
    async def migrate_slab(self, info: Info, slab: Slab.Input) -> MigrateSlabResponse:
        """Migrate a slab"""
        return await RenterdBaseResolver.handle_api_call(info, "migrate_slab", slab=slab)

    @strawberry.mutation
    async def reset_account_drift(self, info: Info, account_id: str) -> bool:
        """Reset account drift"""
        await RenterdBaseResolver.handle_api_call(info, "reset_account_drift", account_id=account_id)
        return True

    @strawberry.mutation
    async def register_worker_event(self, info: Info, event: WebhookEvent.Input) -> bool:
        """Register a worker event"""
        await RenterdBaseResolver.handle_api_call(info, "register_worker_event", event=event)
        return True
