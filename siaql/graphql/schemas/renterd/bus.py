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
    Event,
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
    async def accounts(self, info: Info, owner: Optional[str] = None) -> List[Account]:
        return await RenterdBaseResolver.handle_api_call(info, "get_accounts", owner=owner)

    @strawberry.field
    async def alerts(self, info: Info, opts: AlertsOpts.Input) -> AlertsResponse:
        return await RenterdBaseResolver.handle_api_call(info, "get_alerts", opts=opts)

    @strawberry.field
    async def autopilot(self, info: Info, id: str) -> Autopilot:
        return await RenterdBaseResolver.handle_api_call(info, "get_autopilot", id=id)

    @strawberry.field
    async def get_state(self, info: Info) -> BusStateResponse:
        """Get the current bus state"""
        return await RenterdBaseResolver.handle_api_call(info, "get_state")

    @strawberry.field
    async def contract_renewed(self, info: Info, id: FileContractID) -> ContractMetadata:
        """Get the renewed contract for a given contract ID"""
        return await RenterdBaseResolver.handle_api_call(info, "get_contract_renewed", id=id)

    @strawberry.field
    async def consensus_network(self, info: Info) -> Network:
        return await RenterdBaseResolver.handle_api_call(info, "get_consensus_network")

    @strawberry.field
    async def multipart_list_parts(
        self, info: Info, req: MultipartListPartsRequest.Input
    ) -> MultipartListPartsResponse:
        """List parts of a multipart upload"""
        return await RenterdBaseResolver.handle_api_call(info, "list_multipart_parts", req=req)

    @strawberry.field
    async def multipart_list_uploads(
        self, info: Info, req: MultipartListUploadsRequest.Input
    ) -> MultipartListUploadsResponse:
        """List all multipart uploads"""
        return await RenterdBaseResolver.handle_api_call(info, "list_multipart_uploads", req=req)

    @strawberry.field
    async def multipart_upload(self, info: Info, id: str) -> MultipartUpload:
        return await RenterdBaseResolver.handle_api_call(info, "get_multipart_upload", id=id)

    @strawberry.field
    async def autopilots(self, info: Info) -> List[Autopilot]:
        return await RenterdBaseResolver.handle_api_call(info, "get_autopilots")

    @strawberry.field
    async def buckets(self, info: Info) -> List[Bucket]:
        return await RenterdBaseResolver.handle_api_call(info, "get_buckets")

    @strawberry.field
    async def bucket(self, info: Info, name: str) -> Bucket:
        return await RenterdBaseResolver.handle_api_call(info, "get_bucket", name=name)

    @strawberry.field
    async def consensus_state(self, info: Info) -> ConsensusState:
        return await RenterdBaseResolver.handle_api_call(info, "get_consensus_state")

    @strawberry.field
    async def contracts(self, info: Info, contract_set: Optional[str] = None) -> List[ContractMetadata]:
        return await RenterdBaseResolver.handle_api_call(info, "get_contracts", contract_set=contract_set)

    @strawberry.field
    async def contract(self, info: Info, id: FileContractID) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "get_contract", id=id)

    @strawberry.field
    async def contract_size(self, info: Info, id: FileContractID) -> ContractSize:
        return await RenterdBaseResolver.handle_api_call(info, "get_contract_size", id=id)

    @strawberry.field
    async def get_hosts(
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
    async def hosts_allowlist(self, info: Info) -> List[PublicKey]:
        return await RenterdBaseResolver.handle_api_call(info, "get_hosts_allowlist")

    @strawberry.field
    async def hosts_blocklist(self, info: Info) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(info, "get_hosts_blocklist")

    @strawberry.field
    async def host(self, info: Info, public_key: PublicKey) -> Host:
        return await RenterdBaseResolver.handle_api_call(info, "get_host", public_key=public_key)

    @strawberry.field
    async def search_hosts(self, info: Info, req: SearchHostsRequest.Input) -> List[Host]:
        return await RenterdBaseResolver.handle_api_call(info, "search_hosts", req=req)

    @strawberry.field
    async def object(self, info: Info, path: str, bucket: Optional[str] = None, only_metadata: bool = False) -> Object:
        return await RenterdBaseResolver.handle_api_call(
            info, "get_object", path=path, bucket=bucket, only_metadata=only_metadata
        )

    @strawberry.field
    async def search_objects(
        self, info: Info, key: str, bucket: str = "default", offset: int = 0, limit: int = -1
    ) -> List[ObjectMetadata]:
        return await RenterdBaseResolver.handle_api_call(
            info, "search_objects", key=key, bucket=bucket, offset=offset, limit=limit
        )

    @strawberry.field
    async def objects_stats(self, info: Info) -> ObjectsStatsResponse:
        return await RenterdBaseResolver.handle_api_call(info, "get_objects_stats")

    @strawberry.field
    async def slab_buffers(self, info: Info) -> List[SlabBuffer]:
        return await RenterdBaseResolver.handle_api_call(info, "get_slab_buffers")

    @strawberry.field
    async def wallet(self, info: Info) -> WalletResponse:
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet")

    @strawberry.field
    async def webhooks(self, info: Info) -> WebhookResponse:
        return await RenterdBaseResolver.handle_api_call(info, "get_webhooks")

    @strawberry.field
    async def gouging_params(self, info: Info) -> GougingParams:
        return await RenterdBaseResolver.handle_api_call(info, "get_gouging_params")

    @strawberry.field
    async def upload_params(self, info: Info) -> UploadParams:
        return await RenterdBaseResolver.handle_api_call(info, "get_upload_params")

    @strawberry.field
    async def consensus_siafund_fee(self, info: Info, payout: Currency) -> Currency:
        return await RenterdBaseResolver.handle_api_call(info, "get_consensus_siafund_fee", payout=payout)

    @strawberry.field
    async def contract_sets(self, info: Info) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(info, "get_contract_sets")

    @strawberry.field
    async def contract_roots(self, info: Info, id: FileContractID) -> ContractRootsResponse:
        return await RenterdBaseResolver.handle_api_call(info, "get_contract_roots", id=id)

    @strawberry.field
    async def contract_ancestors(self, info: Info, id: FileContractID, min_start_height: int) -> List[ArchivedContract]:
        return await RenterdBaseResolver.handle_api_call(
            info, "get_contract_ancestors", id=id, min_start_height=min_start_height
        )

    @strawberry.field
    async def contracts_prunable(self, info: Info) -> ContractsPrunableDataResponse:
        return await RenterdBaseResolver.handle_api_call(info, "get_contracts_prunable")

    @strawberry.field
    async def hosts_scanning(
        self, info: Info, last_scan: Optional[str] = None, offset: int = 0, limit: int = -1
    ) -> List[HostAddress]:
        return await RenterdBaseResolver.handle_api_call(
            info, "get_hosts_scanning", last_scan=last_scan, offset=offset, limit=limit
        )

    @strawberry.field
    async def metric(
        self, info: Info, key: str, start: str, n: int, interval: str
    ) -> JSON:  # Response type varies based on metric type
        return await RenterdBaseResolver.handle_api_call(
            info, "get_metric", key=key, start=start, n=n, interval=interval
        )

    @strawberry.field
    async def settings(self, info: Info) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(info, "get_settings")

    @strawberry.field
    async def setting(self, info: Info, key: str) -> str:
        return await RenterdBaseResolver.handle_api_call(info, "get_setting", key=key)

    @strawberry.field
    async def slab(self, info: Info, key: str) -> Slab:
        return await RenterdBaseResolver.handle_api_call(info, "get_slab", key=key)

    @strawberry.field
    async def slab_objects(self, info: Info, key: str) -> List[ObjectMetadata]:
        return await RenterdBaseResolver.handle_api_call(info, "get_slab_objects", key=key)

    @strawberry.field
    async def slabs_partial(self, info: Info, key: str, offset: int, length: int) -> str:
        return await RenterdBaseResolver.handle_api_call(
            info, "get_slabs_partial", key=key, offset=offset, length=length
        )

    @strawberry.field
    async def syncer_address(self, info: Info) -> str:
        return await RenterdBaseResolver.handle_api_call(info, "get_syncer_address")

    @strawberry.field
    async def syncer_peers(self, info: Info) -> List[str]:
        return await RenterdBaseResolver.handle_api_call(info, "get_syncer_peers")

    @strawberry.field
    async def txpool_recommended_fee(self, info: Info) -> Currency:
        return await RenterdBaseResolver.handle_api_call(info, "get_txpool_recommended_fee")

    @strawberry.field
    async def txpool_transactions(self, info: Info) -> List[Transaction]:
        return await RenterdBaseResolver.handle_api_call(info, "get_txpool_transactions")

    @strawberry.field
    async def wallet_outputs(self, info: Info) -> List[SiacoinElement]:
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_outputs")

    @strawberry.field
    async def wallet_pending(self, info: Info) -> List[Transaction]:
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_pending")

    @strawberry.field
    async def wallet_transactions(self, info: Info, offset: int = 0, limit: int = -1) -> List[Transaction]:
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_transactions", offset=offset, limit=limit)


@strawberry.type
class BusMutations:
    @strawberry.mutation
    async def update_autopilot_host_check(
        self, info: Info, autopilot_id: str, host_key: PublicKey, check: HostCheck.Input
    ) -> bool:
        await RenterdBaseResolver.handle_api_call(
            info, "update_autopilot_host_check", autopilot_id=autopilot_id, host_key=host_key, check=check
        )
        return True

    @strawberry.mutation
    async def fund_account(self, info: Info, req: AccountsFundRequest.Input) -> AccountsFundResponse:
        return await RenterdBaseResolver.handle_api_call(info, "fund_account", req=req)

    @strawberry.mutation
    async def save_accounts(self, info: Info, req: AccountsSaveRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "save_accounts", req=req)
        return True

    @strawberry.mutation
    async def dismiss_alerts(self, info: Info, ids: List[Hash256]) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "dismiss_alerts", ids=ids)
        return True

    @strawberry.mutation
    async def register_alert(self, info: Info, alert: Alert.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "register_alert", alert=alert)
        return True

    @strawberry.mutation
    async def update_autopilot(self, info: Info, id: str, autopilot: Autopilot.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_autopilot", id=id, autopilot=autopilot)
        return True

    @strawberry.mutation
    async def create_bucket(self, info: Info, req: BucketCreateRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "create_bucket", req=req)
        return True

    @strawberry.mutation
    async def delete_bucket(self, info: Info, name: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_bucket", name=name)
        return True

    @strawberry.mutation
    async def update_contract_set(self, info: Info, set_name: str, req: ContractSetUpdateRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_contract_set", set_name=set_name, req=req)
        return True

    @strawberry.mutation
    async def delete_contract_set(self, info: Info, set_name: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_contract_set", set_name=set_name)
        return True

    @strawberry.mutation
    async def acquire_contract(
        self, info: Info, id: FileContractID, req: ContractAcquireRequest.Input
    ) -> ContractAcquireResponse:
        return await RenterdBaseResolver.handle_api_call(info, "acquire_contract", id=id, req=req)

    @strawberry.mutation
    async def keepalive_contract(self, info: Info, id: FileContractID, req: ContractKeepaliveRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "keepalive_contract", id=id, req=req)
        return True

    @strawberry.mutation
    async def release_contract(self, info: Info, id: FileContractID, lock_id: int) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "release_contract", id=id, lock_id=lock_id)
        return True

    @strawberry.mutation
    async def prune_contract(
        self, info: Info, id: FileContractID, req: ContractPruneRequest.Input
    ) -> ContractPruneResponse:
        return await RenterdBaseResolver.handle_api_call(info, "prune_contract", id=id, req=req)

    @strawberry.mutation
    async def renew_contract(self, info: Info, id: FileContractID, req: ContractRenewRequest.Input) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "renew_contract", id=id, req=req)

    @strawberry.mutation
    async def add_renewed_contract(
        self, info: Info, id: FileContractID, req: ContractRenewedRequest.Input
    ) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "add_renewed_contract", id=id, req=req)

    @strawberry.mutation
    async def add_contract(self, info: Info, id: FileContractID, req: ContractAddRequest.Input) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "add_contract", id=id, req=req)

    @strawberry.mutation
    async def archive_contracts(self, info: Info, req: ContractsArchiveRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "archive_contracts", req=req)
        return True

    @strawberry.mutation
    async def record_contract_spending(self, info: Info, records: List[ContractSpendingRecord.Input]) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "record_contract_spending", records=records)
        return True

    @strawberry.mutation
    async def update_hosts_allowlist(self, info: Info, req: UpdateAllowlistRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_hosts_allowlist", req=req)
        return True

    @strawberry.mutation
    async def delete_contract(self, info: Info, id: FileContractID) -> bool:
        """Delete a contract by ID"""
        await RenterdBaseResolver.handle_api_call(info, "delete_contract", id=id)
        return True

    @strawberry.mutation
    async def update_hosts_blocklist(self, info: Info, req: UpdateBlocklistRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_hosts_blocklist", req=req)
        return True

    @strawberry.mutation
    async def record_hosts_scan(self, info: Info, req: HostsScanRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "record_hosts_scan", req=req)
        return True

    @strawberry.mutation
    async def record_price_tables(self, info: Info, req: HostsPriceTablesRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "record_price_tables", req=req)
        return True

    @strawberry.mutation
    async def add_object(self, info: Info, path: str, req: AddObjectRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "add_object", path=path, req=req)
        return True

    @strawberry.mutation
    async def copy_object(self, info: Info, req: CopyObjectsRequest.Input) -> ObjectMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "copy_object", req=req)

    @strawberry.mutation
    async def delete_object(self, info: Info, path: str, bucket: Optional[str] = None, batch: bool = False) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_object", path=path, bucket=bucket, batch=batch)
        return True

    @strawberry.mutation
    async def rename_object(self, info: Info, req: ObjectsRenameRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "rename_object", req=req)
        return True

    @strawberry.mutation
    async def list_objects(self, info: Info, req: ObjectsListRequest.Input) -> ObjectsListResponse:
        return await RenterdBaseResolver.handle_api_call(info, "list_objects", req=req)

    @strawberry.mutation
    async def create_multipart_upload(self, info: Info, req: MultipartCreateRequest.Input) -> MultipartCreateResponse:
        return await RenterdBaseResolver.handle_api_call(info, "create_multipart_upload", req=req)

    @strawberry.mutation
    async def abort_multipart_upload(self, info: Info, req: MultipartAbortRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "abort_multipart_upload", req=req)
        return True

    @strawberry.mutation
    async def complete_multipart_upload(
        self, info: Info, req: MultipartCompleteRequest.Input
    ) -> MultipartCompleteResponse:
        return await RenterdBaseResolver.handle_api_call(info, "complete_multipart_upload", req=req)

    @strawberry.mutation
    async def add_multipart_part(self, info: Info, req: MultipartAddPartRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "add_multipart_part", req=req)
        return True

    @strawberry.mutation
    async def form_contract(self, info: Info, req: ContractFormRequest.Input) -> ContractMetadata:
        return await RenterdBaseResolver.handle_api_call(info, "form_contract", req=req)

    @strawberry.mutation
    async def fetch_packed_slabs(self, info: Info, req: PackedSlabsRequestGET.Input) -> List[PackedSlab]:
        return await RenterdBaseResolver.handle_api_call(info, "fetch_packed_slabs", req=req)

    @strawberry.mutation
    async def mark_packed_slabs_uploaded(self, info: Info, req: PackedSlabsRequestPOST.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "mark_packed_slabs_uploaded", req=req)
        return True

    @strawberry.mutation
    async def delete_host_sector(self, info: Info, host_key: PublicKey, root: Hash256) -> int:
        return await RenterdBaseResolver.handle_api_call(info, "delete_host_sector", host_key=host_key, root=root)

    @strawberry.mutation
    async def wallet_fund(self, info: Info, req: WalletFundRequest.Input) -> WalletFundResponse:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_fund", req=req)

    @strawberry.mutation
    async def wallet_redistribute(self, info: Info, req: WalletRedistributeRequest.Input) -> List[FileContractID]:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_redistribute", req=req)

    @strawberry.mutation
    async def wallet_send_siacoins(self, info: Info, req: WalletSendRequest.Input) -> TransactionID:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_send_siacoins", req=req)

    @strawberry.mutation
    async def wallet_sign_transaction(self, info: Info, req: WalletSignRequest.Input) -> Transaction:
        return await RenterdBaseResolver.handle_api_call(info, "wallet_sign_transaction", req=req)

    @strawberry.mutation
    async def wallet_discard_transaction(self, info: Info, transaction: Transaction.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "wallet_discard_transaction", transaction=transaction)
        return True

    @strawberry.mutation
    async def register_webhook(self, info: Info, webhook: Webhook.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "register_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def delete_webhook(self, info: Info, webhook: Webhook.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def broadcast_action(self, info: Info, event: WebhookEvent.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "broadcast_action", event=event)
        return True

    @strawberry.mutation
    async def refresh_health(self, info: Info) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "refresh_health")
        return True

    @strawberry.mutation
    async def update_setting(self, info: Info, key: str, value: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_setting", key=key, value=value)
        return True

    @strawberry.mutation
    async def delete_setting(self, info: Info, key: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_setting", key=key)
        return True

    @strawberry.mutation
    async def sync_connect(self, info: Info, addr: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "sync_connect", addr=addr)
        return True

    @strawberry.mutation
    async def txpool_broadcast(self, info: Info, transactions: List[Transaction.Input]) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "txpool_broadcast", transactions=transactions)
        return True

    @strawberry.mutation
    async def consensus_accept_block(self, info: Info, block: Block.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "consensus_accept_block", block=block)
        return True

    @strawberry.mutation
    async def update_bucket_policy(self, info: Info, name: str, policy: BucketPolicy.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_bucket_policy", name=name, policy=policy)
        return True

    @strawberry.mutation
    async def delete_contracts_all(self, info: Info) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_contracts_all")
        return True

    @strawberry.mutation
    async def contract_broadcast(self, info: Info, id: FileContractID) -> TransactionID:
        return await RenterdBaseResolver.handle_api_call(info, "contract_broadcast", id=id)

    @strawberry.mutation
    async def hosts_reset_lost_sectors(self, info: Info, hostkey: PublicKey) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "hosts_reset_lost_sectors", hostkey=hostkey)
        return True

    @strawberry.mutation
    async def hosts_remove(self, info: Info, req: HostsRemoveRequest.Input) -> int:
        return await RenterdBaseResolver.handle_api_call(
            info,
            "hosts_remove",
            req=req,
        )

    @strawberry.mutation
    async def add_slabs_partial(
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
    async def update_metric(self, info: Info, key: str, data: JSON) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_metric", key=key, data=data)
        return True

    @strawberry.mutation
    async def delete_metric(self, info: Info, key: str, cutoff: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "delete_metric", key=key, cutoff=cutoff)
        return True

    @strawberry.mutation
    async def slabs_migration(self, info: Info, req: MigrationSlabsRequest.Input) -> UnhealthySlabsResponse:
        return await RenterdBaseResolver.handle_api_call(info, "slabs_migration", req=req)

    @strawberry.mutation
    async def update_slab(self, info: Info, slab: Slab.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "update_slab", slab=slab)
        return True

    @strawberry.mutation
    async def upload_track(self, info: Info, id: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "upload_track", id=id)
        return True

    @strawberry.mutation
    async def upload_add_sector(self, info: Info, id: str, req: UploadSectorRequest.Input) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "upload_add_sector", req=req)
        return True

    @strawberry.mutation
    async def upload_finished(self, info: Info, id: str) -> bool:
        await RenterdBaseResolver.handle_api_call(info, "upload_finished", id=id)
        return True
