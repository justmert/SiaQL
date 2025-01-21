import strawberry
from typing import List
from strawberry.types import Info

from siaql.graphql.schemas.types import UpdateAllowlistRequest
from ....types import *
from ...resolvers.renterd import RenterdBaseResolver


@strawberry.type
class BusQueries(RenterdBaseResolver):
    @strawberry.field
    async def accounts(self, info: Info, owner: str) -> List[Account]:
        """Get all accounts"""
        return await RenterdBaseResolver.handle_api_call(info, "get_accounts", owner=owner)

    @strawberry.mutation
    async def post_account(self, info: Info, account_id: str, host_key: PublicKey) -> bool:
        """Add or update an account"""
        await self.handle_api_call(info, "post_account", account_id=account_id, hostKey=host_key)
        return True

    @strawberry.mutation
    async def lock_account(
        self, info: Info, account_id: str, host_key: PublicKey, exclusive: bool, duration: DurationMS
    ) -> AccountsLockHandlerResponse:
        """Lock an account"""
        return await self.handle_api_call(
            info, "lock_account", account_id=account_id, hostKey=host_key, exclusive=exclusive, duration=duration
        )

    @strawberry.mutation
    async def unlock_account(self, info: Info, account_id: str, lock_id: int) -> bool:
        """Unlock an account"""
        await self.handle_api_call(info, "unlock_account", account_id=account_id, lockID=lock_id)
        return True

    @strawberry.mutation
    async def add_account_balance(self, info: Info, account_id: str, request: AccountsAddBalanceRequest) -> bool:
        """Add balance to an account"""
        await self.handle_api_call(info, "add_account_balance", account_id=account_id, request=request)
        return True

    @strawberry.mutation
    async def update_account_balance(self, info: Info, account_id: str, request: AccountsUpdateBalanceRequest) -> bool:
        """Update account balance"""
        await self.handle_api_call(info, "update_account_balance", account_id=account_id, request=request)
        return True

    @strawberry.mutation
    async def requires_sync_account(self, info: Info, account_id: str, request: AccountsRequiresSyncRequest) -> bool:
        """Mark account as requiring sync"""
        await self.handle_api_call(info, "requires_sync_account", account_id=account_id, request=request)
        return True

    @strawberry.mutation
    async def reset_drift_account(self, info: Info, account_id: str) -> bool:
        """Reset account drift"""
        await self.handle_api_call(info, "reset_drift_account", account_id=account_id)
        return True

    @strawberry.field
    async def alerts(self, info: Info, severity: str, offset: int, limit: int) -> AlertsResponse:
        """Get alerts"""
        return await RenterdBaseResolver.handle_api_call(
            info, "get_alerts", severity=severity, offset=offset, limit=limit
        )

    @strawberry.mutation
    async def dismiss_alerts(self, info: Info, ids: List[Hash256]) -> bool:
        """Dismiss alerts"""
        await RenterdBaseResolver.handle_api_call(info, "dismiss_alerts", ids=ids)
        return True

    @strawberry.mutation
    async def register_alert(self, info: Info, alert: Alert) -> bool:
        """Register alert"""
        await RenterdBaseResolver.handle_api_call(info, "register_alert", alert=alert)
        return True

    @strawberry.field
    async def buckets(self, info: Info) -> List[Bucket]:
        """Get all buckets"""
        return await RenterdBaseResolver.handle_api_call(info, "get_buckets")

    @strawberry.mutation
    async def create_bucket(self, info: Info, name: str, policy: BucketPolicy) -> bool:
        """Create a new bucket"""
        await RenterdBaseResolver.handle_api_call(info, "create_bucket", name=name, policy=policy)
        return True

    @strawberry.mutation
    async def get_bucket(self, info: Info, name: str) -> Bucket:
        """Returns a bucket with the given name"""
        await RenterdBaseResolver.handle_api_call(info, "get_bucket", name=name)
        return True

    @strawberry.mutation
    async def delete_bucket(self, info: Info, name: str) -> bool:
        """Delete a bucket"""
        await RenterdBaseResolver.handle_api_call(info, "delete_bucket", name=name)
        return True

    @strawberry.mutation
    async def update_bucket_policy(self, info: Info, name: str, policy: BucketPolicy) -> bool:
        """Update bucket policy"""
        await RenterdBaseResolver.handle_api_call(info, "update_bucket_policy", name=name, policy=policy)
        return True

    @strawberry.mutation
    async def accept_block(self, info: Info, block: Block) -> bool:
        """Accept block"""
        await RenterdBaseResolver.handle_api_call(info, "accept_block", block=block)
        return True

    @strawberry.field
    async def consensus_state(self, info: Info) -> ConsensusState:
        """Get consensus state"""
        return await RenterdBaseResolver.handle_api_call(info, "get_consensus_state")

    @strawberry.field
    async def consensus_siafundfee(self, info: Info, payout: Currency) -> Currency:
        """Get siafund fee for a given payout"""
        return await self.handle_api_call(info, "get_consensus_siafundfee", payout=payout)

    @strawberry.field
    async def contract(self, info: Info, id: str) -> ContractMetadata:
        """Get contract by ID"""
        return await RenterdBaseResolver.handle_api_call(info, "get_contract", id=id)

    @strawberry.mutation
    async def delete_contract(self, info: Info, contract_id: str) -> bool:
        """Delete a contract"""
        await RenterdBaseResolver.handle_api_call(info, "delete_contract", contract_id=contract_id)
        return True

    @strawberry.mutation
    async def post_contract(self, info: Info, contract_id: str, contract: ContractAddRequest) -> bool:
        """Add a contract to the bus"""
        await self.handle_api_call(info, "post_contract", contract_id=contract_id, contract=contract)
        return True

    @strawberry.mutation
    async def acquire_contract(
        self, info: Info, contract_id: str, duration: DurationMS, priority: int
    ) -> ContractAcquireResponse:
        """Acquire contract"""
        return await RenterdBaseResolver.handle_api_call(
            info, "acquire_contract", contract_id=contract_id, duration=duration, priority=priority
        )

    @strawberry.mutation
    async def post_contract_keepalive(self, info: Info, contract_id: str, request: ContractKeepaliveRequest) -> bool:
        """Extend duration on an already acquired lock"""
        await self.handle_api_call(info, "post_contract_keepalive", contract_id=contract_id, request=request)
        return True

    @strawberry.field
    async def contract_ancestors(self, info: Info, contract_id: str, min_start_height: int) -> List[ContractMetadata]:
        """Get contract ancestors"""
        return await RenterdBaseResolver.handle_api_call(
            info, "contract_ancestors", contract_id=contract_id, min_start_height=min_start_height
        )

    @strawberry.mutation
    async def release_contract(self, info: Info, contract_id: str, lock_id: int) -> bool:
        """Release contract"""
        await RenterdBaseResolver.handle_api_call(info, "release_contract", contract_id=contract_id, lock_id=lock_id)
        return True

    @strawberry.field
    async def contract_roots(self, info: Info, contract_id: str) -> List[Hash256]:
        """Get contract roots"""
        return await RenterdBaseResolver.handle_api_call(info, "get_contract_roots", contract_id=contract_id)

    @strawberry.field
    async def contract_size(self, info: Info, contract_id: str) -> ContractSize:
        """Get contract size"""
        return await self.handle_api_call(info, "get_contract_size", contract_id=contract_id)

    @strawberry.field
    async def contracts(self, info: Info, filter_mode: str = "active") -> List[ContractMetadata]:
        """Get contracts"""
        return await RenterdBaseResolver.handle_api_call(info, "get_contracts", filter_mode=filter_mode)

    @strawberry.mutation
    async def archive_contracts(self, info: Info, to_archive: Dict[FileContractID, str]) -> bool:
        """Archive contracts"""
        await self.handle_api_call(info, "post_contracts_archive", to_archive=to_archive)
        return True

    @strawberry.mutation
    async def delete_all_contracts(self, info: Info) -> bool:
        """Delete all contracts"""
        await self.handle_api_call(info, "delete_contracts_all")
        return True

    @strawberry.field
    async def contracts_prunable(self, info: Info) -> ContractsPrunableDataResponse:
        """Get prunable contracts data"""
        return await self.handle_api_call(info, "get_contracts_prunable")

    @strawberry.field
    async def contracts_renewed(self, info: Info, contract_id: str) -> ContractMetadata:
        """Get renewed contract"""
        return await self.handle_api_call(info, "get_contracts_renewed", contract_id=contract_id)

    @strawberry.mutation
    async def put_contract_set(self, info: Info, set_name: str, contract_ids: List[FileContractID]) -> bool:
        """Create a new contract set"""
        await self.handle_api_call(info, "put_contracts_set", set_name=set_name, contract_ids=contract_ids)
        return True

    @strawberry.mutation
    async def delete_contract_set(self, info: Info, set_name: str) -> bool:
        """Delete a contract set"""
        await self.handle_api_call(info, "delete_contracts_set", set_name=set_name)
        return True

    @strawberry.field
    async def contracts_sets(self, info: Info) -> List[str]:
        """Get all contract set names"""
        return await self.handle_api_call(info, "get_contracts_sets")

    @strawberry.mutation
    async def record_contract_spending(self, info: Info, records: List[ContractSpendingRecord]) -> bool:
        """Record contract spending"""
        await self.handle_api_call(info, "post_contracts_spending", records=records)
        return True

    @strawberry.field
    async def host(self, info: Info, pubkey: str) -> Host:
        """Get host information"""
        return await RenterdBaseResolver.handle_api_call(info, "get_host", pubkey=pubkey)

    @strawberry.mutation
    async def reset_lost_sectors(self, info: Info, pubkey: str) -> bool:
        """Reset lost sectors for a host"""
        await RenterdBaseResolver.handle_api_call(info, "reset_lost_sectors", pubkey=pubkey)
        return True

    @strawberry.field
    async def hosts(self, info: Info, offset: int = 0, limit: int = -1) -> List[Host]:
        """Get list of hosts"""
        return await RenterdBaseResolver.handle_api_call(info, "get_hosts", offset=offset, limit=limit)

    @strawberry.field
    async def hosts_allowlist(self, info: Info) -> List[PublicKey]:
        """Get hosts allowlist"""
        return await self.handle_api_call(info, "get_hosts_allowlist")

    @strawberry.mutation
    async def update_hosts_allowlist(self, info: Info, request: UpdateAllowlistRequest) -> bool:
        """Update hosts allowlist"""
        await self.handle_api_call(info, "update_hosts_allowlist", request=request)
        return True

    @strawberry.field
    async def hosts_blocklist(self, info: Info) -> List[str]:
        """Get hosts blocklist"""
        return await self.handle_api_call(info, "get_hosts_blocklist")

    @strawberry.mutation
    async def update_hosts_blocklist(self, info: Info, request: UpdateBlocklistRequest) -> bool:
        """Update hosts blocklist"""
        await self.handle_api_call(info, "update_hosts_blocklist", request=UpdateBlocklistRequest)
        return True

    @strawberry.mutation
    async def record_hosts_interactions(self, info: Info, interactions: List[HostScan]) -> bool:
        """Record host interactions"""
        await self.handle_api_call(info, "post_hosts_interactions", interactions=interactions)
        return True

    @strawberry.mutation
    async def remove_hosts(self, info: Info, request: HostsRemoveRequest) -> int:
        """Remove offline hosts"""
        return await RenterdBaseResolver.handle_api_call(info, "remove_hosts", request=request)

    @strawberry.field
    async def metrics(self, info: Info, key: str, start: str, n: int, interval: str) -> Any:
        """Get metrics"""
        return await RenterdBaseResolver.handle_api_call(
            info, "get_metrics", key=key, start=start, n=n, interval=interval
        )

    @strawberry.mutation
    async def delete_metrics(self, info: Info, key: str, cutoff: str) -> bool:
        """Delete metrics"""
        await RenterdBaseResolver.handle_api_call(info, "delete_metrics", key=key, cutoff=cutoff)
        return True

    @strawberry.field
    async def hosts_scanning(self, info: Info, offset: int, limit: int, last_scan: str) -> List[Host]:
        """Get hosts for scanning"""
        return await self.handle_api_call(info, "get_hosts_scanning", offset=offset, limit=limit, last_scan=last_scan)

    @strawberry.mutation
    async def abort_multipart_upload(self, info: Info, request: MultipartAbortRequest) -> bool:
        """Abort multipart upload"""
        await RenterdBaseResolver.handle_api_call(info, "abort_multipart_upload", request=request)
        return True

    @strawberry.mutation
    async def complete_multipart_upload(
        self, info: Info, request: MultipartCompleteRequest
    ) -> MultipartCompleteResponse:
        """Complete multipart upload"""
        return await RenterdBaseResolver.handle_api_call(info, "complete_multipart_upload", request=request)

    @strawberry.mutation
    async def create_multipart_upload(self, info: Info, request: MultipartCreateRequest) -> MultipartCreateResponse:
        """Create multipart upload"""
        return await RenterdBaseResolver.handle_api_call(info, "create_multipart_upload", request=request)

    @strawberry.mutation
    async def list_multipart_upload_parts(
        self, info: Info, request: MultipartListPartsRequest
    ) -> MultipartListPartsResponse:
        """List multipart upload parts"""
        return await RenterdBaseResolver.handle_api_call(info, "list_multipart_upload_parts", request=request)

    @strawberry.mutation
    async def list_multipart_uploads(
        self, info: Info, request: MultipartListUploadsRequest
    ) -> MultipartListUploadsResponse:
        """List multipart uploads"""
        return await RenterdBaseResolver.handle_api_call(info, "list_multipart_uploads", request=request)

    @strawberry.mutation
    async def upload_part(self, info: Info, request: MultipartAddPartRequest) -> bool:
        """Upload a part of a multipart upload"""
        return await RenterdBaseResolver.handle_api_call(info, "put_multipart_part", request=request)

    # Object endpoints
    @strawberry.field
    async def get_object(self, info: Info, key: str) -> Object:
        """Get object metadata"""
        return await RenterdBaseResolver.handle_api_call(info, "get_object", key=key)

    @strawberry.mutation
    async def put_object(self, info: Info, key: str, request: AddObjectRequest) -> bool:
        """Store object metadata"""
        await RenterdBaseResolver.handle_api_call(info, "put_object", key=key, request=request)
        return True

    @strawberry.mutation
    async def delete_object(self, info: Info, key: str) -> bool:
        """Delete object"""
        await RenterdBaseResolver.handle_api_call(info, "delete_object", key=key)
        return True

    @strawberry.mutation
    async def copy_object(self, info: Info, request: CopyObjectsRequest) -> ObjectMetadata:
        """Copy object"""
        return await RenterdBaseResolver.handle_api_call(info, "post_objects_copy", request=request)

    @strawberry.field
    async def list_objects(self, info: Info, request: ObjectsListRequest) -> ObjectsResponse:
        """List objects"""
        return await RenterdBaseResolver.handle_api_call(info, "post_objects_list", request=request)

    @strawberry.mutation
    async def rename_objects(self, info: Info, request: ObjectsRenameRequest) -> bool:
        """Rename objects"""
        await RenterdBaseResolver.handle_api_call(info, "post_objects_rename", request=request)
        return True

    @strawberry.field
    async def download_params(self, info: Info) -> DownloadParams:
        """Get download parameters"""
        return await RenterdBaseResolver.handle_api_call(info, "get_download_params")

    @strawberry.field
    async def gouging_params(self, info: Info) -> GougingParams:
        """Get gouging parameters"""
        return await RenterdBaseResolver.handle_api_call(info, "get_gouging_params")

    @strawberry.field
    async def upload_params(self, info: Info) -> UploadParams:
        """Get upload parameters"""
        return await RenterdBaseResolver.handle_api_call(info, "get_upload_params")

    @strawberry.field
    async def search_objects(self, info: Info, bucket: str, key: str, offset: int, limit: int) -> List[str]:
        """Search objects"""
        return await self.handle_api_call(
            info, "get_search_objects", bucket=bucket, key=key, offset=offset, limit=limit
        )

    @strawberry.field
    async def settings(self, info: Info) -> List[str]:
        """Get all available settings keys"""
        return await self.handle_api_call(info, "get_settings")

    @strawberry.field
    async def setting(self, info: Info, key: str) -> Any:
        """Get setting for specific key"""
        return await self.handle_api_call(info, "get_setting", key=key)

    @strawberry.mutation
    async def update_setting(self, info: Info, key: str, value: Any) -> bool:
        """Update setting"""
        await self.handle_api_call(info, "put_setting", key=key, value=value)
        return True

    @strawberry.mutation
    async def delete_setting(self, info: Info, key: str) -> bool:
        """Delete setting"""
        await self.handle_api_call(info, "delete_setting", key=key)
        return True

    @strawberry.field
    async def slabs_for_migration(self, info: Info, request: MigrationSlabsRequest) -> SlabsForMigrationResponse:
        """Get slabs for migration"""
        return await RenterdBaseResolver.handle_api_call(info, "get_slabs_for_migration", request=request)

    @strawberry.field
    async def get_partial_slab(self, info: Info, key: EncryptionKey, offset: int, length: int) -> bytes:
        """Get a partial slab"""
        return await RenterdBaseResolver.handle_api_call(
            info, "get_partial_slab", key=key, offset=offset, length=length
        )

    @strawberry.mutation
    async def add_partial_slab(
        self, info: Info, data: bytes, min_shards: int, total_shards: int
    ) -> AddPartialSlabResponse:
        """Add a partial slab"""
        return await RenterdBaseResolver.handle_api_call(
            info, "add_partial_slab", data=data, min_shards=min_shards, total_shards=total_shards
        )

    @strawberry.field
    async def get_slab(self, info: Info, key: EncryptionKey) -> Slab:
        """Get slab by key"""
        return await RenterdBaseResolver.handle_api_call(info, "get_slab", key=key)

    @strawberry.field
    async def get_slab_objects(self, info: Info, key: str) -> SlabObjects:
        """Get objects associated with a slab"""
        return await RenterdBaseResolver.handle_api_call(info, "get_slab_objects", key=key)

    @strawberry.mutation
    async def update_slab(self, info: Info, key: str, sectors: List[UploadedSector]) -> bool:
        """Update a slab"""
        await RenterdBaseResolver.handle_api_call(info, "update_slab", key=key, sectors=sectors)
        return True

    @strawberry.mutation
    async def refresh_health(self, info: Info) -> bool:
        """Refresh slab health"""
        await RenterdBaseResolver.handle_api_call(info, "refresh_health")
        return True

    @strawberry.field
    async def state(self, info: Info) -> BusStateResponse:
        """Get bus state"""
        return await self.handle_api_call(info, "get_state")

    @strawberry.field
    async def stats_objects(self, info: Info) -> ObjectsStatsResponse:
        """Get object statistics"""
        return await self.handle_api_call(info, "get_stats_objects")

    @strawberry.field
    async def syncer_address(self, info: Info) -> str:
        """Get syncer address"""
        return await RenterdBaseResolver.handle_api_call(info, "get_syncer_address")

    @strawberry.mutation
    async def syncer_connect(self, info: Info, address: str) -> bool:
        """Connect to a peer"""
        await RenterdBaseResolver.handle_api_call(info, "post_syncer_connect", address=address)
        return True

    @strawberry.mutation
    async def broadcast_transaction(self, info: Info, transaction: List[Transaction]) -> bool:
        """Broadcast transaction"""
        await RenterdBaseResolver.handle_api_call(info, "post_txpool_broadcast", transaction=transaction)
        return True

    @strawberry.field
    async def recommended_fee(self, info: Info) -> Currency:
        """Get recommended transaction fee"""
        return await RenterdBaseResolver.handle_api_call(info, "get_txpool_recommendedfee")

    @strawberry.field
    async def txpool_transactions(self, info: Info) -> List[Transaction]:
        """Get transaction pool transactions"""
        return await RenterdBaseResolver.handle_api_call(info, "get_txpool_transactions")

    @strawberry.mutation
    async def track_upload(self, info: Info, upload_id: str) -> bool:
        """Track an upload"""
        await RenterdBaseResolver.handle_api_call(info, "track_upload", upload_id=upload_id)
        return True

    @strawberry.mutation
    async def finish_upload(self, info: Info, upload_id: str) -> bool:
        """Finish an upload"""
        await RenterdBaseResolver.handle_api_call(info, "finish_upload", upload_id=upload_id)
        return True

    @strawberry.mutation
    async def add_upload_sector(self, info: Info, upload_id: str, roots: List[Hash256]) -> bool:
        """Add sector to upload"""
        await RenterdBaseResolver.handle_api_call(info, "add_upload_sector", upload_id=upload_id, roots=roots)
        return True

    @strawberry.field
    async def wallet(self, info: Info) -> WalletResponse:
        """Get wallet information"""
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet")

    @strawberry.field
    async def wallet_address(self, info: Info) -> str:
        """Get wallet address"""
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_address")

    @strawberry.field
    async def wallet_balance(self, info: Info) -> Currency:
        """Get wallet balance"""
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_balance")

    @strawberry.field
    async def wallet_outputs(self, info: Info) -> List[SiacoinElement]:
        """Get wallet outputs"""
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_outputs")

    @strawberry.field
    async def wallet_pending(self, info: Info) -> List[Transaction]:
        """Get pending transactions"""
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_pending")

    @strawberry.field
    async def wallet_transactions(self, info: Info) -> List[Transaction]:
        """Get wallet transactions"""
        return await RenterdBaseResolver.handle_api_call(info, "get_wallet_transactions")

    @strawberry.mutation
    async def discard_transaction(self, info: Info, transaction: Transaction) -> bool:
        """Discard a transaction"""
        await RenterdBaseResolver.handle_api_call(info, "discard_transaction", transaction=transaction)
        return True

    @strawberry.mutation
    async def fund_wallet(self, info: Info, request: WalletFundRequest) -> WalletFundResponse:
        """Fund wallet"""
        return await RenterdBaseResolver.handle_api_call(info, "fund_wallet", request=request)

    @strawberry.mutation
    async def prepare_form_contract(self, info: Info, request: ContractFormRequest) -> RHPFormResponse:
        """Prepare contract formation"""
        return await RenterdBaseResolver.handle_api_call(info, "prepare_form_contract", request=request)

    @strawberry.mutation
    async def prepare_renew_contract(self, info: Info, request: ContractRenewRequest) -> RHPFormResponse:
        """Prepare contract renewal"""
        return await RenterdBaseResolver.handle_api_call(info, "prepare_renew_contract", request=request)

    @strawberry.mutation
    async def redistribute_wallet(self, info: Info, amount: Currency, outputs: int) -> List[TransactionID]:
        """Redistribute wallet"""
        return await RenterdBaseResolver.handle_api_call(info, "redistribute_wallet", amount=amount, outputs=outputs)

    @strawberry.mutation
    async def sign_transaction(self, info: Info, request: WalletSignRequest) -> Transaction:
        """Sign a transaction"""
        return await RenterdBaseResolver.handle_api_call(info, "sign_transaction", request=request)

    @strawberry.field
    async def webhooks(self, info: Info) -> WebhookResponse:
        """Get all webhooks"""
        return await RenterdBaseResolver.handle_api_call(info, "get_webhooks")

    @strawberry.mutation
    async def register_webhook(self, info: Info, webhook: Webhook) -> bool:
        """Register webhook"""
        await RenterdBaseResolver.handle_api_call(info, "register_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def delete_webhook(self, info: Info, webhook: Webhook) -> bool:
        """Delete webhook"""
        await RenterdBaseResolver.handle_api_call(info, "delete_webhook", webhook=webhook)
        return True

    @strawberry.mutation
    async def broadcast_webhook_action(self, info: Info, action: Event) -> bool:
        """Broadcast webhook action"""
        await RenterdBaseResolver.handle_api_call(info, "broadcast_webhook_action", action=action)
        return True
