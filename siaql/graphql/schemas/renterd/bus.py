from typing import Any, Callable, Dict, List, Optional, TypeVar

import strawberry
from strawberry.types import Info

from siaql.graphql.resolvers.renterd import RenterdBaseResolver
from siaql.graphql.schemas.types import (
    Account,
    AccountsFundRequest,
    AccountsFundResponse,
    AccountsSaveRequest,
    Alert,
    AlertsResponse,
    AutopilotConfig,
    AutopilotStateResponse,
    AutopilotTriggerRequest,
    AutopilotTriggerResponse,
    BackupRequest,
    Bucket,
    BucketCreateRequest,
    BucketUpdatePolicyRequest,
    BusStateResponse,
    ConfigEvaluationRequest,
    ConfigEvaluationResponse,
    ConsensusState,
    ContractAcquireRequest,
    ContractAcquireResponse,
    ContractFormRequest,
    ContractKeepaliveRequest,
    ContractMetadata,
    ContractPruneRequest,
    ContractPruneResponse,
    ContractReleaseRequest,
    ContractRenewRequest,
    ContractsArchiveRequest,
    ContractSize,
    ContractsOpts,
    ContractSpendingRecord,
    ContractsPrunableDataResponse,
    Event,
    GougingSettings,
    Host,
    HostChecks,
    HostOptions,
    HostScanRequest,
    HostScanResponse,
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
    ObjectsRemoveRequest,
    ObjectsRenameRequest,
    ObjectsResponse,
    ObjectsStatsOpts,
    ObjectsStatsResponse,
    PackedSlab,
    PackedSlabsRequestGET,
    PackedSlabsRequestPOST,
    PinnedSettings,
    S3Settings,
    SlabBuffer,
    SlabsForMigrationResponse,
    Transaction,
    UpdateAllowlistRequest,
    UpdateBlocklistRequest,
    UpdateSlabRequest,
    UploadParams,
    UploadSettings,
    WalletRedistributeRequest,
    WalletResponse,
    WalletSendRequest,
    Webhook,
    WebhookResponse,
)


