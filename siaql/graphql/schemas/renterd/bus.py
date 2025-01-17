from typing import List, Optional
import strawberry
from strawberry.types import Info

from siaql.graphql.resolvers.renterd import RenterdBaseResolver

@strawberry.type
class Account:
    id: str
    host: str
    balance: float
    drift: float
    requires_sync: bool = strawberry.field(name="requiresSync")

@strawberry.type
class AccountLock:
    account: Account
    lock_id: int = strawberry.field(name="lockID")

@strawberry.type
class BusQueries:
    @strawberry.field
    async def accounts(self, info: Info) -> List[Account]:
        """Returns all known ephemeral accounts from the bus.
        
        Returns:
            List of accounts with their details including ID, host,
            balance, drift, and sync status.
        """
        def transform_accounts(data: List[dict]) -> List[Account]:
            return [
                Account(
                    id=account["id"],
                    host=account["host"],
                    balance=account["balance"],
                    drift=account["drift"],
                    requires_sync=account["requiresSync"]
                )
                for account in data
            ]
            
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_accounts",
            transform_accounts
        )

@strawberry.type
class BusMutations:
    @strawberry.mutation
    async def get_or_create_account(
        self,
        info: Info,
        account_id: str = strawberry.field(description="The ID of the account (ed25519 public key)"),
        host_key: str = strawberry.field(name="hostKey", description="The host's public key to attach to the account")
    ) -> Account:
        """Returns the account with the given ID or creates it if it doesn't exist."""
        def transform_account(data: dict) -> Account:
            return Account(
                id=data["id"],
                host=data["host"],
                balance=data["balance"],
                drift=data["drift"],
                requires_sync=data["requiresSync"]
            )
            
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_or_create_account",
            transform_account,
            account_id=account_id,
            host_key=host_key
        )

    @strawberry.mutation
    async def lock_account(
        self,
        info: Info,
        account_id: str = strawberry.field(description="The ID of the account (ed25519 public key)"),
        host_key: str = strawberry.field(name="hostKey", description="The host's public key"),
        exclusive: bool = strawberry.field(description="Whether to lock exclusively (required for syncing)"),
        duration: str = strawberry.field(description="Time in nanoseconds after which the account is unlocked automatically")
    ) -> AccountLock:
        """Locks an account either exclusively or not.
        
        Usually workers will deposit and withdraw from accounts with a regular lock
        but for syncing the account balance with hosts an exclusive lock is required.
        """
        def transform_lock(data: dict) -> AccountLock:
            return AccountLock(
                account=Account(
                    id=data["account"]["id"],
                    host=data["account"]["host"],
                    balance=data["account"]["balance"],
                    drift=data["account"]["drift"],
                    requires_sync=data["account"]["requiresSync"]
                ),
                lock_id=data["lockID"]
            )
            
        return await RenterdBaseResolver.handle_api_call(
            info,
            "lock_account",
            transform_lock,
            account_id=account_id,
            host_key=host_key,
            exclusive=exclusive,
            duration=duration
        )

    @strawberry.mutation
    async def unlock_account(
        self,
        info: Info,
        account_id: str = strawberry.field(description="The ID of the account (ed25519 public key)"),
        lock_id: int = strawberry.field(name="lockID", description="The lock ID returned when locking the account")
    ) -> bool:
        """Unlocks a previously locked account.
        
        This is the counterpart to the account locking endpoint. The lock id returned
        when locking an account can be used to unlock it again before the locking
        duration has passed and the account gets unlocked automatically.
        """
        await RenterdBaseResolver.handle_api_call(
            info,
            "unlock_account",
            None,
            account_id=account_id,
            lock_id=lock_id
        )
        return True

    @strawberry.mutation
    async def add_account_balance(
        self,
        info: Info,
        account_id: str = strawberry.field(description="The ID of the account (ed25519 public key)"),
        host_key: str = strawberry.field(name="hostKey", description="The host's public key"),
        amount: int = strawberry.field(description="Amount to add (positive) or withdraw (negative)")
    ) -> bool:
        """Deposits or withdraws tokens into/from an ephemeral account.
        
        The caller should hold a non-exclusive lock on the account.
        Use positive amount for deposits and negative amount for withdrawals.
        """
        await RenterdBaseResolver.handle_api_call(
            info,
            "add_account_balance",
            None,
            account_id=account_id,
            host_key=host_key,
            amount=amount
        )
        return True

    @strawberry.mutation
    async def update_account_balance(
        self,
        info: Info,
        account_id: str = strawberry.field(description="The ID of the account (ed25519 public key)"),
        host_key: str = strawberry.field(name="hostKey", description="The host's public key"),
        amount: int = strawberry.field(description="The new balance value to set")
    ) -> bool:
        """Updates the balance of an account to the provided value.
        
        The caller should acquire an exclusive lock before calling this endpoint.
        This endpoint is typically used for syncing account balances with hosts.
        """
        await RenterdBaseResolver.handle_api_call(
            info,
            "update_account_balance",
            None,
            account_id=account_id,
            host_key=host_key,
            amount=amount
        )
        return True

    @strawberry.mutation
    async def mark_account_for_sync(
        self,
        info: Info,
        account_id: str = strawberry.field(description="The ID of the account (ed25519 public key)"),
        host_key: str = strawberry.field(name="hostKey", description="The host's public key")
    ) -> bool:
        """Marks the account as requiring a balance sync.
        
        Usually set by workers when operations fail with an error indicating
        an insufficient balance. The autopilot (if enabled) will periodically
        check for accounts that require syncing and initiate the sync automatically.
        """
        await RenterdBaseResolver.handle_api_call(
            info,
            "mark_account_for_sync",
            None,
            account_id=account_id,
            host_key=host_key
        )
        return True


@strawberry.mutation
async def reset_account_drift(self, info: Info, id: str) -> bool:
    """Resets the drift on ephemeral accounts.
    
    The drift tracks by how much Siacoin the expected balance of `renterd` 
    differs from the host's over time. If the drift is too large, the autopilot 
    refuses to pour more money into a host's account. Resetting the drift will 
    cause the autopilot to fund the account again.
    
    Args:
        id: The id of the account for which to reset the drift
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "reset_account_drift",
        lambda _: True,
        id=id
    )
    return True


@strawberry.field
async def alerts(self, info: Info, params: Optional[AlertsParams] = None) -> List[Alert]:
    """Lists all currently registered alerts.
    
    Args:
        params: Optional pagination parameters
        
    Returns:
        List of alerts with their details
    """
    def transform_alerts(data: List[dict]) -> List[Alert]:
        return [
            Alert(
                id=alert["id"],
                severity=alert["severity"],
                message=alert["message"],
                data=AlertData(
                    account_id=alert["data"]["accountID"],
                    contract_id=alert["data"]["contractID"],
                    host_key=alert["data"]["hostKey"], 
                    origin=alert["data"]["origin"]
                ),
                timestamp=alert["timestamp"]
            )
            for alert in data
        ]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_alerts",
        transform_alerts,
        offset=params.offset if params else 0,
        limit=params.limit if params else -1
    )


@strawberry.mutation  
async def dismiss_alerts(self, info: Info, alert_ids: Optional[List[str]] = None, all: bool = False) -> bool:
    """Dismisses alerts with the given ids or all alerts.
    
    Args:
        alert_ids: List of alert IDs to dismiss
        all: If True, dismisses all alerts regardless of provided IDs
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "dismiss_alerts",
        lambda _: True,
        alert_ids=alert_ids,
        all=all
    )
    return True


