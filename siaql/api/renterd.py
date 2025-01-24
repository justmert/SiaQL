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
    AddObjectRequest,
    AddPartialSlabResponse,
    Alert,
    AlertsOpts,
    AlertsResponse,
    ArchivedContract,
    Autopilot,
    AutopilotConfig,
    AutopilotStateResponse,
    Block,
    Bucket,
    BucketCreateRequest,
    BucketPolicy,
    BusStateResponse,
    ConfigEvaluationRequest,
    ConfigEvaluationResponse,
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
    ContractsResponse,
    CopyObjectsRequest,
    Currency,
    DeleteObjectOptions,
    DownloadStatsResponse,
    FileContractID,
    GetObjectResponse,
    GougingParams,
    Hash256,
    HeadObjectOptions,
    HeadObjectResponse,
    Host,
    HostAddress,
    HostCheck,
    HostPriceTable,
    HostResponse,
    HostsPriceTablesRequest,
    HostsRemoveRequest,
    HostsScanRequest,
    MemoryResponse,
    MigrateSlabResponse,
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
    RHPPriceTableRequest,
    RHPScanRequest,
    RHPScanResponse,
    SearchHostsRequest,
    SiacoinElement,
    Slab,
    SlabBuffer,
    Transaction,
    TransactionID,
    UnhealthySlabsResponse,
    UpdateAllowlistRequest,
    UpdateBlocklistRequest,
    UploadID,
    UploadObjectOptions,
    UploadObjectResponse,
    UploadParams,
    UploadSectorRequest,
    UploadStatsResponse,
    WalletFundRequest,
    WalletFundResponse,
    WalletRedistributeRequest,
    WalletResponse,
    WalletSendRequest,
    WalletSignRequest,
    Webhook,
    WebhookEvent,
    WebhookResponse,
    WorkerStateResponse,
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
    @handle_api_errors(RenterdError)
    async def get_accounts(self, owner: Optional[str] = None) -> List[Account]:
        response = await self.client.get("/bus/accounts", params={"owner": owner})
        return response.json()

    @handle_api_errors(RenterdError)
    async def save_accounts(self, req: AccountsSaveRequest) -> None:
        await self.client.post("/bus/accounts", json=req.dict())

    @handle_api_errors(RenterdError)
    async def fund_account(self, req: AccountsFundRequest) -> AccountsFundResponse:
        response = await self.client.post("/bus/accounts/fund", json=req.dict())
        return response.json()

    # Alert endpoints
    @handle_api_errors(RenterdError)
    async def get_alerts(self, opts: AlertsOpts) -> AlertsResponse:
        response = await self.client.get("/bus/alerts", params={**opts.dict()})
        return response.json()

    @handle_api_errors(RenterdError)
    async def dismiss_alerts(self, ids: List[Hash256]) -> None:
        await self.client.post("/bus/alerts/dismiss", json=ids)

    @handle_api_errors(RenterdError)
    async def register_alert(self, alert: Alert) -> None:
        await self.client.post("/bus/alerts/register", json=alert.dict())

    # Autopilot endpoints
    @handle_api_errors(RenterdError)
    async def get_autopilots(self) -> List[Autopilot]:
        response = await self.client.get("/bus/autopilots")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_autopilot(self, id: str) -> Autopilot:
        response = await self.client.get(f"/bus/autopilot/{id}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_autopilot(self, id: str, autopilot: Autopilot) -> None:
        await self.client.put(f"/bus/autopilot/{id}", json=autopilot.dict())

    @handle_api_errors(RenterdError)
    async def update_autopilot_host_check(self, autopilot_id: str, host_key: PublicKey, check: HostCheck) -> None:
        await self.client.put(f"/bus/autopilot/{autopilot_id}/host/{host_key}/check", json=check.dict())

    # Bucket endpoints
    @handle_api_errors(RenterdError)
    async def get_buckets(self) -> List[Bucket]:
        response = await self.client.get("/bus/buckets")
        return response.json()

    @handle_api_errors(RenterdError)
    async def create_bucket(self, req: BucketCreateRequest) -> None:
        await self.client.post("/bus/buckets", json=req.dict())

    @handle_api_errors(RenterdError)
    async def update_bucket_policy(self, name: str, policy: BucketPolicy) -> None:
        await self.client.put(f"/bus/bucket/{name}/policy", json=policy.dict())

    @handle_api_errors(RenterdError)
    async def delete_bucket(self, name: str) -> None:
        await self.client.delete(f"/bus/bucket/{name}")

    @handle_api_errors(RenterdError)
    async def get_bucket(self, name: str) -> Bucket:
        response = await self.client.get(f"/bus/bucket/{name}")
        return response.json()

    # Consensus endpoints
    @handle_api_errors(RenterdError)
    async def consensus_accept_block(self, block: Block) -> None:
        await self.client.post("/bus/consensus/acceptblock", json=block.dict())

    @handle_api_errors(RenterdError)
    async def get_consensus_network(self) -> Network:
        response = await self.client.get("/bus/consensus/network")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_consensus_siafund_fee(self, payout: Currency) -> Currency:
        response = await self.client.get(f"/bus/consensus/siafundfee/{payout}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_consensus_state(self) -> ConsensusState:
        response = await self.client.get("/bus/consensus/state")
        return response.json()

    # Contract endpoints
    @handle_api_errors(RenterdError)
    async def form_contract(self, req: ContractFormRequest) -> ContractMetadata:
        response = await self.client.post("/bus/contracts", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contracts(self, contract_set: Optional[str] = None) -> List[ContractMetadata]:
        params = {"contractset": contract_set} if contract_set else None
        response = await self.client.get("/bus/contracts", params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_contracts_all(self) -> None:
        await self.client.delete("/bus/contracts/all")

    @handle_api_errors(RenterdError)
    async def archive_contracts(self, req: ContractsArchiveRequest) -> None:
        await self.client.post("/bus/contracts/archive", json=req.dict())

    @handle_api_errors(RenterdError)
    async def get_contracts_prunable(self) -> ContractsPrunableDataResponse:
        response = await self.client.get("/bus/contracts/prunable")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_renewed(self, id: FileContractID) -> ContractMetadata:
        response = await self.client.get(f"/bus/contracts/renewed/{id}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_sets(self) -> List[str]:
        response = await self.client.get("/bus/contracts/sets")
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_contract_set(self, set_name: str, req: ContractSetUpdateRequest) -> None:
        await self.client.post(f"/bus/contracts/set/{set_name}", json=req.dict())

    @handle_api_errors(RenterdError)
    async def delete_contract_set(self, set_name: str) -> None:
        await self.client.delete(f"/bus/contracts/set/{set_name}")

    @handle_api_errors(RenterdError)
    async def record_contract_spending(self, records: List[ContractSpendingRecord]) -> None:
        await self.client.post("/bus/contracts/spending", json=[r.dict() for r in records])

    @handle_api_errors(RenterdError)
    async def get_contract(self, id: FileContractID) -> ContractMetadata:
        response = await self.client.get(f"/bus/contract/{id}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def add_contract(self, id: FileContractID, req: ContractAddRequest) -> ContractMetadata:
        response = await self.client.post(f"/bus/contract/{id}", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_contract(self, id: FileContractID) -> None:
        await self.client.delete(f"/bus/contract/{id}")

    @handle_api_errors(RenterdError)
    async def acquire_contract(self, id: FileContractID, req: ContractAcquireRequest) -> ContractAcquireResponse:
        response = await self.client.post(f"/bus/contract/{id}/acquire", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_ancestors(self, id: FileContractID, min_start_height: int) -> List[ArchivedContract]:
        response = await self.client.get(f"/bus/contract/{id}/ancestors", params={"minStartHeight": min_start_height})
        return response.json()

    @handle_api_errors(RenterdError)
    async def contract_broadcast(self, id: FileContractID) -> TransactionID:
        response = await self.client.post(f"/bus/contract/{id}/broadcast")
        return response.json()

    @handle_api_errors(RenterdError)
    async def keepalive_contract(self, id: FileContractID, req: ContractKeepaliveRequest) -> None:
        await self.client.post(f"/bus/contract/{id}/keepalive", json=req.dict())

    @handle_api_errors(RenterdError)
    async def prune_contract(self, id: FileContractID, req: ContractPruneRequest) -> ContractPruneResponse:
        response = await self.client.post(f"/bus/contract/{id}/prune", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def renew_contract(self, id: FileContractID, req: ContractRenewRequest) -> ContractMetadata:
        response = await self.client.post(f"/bus/contract/{id}/renew", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def add_renewed_contract(self, id: FileContractID, req: ContractRenewedRequest) -> ContractMetadata:
        response = await self.client.post(f"/bus/contract/{id}/renewed", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def release_contract(self, id: FileContractID, lock_id: int) -> None:
        await self.client.post(f"/bus/contract/{id}/release", json={"lockID": lock_id})

    @handle_api_errors(RenterdError)
    async def get_contract_roots(self, id: FileContractID) -> ContractRootsResponse:
        response = await self.client.get(f"/bus/contract/{id}/roots")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_size(self, id: FileContractID) -> ContractSize:
        response = await self.client.get(f"/bus/contract/{id}/size")
        return response.json()

    # Host endpoints
    @handle_api_errors(RenterdError)
    async def get_hosts(self) -> List[Host]:
        response = await self.client.get("/bus/hosts")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_hosts_allowlist(self) -> List[PublicKey]:
        response = await self.client.get("/bus/hosts/allowlist")
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_hosts_allowlist(self, req: UpdateAllowlistRequest) -> None:
        await self.client.put("/bus/hosts/allowlist", json=req.dict())

    @handle_api_errors(RenterdError)
    async def get_hosts_blocklist(self) -> List[str]:
        response = await self.client.get("/bus/hosts/blocklist")
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_hosts_blocklist(self, req: UpdateBlocklistRequest) -> None:
        await self.client.put("/bus/hosts/blocklist", json=req.dict())

    @handle_api_errors(RenterdError)
    async def record_price_tables(self, req: HostsPriceTablesRequest) -> None:
        await self.client.post("/bus/hosts/pricetables", json=req.dict())

    @handle_api_errors(RenterdError)
    async def hosts_remove(self, req: HostsRemoveRequest) -> int:
        response = await self.client.post(
            "/bus/hosts/remove",
            json=req.dict(),
        )
        return response.json()

    @handle_api_errors(RenterdError)
    async def record_hosts_scan(self, req: HostsScanRequest) -> None:
        await self.client.post("/bus/hosts/scans", json=req.dict())

    @handle_api_errors(RenterdError)
    async def get_hosts_scanning(
        self, last_scan: Optional[str] = None, offset: int = 0, limit: int = -1
    ) -> List[HostAddress]:
        params = {"lastScan": last_scan, "offset": offset, "limit": limit}
        response = await self.client.get("/bus/hosts/scanning", params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_host(self, public_key: PublicKey) -> Host:
        response = await self.client.get(f"/bus/host/{public_key}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def hosts_reset_lost_sectors(self, hostkey: PublicKey) -> None:
        await self.client.post(f"/bus/host/{hostkey}/resetlostsectors")

    # Metric endpoints
    @handle_api_errors(RenterdError)
    async def update_metric(self, key: str, data: Any) -> None:
        await self.client.put(f"/bus/metric/{key}", json=data)

    @handle_api_errors(RenterdError)
    async def get_metric(self, key: str, start: str, n: int, interval: str) -> Any:
        params = {"start": start, "n": n, "interval": interval}
        response = await self.client.get(f"/bus/metric/{key}", params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_metric(self, key: str, cutoff: str) -> None:
        await self.client.delete(f"/bus/metric/{key}", params={"cutoff": cutoff})

    # Multipart endpoints
    @handle_api_errors(RenterdError)
    async def create_multipart_upload(self, req: MultipartCreateRequest) -> MultipartCreateResponse:
        response = await self.client.post("/bus/multipart/create", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def abort_multipart_upload(self, req: MultipartAbortRequest) -> None:
        await self.client.post("/bus/multipart/abort", json=req.dict())

    @handle_api_errors(RenterdError)
    async def complete_multipart_upload(self, req: MultipartCompleteRequest) -> MultipartCompleteResponse:
        response = await self.client.post("/bus/multipart/complete", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def add_multipart_part(self, req: MultipartAddPartRequest) -> None:
        await self.client.put("/bus/multipart/part", json=req.dict())

    @handle_api_errors(RenterdError)
    async def get_multipart_upload(self, id: str) -> MultipartUpload:
        response = await self.client.get(f"/bus/multipart/upload/{id}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_uploads(self, req: MultipartListUploadsRequest) -> MultipartListUploadsResponse:
        response = await self.client.post("/bus/multipart/listuploads", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_parts(self, req: MultipartListPartsRequest) -> MultipartListPartsResponse:
        response = await self.client.post("/bus/multipart/listparts", json=req.dict())
        return response.json()

    # Object endpoints
    @handle_api_errors(RenterdError)
    async def get_object(self, path: str, bucket: Optional[str] = None, only_metadata: bool = False) -> Object:
        params = {"bucket": bucket, "onlymetadata": only_metadata} if bucket else {"onlymetadata": only_metadata}
        response = await self.client.get(f"/bus/objects/{path}", params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def add_object(self, path: str, req: AddObjectRequest) -> None:
        await self.client.put(f"/bus/objects/{path}", json=req.dict())

    @handle_api_errors(RenterdError)
    async def delete_object(self, path: str, bucket: Optional[str] = None, batch: bool = False) -> None:
        params = {"bucket": bucket, "batch": batch} if bucket else {"batch": batch}
        await self.client.delete(f"/bus/objects/{path}", params=params)

    @handle_api_errors(RenterdError)
    async def copy_object(self, req: CopyObjectsRequest) -> ObjectMetadata:
        response = await self.client.post("/bus/objects/copy", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def rename_object(self, req: ObjectsRenameRequest) -> None:
        await self.client.post("/bus/objects/rename", json=req.dict())

    @handle_api_errors(RenterdError)
    async def list_objects(self, req: ObjectsListRequest) -> ObjectsListResponse:
        response = await self.client.post("/bus/objects/list", json=req.dict())
        return response.json()

    # Parameter endpoints
    @handle_api_errors(RenterdError)
    async def get_gouging_params(self) -> GougingParams:
        response = await self.client.get("/bus/params/gouging")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_upload_params(self) -> UploadParams:
        response = await self.client.get("/bus/params/upload")
        return response.json()

    # Slab buffer endpoints
    @handle_api_errors(RenterdError)
    async def get_slab_buffers(self) -> List[SlabBuffer]:
        response = await self.client.get("/bus/slabbuffers")
        return response.json()

    @handle_api_errors(RenterdError)
    async def mark_packed_slabs_uploaded(self, req: PackedSlabsRequestPOST) -> None:
        await self.client.post("/bus/slabbuffer/done", json=req.dict())

    @handle_api_errors(RenterdError)
    async def fetch_packed_slabs(self, req: PackedSlabsRequestGET) -> List[PackedSlab]:
        response = await self.client.post("/bus/slabbuffer/fetch", json=req.dict())
        return response.json()

    # Search endpoints
    @handle_api_errors(RenterdError)
    async def search_hosts(self, req: SearchHostsRequest) -> List[Host]:
        response = await self.client.post("/bus/search/hosts", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def search_objects(
        self, key: str, bucket: str = "default", offset: int = 0, limit: int = -1
    ) -> List[ObjectMetadata]:
        params = {"key": key, "bucket": bucket, "offset": offset, "limit": limit}
        response = await self.client.get("/bus/search/objects", params=params)
        return response.json()

    # Sector endpoints
    @handle_api_errors(RenterdError)
    async def delete_host_sector(self, host_key: PublicKey, root: Hash256) -> int:
        response = await self.client.delete(f"/bus/sectors/{host_key}/{root}")
        return response.json()

    # Settings endpoints
    @handle_api_errors(RenterdError)
    async def get_settings(self) -> List[str]:
        response = await self.client.get("/bus/settings")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_setting(self, key: str) -> str:
        response = await self.client.get(f"/bus/setting/{key}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_setting(self, key: str, value: str) -> None:
        await self.client.put(f"/bus/setting/{key}", json=value)

    @handle_api_errors(RenterdError)
    async def delete_setting(self, key: str) -> None:
        await self.client.delete(f"/bus/setting/{key}")

    # Slab endpoints
    @handle_api_errors(RenterdError)
    async def slabs_migration(self, req: MigrationSlabsRequest) -> UnhealthySlabsResponse:
        response = await self.client.post("/bus/slabs/migration", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_slabs_partial(self, key: str, offset: int, length: int) -> bytes:
        params = {"offset": offset, "length": length}
        response = await self.client.get(f"/bus/slabs/partial/{key}", params=params)
        return response.content

    @handle_api_errors(RenterdError)
    async def add_slabs_partial(
        self, data: bytes, min_shards: int, total_shards: int, contract_set: str
    ) -> AddPartialSlabResponse:
        params = {"minShards": min_shards, "totalShards": total_shards, "contractSet": contract_set}
        response = await self.client.post("/bus/slabs/partial", content=data, params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def refresh_health(self) -> None:
        await self.client.post("/bus/slabs/refreshhealth")

    @handle_api_errors(RenterdError)
    async def get_slab(self, key: str) -> Slab:
        response = await self.client.get(f"/bus/slab/{key}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_slab_objects(self, key: str) -> List[ObjectMetadata]:
        response = await self.client.get(f"/bus/slab/{key}/objects")
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_slab(self, slab: Slab) -> None:
        await self.client.put("/bus/slab", json=slab.dict())

    # State endpoints
    @handle_api_errors(RenterdError)
    async def get_state(self) -> BusStateResponse:
        response = await self.client.get("/bus/state")
        return response.json()

    # Stats endpoints
    @handle_api_errors(RenterdError)
    async def get_objects_stats(self) -> ObjectsStatsResponse:
        response = await self.client.get("/bus/stats/objects")
        return response.json()

    # Syncer endpoints
    @handle_api_errors(RenterdError)
    async def get_syncer_address(self) -> str:
        response = await self.client.get("/bus/syncer/address")
        return response.json()

    @handle_api_errors(RenterdError)
    async def sync_connect(self, addr: str) -> None:
        await self.client.post("/bus/syncer/connect", json=addr)

    @handle_api_errors(RenterdError)
    async def get_syncer_peers(self) -> List[str]:
        response = await self.client.get("/bus/syncer/peers")
        return response.json()

    # Transaction pool endpoints
    @handle_api_errors(RenterdError)
    async def get_txpool_recommended_fee(self) -> Currency:
        response = await self.client.get("/bus/txpool/recommendedfee")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_txpool_transactions(self) -> List[Transaction]:
        response = await self.client.get("/bus/txpool/transactions")
        return response.json()

    @handle_api_errors(RenterdError)
    async def txpool_broadcast(self, transactions: List[Transaction]) -> None:
        await self.client.post("/bus/txpool/broadcast", json=transactions)

    # Upload endpoints
    @handle_api_errors(RenterdError)
    async def upload_track(self, id: str) -> None:
        await self.client.post(f"/bus/upload/{id}")

    @handle_api_errors(RenterdError)
    async def upload_finished(self, id: str) -> None:
        await self.client.delete(f"/bus/upload/{id}")

    @handle_api_errors(RenterdError)
    async def upload_add_sector(self, id: UploadID, req: UploadSectorRequest) -> None:
        await self.client.post(f"/bus/upload/{id}/sector", json=req.dict())

    # Wallet endpoints
    @handle_api_errors(RenterdError)
    async def get_wallet(self) -> WalletResponse:
        response = await self.client.get("/bus/wallet")
        return response.json()

    @handle_api_errors(RenterdError)
    async def wallet_discard_transaction(self, transaction: Transaction) -> None:
        await self.client.post("/bus/wallet/discard", json=transaction.dict())

    @handle_api_errors(RenterdError)
    async def wallet_fund(self, req: WalletFundRequest) -> WalletFundResponse:
        response = await self.client.post(
            "/bus/wallet/fund",
            json=req.dict(),
        )
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_outputs(self) -> List[SiacoinElement]:
        response = await self.client.get("/bus/wallet/outputs")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_pending(self) -> List[Transaction]:
        response = await self.client.get("/bus/wallet/pending")
        return response.json()

    @handle_api_errors(RenterdError)
    async def wallet_redistribute(self, req: WalletRedistributeRequest) -> List[TransactionID]:
        response = await self.client.post("/bus/wallet/redistribute", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def wallet_send_siacoins(self, req: WalletSendRequest) -> TransactionID:
        response = await self.client.post("/bus/wallet/send", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def wallet_sign_transaction(self, req: WalletSignRequest) -> Transaction:
        response = await self.client.post(
            "/bus/wallet/sign",
            json=req.dict(),
        )
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_transactions(self, offset: int = 0, limit: int = -1) -> List[Transaction]:
        params = {"offset": offset, "limit": limit}
        response = await self.client.get("/bus/wallet/transactions", params=params)
        return response.json()

    # Webhook endpoints
    @handle_api_errors(RenterdError)
    async def get_webhooks(self) -> WebhookResponse:
        response = await self.client.get("/bus/webhooks")
        return response.json()

    @handle_api_errors(RenterdError)
    async def register_webhook(self, webhook: Webhook) -> None:
        await self.client.post("/bus/webhooks", json=webhook.dict())

    @handle_api_errors(RenterdError)
    async def broadcast_action(self, event: WebhookEvent) -> None:
        await self.client.post("/bus/webhooks/action", json=event.dict())

    @handle_api_errors(RenterdError)
    async def delete_webhook(self, webhook: Webhook) -> None:
        await self.client.post("/bus/webhook/delete", json=webhook.dict())

    # Autopilot endpoints
    @handle_api_errors(RenterdError)
    async def get_autopilot_config(self) -> AutopilotConfig:
        response = await self.client.get("/autopilot/config")
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_autopilot_config(self, config: AutopilotConfig) -> None:
        await self.client.put("/autopilot/config", json=config.dict())

    @handle_api_errors(RenterdError)
    async def get_autopilot_host(self, host_key: PublicKey) -> HostResponse:
        response = await self.client.get(f"/autopilot/host/{host_key}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_autopilot_hosts(self, opts: SearchHostsRequest) -> List[HostResponse]:
        response = await self.client.post("/autopilot/hosts", params=opts)
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_autopilot_state(self) -> AutopilotStateResponse:
        response = await self.client.get("/autopilot/state")
        return response.json()

    @handle_api_errors(RenterdError)
    async def trigger_autopilot(self, force_scan: bool = False) -> bool:
        response = await self.client.post("/autopilot/trigger", json={"forceScan": force_scan})
        return response.json()

    @handle_api_errors(RenterdError)
    async def evaluate_autopilot_config(self, req: ConfigEvaluationRequest) -> ConfigEvaluationResponse:
        response = await self.client.post("/autopilot/config", json=req.dict())
        return response.json()

    # Worker endpoints
    @handle_api_errors(RenterdError)
    async def get_worker_state(self) -> WorkerStateResponse:
        response = await self.client.get("/worker/state")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_memory(self) -> MemoryResponse:
        response = await self.client.get("/worker/memory")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_id(self) -> str:
        response = await self.client.get("/worker/id")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_accounts(self) -> List[Account]:
        response = await self.client.get("/worker/accounts")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_account(self, host_key: str) -> Account:
        response = await self.client.get(f"/worker/account/{host_key}")
        return response.json()

    @handle_api_errors(RenterdError)
    async def rhp_scan(self, req: RHPScanRequest) -> RHPScanResponse:
        response = await self.client.post("/worker/rhp/scan", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def rhp_price_table(self, req: RHPPriceTableRequest) -> HostPriceTable:
        response = await self.client.post("/worker/rhp/pricetable", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_contracts(self, host_timeout: Optional[int] = None) -> ContractsResponse:
        params = {"hosttimeout": host_timeout} if host_timeout else None
        response = await self.client.get("/worker/rhp/contracts", params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_object(self, bucket: str, path: str, opts: GetObjectResponse) -> GetObjectResponse:
        params = {"bucket": bucket, **opts.dict()}
        response = await self.client.get(f"/worker/objects/{path}", params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def head_object(self, bucket: str, path: str, opts: HeadObjectOptions) -> HeadObjectResponse:
        params = {"bucket": bucket, **opts.dict()}
        response = await self.client.head(f"/worker/objects/{path}", params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def upload_object(
        self, bucket: str, path: str, data: bytes, options: UploadObjectOptions
    ) -> UploadObjectResponse:
        params = {"bucket": bucket, **UploadObjectOptions.dict()}
        response = await self.client.put(
            f"/worker/objects/{path}", content=data, params=params, headers=options.get("metadata", {})
        )
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_worker_object(self, bucket: str, path: str, opts: DeleteObjectOptions) -> None:
        params = {"bucket": bucket, **opts.dict()}
        await self.client.delete(f"/worker/objects/{path}", params=params)

    @handle_api_errors(RenterdError)
    async def multipart_create(self, req: MultipartCreateRequest) -> MultipartCreateResponse:
        response = await self.client.post("/worker/multipart/create", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def multipart_abort(self, req: MultipartAbortRequest) -> None:
        await self.client.post("/worker/multipart/abort", json=req.dict())

    @handle_api_errors(RenterdError)
    async def multipart_complete(self, req: MultipartCompleteRequest) -> MultipartCompleteResponse:
        response = await self.client.post("/worker/multipart/complete", json=req.dict())
        return response.json()

    @handle_api_errors(RenterdError)
    async def multipart_upload(self, path: str, req: MultipartAddPartRequest) -> None:
        await self.client.put(f"/worker/multipart/{path}", json=req.dict())

    @handle_api_errors(RenterdError)
    async def migrate_slab(self, slab: Slab, contract_set: Optional[str] = None) -> MigrateSlabResponse:
        params = {"contractset": contract_set} if contract_set else None
        response = await self.client.post("/worker/slab/migrate", json=slab.dict(), params=params)
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_downloads_stats(self) -> DownloadStatsResponse:
        response = await self.client.get("/worker/stats/downloads")
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_uploads_stats(self) -> UploadStatsResponse:
        response = await self.client.get("/worker/stats/uploads")
        return response.json()

    @handle_api_errors(RenterdError)
    async def reset_account_drift(self, account_id: str) -> None:
        await self.client.post(f"/worker/account/{account_id}/resetdrift")

    @handle_api_errors(RenterdError)
    async def register_worker_event(self, event: WebhookEvent) -> None:
        await self.client.post("/worker/event", json=event.dict())
