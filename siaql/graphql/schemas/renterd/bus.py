from typing import Any, Dict, List, Optional

import strawberry
from strawberry.types import Info

from siaql.graphql.resolvers.renterd import RenterdBaseResolver

from siaql.graphql.schemas.types import (
    Account,
    AccountsFundRequest,
    AccountsFundResponse,
    AccountsSaveRequest,
    AddObjectRequest,
    AddPartialSlabResponse,
    Alert,
    AlertsOpts,
    AlertsResponse,
    ArchivedContract,
    Autopilot,
    Block,
    Bucket,
    BucketCreateRequest,
    BucketPolicy,
    BusStateResponse,
    ConsensusState,
    ContractAcquireRequest,
    ContractAcquireResponse,
    ContractAddRequest,
    ContractFormRequest,
    ContractKeepaliveRequest,
    ContractMetadata,
    ContractPruneRequest,
    ContractPruneResponse,
    ContractRenewedRequest,
    ContractRenewRequest,
    ContractRootsResponse,
    ContractsArchiveRequest,
    ContractSetUpdateRequest,
    ContractSize,
    ContractSpendingRecord,
    ContractsPrunableDataResponse,
    CopyObjectsRequest,
    Currency,
    FileContractID,
    GougingParams,
    Hash256,
    Host,
    HostAddress,
    HostCheck,
    HostsPriceTablesRequest,
    HostsRemoveRequest,
    HostsScanRequest,
    MigrationSlabsRequest,
    MultipartAbortRequest,
    MultipartAddPartRequest,
    MultipartCompleteRequest,
    MultipartCompleteResponse,
    MultipartCreateRequest,
    MultipartCreateResponse,
    MultipartListPartsRequest,
    MultipartListPartsResponse,
    MultipartListUploadsRequest,
    MultipartListUploadsResponse,
    MultipartUpload,
    Network,
    Object,
    ObjectMetadata,
    ObjectsListRequest,
    ObjectsListResponse,
    ObjectsRenameRequest,
    ObjectsStatsResponse,
    PackedSlab,
    PackedSlabsRequestGET,
    PackedSlabsRequestPOST,
    PublicKey,
    SearchHostsRequest,
    SiacoinElement,
    Slab,
    SlabBuffer,
    Transaction,
    TransactionID,
    UnhealthySlabsResponse,
    UpdateAllowlistRequest,
    UpdateBlocklistRequest,
    UploadParams,
    UploadSectorRequest,
    WalletFundRequest,
    WalletFundResponse,
    WalletRedistributeRequest,
    WalletResponse,
    WalletSendRequest,
    WalletSignRequest,
    Webhook,
    WebhookEvent,
    WebhookResponse,
)
from siaql.graphql.resolvers.filter import FilterInput, PaginationInput, SortInput

from strawberry.scalars import JSON