@strawberry.mutation
async def register_alert(self, info: Info, alert: AlertInput) -> bool:
    """Registers a new alert.
    
    Usually called by workers and the autopilot. An alert requires a unique id, 
    severity (info|warning/error|critical) and a message that describes the reason.
    
    Args:
        alert: The alert details to register
        
    Returns:
        True if registration successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "register_alert",
        lambda _: True,
        alert=alert
    )
    return True


@strawberry.field
async def autopilots(self, info: Info) -> List[Autopilot]:
    """Returns all autopilot configurations stored in the bus.
    
    Returns:
        List of autopilot configurations
    """
    def transform_autopilots(data: List[dict]) -> List[Autopilot]:
        return [
            Autopilot(
                id=ap["id"],
                config=AutopilotConfig(
                    contracts=ContractConfig(**ap["config"]["contracts"]),
                    hosts=HostsConfig(**ap["config"]["hosts"]),
                    wallet=WalletConfig(**ap["config"]["wallet"])
                ),
                current_period=ap["currentPeriod"]
            )
            for ap in data
        ]
    
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_autopilots",
        transform_autopilots
    )

@strawberry.field
async def autopilot(self, info: Info, id: str) -> Autopilot:
    """Returns the autopilot configuration for a given id.
    
    Args:
        id: ID of the autopilot to return
        
    Returns:
        Autopilot configuration
    """
    def transform_autopilot(data: dict) -> Autopilot:
        return Autopilot(
            id=data["id"],
            config=AutopilotConfig(
                contracts=ContractConfig(**data["config"]["contracts"]),
                hosts=HostsConfig(**data["config"]["hosts"]),
                wallet=WalletConfig(**data["config"]["wallet"])
            ),
            current_period=data["currentPeriod"]
        )
    
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_autopilot",
        transform_autopilot,
        id=id
    )

@strawberry.mutation
async def update_autopilot(self, info: Info, id: str, config: AutopilotConfigInput) -> bool:
    """Updates an autopilot configuration.
    
    Args:
        id: ID of the autopilot to modify
        config: New configuration
        
    Returns:
        True if update successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_autopilot",
        lambda _: True,
        id=id,
        config=config
    )
    return True


@strawberry.field
async def contract(self, info: Info, id: str) -> Contract:
    """Returns contract metadata for an active contract.
    
    Args:
        id: Contract ID
        
    Returns:
        Contract metadata
    """
    def transform_contract(data: dict) -> Contract:
        return Contract(
            id=data["id"],
            host_ip=data["hostIP"],
            host_key=data["hostKey"],
            siamux_addr=data["siamuxAddr"],
            proof_height=data["proofHeight"],
            revision_height=data["revisionHeight"],
            revision_number=data["revisionNumber"],
            start_height=data["startHeight"],
            window_start=data["windowStart"],
            window_end=data["windowEnd"],
            renewed_from=data["renewedFrom"],
            spending=ContractSpending(**data["spending"]),
            total_cost=data["totalCost"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract",
        transform_contract,
        id=id
    )

@strawberry.field 
async def contracts(self, info: Info, contract_set: Optional[str] = None) -> List[Contract]:
    """Returns all active contracts the bus is aware of.
    
    Args:
        contract_set: Optional contract set to filter by
        
    Returns:
        List of active contracts
    """
    def transform_contracts(data: List[dict]) -> List[Contract]:
        return [
            Contract(
                id=contract["id"],
                host_ip=contract["hostIP"],
                host_key=contract["hostKey"],
                siamux_addr=contract["siamuxAddr"],
                proof_height=contract["proofHeight"],
                revision_height=contract["revisionHeight"],
                revision_number=contract["revisionNumber"],
                size=contract.get("size"),
                start_height=contract["startHeight"],
                state=contract.get("state"),
                window_start=contract["windowStart"],
                window_end=contract["windowEnd"],
                contract_price=contract.get("contractPrice"),
                renewed_from=contract["renewedFrom"],
                spending=ContractSpending(**contract["spending"]),
                total_cost=contract["totalCost"],
                sets=contract.get("sets")
            )
            for contract in data
        ]
        
    return await RenterdBaseResolver.handle_api_call(
        info, 
        "get_contracts",
        transform_contracts,
        contract_set=contract_set
    )

@strawberry.field
async def contract_roots(self, info: Info, id: str) -> ContractRoots:
    """Returns the roots of all used sectors for a given contract.
    
    Args:
        id: Contract ID
        
    Returns:
        Contract sector roots
    """
    def transform_roots(data: dict) -> ContractRoots:
        return ContractRoots(roots=data["roots"])
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_roots",
        transform_roots,
        id=id
    )

@strawberry.field
async def contract_size(self, info: Info, id: str) -> ContractSize:
    """Returns the total contract size and prunable amount.
    
    Args:
        id: Contract ID
        
    Returns:
        Contract size information
    """
    def transform_size(data: dict) -> ContractSize:
        return ContractSize(
            prunable=data["prunable"],
            size=data["size"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_size",
        transform_size,
        id=id
    )

@strawberry.field
async def contract_ancestors(self, info: Info, id: str) -> List[ArchivedContract]:
    """Returns chain of ancestors for a given contract.
    
    Args:
        id: Contract ID
        
    Returns:
        List of archived contract ancestors
    """
    def transform_ancestors(data: List[dict]) -> List[ArchivedContract]:
        return [
            ArchivedContract(
                id=contract["id"],
                host_key=contract["hostKey"],
                renewed_to=contract["renewedTo"],
                spending=ContractSpending(**contract["spending"]),
                proof_height=contract["proofHeight"],
                revision_height=contract["revisionHeight"],
                revision_number=contract["revisionNumber"],
                size=contract["size"],
                start_height=contract["startHeight"],
                state=contract["state"],
                window_start=contract["windowStart"],
                window_end=contract["windowEnd"]
            )
            for contract in data
        ]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_ancestors",
        transform_ancestors,
        id=id
    )

@strawberry.mutation
async def delete_contract(self, info: Info, id: str) -> bool:
    """Deletes a contract from the bus.
    
    Args:
        id: Contract ID
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_contract",
        lambda _: True,
        id=id
    )
    return True

@strawberry.mutation
async def delete_all_contracts(self, info: Info) -> bool:
    """Deletes all contracts from the bus.
    
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_all_contracts",
        lambda _: True
    )
    return True


@strawberry.mutation
async def acquire_contract(self, info: Info, id: str, params: ContractAcquireInput) -> ContractLock:
    """Acquires a contract for up to a given duration.
    
    Args:
        id: Contract ID
        params: Acquisition parameters
        
    Returns:
        Lock information
    """
    def transform_lock(data: dict) -> ContractLock:
        return ContractLock(lock_id=data["lockID"])
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "acquire_contract",
        transform_lock,
        id=id,
        duration=params.duration,
        priority=params.priority
    )

@strawberry.mutation
async def keepalive_contract(self, info: Info, id: str, params: ContractAcquireInput) -> ContractLock:
    """Extends the lock duration on a previously acquired contract.
    
    Args:
        id: Contract ID
        params: Keepalive parameters
        
    Returns:
        Lock information
    """
    def transform_lock(data: dict) -> ContractLock:
        return ContractLock(lock_id=data["lockID"])
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "keepalive_contract",
        transform_lock,
        id=id,
        duration=params.duration,
        priority=params.priority
    )

@strawberry.mutation
async def release_contract(self, info: Info, id: str, lock: ContractLockInput) -> bool:
    """Releases a previously acquired contract.
    
    Args:
        id: Contract ID
        lock: Lock information
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "release_contract",
        lambda _: True,
        id=id,
        lock_id=lock.lock_id
    )
    return True

@strawberry.mutation
async def archive_contracts(self, info: Info, reasons: Dict[str, str]) -> bool:
    """Archives contracts with the provided contract IDs.
    
    Args:
        reasons: Map of contract IDs to archival reasons
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "archive_contracts",
        lambda _: True,
        reasons=reasons
    )
    return True


@strawberry.field
async def consensus_state(self, info: Info) -> ConsensusState:
    """Returns info about current consensus state.
    
    Returns:
        Current consensus state
    """
    def transform_state(data: dict) -> ConsensusState:
        return ConsensusState(
            block_height=data["blockHeight"],
            last_block_time=data["lastBlockTime"],
            synced=data["synced"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_consensus_state",
        transform_state
    )

@strawberry.field 
async def siafund_fee(self, info: Info, payout: str) -> str:
    """Returns appropriate siafund fee for a given contract payout.
    
    Args:
        payout: Total contract payout
        
    Returns:
        Calculated siafund fee
    """
    def transform_fee(data: str) -> str:
        return data
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_siafund_fee",
        transform_fee,
        payout=payout
    )

