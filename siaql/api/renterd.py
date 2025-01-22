import json
from functools import wraps
from typing import Any, Dict, List, Optional, Union

import httpx
from httpx import AsyncClient, BasicAuth

from siaql.api.utils import APIError, handle_api_errors
from siaql.graphql.schemas.types import (
    Account,
    AccountsFundRequest,
    AccountsFundResponse,
    AccountsSaveRequest,
    Alert,
    AlertsResponse,
    AutopilotConfig,
    AutopilotStateResponse,
    BackupRequest,
    Bucket,
    BucketCreateRequest,
    BucketUpdatePolicyRequest,
    BusStateResponse,
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
    UploadSettings,
    WalletRedistributeRequest,
    WalletResponse,
    WalletSendRequest,
    Webhook,
    WebhookResponse,
)


class RenterdError(Exception):
    """Base exception for renterd API errors"""

    pass


class RenterdClient:
    """Client for the renterd API"""

    def __init__(self, base_url: str = "http://localhost:9980", api_password: Optional[str] = None):
        # Ensure base_url doesn't have trailing slash and has /api
        self.base_url = f"{base_url.rstrip('/')}/api"
        if api_password:
            auth = httpx.BasicAuth(username="", password=api_password)
            self.client = httpx.AsyncClient(base_url=self.base_url, auth=auth, timeout=30.0)
        else:
            self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    # Account endpoints
    # Account endpoints
    @handle_api_errors(RenterdError)
    async def get_accounts(self, owner: str) -> List[Account]:
        """Get all accounts"""
        response = await self.client.get("/accounts", params={"owner": owner})
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_fund_account(self, request: AccountsFundRequest) -> AccountsFundResponse:
        """Fund an account"""
        response = await self.client.post("/accounts/fund", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_save_accounts(self, request: AccountsSaveRequest) -> None:
        """Save accounts"""
        response = await self.client.post("/accounts", json=request)
        response.raise_for_status()

    # Alert endpoints
    @handle_api_errors(RenterdError)
    async def get_alerts(
        self, severity: Optional[str] = None, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> AlertsResponse:
        """Get alerts"""
        params = {}
        if severity:
            params["severity"] = severity
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        response = await self.client.get("/alerts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_register_alert(self, alert: Alert) -> None:
        """Register an alert"""
        response = await self.client.post("/alerts/register", json=alert)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_dismiss_alerts(self, ids: List[str]) -> None:
        """Dismiss alerts"""
        response = await self.client.post("/alerts/dismiss", json=ids)
        response.raise_for_status()

    # Autopilot endpoints
    @handle_api_errors(RenterdError)
    async def get_autopilot_config(self) -> AutopilotConfig:
        """Get autopilot configuration"""
        response = await self.client.get("/autopilot")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_autopilot_state(self) -> AutopilotStateResponse:
        """Get autopilot state"""
        response = await self.client.get("/autopilot/state")
        response.raise_for_status()
        return response.json()

    # Bus state endpoint
    @handle_api_errors(RenterdError)
    async def get_bus_state(self) -> BusStateResponse:
        """Get bus state"""
        response = await self.client.get("/state")
        response.raise_for_status()
        return response.json()

    # Bucket endpoints
    @handle_api_errors(RenterdError)
    async def get_buckets(self) -> List[Bucket]:
        """Get all buckets"""
        response = await self.client.get("/buckets")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_bucket(self, name: str) -> Bucket:
        """Get bucket by name"""
        response = await self.client.get(f"/bucket/{name}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_create_bucket(self, request: BucketCreateRequest) -> None:
        """Create a bucket"""
        response = await self.client.post("/buckets", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def put_bucket_policy(self, name: str, request: BucketUpdatePolicyRequest) -> None:
        """Update bucket policy"""
        response = await self.client.put(f"/bucket/{name}/policy", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_bucket(self, name: str) -> None:
        """Delete a bucket"""
        response = await self.client.delete(f"/bucket/{name}")
        response.raise_for_status()

    # Consensus endpoints
    @handle_api_errors(RenterdError)
    async def get_consensus_state(self) -> ConsensusState:
        """Get consensus state"""
        response = await self.client.get("/consensus/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_consensus_network(self) -> Network:
        """Get consensus network"""
        response = await self.client.get("/consensus/network")
        response.raise_for_status()
        return response.json()

    # Contract endpoints
    @handle_api_errors(RenterdError)
    async def get_contracts(self, opts: Optional[ContractsOpts] = None) -> List[ContractMetadata]:
        """Get all contracts"""
        params = {}
        if opts:
            if opts.filter_mode:
                params["filtermode"] = opts.filter_mode
        response = await self.client.get("/contracts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract(self, id: str) -> ContractMetadata:
        """Get contract by ID"""
        response = await self.client.get(f"/contract/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_archive_contracts(self, request: ContractsArchiveRequest) -> None:
        """Archive contracts"""
        response = await self.client.post("/contracts/archive", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_all_contracts(self) -> None:
        """Delete all contracts"""
        response = await self.client.delete("/contracts/all")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_form_contract(self, request: ContractFormRequest) -> ContractMetadata:
        """Form a new contract"""
        response = await self.client.post("/contracts/form", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_size(self, contract_id: str) -> ContractSize:
        """Get contract size"""
        response = await self.client.get(f"/contract/{contract_id}/size")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contracts_prunable_data(self) -> ContractsPrunableDataResponse:
        """Get prunable contracts data"""
        response = await self.client.get("/contracts/prunable")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_broadcast_contract(self, contract_id: str) -> str:
        """Broadcast a contract"""
        response = await self.client.post(f"/contract/{contract_id}/broadcast")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_renew_contract(self, contract_id: str, request: ContractRenewRequest) -> ContractMetadata:
        """Renew a contract"""
        response = await self.client.post(f"/contract/{contract_id}/renew", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_roots(self, contract_id: str) -> List[str]:
        """Get contract roots"""
        response = await self.client.get(f"/contract/{contract_id}/roots")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_ancestors(self, contract_id: str, min_start_height: int) -> List[ContractMetadata]:
        """Get contract ancestors"""
        params = {"minstartheight": min_start_height}
        response = await self.client.get(f"/contract/{contract_id}/ancestors", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_acquire_contract(self, contract_id: str, request: ContractAcquireRequest) -> ContractAcquireResponse:
        """Acquire a contract"""
        response = await self.client.post(f"/contract/{contract_id}/acquire", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_keepalive_contract(self, contract_id: str, request: ContractKeepaliveRequest) -> None:
        """Keepalive a contract"""
        response = await self.client.post(f"/contract/{contract_id}/keepalive", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_prune_contract(self, contract_id: str, request: ContractPruneRequest) -> ContractPruneResponse:
        """Prune a contract"""
        response = await self.client.post(f"/contract/{contract_id}/prune", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_release_contract(self, contract_id: str, request: ContractReleaseRequest) -> None:
        """Release a contract"""
        response = await self.client.post(f"/contract/{contract_id}/release", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def put_contract_usability(self, contract_id: str, usability: str) -> None:
        """Update contract usability"""
        response = await self.client.put(f"/contract/{contract_id}/usability", json=usability)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_contract(self, contract_id: str) -> None:
        """Delete a contract"""
        response = await self.client.delete(f"/contract/{contract_id}")
        response.raise_for_status()

    # Host endpoints
    @handle_api_errors(RenterdError)
    async def get_hosts(self, opts: Optional[HostOptions] = None) -> List[Host]:
        """Get all hosts"""
        response = await self.client.get("/hosts", params=opts.__dict__ if opts else None)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_host(self, pubkey: str) -> Host:
        """Get host by public key"""
        response = await self.client.get(f"/host/{pubkey}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_scan_host(self, hostkey: str, request: HostScanRequest) -> HostScanResponse:
        """Scan a host"""
        response = await self.client.post(f"/host/{hostkey}/scan", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_reset_lost_sectors(self, hostkey: str) -> None:
        """Reset lost sectors for a host"""
        response = await self.client.post(f"/host/{hostkey}/resetlostsectors")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def put_host_check(self, hostkey: str, check: HostChecks) -> None:
        """Update host check"""
        response = await self.client.put(f"/host/{hostkey}/check", json=check)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_host_allowlist(self) -> List[str]:
        """Get host allowlist"""
        response = await self.client.get("/hosts/allowlist")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_host_blocklist(self) -> List[str]:
        """Get host blocklist"""
        response = await self.client.get("/hosts/blocklist")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def put_update_allowlist(self, request: UpdateAllowlistRequest) -> None:
        """Update host allowlist"""
        response = await self.client.put("/hosts/allowlist", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def put_update_blocklist(self, request: UpdateBlocklistRequest) -> None:
        """Update host blocklist"""
        response = await self.client.put("/hosts/blocklist", json=request)
        response.raise_for_status()

    # Multipart upload endpoints
    @handle_api_errors(RenterdError)
    async def post_create_multipart_upload(self, request: MultipartCreateRequest) -> MultipartCreateResponse:
        """Create multipart upload"""
        response = await self.client.post("/multipart/create", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_complete_multipart_upload(self, request: MultipartCompleteRequest) -> MultipartCompleteResponse:
        """Complete multipart upload"""
        response = await self.client.post("/multipart/complete", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_abort_multipart_upload(self, request: MultipartAbortRequest) -> None:
        """Abort multipart upload"""
        response = await self.client.post("/multipart/abort", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def put_add_multipart_part(self, request: MultipartAddPartRequest) -> None:
        """Add multipart part"""
        response = await self.client.put("/multipart/part", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_multipart_upload(self, upload_id: str) -> MultipartUpload:
        """Get multipart upload details"""
        response = await self.client.get(f"/multipart/upload/{upload_id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_list_multipart_uploads(self, request: MultipartListUploadsRequest) -> MultipartListUploadsResponse:
        """List multipart uploads"""
        response = await self.client.post("/multipart/listuploads", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_list_multipart_parts(self, request: MultipartListPartsRequest) -> MultipartListPartsResponse:
        """List multipart parts"""
        response = await self.client.post("/multipart/listparts", json=request)
        response.raise_for_status()
        return response.json()

    # Object endpoints
    @handle_api_errors(RenterdError)
    async def get_object(self, bucket: str, key: str, only_metadata: bool = False) -> Object:
        """Get object or object metadata"""
        params = {"bucket": bucket, "onlymetadata": str(only_metadata).lower()}
        response = await self.client.get(f"/object/{key}", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_objects(self, prefix: str, opts: Dict[str, Any]) -> ObjectsResponse:
        """List objects"""
        response = await self.client.get(f"/objects/{prefix}", params=opts)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_remove_objects(self, request: ObjectsRemoveRequest) -> None:
        """Remove objects"""
        response = await self.client.post("/objects/remove", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_rename_objects(self, request: ObjectsRenameRequest) -> None:
        """Rename objects"""
        response = await self.client.post("/objects/rename", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_object(self, bucket: str, key: str) -> None:
        """Delete object"""
        params = {"bucket": bucket}
        response = await self.client.delete(f"/object/{key}", params=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_objects_stats(self, opts: Dict[str, Any]) -> ObjectsStatsResponse:
        """Get objects stats"""
        response = await self.client.get("/stats/objects", params=opts)
        response.raise_for_status()
        return response.json()

    # Settings endpoints
    @handle_api_errors(RenterdError)
    async def get_settings_gouging(self) -> GougingSettings:
        """Get gouging settings"""
        response = await self.client.get("/settings/gouging")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_settings_gouging(self, settings: GougingSettings) -> None:
        """Update gouging settings"""
        response = await self.client.put("/settings/gouging", json=settings)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_settings_pinned(self) -> PinnedSettings:
        """Get pinned settings"""
        response = await self.client.get("/settings/pinned")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_settings_pinned(self, settings: PinnedSettings) -> None:
        """Update pinned settings"""
        response = await self.client.put("/settings/pinned", json=settings)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_settings_s3(self) -> S3Settings:
        """Get S3 settings"""
        response = await self.client.get("/settings/s3")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_settings_s3(self, settings: S3Settings) -> None:
        """Update S3 settings"""
        response = await self.client.put("/settings/s3", json=settings)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_settings_upload(self) -> UploadSettings:
        """Get upload settings"""
        response = await self.client.get("/settings/upload")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_settings_upload(self, settings: UploadSettings) -> None:
        """Update upload settings"""
        response = await self.client.put("/settings/upload", json=settings)
        response.raise_for_status()

    # Slab endpoints
    @handle_api_errors(RenterdError)
    async def get_slab(self, key: str) -> Any:
        """Get slab"""
        response = await self.client.get(f"/slab/{key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_update_slab(self, key: str, request: UpdateSlabRequest) -> None:
        """Update slab"""
        response = await self.client.put(f"/slab/{key}", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_slab_buffers(self) -> List[SlabBuffer]:
        """Get slab buffers"""
        response = await self.client.get("/slabbuffers")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_fetch_packed_slabs(self, request: PackedSlabsRequestGET) -> List[PackedSlab]:
        """Fetch packed slabs"""
        response = await self.client.post("/slabbuffer/fetch", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_mark_packed_slabs_uploaded(self, request: PackedSlabsRequestPOST) -> None:
        """Mark packed slabs as uploaded"""
        response = await self.client.post("/slabbuffer/done", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_get_slabs_for_migration(self, request: MigrationSlabsRequest) -> SlabsForMigrationResponse:
        """Get slabs for migration"""
        response = await self.client.post("/slabs/migration", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_refresh_slabs_health(self) -> None:
        """Refresh slabs health"""
        response = await self.client.post("/slabs/refreshhealth")
        response.raise_for_status()

    # Upload endpoints
    @handle_api_errors(RenterdError)
    async def post_track_upload(self, upload_id: str) -> None:
        """Track upload"""
        response = await self.client.post(f"/upload/{upload_id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_upload(self, upload_id: str) -> None:
        """Delete upload"""
        response = await self.client.delete(f"/upload/{upload_id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_add_uploading_sectors(self, upload_id: str, roots: List[str]) -> None:
        """Add uploading sectors"""
        response = await self.client.post(f"/upload/{upload_id}/sector", json=roots)
        response.raise_for_status()

    # Wallet endpoints
    @handle_api_errors(RenterdError)
    async def get_wallet(self) -> WalletResponse:
        """Get wallet"""
        response = await self.client.get("/wallet")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_send_siacoins(self, request: WalletSendRequest) -> str:
        """Send siacoins"""
        response = await self.client.post("/wallet/send", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_redistribute_wallet(self, request: WalletRedistributeRequest) -> List[str]:
        """Redistribute wallet"""
        response = await self.client.post("/wallet/redistribute", json=request)
        response.raise_for_status()
        return response.json()

    # Webhook endpoints
    @handle_api_errors(RenterdError)
    async def get_webhook_info(self) -> WebhookResponse:
        """Get webhook info"""
        response = await self.client.get("/webhooks")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_register_webhook(self, webhook: Webhook) -> None:
        """Register webhook"""
        response = await self.client.post("/webhooks", json=webhook)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_delete_webhook(self, webhook: Webhook) -> None:
        """Delete webhook"""
        response = await self.client.post("/webhook/delete", json=webhook)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_broadcast_action(self, event: Event) -> None:
        """Broadcast action"""
        response = await self.client.post("/webhooks/action", json=event)
        response.raise_for_status()

    # System endpoints
    @handle_api_errors(RenterdError)
    async def post_backup(self, request: BackupRequest) -> None:
        """Create backup"""
        response = await self.client.post("/system/sqlite3/backup", json=request)
        response.raise_for_status()

    # Transaction endpoints
    @handle_api_errors(RenterdError)
    async def post_accept_block(self, block: Dict[str, Any]) -> None:
        """Accept block"""
        response = await self.client.post("/consensus/acceptblock", json=block)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_broadcast_transaction(self, txn_set: List[Transaction]) -> None:
        """Broadcast transaction"""
        response = await self.client.post("/txpool/broadcast", json=txn_set)
        response.raise_for_status()