@strawberry.type
class BusQueries:
    @strawberry.field
    async def renterd_accounts(
        self,
        info: Info,
        owner: Optional[str] = None,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Account]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_accounts",
            owner=owner,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_alerts(
        self,
        info: Info,
        opts: AlertsOpts.Input,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> AlertsResponse:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_alerts",
            opts=opts,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_autopilot(
        self,
        info: Info,
        id: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Autopilot:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_autopilot",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_get_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> BusStateResponse:
        """Get the current bus state"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_state",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contract_renewed(
        self,
        info: Info,
        id: FileContractID,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ContractMetadata:
        """Get the renewed contract for a given contract ID"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contract_renewed",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_consensus_network(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Network:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_consensus_network",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_multipart_list_parts(
        self,
        info: Info,
        req: MultipartListPartsRequest.Input,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> MultipartListPartsResponse:
        """List parts of a multipart upload"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "list_multipart_parts",
            req=req,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_multipart_list_uploads(
        self,
        info: Info,
        req: MultipartListUploadsRequest.Input,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> MultipartListUploadsResponse:
        """List all multipart uploads"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "list_multipart_uploads",
            req=req,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_multipart_upload(
        self,
        info: Info,
        id: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> MultipartUpload:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_multipart_upload",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_autopilots(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Autopilot]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_autopilots",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_buckets(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Bucket]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_buckets",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_bucket(
        self,
        info: Info,
        name: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Bucket:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_bucket",
            name=name,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_consensus_state(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ConsensusState:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_consensus_state",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contracts(
        self,
        info: Info,
        contract_set: Optional[str] = None,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[ContractMetadata]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contracts",
            contract_set=contract_set,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contract(
        self,
        info: Info,
        id: FileContractID,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contract",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contract_size(
        self,
        info: Info,
        id: FileContractID,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ContractSize:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contract_size",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_get_hosts(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Host]:
        """Get all hosts"""
        return await RenterdBaseResolver.handle_api_call(
            info, "get_hosts", filter_input=filter, sort_input=sort, pagination_input=pagination
        )

    @strawberry.field
    async def renterd_hosts_allowlist(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[PublicKey]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_hosts_allowlist",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_hosts_blocklist(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_hosts_blocklist",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_host(
        self,
        info: Info,
        public_key: PublicKey,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Host:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_host",
            public_key=public_key,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_search_hosts(
        self,
        info: Info,
        req: SearchHostsRequest.Input,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Host]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "search_hosts",
            req=req,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_object(
        self,
        info: Info,
        path: str,
        bucket: Optional[str] = None,
        only_metadata: bool = False,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Object:
        return await RenterdBaseResolver.handle_api_call(
            info, "get_object", path=path, bucket=bucket, only_metadata=only_metadata
        )

    @strawberry.field
    async def renterd_search_objects(
        self,
        info: Info,
        key: str,
        bucket: str = "default",
        offset: int = 0,
        limit: int = -1,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[ObjectMetadata]:
        return await RenterdBaseResolver.handle_api_call(
            info, "search_objects", key=key, bucket=bucket, offset=offset, limit=limit
        )

    @strawberry.field
    async def renterd_objects_stats(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ObjectsStatsResponse:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_objects_stats",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_slab_buffers(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[SlabBuffer]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_slab_buffers",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_wallet(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> WalletResponse:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_wallet",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_webhooks(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> WebhookResponse:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_webhooks",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_gouging_params(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> GougingParams:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_gouging_params",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_upload_params(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> UploadParams:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_upload_params",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_consensus_siafund_fee(
        self,
        info: Info,
        payout: Currency,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Currency:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_consensus_siafund_fee",
            payout=payout,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contract_sets(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contract_sets",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contract_roots(
        self,
        info: Info,
        id: FileContractID,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ContractRootsResponse:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contract_roots",
            id=id,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contract_ancestors(
        self,
        info: Info,
        id: FileContractID,
        min_start_height: int,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[ArchivedContract]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contract_ancestors",
            id=id,
            min_start_height=min_start_height,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_contracts_prunable(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> ContractsPrunableDataResponse:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_contracts_prunable",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_hosts_scanning(
        self,
        info: Info,
        last_scan: Optional[str] = None,
        offset: int = 0,
        limit: int = -1,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[HostAddress]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_hosts_scanning",
            last_scan=last_scan,
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_metric(
        self,
        info: Info,
        key: str,
        start: str,
        n: int,
        interval: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> JSON:  # Response type varies based on metric type
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_metric",
            key=key,
            start=start,
            n=n,
            interval=interval,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_settings(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_settings",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_setting(
        self,
        info: Info,
        key: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> str:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_setting",
            key=key,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_slab(
        self,
        info: Info,
        key: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Slab:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_slab",
            key=key,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_slab_objects(
        self,
        info: Info,
        key: str,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[ObjectMetadata]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_slab_objects",
            key=key,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_slabs_partial(
        self,
        info: Info,
        key: str,
        offset: int,
        length: int,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> str:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_slabs_partial",
            key=key,
            offset=offset,
            length=length,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_syncer_address(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> str:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_syncer_address",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_syncer_peers(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_syncer_peers",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_txpool_recommended_fee(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Currency:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_txpool_recommended_fee",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_txpool_transactions(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Transaction]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_txpool_transactions",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_wallet_outputs(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[SiacoinElement]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_wallet_outputs",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_wallet_pending(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Transaction]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_wallet_pending",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def renterd_wallet_transactions(
        self,
        info: Info,
        offset: int = 0,
        limit: int = -1,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Transaction]:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_wallet_transactions",
            offset=offset,
            limit=limit,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )


@strawberry.type
class BusMutations:
    @strawberry.mutation
    async def renterd_update_autopilot_host_check(
        self, info: Info, autopilot_id: str, host_key: PublicKey, check: HostCheck.Input
    ) -> bool:
        await RenterdBaseResolver.handle_api_call(
            info, "update_autopilot_host_check", autopilot_id=autopilot_id, host_key=host_key, check=check
        )
        return True

    @strawberry.mutation
    async def renterd_fund_account(self, info: Info, req: AccountsFundRequest.Input) -> AccountsFundResponse:
        return await RenterdBaseResolver.handle_api_call(info, "fund_account", req=req)

    @strawberry.mutation
    async def renterd_save_accounts(self, info: Info, req: AccountsSaveRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "save_accounts", req=req)
        return True

    @strawberry.mutation
    async def renterd_dismiss_alerts(self, info: Info, ids: List[Hash256]) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "dismiss_alerts", ids=ids)
        return True

    @strawberry.mutation
    async def renterd_register_alert(self, info: Info, alert: Alert.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "register_alert", alert=alert)
        return True

    @strawberry.mutation
    async def renterd_update_autopilot(self, info: Info, id: str, autopilot: Autopilot.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_autopilot", id=id, autopilot=autopilot)
        return True

    @strawberry.mutation
    async def renterd_create_bucket(self, info: Info, req: BucketCreateRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "create_bucket", req=req)
        return True

    @strawberry.mutation
    async def renterd_delete_bucket(self, info: Info, name: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_bucket", name=name)
        return True

    @strawberry.mutation
    async def renterd_update_contract_set(self, info: Info, set_name: str, req: ContractSetUpdateRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_contract_set", set_name=set_name, req=req)
        return True

    @strawberry.mutation
    async def renterd_delete_contract_set(self, info: Info, set_name: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_contract_set", set_name=set_name)
        return True

    @strawberry.mutation
    async def renterd_acquire_contract(
        self, info: Info, id: FileContractID, req: ContractAcquireRequest.Input
    ) -> ContractAcquireResponse:
        return await RenterdBaseResolver.handle_api_call(info, "acquire_contract", id=id, req=req)

    @strawberry.mutation
    async def renterd_keepalive_contract(self, info: Info, id: FileContractID, req: ContractKeepaliveRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "keepalive_contract", id=id, req=req)
        return True

    @strawberry.mutation
    async def renterd_release_contract(self, info: Info, id: FileContractID, lock_id: int) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "release_contract", id=id, lock_id=lock_id)
        return True

    @strawberry.mutation
    async def renterd_prune_contract(
        self, info: Info, id: FileContractID, req: ContractPruneRequest.Input
    ) -> ContractPruneResponse:
        return await RenterdBaseResolver.handle_api_call(info, "prune_contract", id=id, req=req)

    @strawberry.mutation
    async def renterd_renew_contract(self, info: Info, id: FileContractID, req: ContractRenewRequest.Input) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "renew_contract", id=id, req=req)

    @strawberry.mutation
    async def renterd_add_renewed_contract(
        self, info: Info, id: FileContractID, req: ContractRenewedRequest.Input
    ) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "add_renewed_contract", id=id, req=req)

    @strawberry.mutation
    async def renterd_add_contract(self, info: Info, id: FileContractID, req: ContractAddRequest.Input) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "add_contract", id=id, req=req)

    @strawberry.mutation
    async def renterd_archive_contracts(self, info: Info, req: ContractsArchiveRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "archive_contracts", req=req)
        return True

    @strawberry.mutation
    async def renterd_record_contract_spending(self, info: Info, records: List[ContractSpendingRecord.Input]) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "record_contract_spending", records=records)
        return True

    @strawberry.mutation
    async def renterd_update_hosts_allowlist(self, info: Info, req: UpdateAllowlistRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_hosts_allowlist", req=req)
        return True

    @strawberry.mutation
    async def renterd_delete_contract(self, info: Info, id: FileContractID) -> bool:
        """Delete a contract by ID"""
        await RenterdBaseResolver.handle_api_call(info, "delete_contract", id=id)
        return True

    @strawberry.mutation
    async def renterd_update_hosts_blocklist(self, info: Info, req: UpdateBlocklistRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_hosts_blocklist", req=req)
        return True

    @strawberry.mutation
    async def renterd_record_hosts_scan(self, info: Info, req: HostsScanRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "record_hosts_scan", req=req)
        return True

    @strawberry.mutation
    async def renterd_record_price_tables(self, info: Info, req: HostsPriceTablesRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "record_price_tables", req=req)
        return True

    @strawberry.mutation
    async def renterd_add_object(self, info: Info, path: str, req: AddObjectRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "add_object", path=path, req=req)
        return True

    @strawberry.mutation
    async def renterd_copy_object(self, info: Info, req: CopyObjectsRequest.Input) -> ObjectMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "copy_object", req=req)

    @strawberry.mutation
    async def renterd_delete_object(self, info: Info, path: str, bucket: Optional[str] = None, batch: bool = False) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_object", path=path, bucket=bucket, batch=batch)
        return True

    @strawberry.mutation
    async def renterd_rename_object(self, info: Info, req: ObjectsRenameRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "rename_object", req=req)
        return True

    @strawberry.mutation
    async def renterd_list_objects(self, info: Info, req: ObjectsListRequest.Input) -> ObjectsListResponse:
        return await RenterdBaseResolver.handle_api_call(info, "list_objects", req=req)

    @strawberry.mutation
    async def renterd_create_multipart_upload(self, info: Info, req: MultipartCreateRequest.Input) -> MultipartCreateResponse:
        return await RenterdBaseResolver.handle_api_call(info, "create_multipart_upload", req=req)

    @strawberry.mutation
    async def renterd_abort_multipart_upload(self, info: Info, req: MultipartAbortRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "abort_multipart_upload", req=req)
        return True

    @strawberry.mutation
    async def renterd_complete_multipart_upload(
        self, info: Info, req: MultipartCompleteRequest.Input
    ) -> MultipartCompleteResponse:
        return await RenterdBaseResolver.handle_api_call(info, "complete_multipart_upload", req=req)

    @strawberry.mutation
    async def renterd_add_multipart_part(self, info: Info, req: MultipartAddPartRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "add_multipart_part", req=req)
        return True

    @strawberry.mutation
    async def renterd_form_contract(self, info: Info, req: ContractFormRequest.Input) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "form_contract", req=req)

    @strawberry.mutation
    async def renterd_fetch_packed_slabs(self, info: Info, req: PackedSlabsRequestGET.Input) -> List[PackedSlab]:
        return await RenterdBaseResolver.handle_api_call(info, "fetch_packed_slabs", req=req)

    @strawberry.mutation
    async def renterd_mark_packed_slabs_uploaded(self, info: Info, req: PackedSlabsRequestPOST.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "mark_packed_slabs_uploaded", req=req)
        return True

    @strawberry.mutation
    async def renterd_delete_host_sector(self, info: Info, host_key: PublicKey, root: Hash256) -> int:
        return await RenterdBaseResolver.handle_api_call(info, "delete_host_sector", host_key=host_key, root=root)

    @strawberry.mutation
    async def renterd_wallet_fund(self, info: Info, req: WalletFundRequest.Input) -> WalletFundResponse:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_fund", req=req)

    @strawberry.mutation
    async def renterd_wallet_redistribute(self, info: Info, req: WalletRedistributeRequest.Input) -> List[FileContractID]:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_redistribute", req=req)

    @strawberry.mutation
    async def renterd_wallet_send_siacoins(self, info: Info, req: WalletSendRequest.Input) -> TransactionID:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_send_siacoins", req=req)

    @strawberry.mutation
    async def renterd_wallet_sign_transaction(self, info: Info, req: WalletSignRequest.Input) -> Transaction:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_sign_transaction", req=req)

    @strawberry.mutation
    async def renterd_wallet_discard_transaction(self, info: Info, transaction: Transaction.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "wallet_discard_transaction", transaction=transaction)
        return True

    @strawberry.mutation
    async def renterd_register_webhook(self, info: Info, webhook: Webhook.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "register_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def renterd_delete_webhook(self, info: Info, webhook: Webhook.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def renterd_broadcast_action(self, info: Info, event: WebhookEvent.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "broadcast_action", event=event)
        return True

    @strawberry.mutation
    async def renterd_refresh_health(self, info: Info) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "refresh_health")
        return True

    @strawberry.mutation
    async def renterd_update_setting(self, info: Info, key: str, value: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_setting", key=key, value=value)
        return True

    @strawberry.mutation
    async def renterd_delete_setting(self, info: Info, key: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_setting", key=key)
        return True

    @strawberry.mutation
    async def renterd_sync_connect(self, info: Info, addr: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "sync_connect", addr=addr)
        return True

    @strawberry.mutation
    async def renterd_txpool_broadcast(self, info: Info, transactions: List[Transaction.Input]) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "txpool_broadcast", transactions=transactions)
        return True

    @strawberry.mutation
    async def renterd_consensus_accept_block(self, info: Info, block: Block.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "consensus_accept_block", block=block)
        return True

    @strawberry.mutation
    async def renterd_update_bucket_policy(self, info: Info, name: str, policy: BucketPolicy.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_bucket_policy", name=name, policy=policy)
        return True

    @strawberry.mutation
    async def renterd_delete_contracts_all(self, info: Info) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_contracts_all")
        return True

    @strawberry.mutation
    async def renterd_contract_broadcast(self, info: Info, id: FileContractID) -> TransactionID:
        return await RenterdBaseResolver.handle_api_call(info, "contract_broadcast", id=id)

    @strawberry.mutation
    async def renterd_hosts_reset_lost_sectors(self, info: Info, hostkey: PublicKey) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "hosts_reset_lost_sectors", hostkey=hostkey)
        return True

    @strawberry.mutation
    async def renterd_hosts_remove(self, info: Info, req: HostsRemoveRequest.Input) -> int:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "hosts_remove",
            req=req,
        )

    @strawberry.mutation
    async def renterd_add_slabs_partial(
        self, info: Info, data: str, min_shards: int, total_shards: int, contract_set: str
    ) -> AddPartialSlabResponse:
        """Add partial slab data"""
        return await RenterdBaseResolver.handle_api_call(
            info,
            "add_slabs_partial",
            data=data,
            min_shards=min_shards,
            total_shards=total_shards,
            contract_set=contract_set,
        )

    @strawberry.mutation
    async def renterd_update_metric(self, info: Info, key: str, data: JSON) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_metric", key=key, data=data)
        return True

    @strawberry.mutation
    async def renterd_delete_metric(self, info: Info, key: str, cutoff: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_metric", key=key, cutoff=cutoff)
        return True

    @strawberry.mutation
    async def renterd_slabs_migration(self, info: Info, req: MigrationSlabsRequest.Input) -> UnhealthySlabsResponse:
        return await RenterdBaseResolver.handle_api_call(info, "slabs_migration", req=req)

    @strawberry.mutation
    async def renterd_update_slab(self, info: Info, slab: Slab.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_slab", slab=slab)
        return True

    @strawberry.mutation
    async def renterd_upload_track(self, info: Info, id: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "upload_track", id=id)
        return True

    @strawberry.mutation
    async def renterd_upload_add_sector(self, info: Info, id: str, req: UploadSectorRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "upload_add_sector", req=req)
        return True

    @strawberry.mutation
    async def renterd_upload_finished(self, info: Info, id: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "upload_finished", id=id)
        return True
