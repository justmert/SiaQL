from typing import Optional, Dict, List, Any, Union
from httpx import AsyncClient, BasicAuth
from ..types import *


class RenterdClient:
    def __init__(
        self,
        autopilot_url: str = "http://localhost:9980",
        bus_url: str = "http://localhost:9980",
        worker_url: str = "http://localhost:9980",
        api_password: Optional[str] = None,
    ):
        # Initialize clients for each component

        self.autopilot_client = self._create_client(f"{autopilot_url.rstrip('/')}/api/autopilot", api_password)
        self.bus_client = self._create_client(f"{bus_url.rstrip('/')}/api/bus", api_password)
        self.worker_client = self._create_client(f"{worker_url.rstrip('/')}/api/worker", api_password)

    def _create_client(self, base_url: str, api_password: Optional[str]) -> AsyncClient:
        if api_password:
            auth = BasicAuth(username="", password=api_password)
            return AsyncClient(base_url=base_url, auth=auth, timeout=30.0)
        return AsyncClient(base_url=base_url, timeout=30.0)

    async def close(self):
        """Close all HTTP clients"""
        await self.autopilot_client.aclose()
        await self.bus_client.aclose()
        await self.worker_client.aclose()

    # Autopilot endpoints
    @handle_api_errors(RenterdError)
    async def get_autopilot_config(self) -> AutopilotConfig:
        response = await self.autopilot_client.get("/config")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_autopilot_config(self, config: AutopilotConfig) -> None:
        response = await self.autopilot_client.put("/config", json=config)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def trigger_autopilot(self, force_scan: bool = False) -> bool:
        response = await self.autopilot_client.post("/trigger", json={"forceScan": force_scan})
        response.raise_for_status()
        return response.json()["triggered"]

    @handle_api_errors(RenterdError)
    async def get_autopilot_host(self, host_key: str) -> Host:
        response = await self.autopilot_client.get(f"/host/{host_key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def search_hosts(self, request: HostsRequest) -> List[Host]:
        response = await self.autopilot_client.post("/hosts", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_autopilot_state(self) -> AutopilotStateResponse:
        response = await self.autopilot_client.get("/state")
        response.raise_for_status()
        return response.json()

    # ----------------------------------------

    # Worker endpoints
    @handle_api_errors(RenterdError)
    async def get_worker_account(self, host_key: str) -> Account:
        response = await self.worker_client.get(f"/account/{host_key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_id(self) -> str:
        response = await self.worker_client.get("/id")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_memory_state(self) -> MemoryResponse:
        response = await self.worker_client.get("/memory")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def upload_object(self, bucket: str, key: str, data: str, opts: UploadObjectOptions) -> UploadObjectResponse:
        params = {"bucket": bucket, **opts.__dict__}
        response = await self.worker_client.put(f"/objects/{key}", params=params, content=data)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_object(self, bucket: str, key: str) -> None:
        params = {"bucket": bucket}
        response = await self.worker_client.delete(f"/objects/{key}", params=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_worker_object(self, bucket: str, key: str, opts: DownloadObjectOptions) -> GetObjectResponse:
        """Download object from worker"""
        response = await self.client.get(f"/objects/{key}", params={"bucket": bucket, **opts})
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_rhp_contracts(self) -> Dict[str, Contract]:
        """Get all contracts"""
        response = await self.client.get("/rhp/contracts")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def broadcast_contract(self, contract_id: str) -> None:
        """Broadcast contract"""
        response = await self.client.post(f"/rhp/{contract_id}/broadcast")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def prune_contract(self, contract_id: str, request: ContractPruneRequest) -> ContractPruneResponse:
        """Prune contract"""
        response = await self.client.post(f"/rhp/{contract_id}/prune", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_roots(self, contract_id: str) -> List[str]:
        """Get contract roots"""
        response = await self.client.post(f"/rhp/{contract_id}/roots")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def form_contract(self, request: ContractFormRequest) -> ContractMetadata:
        """Form a new contract"""
        response = await self.client.post("/rhp/form", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def fund_contract(self, request: RHPFundRequest) -> None:
        """Fund a contract"""
        response = await self.client.post("/rhp/fund", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def renew_contract(self, request: ContractRenewRequest) -> ContractMetadata:
        """Renew a contract"""
        response = await self.client.post("/rhp/renew", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def scan_host(self, request: HostScanRequest) -> HostScanResponse:
        """Scan a host"""
        response = await self.client.post("/rhp/scan", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def sync_contract(self, request: RHPSyncRequest) -> None:
        """Sync a contract"""
        response = await self.client.post("/rhp/sync", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def migrate_slab(self, request: MigrationSlabsRequest) -> SlabsForMigrationResponse:
        """Migrate a slab"""
        response = await self.client.post("/slab/migrate", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_state(self) -> WorkerStateResponse:
        """Get worker state"""
        response = await self.client.get("/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_download_stats(self) -> DownloadStatsResponse:
        response = await self.worker_client.get("/stats/downloads")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_upload_stats(self) -> UploadStatsResponse:
        response = await self.worker_client.get("/stats/uploads")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def upload_multipart_part(
        self, bucket: str, key: str, upload_id: str, part_number: int, opts: UploadMultipartUploadPartOptions
    ) -> UploadMultipartUploadPartResponse:
        params = {"bucket": bucket, "uploadid": upload_id, "partnumber": part_number, **opts.__dict__}
        response = await self.worker_client.put(f"/multipart/{key}", params=params)
        response.raise_for_status()
        return response.json()

    # ----------------------------------------

    # Bus endpoints
    @handle_api_errors(RenterdError)
    async def get_accounts(self, owner: str) -> List[Account]:
        response = await self.bus_client.get("/accounts", params={"owner": owner})
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_account(self, account_id: str, hostKey: PublicKey) -> None:
        """Add or update an account"""
        response = await self.client.post(f"/account/{account_id}", json={"hostKey": hostKey})
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def lock_account(
        self, account_id: str, hostKey: PublicKey, exclusive: bool, duration: DurationMS
    ) -> AccountsLockHandlerResponse:
        """Lock an account"""
        response = await self.client.post(
            f"/account/{account_id}/lock", json={"hostKey": hostKey, "exclusive": exclusive, "duration": duration}
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def unlock_account(self, account_id: str, lockID: int) -> None:
        """Unlock an account"""
        response = await self.client.post(f"/account/{account_id}/unlock", json={"lockID": lockID})
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def add_account_balance(self, account_id: str, request: AccountsAddBalanceRequest) -> None:
        response = await self.bus_client.post(f"/account/{account_id}/add", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def update_account_balance(self, account_id: str, request: AccountsUpdateBalanceRequest) -> None:
        response = await self.bus_client.post(f"/account/{account_id}/update", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def requires_sync_account(self, account_id: str, request: AccountsRequiresSyncRequest) -> None:
        """Mark account as requiring sync"""
        response = await self.client.post(f"/account/{account_id}/requiressync", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def reset_drift_account(self, account_id: str) -> None:
        """Reset account drift"""
        response = await self.client.post(f"/account/{account_id}/resetdrift")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_alerts(self, severity: str, offset: int, limit: int) -> AlertsResponse:
        params = {"severity": severity, "offset": offset, "limit": limit}
        response = await self.bus_client.get("/alerts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def dismiss_alerts(self, ids: List[Hash256]) -> None:
        response = await self.bus_client.post("/alerts/dismiss", json=ids)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def register_alert(self, alert: Alert) -> None:
        response = await self.bus_client.post("/alerts/register", json=alert)
        response.raise_for_status()

    # Autopilot endpoints
    @handle_api_errors(RenterdError)  #  MISSING
    async def get_autopilots(self) -> List[AutopilotConfig]:
        """Get all autopilot configurations"""
        response = await self.client.get("/autopilots")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)  #  MISSING
    async def get_autopilot(self, autopilot_id: str) -> AutopilotConfig:
        """Get specific autopilot configuration"""
        response = await self.client.get(f"/autopilot/{autopilot_id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)  #  MISSING
    async def update_autopilot(self, autopilot_id: str, config: AutopilotConfig) -> None:
        """Update specific autopilot configuration"""
        response = await self.client.put(f"/autopilot/{autopilot_id}", json=config)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_buckets(self) -> List[Bucket]:
        response = await self.bus_client.get("/buckets")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def create_bucket(self, name: str, policy: BucketPolicy) -> None:
        response = await self.bus_client.post("/buckets", json={"name": name, "policy": policy})
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_bucket(self, name: str) -> Bucket:
        response = await self.bus_client.get(f"/bucket/{name}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_bucket(self, name: str) -> None:
        response = await self.bus_client.delete(f"/bucket/{name}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def update_bucket_policy(self, name: str, policy: BucketPolicy) -> None:
        response = await self.bus_client.put(f"/bucket/{name}/policy", json={"policy": policy})
        response.raise_for_status()

        # Consensus endpoints

    @handle_api_errors(RenterdError)
    async def accept_block(self, block: Block) -> None:
        response = await self.bus_client.post("/consensus/acceptblock", json=block)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_consensus_state(self) -> ConsensusState:
        response = await self.bus_client.get("/consensus/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_consensus_siafundfee(self, payout: Currency) -> Currency:
        """Get siafund fee for a given payout"""
        response = await self.client.get(f"/consensus/siafundfee/{payout}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract(self, id: str) -> ContractMetadata:
        response = await self.bus_client.get(f"/contract/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_contract(self, contract_id: str) -> None:
        """Delete a contract"""
        response = await self.client.delete(f"/contract/{contract_id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_contract(self, contract_id: str, contract: ContractAddRequest) -> None:
        """Add a contract to the bus"""
        response = await self.client.post(f"/contract/{contract_id}", json=contract)
        response.raise_for_status()

    # Contract related endpoints
    @handle_api_errors(RenterdError)
    async def acquire_contract(self, contract_id: str, duration: DurationMS, priority: int) -> ContractAcquireResponse:
        response = await self.bus_client.post(
            f"/contract/{contract_id}/acquire", json={"duration": duration, "priority": priority}
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_contract_keepalive(self, contract_id: str, request: ContractKeepaliveRequest) -> None:
        """Extend duration on an already acquired lock"""
        response = await self.client.post(f"/contract/{contract_id}/keepalive", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def contract_ancestors(self, contract_id: str, min_start_height: int) -> List[ContractMetadata]:
        params = {"minstartheight": min_start_height}
        response = await self.bus_client.get(f"/contract/{contract_id}/ancestors", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def release_contract(self, contract_id: str, lock_id: int) -> None:
        response = await self.bus_client.post(f"/contract/{contract_id}/release", json={"lockID": lock_id})
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_contract_roots(self, contract_id: str) -> List[Hash256]:
        response = await self.bus_client.get(f"/contract/{contract_id}/roots")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_size(self, contract_id: str) -> ContractSize:
        """Get contract size"""
        response = await self.client.get(f"/contract/{contract_id}/size")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contracts(self, filter_mode: str = "active") -> List[ContractMetadata]:
        response = await self.bus_client.get("/contracts", params={"filtermode": filter_mode})
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_contracts_archive(self, to_archive: Dict[FileContractID, str]) -> None:
        """Archive contracts"""
        response = await self.client.post("/contracts/archive", json=to_archive)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_contracts_all(self) -> None:
        """Delete all contracts"""
        response = await self.client.delete("/contracts/all")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_contracts_prunable(self) -> ContractsPrunableDataResponse:
        """Get prunable contracts data"""
        response = await self.client.get("/contracts/prunable")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contracts_renewed(self, contract_id: str) -> ContractMetadata:
        """Get renewed contract"""
        response = await self.client.get(f"/contracts/renewed/{contract_id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_contracts_set(self, set_name: str, contract_ids: List[FileContractID]) -> None:
        """Create a new contract set"""
        response = await self.client.put(f"/contracts/set/{set_name}", json=contract_ids)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_contracts_set(self, set_name: str) -> None:
        """Delete a contract set"""
        response = await self.client.delete(f"/contracts/set/{set_name}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_contracts_sets(self) -> List[str]:
        """Get all contract set names"""
        response = await self.client.get("/contracts/sets")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_contracts_spending(self, records: List[ContractSpendingRecord]) -> None:
        """Record contract spending"""
        response = await self.client.post("/contracts/spending", json=records)
        response.raise_for_status()

    # Host related endpoints
    @handle_api_errors(RenterdError)
    async def get_host(self, pubkey: str) -> Host:
        """Get host information"""
        response = await self.client.get(f"/host/{pubkey}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def reset_lost_sectors(self, pubkey: str) -> None:
        """Reset lost sectors for a host"""
        response = await self.client.post(f"/host/{pubkey}/resetlostsectors")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_hosts(self, offset: int, limit: int) -> List[Host]:
        """Get list of hosts"""
        params = {"offset": offset, "limit": limit}
        response = await self.client.get("/hosts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_hosts_allowlist(self) -> List[PublicKey]:
        """Get hosts allowlist"""
        response = await self.client.get("/hosts/allowlist")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_hosts_allowlist(self, request: UpdateAllowlistRequest) -> None:
        response = await self.bus_client.put("/hosts/allowlist", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_hosts_blocklist(self) -> List[str]:
        response = await self.bus_client.get("/hosts/blocklist")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_hosts_blocklist(self, request: UpdateBlocklistRequest) -> None:
        response = await self.bus_client.put("/hosts/blocklist", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_hosts_interactions(self, interactions: List[HostScan]) -> None:
        """Record host interactions"""
        response = await self.client.post("/hosts/interactions", json=interactions)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def remove_hosts(self, request: HostsRemoveRequest) -> int:
        """Remove offline hosts"""
        response = await self.client.post("/hosts/remove", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_hosts_scanning(self, offset: int, limit: int, last_scan: str) -> List[Host]:
        """Get hosts for scanning"""
        params = {"offset": offset, "limit": limit, "lastScan": last_scan}
        response = await self.client.get("/hosts/scanning", params=params)
        response.raise_for_status()
        return response.json()

    # Metrics endpoints
    @handle_api_errors(RenterdError)
    async def get_metrics(self, key: str, start: str, n: int, interval: str) -> Any:
        """Get metrics"""
        params = {"start": start, "n": n, "interval": interval}
        response = await self.client.get(f"/metric/{key}", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_metrics(self, key: str, cutoff: str) -> None:
        """Delete metrics"""
        params = {"cutoff": cutoff}
        response = await self.client.delete(f"/metric/{key}", params=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def abort_multipart_upload(self, request: MultipartAbortRequest) -> None:
        response = await self.bus_client.post("/multipart/abort", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def complete_multipart_upload(self, request: MultipartCompleteRequest) -> MultipartCompleteResponse:
        response = await self.bus_client.post("/multipart/complete", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def create_multipart_upload(self, request: MultipartCreateRequest) -> MultipartCreateResponse:
        response = await self.bus_client.post("/multipart/create", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_upload_parts(self, request: MultipartListPartsRequest) -> MultipartListPartsResponse:
        response = await self.bus_client.post("/multipart/listparts", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_uploads(self, request: MultipartListUploadsRequest) -> MultipartListUploadsResponse:
        response = await self.bus_client.post("/multipart/listuploads", json=request)
        response.raise_for_status()
        return response.json()

    # Multipart endpoints
    @handle_api_errors(RenterdError)
    async def put_multipart_part(self, request: MultipartAddPartRequest) -> None:
        """Add a new part to multipart upload"""
        response = await self.client.put("/multipart/part", json=request)
        response.raise_for_status()

    # Object endpoints
    @handle_api_errors(RenterdError)
    async def get_object(self, key: str) -> Object:
        """Get object metadata"""
        response = await self.client.get(f"/objects/{key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_object(self, key: str, request: AddObjectRequest) -> None:
        """Store object metadata"""
        response = await self.client.put(f"/objects/{key}", json=request)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_object(self, key: str) -> None:
        """Delete object"""
        response = await self.client.delete(f"/objects/{key}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def post_objects_copy(self, request: CopyObjectsRequest) -> ObjectMetadata:
        """Copy object"""
        response = await self.client.post("/objects/copy", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_objects_list(self, request: ObjectsListRequest) -> ObjectsResponse:
        """List objects"""
        response = await self.client.post("/objects/list", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_objects_rename(self, request: ObjectsRenameRequest) -> None:
        """Rename objects"""
        response = await self.client.post("/objects/rename", json=request)
        response.raise_for_status()

    # Params endpoints
    @handle_api_errors(RenterdError)
    async def get_download_params(self) -> DownloadParams:
        """Get download parameters"""
        response = await self.client.get("/params/download")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_gouging_params(self) -> GougingParams:
        """Get gouging parameters"""
        response = await self.client.get("/params/gouging")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_upload_params(self) -> UploadParams:
        """Get upload parameters"""
        response = await self.client.get("/params/upload")
        response.raise_for_status()
        return response.json()

    # Search endpoints
    @handle_api_errors(RenterdError)
    async def post_search_hosts(self, request: HostsRequest) -> List[Host]:
        """Search hosts"""
        response = await self.client.post("/search/hosts", json=request)
        response.raise_for_status()
        return response.json()

    @strawberry.field
    async def search_hosts(self, info: Info, request: HostsRequest) -> List[Host]:
        """Search hosts"""
        return await self.handle_api_call(info, "post_search_hosts", request=request)

    @handle_api_errors(RenterdError)
    async def get_search_objects(self, bucket: str, key: str, offset: int, limit: int) -> List[str]:
        """Search objects"""
        params = {"bucket": bucket, "key": key, "offset": offset, "limit": limit}
        response = await self.client.get("/search/objects", params=params)
        response.raise_for_status()
        return response.json()

    # Settings endpoints
    @handle_api_errors(RenterdError)
    async def get_settings(self) -> List[str]:
        """Get all available settings keys"""
        response = await self.client.get("/settings")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_setting(self, key: str) -> Any:
        """Get setting for specific key"""
        response = await self.client.get(f"/setting/{key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_setting(self, key: str, value: Any) -> None:
        """Update setting for specific key"""
        response = await self.client.put(f"/setting/{key}", json=value)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_setting(self, key: str) -> None:
        """Delete setting for specific key"""
        response = await self.client.delete(f"/setting/{key}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_slabs_for_migration(self, request: MigrationSlabsRequest) -> SlabsForMigrationResponse:
        response = await self.bus_client.post("/slabs/migration", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_partial_slab(self, key: EncryptionKey, offset: int, length: int) -> bytes:
        params = {"offset": offset, "length": length}
        response = await self.bus_client.get(f"/slabs/partial/{key}", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def add_partial_slab(self, data: bytes, min_shards: int, total_shards: int) -> AddPartialSlabResponse:
        params = {"minshards": min_shards, "totalshards": total_shards}
        response = await self.bus_client.post("/slabs/partial", data=data, params=params)
        response.raise_for_status()
        return response.json()

    # Slab endpoints
    @handle_api_errors(RenterdError)
    async def get_slab(self, key: EncryptionKey) -> Slab:
        response = await self.bus_client.get(f"/slab/{key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_slab_objects(self, key: str) -> SlabObjects:
        """Get objects associated with a slab"""
        response = await self.client.get(f"/slab/{key}/objects")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_slab(self, key: str, sectors: List[UploadedSector]) -> None:
        """Update a slab"""
        response = await self.client.put(f"/slab/{key}", json=sectors)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def refresh_health(self) -> None:
        response = await self.bus_client.post("/slabs/refreshhealth")
        response.raise_for_status()

    # State endpoint
    @handle_api_errors(RenterdError)
    async def get_state(self) -> BusStateResponse:
        """Get bus state"""
        response = await self.client.get("/state")
        response.raise_for_status()
        return response.json()

    # Stats endpoint
    @handle_api_errors(RenterdError)
    async def get_stats_objects(self) -> ObjectsStatsResponse:
        """Get object statistics"""
        response = await self.client.get("/stats/objects")
        response.raise_for_status()
        return response.json()

    # Syncer endpoints
    @handle_api_errors(RenterdError)
    async def get_syncer_address(self) -> str:
        response = await self.bus_client.get("/syncer/address")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_syncer_connect(self, address: str) -> None:
        """Connect to peer"""
        response = await self.client.post("/syncer/connect", json=address)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_syncer_peers(self) -> List[str]:
        """Get syncer peers"""
        response = await self.client.get("/syncer/peers")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def post_txpool_broadcast(self, transactions: List[Transaction]) -> None:
        """Broadcast transactions"""
        response = await self.client.post("/txpool/broadcast", json=transactions)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_txpool_recommendedfee(self) -> Currency:
        """Get recommended transaction fee"""
        response = await self.client.get("/txpool/recommendedfee")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_txpool_transactions(self) -> List[Transaction]:
        """Get transaction pool transactions"""
        response = await self.client.get("/txpool/transactions")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def track_upload(self, upload_id: str) -> None:
        response = await self.worker_client.post(f"/upload/{upload_id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def finish_upload(self, upload_id: str) -> None:
        response = await self.worker_client.delete(f"/upload/{upload_id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def add_upload_sector(self, upload_id: str, roots: List[Hash256]) -> None:
        response = await self.worker_client.post(f"/upload/{upload_id}/sector", json=roots)
        response.raise_for_status()

    # Wallet endpoints
    @handle_api_errors(RenterdError)
    async def get_wallet(self) -> WalletResponse:
        """Get wallet information"""
        response = await self.client.get("/wallet")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_address(self) -> str:
        """Get wallet address"""
        response = await self.client.get("/wallet/address")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_balance(self) -> Currency:
        """Get wallet balance"""
        response = await self.client.get("/wallet/balance")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def discard_transaction(self, transaction: Transaction) -> None:
        """Discard a transaction"""
        response = await self.client.post("/wallet/discard", json=transaction)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def fund_wallet(self, request: WalletFundRequest) -> WalletFundResponse:
        """Fund wallet"""
        response = await self.client.post("/wallet/fund", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_outputs(self) -> List[SiacoinElement]:
        """Get wallet outputs"""
        response = await self.client.get("/wallet/outputs")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_pending(self) -> List[Transaction]:
        """Get pending transactions"""
        response = await self.client.get("/wallet/pending")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def prepare_form_contract(self, request: ContractFormRequest) -> RHPFormResponse:
        """Prepare contract formation"""
        response = await self.client.post("/wallet/prepare/form", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def prepare_renew_contract(self, request: ContractRenewRequest) -> RHPFormResponse:
        """Prepare contract renewal"""
        response = await self.client.post("/wallet/prepare/renew", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def redistribute_wallet(self, amount: Currency, outputs: int) -> List[TransactionID]:
        """Redistribute wallet funds"""
        request = {"amount": amount, "outputs": outputs}
        response = await self.client.post("/wallet/redistribute", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def sign_transaction(self, request: WalletSignRequest) -> Transaction:
        """Sign a transaction"""
        response = await self.client.post("/wallet/sign", json=request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_transactions(self) -> List[Transaction]:
        """Get wallet transactions"""
        response = await self.client.get("/wallet/transactions")
        response.raise_for_status()
        return response.json()

    # Webhook endpoints
    @handle_api_errors(RenterdError)
    async def get_webhooks(self) -> WebhookResponse:
        response = await self.bus_client.get("/webhooks")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def register_webhook(self, webhook: Webhook) -> None:
        response = await self.bus_client.post("/webhooks", json=webhook)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_webhook(self, webhook: Webhook) -> None:
        response = await self.bus_client.post("/webhook/delete", json=webhook)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def broadcast_webhook_action(self, action: Event) -> None:
        response = await self.bus_client.post("/webhooks/action", json=action)
        response.raise_for_status()