@strawberry.mutation
async def accept_block(self, info: Info, block: Dict[str, Any]) -> bool:
    """Accepts a mined block.
    
    Upon success, the block is forwarded to node's peers and p2p network.
    
    Args:
        block: Block data to accept
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "accept_block",
        lambda _: True,
        block=block
    )
    return True



class HostResolver:
    @strawberry.field
    async def host(self, info: Info, pubkey: str) -> Host:
        """Returns information about a host identified by public key.
        
        Args:
            pubkey: Host's public key
            
        Returns:
            Host information
        """
        def transform_host(data: dict) -> Host:
            return Host(
                known_since=data["knownSince"],
                public_key=data["publicKey"],
                net_address=data["netAddress"],
                price_table=PriceTable(**data["priceTable"]),
                settings=HostSettings(**data["settings"]),
                interactions=HostInteractions(**data["interactions"]),
                blocked=data.get("blocked", False)
            )
            
        return await RenterdBaseResolver.handle_api_call(
            info,
            "get_host",
            transform_host,
            pubkey=pubkey
        )

@strawberry.field
async def hosts(self, info: Info, offset: int = 0, limit: int = -1) -> List[Host]:
    """Returns information about all known hosts.
    
    Args:
        offset: Starting offset
        limit: Maximum number of hosts to return
        
    Returns:
        List of hosts
    """
    def transform_hosts(data: List[dict]) -> List[Host]:
        return [
            Host(
                known_since=host["knownSince"],
                public_key=host["publicKey"],
                net_address=host["netAddress"],
                price_table=PriceTable(**host["priceTable"]),
                settings=HostSettings(**host["settings"]),
                interactions=HostInteractions(**host["interactions"]),
                blocked=host.get("blocked", False)
            )
            for host in data
        ]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_hosts",
        transform_hosts,
        offset=offset,
        limit=limit
    )

@strawberry.field
async def host_allowlist(self, info: Info) -> List[str]:
    """Returns the current host allowlist.
    
    Returns:
        List of allowed host public keys
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_host_allowlist",
        lambda data: data
    )

@strawberry.field
async def host_blocklist(self, info: Info) -> List[str]:
    """Returns the current host blocklist.
    
    Returns:
        List of blocked host addresses
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_host_blocklist",
        lambda data: data
    )

@strawberry.mutation
async def reset_host_lost_sectors(self, info: Info, pubkey: str) -> bool:
    """Resets the count of lost sectors for a host.
    
    Args:
        pubkey: Host's public key
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "reset_host_lost_sectors",
        lambda _: True,
        pubkey=pubkey
    )
    return True

@strawberry.mutation
async def update_host_allowlist(self, info: Info, input: HostAllowlistInput) -> bool:
    """Updates the host allowlist.
    
    Args:
        input: Allowlist update parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_host_allowlist",
        lambda _: True,
        input=input
    )
    return True

@strawberry.mutation
async def update_host_blocklist(self, info: Info, input: HostBlocklistInput) -> bool:
    """Updates the host blocklist.
    
    Args:
        input: Blocklist update parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_host_blocklist",
        lambda _: True,
        input=input
    )
    return True

@strawberry.mutation
async def record_host_interactions(self, info: Info, interactions: List[HostInteractionInput]) -> bool:
    """Records host interactions.
    
    Args:
        interactions: List of interactions to record
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "record_host_interactions",
        lambda _: True,
        interactions=interactions
    )
    return True


@strawberry.field
async def contracts_prunable(self, info: Info) -> ContractsPrunableInfo:
    """Returns total amount of data in all contracts and prunable data info.
    
    Returns:
        Contract prunable data information
    """
    def transform_prunable(data: dict) -> ContractsPrunableInfo:
        return ContractsPrunableInfo(
            contracts=[
                ContractPrunableInfo(
                    id=contract["id"],
                    prunable=contract["prunable"],
                    size=contract["size"]
                )
                for contract in data["contracts"]
            ],
            total_prunable=data["totalPrunable"],
            total_size=data["totalSize"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contracts_prunable",
        transform_prunable
    )

@strawberry.field
async def contract_renewed(self, info: Info, id: str) -> Optional[Contract]:
    """Returns the contract formed as part of contract renewal.
    
    Args:
        id: Original contract ID
        
    Returns:
        Renewed contract information if exists
    """
    def transform_renewed_contract(data: dict) -> Contract:
        return Contract(
            id=data["id"],
            host_ip=data["hostIP"],
            host_key=data["hostKey"],
            siamux_addr=data["siamuxAddr"],
            proof_height=data["proofHeight"],
            revision_height=data["revisionHeight"],
            revision_number=data["revisionNumber"],
            size=data.get("size"),
            start_height=data["startHeight"],
            window_start=data["windowStart"],
            window_end=data["windowEnd"],
            renewed_from=data["renewedFrom"],
            spending=ContractSpending(**data["spending"]),
            total_cost=data["totalCost"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_renewed",
        transform_renewed_contract,
        id=id
    )

@strawberry.field
async def contract_sets(self, info: Info) -> List[str]:
    """Returns names of all known contract sets.
    
    Returns:
        List of contract set names
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_sets",
        lambda data: data
    )

@strawberry.mutation
async def update_contract_set(self, info: Info, set_name: str, contract_ids: List[str]) -> bool:
    """Creates/updates a named contract set.
    
    Args:
        set_name: Name of contract set
        contract_ids: List of contract IDs in set
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_contract_set",
        lambda _: True,
        set_name=set_name,
        contract_ids=contract_ids
    )
    return True

@strawberry.mutation
async def delete_contract_set(self, info: Info, set_name: str) -> bool:
    """Deletes a contract set.
    
    Args:
        set_name: Name of contract set to delete
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_contract_set",
        lambda _: True,
        set_name=set_name
    )
    return True

@strawberry.mutation
async def update_contracts_spending(self, info: Info, spending: List[ContractSpending]) -> bool:
    """Updates contract spending information.
    
    Args:
        spending: List of contract spending updates
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_contracts_spending",
        lambda _: True,
        spending=spending
    )
    return True

@strawberry.field
async def contracts_prunable(self, info: Info) -> ContractPrunable:
    """Returns total amount of data in all contracts and prunable data.
    
    Returns:
        Contract prunable information with breakdown per contract
    """
    def transform_prunable(data: dict) -> ContractPrunable:
        return ContractPrunable(
            contracts=[
                ContractPrunableInfo(**contract)
                for contract in data["contracts"]
            ],
            total_prunable=data["totalPrunable"],
            total_size=data["totalSize"]
        )
    
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contracts_prunable",
        transform_prunable
    )


@strawberry.mutation
async def remove_hosts(self, info: Info, params: HostRemoveInput) -> int:
    """Removes hosts with given downtime and minimum scan failures.
    
    Args:
        params: Removal criteria
        
    Returns:
        Number of hosts removed
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "remove_hosts",
        lambda count: count,
        params=params
    )
    
@strawberry.field
async def scanning_hosts(self, info: Info, params: ScanningParams) -> List[ScanningHost]:
    """Returns list of hosts for scanning.
    
    Args:
        params: Pagination and filtering parameters
        
    Returns:
        List of hosts to scan
    """
    def transform_hosts(data: List[dict]) -> List[ScanningHost]:
        return [ScanningHost(**host) for host in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_scanning_hosts",
        transform_hosts,
        params=params
    )

@strawberry.field
async def contract_metrics(self, info: Info, params: MetricParams) -> List[ContractMetric]:
    """Returns contract metrics history.
    
    Args:
        params: Query parameters including timeframe and filters
        
    Returns:
        List of contract metrics
    """
    def transform_metrics(data: List[dict]) -> List[ContractMetric]:
        return [ContractMetric(**metric) for metric in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_metrics",
        transform_metrics,
        params=params
    )

@strawberry.field
async def churn_metrics(self, info: Info, params: MetricParams) -> List[ChurnMetric]:
    """Returns contract churn metrics history."""
    def transform_metrics(data: List[dict]) -> List[ChurnMetric]:
        return [ChurnMetric(**metric) for metric in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_churn_metrics", 
        transform_metrics,
        params=params
    )

@strawberry.field
async def contractset_metrics(self, info: Info, params: MetricParams) -> List[ContractSetMetric]:
    """Returns contract set size metrics history."""
    def transform_metrics(data: List[dict]) -> List[ContractSetMetric]:
        return [ContractSetMetric(**metric) for metric in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contractset_metrics",
        transform_metrics,
        params=params
    )

@strawberry.field
async def wallet_metrics(self, info: Info, params: MetricParams) -> List[WalletMetric]:
    """Returns wallet balance metrics history."""
    def transform_metrics(data: List[dict]) -> List[WalletMetric]:
        return [WalletMetric(**metric) for metric in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_wallet_metrics",
        transform_metrics,
        params=params
    )