@strawberry.type
class BusQueries(RenterdBaseResolver):
    @strawberry.field
    async def accounts(self, info: Info, owner: str) -> List[Account]:
        return await self.handle_api_call(info, "get_accounts", owner=owner)

    @strawberry.field
    async def alerts(
        self, info: Info, severity: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> AlertsResponse:
        return await self.handle_api_call(info, "get_alerts", severity=severity, offset=offset, limit=limit)

    @strawberry.field
    async def autopilot_config(self, info: Info) -> AutopilotConfig:
        return await self.handle_api_call(info, "get_autopilot_config")

    @strawberry.field
    async def autopilot_state(self, info: Info) -> AutopilotStateResponse:
        return await self.handle_api_call(info, "get_autopilot_state")

    @strawberry.field
    async def bus_state(self, info: Info) -> BusStateResponse:
        return await self.handle_api_call(info, "get_bus_state")

    @strawberry.field
    async def buckets(self, info: Info) -> List[Bucket]:
        return await self.handle_api_call(info, "get_buckets")

    @strawberry.field
    async def bucket(self, info: Info, name: str) -> Bucket:
        return await self.handle_api_call(info, "get_bucket", name=name)

    @strawberry.field
    async def consensus_state(self, info: Info) -> ConsensusState:
        return await self.handle_api_call(info, "get_consensus_state")

    @strawberry.field
    async def consensus_network(self, info: Info) -> Network:
        return await self.handle_api_call(info, "get_consensus_network")

    @strawberry.field
    async def contract_size(self, info: Info, contract_id: str) -> ContractSize:
        return await self.handle_api_call(info, "get_contract_size", contract_id=contract_id)

    @strawberry.field
    async def contracts(self, info: Info, opts: Optional[ContractsOpts] = None) -> List[ContractMetadata]:
        return await self.handle_api_call(info, "get_contracts", opts=opts)

    @strawberry.field
    async def contract(self, info: Info, id: str) -> ContractMetadata:
        return await self.handle_api_call(info, "get_contract", id=id)

    @strawberry.field
    async def contracts_prunable_data(self, info: Info) -> ContractsPrunableDataResponse:
        return await self.handle_api_call(info, "get_contracts_prunable_data")

    @strawberry.field
    async def contract_roots(self, info: Info, contract_id: str) -> List[str]:
        return await self.handle_api_call(info, "get_contract_roots", contract_id=contract_id)

    @strawberry.field
    async def contract_ancestors(self, info: Info, contract_id: str, min_start_height: int) -> List[ContractMetadata]:
        return await self.handle_api_call(
            info, "get_contract_ancestors", contract_id=contract_id, min_start_height=min_start_height
        )

    @strawberry.field
    async def hosts(self, info: Info, opts: Optional[HostOptions] = None) -> List[Host]:
        return await self.handle_api_call(info, "get_hosts", opts=opts)

    @strawberry.field
    async def host(self, info: Info, pubkey: str) -> Host:
        return await self.handle_api_call(info, "get_host", pubkey=pubkey)

    @strawberry.field
    async def host_allowlist(self, info: Info) -> List[str]:
        return await self.handle_api_call(info, "get_host_allowlist")

    @strawberry.field
    async def host_blocklist(self, info: Info) -> List[str]:
        return await self.handle_api_call(info, "get_host_blocklist")

    @strawberry.field
    async def multipart_upload(self, info: Info, upload_id: str) -> MultipartUpload:
        return await self.handle_api_call(info, "get_multipart_upload", upload_id=upload_id)

    @strawberry.field
    async def object(self, info: Info, bucket: str, key: str, only_metadata: bool = False) -> Object:
        return await self.handle_api_call(info, "get_object", bucket=bucket, key=key, only_metadata=only_metadata)

    @strawberry.field
    async def objects(self, info: Info, prefix: str, opts: Dict[str, Any]) -> ObjectsResponse:
        return await self.handle_api_call(info, "get_objects", prefix=prefix, opts=opts)

    @strawberry.field
    async def objects_stats(self, info: Info, opts: Optional[ObjectsStatsOpts] = None) -> ObjectsStatsResponse:
        return await self.handle_api_call(info, "get_objects_stats", opts=opts)

    @strawberry.field
    async def params_gouging(self, info: Info) -> GougingSettings:
        return await self.handle_api_call(info, "get_params_gouging")

    @strawberry.field
    async def params_upload(self, info: Info) -> UploadParams:
        return await self.handle_api_call(info, "get_params_upload")

    @strawberry.field
    async def settings_gouging(self, info: Info) -> GougingSettings:
        return await self.handle_api_call(info, "get_settings_gouging")

    @strawberry.field
    async def settings_pinned(self, info: Info) -> PinnedSettings:
        return await self.handle_api_call(info, "get_settings_pinned")

    @strawberry.field
    async def settings_s3(self, info: Info) -> S3Settings:
        return await self.handle_api_call(info, "get_settings_s3")

    @strawberry.field
    async def settings_upload(self, info: Info) -> UploadSettings:
        return await self.handle_api_call(info, "get_settings_upload")

    @strawberry.field
    async def slab(self, info: Info, key: str) -> Any:
        return await self.handle_api_call(info, "get_slab", key=key)

    @strawberry.field
    async def slab_buffers(self, info: Info) -> List[SlabBuffer]:
        return await self.handle_api_call(info, "get_slab_buffers")

    @strawberry.field
    async def wallet(self, info: Info) -> WalletResponse:
        return await self.handle_api_call(info, "get_wallet")

    @strawberry.field
    async def webhook_info(self, info: Info) -> WebhookResponse:
        return await self.handle_api_call(info, "get_webhook_info")


@strawberry.type
class BusMutations(RenterdBaseResolver):
    @strawberry.mutation
    async def fund_account(self, info: Info, request: AccountsFundRequest) -> AccountsFundResponse:
        return await self.handle_api_call(info, "post_fund_account", request=request)

    @strawberry.mutation
    async def save_accounts(self, info: Info, request: AccountsSaveRequest) -> bool:
        await self.handle_api_call(info, "post_save_accounts", request=request)
        return True

    @strawberry.mutation
    async def register_alert(self, info: Info, alert: Alert) -> bool:
        await self.handle_api_call(info, "post_register_alert", alert=alert)
        return True

    @strawberry.mutation
    async def dismiss_alerts(self, info: Info, ids: List[str]) -> bool:
        await self.handle_api_call(info, "post_dismiss_alerts", ids=ids)
        return True

    @strawberry.mutation
    async def trigger_autopilot(self, info: Info, request: AutopilotTriggerRequest) -> AutopilotTriggerResponse:
        return await self.handle_api_call(info, "post_trigger_autopilot", request=request)

    @strawberry.mutation
    async def evaluate_config(self, info: Info, request: ConfigEvaluationRequest) -> ConfigEvaluationResponse:
        return await self.handle_api_call(info, "post_evaluate_config", request=request)

    @strawberry.mutation
    async def create_bucket(self, info: Info, request: BucketCreateRequest) -> bool:
        await self.handle_api_call(info, "post_create_bucket", request=request)
        return True

    @strawberry.mutation
    async def update_bucket_policy(self, info: Info, name: str, request: BucketUpdatePolicyRequest) -> bool:
        await self.handle_api_call(info, "put_bucket_policy", name=name, request=request)
        return True

    @strawberry.mutation
    async def delete_bucket(self, info: Info, name: str) -> bool:
        await self.handle_api_call(info, "delete_bucket", name=name)
        return True

    @strawberry.mutation
    async def create_multipart_upload(self, info: Info, request: MultipartCreateRequest) -> MultipartCreateResponse:
        return await self.handle_api_call(info, "post_create_multipart_upload", request=request)

    @strawberry.mutation
    async def complete_multipart_upload(
        self, info: Info, request: MultipartCompleteRequest
    ) -> MultipartCompleteResponse:
        return await self.handle_api_call(info, "post_complete_multipart_upload", request=request)

    @strawberry.mutation
    async def abort_multipart_upload(self, info: Info, request: MultipartAbortRequest) -> bool:
        await self.handle_api_call(info, "post_abort_multipart_upload", request=request)
        return True

    @strawberry.mutation
    async def add_multipart_part(self, info: Info, request: MultipartAddPartRequest) -> bool:
        await self.handle_api_call(info, "put_add_multipart_part", request=request)
        return True

    @strawberry.mutation
    async def list_multipart_uploads(
        self, info: Info, request: MultipartListUploadsRequest
    ) -> MultipartListUploadsResponse:
        return await self.handle_api_call(info, "post_list_multipart_uploads", request=request)

    @strawberry.mutation
    async def list_multipart_parts(self, info: Info, request: MultipartListPartsRequest) -> MultipartListPartsResponse:
        return await self.handle_api_call(info, "post_list_multipart_parts", request=request)

    @strawberry.mutation
    async def archive_contracts(self, info: Info, request: ContractsArchiveRequest) -> bool:
        await self.handle_api_call(info, "post_archive_contracts", request=request)
        return True

    @strawberry.mutation
    async def delete_all_contracts(self, info: Info) -> bool:
        await self.handle_api_call(info, "delete_all_contracts")
        return True

    @strawberry.mutation
    async def form_contract(self, info: Info, request: ContractFormRequest) -> ContractMetadata:
        return await self.handle_api_call(info, "post_form_contract", request=request)

    @strawberry.mutation
    async def broadcast_contract(self, info: Info, contract_id: str) -> str:
        return await self.handle_api_call(info, "post_broadcast_contract", contract_id=contract_id)

    @strawberry.mutation
    async def renew_contract(self, info: Info, contract_id: str, request: ContractRenewRequest) -> ContractMetadata:
        return await self.handle_api_call(info, "post_renew_contract", contract_id=contract_id, request=request)

    @strawberry.mutation
    async def acquire_contract(
        self, info: Info, contract_id: str, request: ContractAcquireRequest
    ) -> ContractAcquireResponse:
        return await self.handle_api_call(info, "post_acquire_contract", contract_id=contract_id, request=request)

    @strawberry.mutation
    async def keepalive_contract(self, info: Info, contract_id: str, request: ContractKeepaliveRequest) -> bool:
        await self.handle_api_call(info, "post_keepalive_contract", contract_id=contract_id, request=request)
        return True

    @strawberry.mutation
    async def prune_contract(
        self, info: Info, contract_id: str, request: ContractPruneRequest
    ) -> ContractPruneResponse:
        return await self.handle_api_call(info, "post_prune_contract", contract_id=contract_id, request=request)

    @strawberry.mutation
    async def release_contract(self, info: Info, contract_id: str, request: ContractReleaseRequest) -> bool:
        await self.handle_api_call(info, "post_release_contract", contract_id=contract_id, request=request)
        return True

    @strawberry.mutation
    async def update_contract_usability(self, info: Info, contract_id: str, usability: str) -> bool:
        await self.handle_api_call(info, "put_contract_usability", contract_id=contract_id, usability=usability)
        return True

    @strawberry.mutation
    async def delete_contract(self, info: Info, contract_id: str) -> bool:
        await self.handle_api_call(info, "delete_contract", contract_id=contract_id)
        return True

    @strawberry.mutation
    async def scan_host(self, info: Info, hostkey: str, request: HostScanRequest) -> HostScanResponse:
        return await self.handle_api_call(info, "post_scan_host", hostkey=hostkey, request=request)

    @strawberry.mutation
    async def reset_lost_sectors(self, info: Info, hostkey: str) -> bool:
        await self.handle_api_call(info, "post_reset_lost_sectors", hostkey=hostkey)
        return True

    @strawberry.mutation
    async def update_host_check(self, info: Info, hostkey: str, check: HostChecks) -> bool:
        await self.handle_api_call(info, "put_host_check", hostkey=hostkey, check=check)
        return True

    @strawberry.mutation
    async def update_allowlist(self, info: Info, request: UpdateAllowlistRequest) -> bool:
        await self.handle_api_call(info, "put_update_allowlist", request=request)
        return True

    @strawberry.mutation
    async def update_blocklist(self, info: Info, request: UpdateBlocklistRequest) -> bool:
        await self.handle_api_call(info, "put_update_blocklist", request=request)
        return True

    @strawberry.mutation
    async def remove_objects(self, info: Info, request: ObjectsRemoveRequest) -> bool:
        await self.handle_api_call(info, "post_remove_objects", request=request)
        return True

    @strawberry.mutation
    async def rename_objects(self, info: Info, request: ObjectsRenameRequest) -> bool:
        await self.handle_api_call(info, "post_rename_objects", request=request)
        return True

    @strawberry.mutation
    async def delete_object(self, info: Info, bucket: str, key: str) -> bool:
        await self.handle_api_call(info, "delete_object", bucket=bucket, key=key)
        return True

    @strawberry.mutation
    async def update_settings_gouging(self, info: Info, settings: GougingSettings) -> bool:
        await self.handle_api_call(info, "put_settings_gouging", settings=settings)
        return True

    @strawberry.mutation
    async def update_settings_pinned(self, info: Info, settings: PinnedSettings) -> bool:
        await self.handle_api_call(info, "put_settings_pinned", settings=settings)
        return True

    @strawberry.mutation
    async def update_settings_s3(self, info: Info, settings: S3Settings) -> bool:
        await self.handle_api_call(info, "put_settings_s3", settings=settings)
        return True

    @strawberry.mutation
    async def update_settings_upload(self, info: Info, settings: UploadSettings) -> bool:
        await self.handle_api_call(info, "put_settings_upload", settings=settings)
        return True

    @strawberry.mutation
    async def fetch_packed_slabs(self, info: Info, request: PackedSlabsRequestGET) -> List[PackedSlab]:
        return await self.handle_api_call(info, "post_fetch_packed_slabs", request=request)

    @strawberry.mutation
    async def mark_packed_slabs_uploaded(self, info: Info, request: PackedSlabsRequestPOST) -> bool:
        await self.handle_api_call(info, "post_mark_packed_slabs_uploaded", request=request)
        return True

    @strawberry.mutation
    async def get_slabs_for_migration(self, info: Info, request: MigrationSlabsRequest) -> SlabsForMigrationResponse:
        return await self.handle_api_call(info, "post_get_slabs_for_migration", request=request)

    @strawberry.mutation
    async def refresh_slabs_health(self, info: Info) -> bool:
        await self.handle_api_call(info, "post_refresh_slabs_health")
        return True

    @strawberry.mutation
    async def update_slab(self, info: Info, key: str, request: UpdateSlabRequest) -> bool:
        await self.handle_api_call(info, "put_update_slab", key=key, request=request)
        return True

    @strawberry.mutation
    async def track_upload(self, info: Info, upload_id: str) -> bool:
        await self.handle_api_call(info, "post_track_upload", upload_id=upload_id)
        return True

    @strawberry.mutation
    async def finish_upload(self, info: Info, upload_id: str) -> bool:
        await self.handle_api_call(info, "delete_upload", upload_id=upload_id)
        return True

    @strawberry.mutation
    async def add_uploading_sectors(self, info: Info, upload_id: str, roots: List[str]) -> bool:
        await self.handle_api_call(info, "post_add_uploading_sectors", upload_id=upload_id, roots=roots)
        return True

    @strawberry.mutation
    async def send_siacoins(self, info: Info, request: WalletSendRequest) -> str:
        return await self.handle_api_call(info, "post_send_siacoins", request=request)

    @strawberry.mutation
    async def redistribute_wallet(self, info: Info, request: WalletRedistributeRequest) -> List[str]:
        return await self.handle_api_call(info, "post_redistribute_wallet", request=request)

    @strawberry.mutation
    async def broadcast_action(self, info: Info, event: Event) -> bool:
        await self.handle_api_call(info, "post_broadcast_action", event=event)
        return True

    @strawberry.mutation
    async def register_webhook(self, info: Info, webhook: Webhook) -> bool:
        await self.handle_api_call(info, "post_register_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def delete_webhook(self, info: Info, webhook: Webhook) -> bool:
        await self.handle_api_call(info, "post_delete_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def backup(self, info: Info, request: BackupRequest) -> bool:
        await self.handle_api_call(info, "post_backup", request=request)
        return True

    @strawberry.mutation
    async def record_contract_spending(self, info: Info, records: List[ContractSpendingRecord]) -> bool:
        await self.handle_api_call(info, "post_record_contract_spending", records=records)
        return True

    @strawberry.mutation
    async def accept_block(self, info: Info, block: Dict[str, Any]) -> bool:
        await self.handle_api_call(info, "post_accept_block", block=block)
        return True

    @strawberry.mutation
    async def broadcast_transaction(self, info: Info, txn_set: List[Transaction]) -> bool:
        await self.handle_api_call(info, "post_broadcast_transaction", txn_set=txn_set)
        return True