@strawberry.mutation
async def delete_metrics(self, info: Info, key: str, cutoff: str) -> bool:
    """Deletes metrics before the cutoff date.
    
    Args:
        key: Type of metric to delete
        cutoff: RFC3339 encoded cutoff date
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_metrics",
        lambda _: True,
        key=key,
        cutoff=cutoff
    )
    return True


@strawberry.field 
async def host(self, info: Info, public_key: str) -> Host:
    """Returns information about a specific host.
    
    Args:
        public_key: Host's public key
        
    Returns:
        Host information
    """
    def transform_host(data: dict) -> Host:
        return Host(
            known_since=data["knownSince"],
            public_key=data["publicKey"],
            net_address=data["netAddress"],
            price_table=PriceTable(**data["priceTable"]),
            settings=HostSettings(**data["settings"]),
            interactions=HostInteractions(**data["interactions"]),
            blocked=data["blocked"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_host",
        transform_host,
        public_key=public_key
    )

@strawberry.field
async def hosts(self, info: Info, offset: int = 0, limit: int = -1) -> List[Host]:
    """Returns information about all known hosts.
    
    Args:
        offset: Pagination offset
        limit: Pagination limit
        
    Returns:
        List of hosts
    """
    def transform_hosts(data: List[dict]) -> List[Host]:
        return [
            Host(
                known_since=host["knownSince"],
                public_key=host["publicKey"],
                net_address=host["netAddress"],
                price_table=PriceTable(**host["priceTable"]),
                settings=HostSettings(**host["settings"]),
                interactions=HostInteractions(**host["interactions"]),
                blocked=host.get("blocked", False)
            )
            for host in data
        ]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_hosts",
        transform_hosts,
        offset=offset,
        limit=limit
    )

@strawberry.field
async def allowlist(self, info: Info) -> List[str]:
    """Returns the current host allowlist.
    
    Returns:
        List of allowed host public keys
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_allowlist",
        lambda data: data
    )

@strawberry.field
async def blocklist(self, info: Info) -> List[str]:
    """Returns the current host blocklist.
    
    Returns:
        List of blocked host addresses
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_blocklist",
        lambda data: data
    )

@strawberry.mutation
async def update_allowlist(self, info: Info, update: HostListUpdateInput) -> bool:
    """Updates the host allowlist.
    
    Args:
        update: Allowlist updates
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_allowlist",
        lambda _: True,
        update=update
    )
    return True

@strawberry.mutation
async def update_blocklist(self, info: Info, update: HostListUpdateInput) -> bool:
    """Updates the host blocklist.
    
    Args:
        update: Blocklist updates
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_blocklist", 
        lambda _: True,
        update=update
    )
    return True

@strawberry.mutation
async def reset_lost_sectors(self, info: Info, public_key: str) -> bool:
    """Resets the lost sector count for a host.
    
    Args:
        public_key: Host's public key
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "reset_lost_sectors",
        lambda _: True,
        public_key=public_key
    )
    return True

@strawberry.mutation
async def record_interactions(self, info: Info, interactions: List[HostInteractionInput]) -> bool:
    """Records host interactions.
    
    Args:
        interactions: List of interactions to record
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "record_interactions",
        lambda _: True, 
        interactions=interactions
    )
    return True


@strawberry.field
async def contract_sets(self, info: Info) -> List[ContractSet]:
    """Returns all contract sets.
    
    Returns:
        List of contract set names
    """
    def transform_sets(data: List[str]) -> List[ContractSet]:
        return [ContractSet(name=name) for name in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_sets",
        transform_sets
    )

@strawberry.mutation
async def update_contract_set(
    self, 
    info: Info, 
    name: str, 
    contracts: ContractSetInput
) -> bool:
    """Updates a contract set.
    
    Args:
        name: Set name
        contracts: Contract IDs to include
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_contract_set",
        lambda _: True,
        name=name,
        contract_ids=contracts.contract_ids
    )
    return True

@strawberry.mutation
async def delete_contract_set(self, info: Info, name: str) -> bool:
    """Deletes a contract set.
    
    Args:
        name: Set name to delete
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_contract_set",
        lambda _: True,
        name=name
    )
    return True

@strawberry.field
async def renewed_contract(self, info: Info, id: str) -> ContractRenewedInfo:
    """Returns the renewed contract info.
    
    Args:
        id: Original contract ID
        
    Returns:
        Renewed contract information
    """
    def transform_renewed(data: dict) -> ContractRenewedInfo:
        return ContractRenewedInfo(
            id=data["id"],
            host_ip=data["hostIP"],
            host_key=data["hostKey"],
            siamux_addr=data["siamuxAddr"],
            proof_height=data["proofHeight"],
            revision_height=data["revisionHeight"], 
            revision_number=data["revisionNumber"],
            size=data["size"],
            start_height=data["startHeight"],
            window_start=data["windowStart"],
            window_end=data["windowEnd"],
            renewed_from=data["renewedFrom"],
            spending=ContractSpending(**data["spending"]),
            total_cost=data["totalCost"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_renewed_contract",
        transform_renewed,
        id=id
    )

@strawberry.mutation
async def update_contract_spending(
    self, 
    info: Info,
    updates: List[ContractSpendingUpdate]
) -> bool:
    """Updates contract spending records.
    
    Args:
        updates: List of spending updates
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_contract_spending",
        lambda _: True,
        updates=updates
    )
    return True


@strawberry.mutation
async def create_multipart_upload(
    self, 
    info: Info,
    upload: MultipartUploadInput
) -> MultipartUploadInfo:
    """Creates a new multipart upload.
    
    Args:
        upload: Upload parameters
        
    Returns:
        Upload ID information
    """
    def transform_upload(data: dict) -> MultipartUploadInfo:
        return MultipartUploadInfo(upload_id=data["uploadID"])
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "create_multipart_upload",
        transform_upload,
        upload=upload
    )

@strawberry.mutation 
async def abort_multipart_upload(
    self,
    info: Info,
    abort: MultipartUploadAbortInput
) -> bool:
    """Aborts an unfinished multipart upload.
    
    Args:
        abort: Abort parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "abort_multipart_upload",
        lambda _: True,
        abort=abort
    )
    return True

@strawberry.mutation
async def complete_multipart_upload(
    self,
    info: Info,
    complete: MultipartUploadCompleteInput
) -> CompleteMultipartUploadResponse:
    """Completes a multipart upload.
    
    Args:
        complete: Complete parameters
        
    Returns:
        Upload completion info with eTag
    """
    def transform_complete(data: dict) -> CompleteMultipartUploadResponse:
        return CompleteMultipartUploadResponse(e_tag=data["eTag"])
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "complete_multipart_upload", 
        transform_complete,
        complete=complete
    )

@strawberry.field
async def list_multipart_parts(
    self,
    info: Info,
    parts: MultipartUploadListPartsInput
) -> MultipartPartsResponse:
    """Lists parts within an unfinished multipart upload.
    
    Args:
        parts: List parts parameters
        
    Returns:
        List of upload parts
    """
    def transform_parts(data: dict) -> MultipartPartsResponse:
        return MultipartPartsResponse(
            has_more=data["hasMore"],
            next_marker=data["nextMarker"],
            parts=[
                MultipartPart(
                    part_number=part["partNumber"],
                    last_modified=part["lastModified"],
                    e_tag=part["eTag"],
                    size=part["size"]
                )
                for part in data["parts"]
            ]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_multipart_parts",
        transform_parts,
        parts=parts
    )

@strawberry.field
async def list_multipart_uploads(
    self,
    info: Info,
    uploads: MultipartUploadListInput
) -> MultipartUploadsResponse:
    """Lists all unfinished multipart uploads.
    
    Args:
        uploads: List uploads parameters
        
    Returns:
        List of unfinished uploads
    """
    def transform_uploads(data: dict) -> MultipartUploadsResponse:
        return MultipartUploadsResponse(
            uploads=[
                MultipartUpload(
                    path=upload["path"],
                    upload_id=upload["uploadID"],
                    created_at=upload["createdAt"]
                )
                for upload in data["uploads"]
            ]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_multipart_uploads",
        transform_uploads,
        uploads=uploads
    )



@strawberry.field
async def get_object(
    self, 
    info: Info, 
    key: str, 
    bucket: Optional[str] = None
) -> ObjectResponse:
    """Fetches metadata for an object.
    
    Args:
        key: Object path/key
        bucket: Optional bucket name
        
    Returns:
        Object metadata
    """
    def transform_object(data: dict) -> ObjectResponse:
        return ObjectResponse(
            has_more=data["hasMore"],
            object=ObjectInfo(
                e_tag=data["object"]["eTag"],
                health=data["object"]["health"],
                mime_type=data["object"]["mimeType"],
                mod_time=data["object"]["modTime"],
                name=data["object"]["name"],
                size=data["object"]["size"],
                key=data["object"]["key"],
                slabs=[
                    ObjectSlab(
                        slab=SlabShard(
                            health=slab["slab"]["health"],
                            key=slab["slab"]["key"],
                            min_shards=slab["slab"]["minShards"],
                            shards=[
                                ShardContract(
                                    contracts=shard["contracts"],
                                    latest_host=shard["latestHost"],
                                    root=shard["root"]
                                )
                                for shard in slab["slab"]["shards"]
                            ]
                        ),
                        offset=slab["offset"],
                        length=slab["length"]
                    )
                    for slab in data["object"]["slabs"]
                ]
            )
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_object",
        transform_object,
        key=key,
        bucket=bucket
    )

@strawberry.field
async def list_objects(
    self,
    info: Info,
    params: ObjectListInput
) -> ObjectListResponse:
    """Lists objects with given prefix.
    
    Args:
        params: List parameters
        
    Returns:
        List of objects
    """
    def transform_list(data: dict) -> ObjectListResponse:
        return ObjectListResponse(
            has_more=data["hasMore"],
            next_marker=data["nextMarker"],
            objects=[
                ObjectListEntry(
                    name=obj["name"],
                    size=obj["size"],
                    health=obj["health"]
                )
                for obj in data["objects"]
            ]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_objects",
        transform_list,
        params=params
    )

@strawberry.mutation
async def put_object(
    self,
    info: Info,
    key: str,
    object: ObjectInfo,
    bucket: Optional[str] = None
) -> bool:
    """Stores object metadata.
    
    Args:
        key: Object path/key  
        object: Object metadata
        bucket: Optional bucket name
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "put_object",
        lambda _: True,
        key=key,
        object=object,
        bucket=bucket
    )
    return True

@strawberry.mutation
async def delete_object(
    self,
    info: Info,
    key: str,
    batch: bool = False,
    bucket: Optional[str] = None
) -> bool:
    """Deletes an object or multiple objects.
    
    Args:
        key: Object path/key
        batch: If true, deletes all objects with prefix
        bucket: Optional bucket name
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_object",
        lambda _: True,
        key=key,
        batch=batch,
        bucket=bucket
    )
    return True

@strawberry.mutation
async def copy_object(
    self,
    info: Info,
    copy: ObjectCopyInput
) -> bool:
    """Copies an object.
    
    Args:
        copy: Copy parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "copy_object",
        lambda _: True,
        copy=copy
    )
    return True

@strawberry.mutation
async def rename_object(
    self,
    info: Info,
    rename: ObjectRenameInput
) -> bool:
    """Renames an object or multiple objects.
    
    Args:
        rename: Rename parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "rename_object",
        lambda _: True,
        rename=rename
    )
    return True


@strawberry.field
async def download_params(self, info: Info) -> DownloadParams:
    """Returns default download parameters.
    
    Returns:
        Download parameters configuration
    """
    def transform_params(data: dict) -> DownloadParams:
        return DownloadParams(
            contract_set=data["ContractSet"],
            consensus_state=DownloadConsensusState(
                block_height=data["ConsensusState"]["BlockHeight"],
                synced=data["ConsensusState"]["Synced"]
            ),
            gouging_settings=DownloadGougingSettings(
                min_max_collateral=data["GougingSettings"]["minMaxCollateral"],
                max_rpc_price=data["GougingSettings"]["maxRPCPrice"],
                max_contract_price=data["GougingSettings"]["maxContractPrice"],
                max_download_price=data["GougingSettings"]["maxDownloadPrice"],
                max_upload_price=data["GougingSettings"]["maxUploadPrice"],
                max_storage_price=data["GougingSettings"]["maxStoragePrice"],
                host_block_height_leeway=data["GougingSettings"]["hostBlockHeightLeeway"]
            ),
            redundancy_settings=RedundancySettings(
                min_shards=data["RedundancySettings"]["minShards"],
                total_shards=data["RedundancySettings"]["totalShards"]
            ),
            transaction_fee=data["TransactionFee"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_download_params",
        transform_params
    )

@strawberry.field
async def download_params(self, info: Info) -> DownloadParameters:
    """Returns default download parameters used by workers."""
    def transform_params(data: dict) -> DownloadParameters:
        return DownloadParameters(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_download_params",
        transform_params
    )

@strawberry.field
async def upload_params(self, info: Info) -> UploadParameters:
    """Returns default upload parameters used by workers."""
    def transform_params(data: dict) -> UploadParameters:
        return UploadParameters(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_upload_params", 
        transform_params
    )

@strawberry.field
async def gouging_params(self, info: Info) -> GougingSettings:
    """Returns default gouging parameters used by workers."""
    def transform_params(data: dict) -> GougingSettings:
        return GougingSettings(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info, 
        "get_gouging_params",
        transform_params
    )

class SettingsResolver:
@strawberry.field
async def settings(self, info: Info) -> List[str]:
    """Returns list of available setting keys."""
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_settings",
        lambda data: data
    )

@strawberry.field
async def setting(self, info: Info, key: str) -> Any:
    """Returns current settings for a specific key.
    
    Args:
        key: Setting key to fetch
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_setting",
        lambda data: data,
        key=key
    )

@strawberry.mutation
async def update_setting(self, info: Info, key: str, value: Any) -> bool:
    """Updates settings for a given key.
    
    Args:
        key: Setting key to update
        value: New setting value
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_setting",
        lambda _: True,
        key=key,
        value=value
    )
    return True

@strawberry.mutation
async def delete_setting(self, info: Info, key: str) -> bool:
    """Deletes settings for a given key.
    
    Args:
        key: Setting key to delete
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_setting",
        lambda _: True,
        key=key
    )
    return True


@strawberry.field
async def state(self, info: Info) -> BusState:
    """Returns bus state info."""
    def transform_state(data: dict) -> BusState:
        return BusState(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_state",
        transform_state
    )

@strawberry.field
async def syncer_address(self, info: Info) -> str:
    """Returns address bus is listening on for p2p connections."""
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_syncer_address",
        lambda addr: addr
    )

@strawberry.field
async def syncer_peers(self, info: Info) -> List[str]:
    """Returns connected p2p network peers."""
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_syncer_peers",
        lambda peers: peers
    )

@strawberry.mutation
async def connect_peer(self, info: Info, address: str) -> bool:
    """Connects to a new peer.
    
    Args:
        address: Peer address to connect to
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "connect_peer",
        lambda _: True,
        address=address
    )
    return True

@strawberry.mutation
async def broadcast_transaction(self, info: Info, transaction: Transaction) -> bool:
    """Broadcasts transaction to p2p network.
    
    Args:
        transaction: Transaction to broadcast
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "broadcast_transaction",
        lambda _: True,
        transaction=transaction
    )
    return True

@strawberry.field
async def recommended_fee(self, info: Info) -> str:
    """Returns recommended transaction fee per byte."""
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_recommended_fee",
        lambda fee: fee
    )

@strawberry.field 
async def object_stats(self, info: Info, bucket: Optional[str] = None) -> ObjectStats:
    """Returns object statistics.
    
    Args:
        bucket: Optional bucket to get stats for
        
    Returns:
        Object statistics
    """
    def transform_stats(data: dict) -> ObjectStats:
        return ObjectStats(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_object_stats",
        transform_stats,
        bucket=bucket
    )


@strawberry.mutation
async def migrate_slabs(self, info: Info, params: SlabMigrationInput) -> List[SlabMigration]:
    """Returns slabs needing migration based on health cutoff.
    
    Args:
        params: Migration parameters
        
    Returns:
        List of slabs to migrate
    """
    def transform_migrations(data: List[dict]) -> List[SlabMigration]:
        return [SlabMigration(**slab) for slab in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_slab_migrations",
        transform_migrations,
        params=params
    )

@strawberry.field
async def partial_slab(self, info: Info, key: str, offset: int, length: int) -> Optional[Slab]:
    """Returns partial slab for given key and range.
    
    Args:
        key: Slab key
        offset: Range start offset 
        length: Range length
        
    Returns:
        Partial slab if found
    """
    def transform_slab(data: dict) -> Optional[Slab]:
        return Slab(**data) if data else None
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_partial_slab",
        transform_slab,
        key=key,
        offset=offset,
        length=length
    )

@strawberry.mutation
async def add_partial_slab(
    self,
    info: Info,
    min_shards: int,
    total_shards: int, 
    contract_set: str
) -> AddPartialSlabResult:
    """Adds a partial slab.
    
    Args:
        min_shards: Minimum shards required
        total_shards: Total shards to create
        contract_set: Contract set to use
        
    Returns:
        Result with slab info and buffer state
    """
    def transform_result(data: dict) -> AddPartialSlabResult:
        return AddPartialSlabResult(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "add_partial_slab",
        transform_result,
        min_shards=min_shards,
        total_shards=total_shards,
        contract_set=contract_set
    )

@strawberry.field
async def slab(self, info: Info, key: str) -> Optional[Slab]: 
    """Returns slab for given key.
    
    Args:
        key: Slab key
        
    Returns:
        Slab if found
    """
    def transform_slab(data: dict) -> Optional[Slab]:
        return Slab(**data) if data else None
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_slab",
        transform_slab,
        key=key
    )

@strawberry.field
async def slab_objects(self, info: Info, key: str) -> List[str]:
    """Returns objects associated with slab.
    
    Args:
        key: Slab key
        
    Returns:
        List of object paths
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_slab_objects",
        lambda data: data,
        key=key
    )

@strawberry.mutation
async def update_slab(
    self,
    info: Info, 
    contract_set: str,
    slab: Slab, 
    used_contracts: Dict[str, str]
) -> bool:
    """Updates slab metadata.
    
    Args:
        contract_set: Contract set name 
        slab: Updated slab data
        used_contracts: Contract mapping
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "update_slab",
        lambda _: True,
        contract_set=contract_set,
        slab=slab,
        used_contracts=used_contracts
    )
    return True

@strawberry.mutation
async def refresh_health(self, info: Info) -> bool:
    """Refreshes health of all slabs.
    
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info, 
        "refresh_health",
        lambda _: True
    )
    return True

@strawberry.field
async def object(
    self,
    info: Info,
    path: str,
    bucket: Optional[str] = None
) -> ObjectListResponse:
    """Returns object metadata.
    
    Args:
        path: Object path
        bucket: Optional bucket name
        
    Returns:
        Object metadata
    """
    def transform_response(data: dict) -> ObjectListResponse:
        return ObjectListResponse(
            has_more=data["hasMore"],
            object=Object(**data["object"])
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_object",
        transform_response,
        path=path,
        bucket=bucket
    )

@strawberry.mutation
async def put_object(
    self,
    info: Info,
    path: str, 
    object: ObjectInput,
    bucket: Optional[str] = None
) -> bool:
    """Stores object metadata.
    
    Args:
        path: Object path
        object: Object metadata
        bucket: Optional bucket name
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "put_object",
        lambda _: True,
        path=path,
        object=object,
        bucket=bucket
    )
    return True

@strawberry.mutation
async def delete_object(
    self,
    info: Info,
    path: str,
    batch: bool = False,
    bucket: Optional[str] = None
) -> bool:
    """Deletes object(s).
    
    Args:
        path: Object path
        batch: If true, deletes all objects starting with path
        bucket: Optional bucket name
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_object",
        lambda _: True,
        path=path,
        batch=batch,
        bucket=bucket
    )
    return True

@strawberry.mutation
async def copy_object(self, info: Info, params: CopyObjectInput) -> bool:
    """Copies object between paths/buckets.
    
    Args:
        params: Copy parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "copy_object",
        lambda _: True,
        params=params  
    )
    return True

@strawberry.mutation
async def rename_object(self, info: Info, params: RenameObjectInput) -> bool:
    """Renames object or objects.
    
    Args:
        params: Rename parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "rename_object",
        lambda _: True,
        params=params
    )
    return True


@strawberry.field
async def wallet_info(self, info: Info) -> WalletInfo:
    """Returns collected information about the wallet."""
    def transform_info(data: dict) -> WalletInfo:
        return WalletInfo(
            scan_height=data["scanHeight"],
            address=data["address"],
            spendable=data["spendable"],
            confirmed=data["confirmed"],
            unconfirmed=data["unconfirmed"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_wallet_info", 
        transform_info
    )

@strawberry.field
async def wallet_address(self, info: Info) -> str:
    """Returns an address that can be used to fund the wallet."""
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_wallet_address",
        lambda data: data
    )

@strawberry.field
async def wallet_balance(self, info: Info) -> str:
    """Returns the current balance of the wallet."""
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_wallet_balance",
        lambda data: data
    )

@strawberry.field 
async def wallet_outputs(self, info: Info) -> List[ScOutput]:
    """Returns all confirmed UTXOs relevant to the wallet."""
    def transform_outputs(data: List[dict]) -> List[ScOutput]:
        return [ScOutput(**output) for output in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_wallet_outputs",
        transform_outputs
    )

@strawberry.field
async def wallet_transactions(self, info: Info) -> List[Transaction]:
    """Returns all confirmed transactions of the wallet."""
    def transform_txns(data: List[dict]) -> List[Transaction]:
        return [
            Transaction(
                raw=txn["Raw"],
                index=txn["Index"],
                id=txn["ID"],
                inflow=txn["Inflow"],
                outflow=txn["Outflow"],
                timestamp=txn["Timestamp"]
            )
            for txn in data
        ]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_wallet_transactions",
        transform_txns
    )


@strawberry.field
async def webhooks(self, info: Info) -> WebhookInfo:
    """Returns all registered webhooks and queue information."""
    def transform_webhooks(data: dict) -> WebhookInfo:
        return WebhookInfo(
            webhooks=[Webhook(**webhook) for webhook in data["webhooks"]],
            queues=[WebhookQueue(**queue) for queue in data["queues"]]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_webhooks",
        transform_webhooks
    )

@strawberry.mutation
async def register_webhook(self, info: Info, webhook: WebhookInput) -> bool:
    """Registers a new webhook."""
    await RenterdBaseResolver.handle_api_call(
        info,
        "register_webhook",
        lambda _: True,
        webhook=webhook
    )
    return True

@strawberry.mutation 
async def delete_webhook(self, info: Info, webhook: WebhookInput) -> bool:
    """Deletes a webhook."""
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_webhook",
        lambda _: True,
        webhook=webhook
    )
    return True

@strawberry.mutation
async def trigger_webhook(self, info: Info, action: WebhookActionInput) -> bool:
    """Triggers webhook action."""
    await RenterdBaseResolver.handle_api_call(
        info,
        "trigger_webhook",
        lambda _: True,
        action=action
    )
    return True

@strawberry.field
async def txpool_transactions(self, info: Info) -> List[TxPoolTransaction]:
    """Returns all unconfirmed transactions in transaction pool."""
    def transform_txns(data: List[dict]) -> List[TxPoolTransaction]:
        return [TxPoolTransaction(**txn) for txn in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_txpool_transactions",
        transform_txns
    )


@strawberry.mutation
async def redistribute_wallet(
    self, 
    info: Info,
    params: RedistributeInput
) -> WalletRedistributeResult:
    """Redistributes wallet funds over multiple outputs.
    
    Args:
        params: Redistribution parameters
        
    Returns:
        Transaction IDs of redistribution transactions
    """
    def transform_result(data: List[str]) -> WalletRedistributeResult:
        return WalletRedistributeResult(transaction_ids=data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "redistribute_wallet",
        transform_result,
        amount=params.amount,
        outputs=params.outputs
    )

@strawberry.mutation
async def sign_transaction(
    self,
    info: Info, 
    input: TransactionSignInput
) -> Dict[str, Any]:
    """Signs a transaction.
    
    Args:
        input: Transaction signing parameters
        
    Returns:
        Signed transaction
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "sign_transaction",
        lambda data: data,
        transaction=input.transaction,
        to_sign=input.to_sign,
        covered_fields=input.covered_fields
    )

@strawberry.mutation
async def prepare_contract_formation(
    self,
    info: Info,
    params: ContractPrepareInput
) -> List[Dict[str, Any]]:
    """Prepares an unsigned contract formation transaction.
    
    Args:
        params: Contract preparation parameters
        
    Returns:
        List of prepared transactions
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "prepare_contract_formation",
        lambda data: data,
        params=params
    )

@strawberry.mutation
async def prepare_contract_renewal(
    self,
    info: Info,
    params: ContractRenewInput 
) -> PreparedTransaction:
    """Prepares an unsigned contract renewal transaction.
    
    Args:
        params: Contract renewal parameters
        
    Returns:
        Prepared transaction data
    """
    def transform_prepared(data: dict) -> PreparedTransaction:
        return PreparedTransaction(
            transaction_set=data["transactionSet"],
            final_payment=data.get("finalPayment")
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "prepare_contract_renewal",
        transform_prepared,
        params=params
    )

@strawberry.mutation
async def discard_transaction(
    self,
    info: Info,
    transaction: Dict[str, Any]
) -> bool:
    """Discards a transaction.
    
    Args:
        transaction: Transaction to discard
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "discard_transaction",
        lambda _: True,
        transaction=transaction
    )
    return True

@strawberry.mutation
async def fund_transaction(
    self,
    info: Info,
    fund_params: TransactionFundInput
) -> Dict[str, Any]:
    """Funds a transaction with the specified amount.
    
    Args:
        fund_params: Transaction funding parameters
        
    Returns:
        Funded transaction details
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "fund_transaction",
        lambda data: data,
        transaction=fund_params.transaction,
        amount=fund_params.amount
    )


@strawberry.mutation
async def abort_multipart_upload(
    self,
    info: Info,
    params: MultipartAbortInput
) -> bool:
    """Aborts an unfinished multipart upload.
    
    Args:
        params: Upload to abort
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "abort_multipart_upload",
        lambda _: True,
        params=params
    )
    return True

@strawberry.field 
async def list_multipart_parts(
    self,
    info: Info,
    params: MultipartListPartsInput
) -> MultipartListPartsResponse:
    """Lists parts within an unfinished multipart upload.
    
    Args:
        params: Parameters for listing parts
        
    Returns:
        List of parts information
    """
    def transform_response(data: dict) -> MultipartListPartsResponse:
        return MultipartListPartsResponse(
            has_more=data["hasMore"],
            next_marker=data["nextMarker"],
            parts=[MultipartPart(**part) for part in data["parts"]]
        )
    
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_multipart_parts",
        transform_response,
        params=params
    )

@strawberry.field
async def list_multipart_uploads(
    self,
    info: Info,
    params: MultipartListUploadsInput
) -> List[MultipartUpload]:
    """Lists all unfinished multipart uploads.
    
    Args:
        params: Parameters for listing uploads
        
    Returns:
        List of unfinished uploads
    """
    def transform_uploads(data: dict) -> List[MultipartUpload]:
        return [MultipartUpload(**upload) for upload in data["uploads"]]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_multipart_uploads",
        transform_uploads,
        params=params
    )

@strawberry.mutation
async def create_multipart_upload(
    self,
    info: Info,
    params: MultipartCreateInput
) -> MultipartCreateResponse:
    """Creates a new multipart upload.
    
    Args:
        params: Upload creation parameters
        
    Returns:
        Upload ID for new upload
    """
    def transform_response(data: dict) -> MultipartCreateResponse:
        return MultipartCreateResponse(upload_id=data["uploadID"])
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "create_multipart_upload",
        transform_response,
        params=params
    )

@strawberry.mutation
async def complete_multipart_upload(
    self,
    info: Info,
    params: MultipartCompleteInput
) -> MultipartCompleteResponse:
    """Completes a multipart upload.
    
    Args:
        params: Upload completion parameters
        
    Returns:
        Upload completion information
    """
    def transform_response(data: dict) -> MultipartCompleteResponse:
        return MultipartCompleteResponse(etag=data["eTag"])
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "complete_multipart_upload",
        transform_response,
        params=params
    )


@strawberry.mutation
async def register_upload(self, info: Info, id: str) -> bool:
    """Registers an ongoing upload.
    
    Args:
        id: Upload ID to register
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "register_upload",
        lambda _: True,
        id=id
    )
    return True

@strawberry.mutation
async def unregister_upload(self, info: Info, id: str) -> bool:
    """Unregisters an ongoing upload.
    
    Args:
        id: Upload ID to unregister
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "unregister_upload",
        lambda _: True,
        id=id
    )
    return True

@strawberry.mutation
async def register_upload_sector(
    self,
    info: Info,
    id: str, 
    sector: UploadSectorInput
) -> bool:
    """Associates a sector with an ongoing upload.
    
    Args:
        id: Upload ID
        sector: Sector information
        
    Returns:
        True if successful
    """ 
    await RenterdBaseResolver.handle_api_call(
        info,
        "register_upload_sector",
        lambda _: True,
        id=id,
        sector=sector
    )
    return True


@strawberry.field
async def list_objects(
    self,
    info: Info,
    params: ObjectListInput,
    path: Optional[str] = None
) -> ObjectListResponse:
    """Lists objects or gets single object info.
    
    Args:
        params: Listing parameters
        path: Optional specific object path
        
    Returns:
        Object listing or single object info
    """
    def transform_response(data: dict) -> ObjectListResponse:
        if "object" in data:
            return ObjectListResponse(
                has_more=data.get("hasMore", False),
                object=ObjectInfo(**data["object"])
            )
        else:
            return ObjectListResponse(
                has_more=data.get("hasMore", False),
                objects=[ObjectInfo(**obj) for obj in data.get("objects", [])]
            )
            
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_objects",
        transform_response,
        params=params,
        path=path
    )

@strawberry.mutation
async def store_object(
    self,
    info: Info,
    input: ObjectStoreInput,
    path: str
) -> bool:
    """Stores object metadata.
    
    Args:
        input: Object metadata
        path: Object path
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "store_object",
        lambda _: True,
        input=input,
        path=path
    )
    return True

@strawberry.mutation
async def delete_object(
    self,
    info: Info,
    path: str,
    bucket: str = "default",
    batch: bool = False
) -> bool:
    """Deletes an object or batch of objects.
    
    Args:
        path: Object path
        bucket: Bucket name
        batch: Whether to delete all objects with prefix
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_object",
        lambda _: True,
        path=path,
        bucket=bucket,
        batch=batch
    )
    return True

@strawberry.mutation
async def copy_object(self, info: Info, params: ObjectCopyInput) -> bool:
    """Copies an object.
    
    Args:
        params: Copy parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "copy_object",
        lambda _: True,
        params=params
    )
    return True

@strawberry.mutation
async def rename_object(self, info: Info, params: ObjectRenameInput) -> bool:
    """Renames an object or multiple objects.
    
    Args:
        params: Rename parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "rename_object",
        lambda _: True,
        params=params
    )
    return True


@strawberry.field
async def consensus_state(self, info: Info) -> ConsensusState:
    """Returns current consensus state."""
    def transform_state(data: dict) -> ConsensusState:
        return ConsensusState(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_consensus_state",
        transform_state
    )

@strawberry.field
async def download_params(self, info: Info) -> DownloadParams:
    """Returns default download parameters."""
    def transform_params(data: dict) -> DownloadParams:
        return DownloadParams(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_download_params",
        transform_params
    )


@strawberry.mutation
async def create_multipart_upload(
    self, 
    info: Info,
    input: MultipartCreateInput
) -> str:
    """Creates a new multipart upload."""
    def transform_response(data: dict) -> str:
        return data["uploadID"]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "create_multipart_upload",
        transform_response,
        input=input
    )

@strawberry.mutation 
async def abort_multipart_upload(
    self,
    info: Info,
    input: MultipartAbortInput
) -> bool:
    """Aborts an unfinished multipart upload."""
    await RenterdBaseResolver.handle_api_call(
        info,
        "abort_multipart_upload",
        lambda _: True,
        input=input
    )
    return True

@strawberry.mutation
async def complete_multipart_upload(
    self,
    info: Info,
    input: MultipartCompleteInput
) -> str:
    """Completes a multipart upload."""
    def transform_response(data: dict) -> str:
        return data["eTag"]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "complete_multipart_upload", 
        transform_response,
        input=input
    )

@strawberry.field
async def list_multipart_parts(
    self,
    info: Info,
    input: MultipartListPartsInput
) -> MultipartPartsResponse:
    """Lists parts within an unfinished multipart upload."""
    def transform_response(data: dict) -> MultipartPartsResponse:
        return MultipartPartsResponse(
            has_more=data["hasMore"],
            next_marker=data["nextMarker"],
            parts=[
                MultipartPart(**part)
                for part in data["parts"]
            ]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_multipart_parts",
        transform_response,
        input=input
    )

@strawberry.field
async def list_multipart_uploads(
    self,
    info: Info,
    input: MultipartListUploadsInput
) -> List[MultipartUpload]:
    """Lists all unfinished multipart uploads."""
    def transform_response(data: dict) -> List[MultipartUpload]:
        return [
            MultipartUpload(**upload)
            for upload in data["uploads"]
        ]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_multipart_uploads",
        transform_response,
        input=input
    )


@strawberry.field
async def worker_state(self, info: Info) -> WorkerState:
    """Returns worker state information."""
    def transform_state(data: dict) -> WorkerState:
        return WorkerState(**data)
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_worker_state",
        transform_state
    )
    
@strawberry.field
async def worker_memory(self, info: Info) -> WorkerMemory:
    """Returns worker memory stats."""
    def transform_memory(data: dict) -> WorkerMemory:
        return WorkerMemory(
            upload=MemoryStats(**data["upload"])
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_worker_memory", 
        transform_memory
    )

@strawberry.field
async def worker_id(self, info: Info) -> str:
    """Returns worker's unique identifier."""
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_worker_id",
        lambda id: id
    )


@strawberry.field
async def list_objects(
    self,
    info: Info, 
    input: ObjectListInput
) -> List[ObjectMetadata]:
    """Lists objects matching given criteria."""
    def transform_objects(data: List[dict]) -> List[ObjectMetadata]:
        return [ObjectMetadata(**obj) for obj in data]
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "list_objects",
        transform_objects,
        bucket=input.bucket,
        prefix=input.prefix,
        marker=input.marker,
        offset=input.offset,
        limit=input.limit
    )

@strawberry.mutation  
async def rename_object(
    self,
    info: Info,
    input: ObjectRenameInput
) -> bool:
    """Renames an object or recursively renames multiple objects."""
    await RenterdBaseResolver.handle_api_call(
        info,
        "rename_object",
        lambda _: True,
        bucket=input.bucket,
        from_path=input.from_path,
        to_path=input.to_path,
        mode=input.mode
    )
    return True

@strawberry.mutation
async def delete_object(
    self,
    info: Info,
    path: str,
    bucket: Optional[str] = None,
    batch: bool = False
) -> bool:
    """Deletes an object or multiple objects if batch is true."""
    await RenterdBaseResolver.handle_api_call(
        info,
        "delete_object", 
        lambda _: True,
        path=path,
        bucket=bucket,
        batch=batch
    )
    return True


@strawberry.field
async def rhp_contracts(self, info: Info, host_timeout: Optional[int] = None) -> RHPContractsResponse:
    """Returns all active contracts with latest revisions from hosts.
    
    Args:
        host_timeout: Timeout in ms for fetching each host's contract
        
    Returns:
        Active contracts with revisions
    """
    def transform_contracts(data: dict) -> RHPContractsResponse:
        return RHPContractsResponse(
            contracts=[
                RHPContract(
                    id=contract["id"],
                    host_ip=contract["hostIP"],
                    host_key=contract["hostKey"],
                    siamux_addr=contract["siamuxAddr"],
                    proof_height=contract["proofHeight"],
                    revision_height=contract["revisionHeight"],
                    revision_number=contract["revisionNumber"],
                    start_height=contract["startHeight"],
                    window_start=contract["windowStart"], 
                    window_end=contract["windowEnd"],
                    renewed_from=contract["renewedFrom"],
                    spending=ContractSpending(**contract["spending"]),
                    total_cost=contract["totalCost"],
                    revision=ContractRevision(**contract["revision"]) if "revision" in contract else None
                )
                for contract in data["contracts"]
            ]
        )
    
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_rhp_contracts",
        transform_contracts,
        host_timeout=host_timeout
    )

@strawberry.mutation
async def broadcast_contract(self, info: Info, id: str) -> bool:
    """Broadcasts latest known revision of contract on network.
    
    Args:
        id: Contract ID
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "broadcast_contract",
        lambda _: True,
        id=id
    )
    return True

@strawberry.mutation 
async def prune_contract(self, info: Info, id: str, timeout: int) -> ContractPruneResponse:
    """Prunes unused data from contract.
    
    Args:
        id: Contract ID
        timeout: Operation timeout in nanoseconds
        
    Returns:
        Pruning results
    """
    def transform_response(data: dict) -> ContractPruneResponse:
        return ContractPruneResponse(
            pruned=data["pruned"],
            remaining=data["remaining"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "prune_contract",
        transform_response,
        id=id,
        timeout=timeout
    )

@strawberry.field
async def contract_roots(self, info: Info, id: str) -> List[str]:
    """Returns sector roots for contract.
    
    Args:
        id: Contract ID
        
    Returns:
        List of sector root hashes
    """
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_contract_roots",
        lambda data: data
    )

@strawberry.mutation
async def form_contract(self, info: Info, input: FormContractInput) -> FormContractResponse:
    """Forms new contract with host.
    
    Args:
        input: Contract formation parameters
        
    Returns:
        Formed contract details
    """
    def transform_response(data: dict) -> FormContractResponse:
        return FormContractResponse(
            contract_id=data["contractID"],
            contract=ContractRevision(**data["contract"]["Revision"]),
            transaction_set=data["transactionSet"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info, 
        "form_contract",
        transform_response,
        **strawberry.asdict(input)
    )




@strawberry.mutation
async def fund_account(self, info: Info, params: RHPFundInput) -> bool:
    """Fund an ephemeral account with a host.
    
    Args:
        params: Funding parameters 
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "fund_account",
        lambda _: True,
        params=params
    )
    return True

@strawberry.mutation  
async def renew_contract(self, info: Info, params: RHPRenewInput) -> RenewedContract:
    """Renew a contract with a host.
    
    Args:
        params: Contract renewal parameters
        
    Returns:
        Renewed contract details
    """
    def transform_response(data: dict) -> RenewedContract:
        return RenewedContract(
            error=data["error"],
            contract_id=data["contractID"],
            contract=ContractRevision(**data["contract"]["Revision"]),
            transaction_set=data["transactionSet"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "renew_contract", 
        transform_response,
        params=params
    )

@strawberry.mutation
async def scan_host(self, info: Info, params: RHPScanInput) -> ScanResponse:
    """Scan a host.
    
    Args:
        params: Host scanning parameters
        
    Returns:
        Host scan results
    """
    def transform_response(data: dict) -> ScanResponse:
        return ScanResponse(
            ping=data["ping"],
            settings=HostSettings(**data["settings"])
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "scan_host",
        transform_response,
        params=params
    )

@strawberry.mutation
async def sync_account(self, info: Info, params: RHPSyncInput) -> bool:
    """Sync ephemeral account balance with host.
    
    Args:
        params: Account sync parameters
        
    Returns:
        True if successful
    """
    await RenterdBaseResolver.handle_api_call(
        info,
        "sync_account",
        lambda _: True, 
        params=params
    )
    return True



@strawberry.field
async def worker_state(self, info: Info) -> WorkerState:
    """Get worker state information.
    
    Returns:
        Current worker state
    """
    def transform_state(data: dict) -> WorkerState:
        return WorkerState(
            id=data["id"],
            start_time=data["startTime"], 
            network=data["network"],
            version=data["version"],
            commit=data["commit"],
            os=data["OS"],
            build_time=data["buildTime"]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_worker_state",
        transform_state
    )

@strawberry.field
async def download_stats(self, info: Info) -> DownloadStats:
    """Get download statistics.
    
    Returns:
        Current download stats
    """
    def transform_stats(data: dict) -> DownloadStats:
        return DownloadStats(
            avg_download_speed_mbps=data["avgDownloadSpeedMBPS"],
            avg_overdrive_pct=data["avgOverdrivePct"],
            healthy_downloaders=data["healthyDownloaders"],
            num_downloaders=data["numDownloaders"],
            downloaders_stats=[
                DownloaderStats(**stats)
                for stats in data["downloadersStats"]
            ]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_download_stats",
        transform_stats
    )

@strawberry.field
async def upload_stats(self, info: Info) -> UploadStats:
    """Get upload statistics.
    
    Returns:
        Current upload stats
    """
    def transform_stats(data: dict) -> UploadStats:
        return UploadStats(
            avg_slab_upload_speed_mbps=data["avgSlabUploadSpeedMBPS"],
            avg_overdrive_pct=data["avgOverdrivePct"],
            healthy_uploaders=data["healthyUploaders"],
            num_uploaders=data["numUploaders"],
            uploaders_stats=[
                UploaderStats(**stats)
                for stats in data["uploadersStats"]
            ]
        )
        
    return await RenterdBaseResolver.handle_api_call(
        info,
        "get_upload_stats",
        transform_stats
    )
