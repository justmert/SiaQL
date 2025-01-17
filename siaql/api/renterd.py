from typing import Dict, List, Any, Optional
import httpx
from .utils import handle_api_errors

class RenterdError(Exception):
    """Base exception for renterd API errors"""
    pass

class RenterdAPI:
    """Client for interacting with the renterd API"""
    
    def __init__(
        self,
        bus_uri: str,
        worker_uri: str,
        autopilot_uri: str,
        bus_password: str,
        worker_password: str,
        autopilot_password: str,
        bus_api_prefix: str = "/api/bus/v1",
        worker_api_prefix: str = "/api/worker/v1",
        autopilot_api_prefix: str = "/api/autopilot/v1"
    ):
        """Initialize the renterd API client.
        
        Args:
            bus_uri: Base URI for the bus API
            worker_uri: Base URI for the worker API
            autopilot_uri: Base URI for the autopilot API
            bus_password: Password for bus API authentication
            worker_password: Password for worker API authentication
            autopilot_password: Password for autopilot API authentication
            bus_api_prefix: API prefix for bus endpoints
            worker_api_prefix: API prefix for worker endpoints
            autopilot_api_prefix: API prefix for autopilot endpoints
        """
        # Initialize clients with authentication
        self.bus_client = httpx.AsyncClient(
            base_url=f"{bus_uri}{bus_api_prefix}",
            headers={"Authorization": f"Bearer {bus_password}"}
        )
        self.worker_client = httpx.AsyncClient(
            base_url=f"{worker_uri}{worker_api_prefix}",
            headers={"Authorization": f"Bearer {worker_password}"}
        )
        self.autopilot_client = httpx.AsyncClient(
            base_url=f"{autopilot_uri}{autopilot_api_prefix}",
            headers={"Authorization": f"Bearer {autopilot_password}"}
        )

    @handle_api_errors(RenterdError)
    async def get_accounts(self) -> List[Dict[str, Any]]:
        """Returns all known ephemeral accounts from the bus.
        
        Returns:
            List of accounts, each containing:
                id: Account ID (ed25519 public key)
                host: Host ID (ed25519 public key)
                balance: Current balance
                drift: Account drift
                requiresSync: Whether the account requires syncing
                
        Raises:
            RenterdError: If there is an error fetching the accounts
        """
        response = await self.bus_client.get("/accounts")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_or_create_account(self, account_id: str, host_key: str) -> Dict[str, Any]:
        """Returns the account with the given ID or creates it if it doesn't exist.
        
        Args:
            account_id: The ID of the account (ed25519 public key)
            host_key: The host's public key to attach to the account
            
        Returns:
            Dict containing account details:
                id: Account ID (ed25519 public key)
                host: Host ID (ed25519 public key)
                balance: Current balance
                drift: Account drift
                requiresSync: Whether the account requires syncing
                
        Raises:
            RenterdError: If there is an error creating/fetching the account
        """
        payload = {
            "hostKey": host_key
        }
        
        response = await self.bus_client.post(
            f"/account/{account_id}",
            json=payload
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def lock_account(
        self,
        account_id: str,
        host_key: str,
        exclusive: bool,
        duration: str
    ) -> Dict[str, Any]:
        """Locks an account either exclusively or not.
        
        Usually workers will deposit and withdraw from accounts with a regular lock
        but for syncing the account balance with hosts an exclusive lock is required.
        
        Args:
            account_id: The ID of the account (ed25519 public key)
            host_key: The host's public key
            exclusive: Whether to lock exclusively (required for syncing)
            duration: Time in nanoseconds after which the account is unlocked automatically
            
        Returns:
            Dict containing:
                account: The account details
                lockID: ID that can be used to unlock the account sooner
                
        Raises:
            RenterdError: If there is an error locking the account
        """
        payload = {
            "hostKey": host_key,
            "exclusive": exclusive,
            "duration": duration
        }
        
        response = await self.bus_client.post(
            f"/account/{account_id}/lock",
            json=payload
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def unlock_account(self, account_id: str, lock_id: int) -> None:
        """Unlocks a previously locked account.
        
        This is the counterpart to the account locking endpoint. The lock id returned
        when locking an account can be used to unlock it again before the locking
        duration has passed and the account gets unlocked automatically.
        
        Args:
            account_id: The ID of the account (ed25519 public key)
            lock_id: The lock ID returned when locking the account
            
        Raises:
            RenterdError: If there is an error unlocking the account
        """
        payload = {
            "lockID": lock_id
        }
        
        response = await self.bus_client.post(
            f"/account/{account_id}/unlock",
            json=payload
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def add_account_balance(self, account_id: str, host_key: str, amount: int) -> None:
        """Deposits or withdraws tokens into/from an ephemeral account.
        
        The caller should hold a non-exclusive lock on the account.
        Use positive amount for deposits and negative amount for withdrawals.
        
        Args:
            account_id: The ID of the account (ed25519 public key)
            host_key: The host's public key
            amount: Amount to add (positive) or withdraw (negative)
            
        Raises:
            RenterdError: If there is an error modifying the account balance
        """
        payload = {
            "host": host_key,
            "amount": amount
        }
        
        response = await self.bus_client.post(
            f"/account/{account_id}/add",
            json=payload
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def update_account_balance(self, account_id: str, host_key: str, amount: int) -> None:
        """Updates the balance of an account to the provided value.
        
        The caller should acquire an exclusive lock before calling this endpoint.
        This endpoint is typically used for syncing account balances with hosts.
        
        Args:
            account_id: The ID of the account (ed25519 public key)
            host_key: The host's public key
            amount: The new balance value to set
            
        Raises:
            RenterdError: If there is an error updating the account balance
        """
        payload = {
            "hostKey": host_key,
            "amount": amount
        }
        
        response = await self.bus_client.post(
            f"/account/{account_id}/update",
            json=payload
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def mark_account_for_sync(self, account_id: str, host_key: str) -> None:
        """Marks the account as requiring a balance sync.
        
        Usually set by workers when operations fail with an error indicating
        an insufficient balance. The autopilot (if enabled) will periodically
        check for accounts that require syncing and initiate the sync automatically.
        
        Args:
            account_id: The ID of the account (ed25519 public key)
            host_key: The host's public key
            
        Raises:
            RenterdError: If there is an error marking the account for sync
        """
        payload = {
            "hostKey": host_key
        }
        
        response = await self.bus_client.post(
            f"/account/{account_id}/requiressync",
            json=payload
        )
        response.raise_for_status()

    # api/renterd.py

    @handle_api_errors(RenterdError)
    async def reset_account_drift(self, id: str) -> None:
        """Resets the drift on the specified ephemeral account.
        
        Args:
            id: The account ID (ed25519 public key)
            
        Raises:
            RenterdError: If there is an error resetting the drift
        """
        response = await self.bus_client.post(f"/account/{id}/resetdrift")
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_alerts(self, offset: int = 0, limit: int = -1) -> List[Dict[str, Any]]:
        """Returns all currently registered alerts.
        
        Args:
            offset: Offset at which to start returning alerts
            limit: Max number of alerts to return
            
        Returns:
            List of alerts with their details
            
        Raises:
            RenterdError: If there is an error fetching the alerts
        """
        params = {"offset": offset, "limit": limit}
        response = await self.bus_client.get("/alerts", params=params)
        response.raise_for_status()
        return response.json()



    @handle_api_errors(RenterdError)
    async def dismiss_alerts(self, alert_ids: Optional[List[str]] = None, all: bool = False) -> None:
        """Dismisses specified alerts or all alerts.
        
        Args:
            alert_ids: List of alert IDs to dismiss
            all: If True, dismisses all alerts
            
        Raises:
            RenterdError: If there is an error dismissing the alerts
        """
        params = {"all": "true"} if all else {}
        response = await self.bus_client.post("/alerts/dismiss", json=alert_ids or [], params=params)
        response.raise_for_status()



    @handle_api_errors(RenterdError)
    async def register_alert(self, alert: Dict[str, Any]) -> None:
        """Registers a new alert.
        
        Args:
            alert: Alert details to register
            
        Raises:
            RenterdError: If there is an error registering the alert
        """
        response = await self.bus_client.post("/alerts/register", json=alert)
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_autopilots(self) -> List[Dict[str, Any]]:
        """Returns all autopilot configurations.
        
        Returns:
            List of autopilot configurations
            
        Raises:
            RenterdError: If there is an error fetching the configurations
        """
        response = await self.bus_client.get("/autopilots")
        response.raise_for_status()
        return response.json()



    @handle_api_errors(RenterdError)
    async def get_autopilot(self, id: str) -> Dict[str, Any]:
        """Returns autopilot configuration for given ID.
        
        Args:
            id: Autopilot ID
            
        Returns:
            Autopilot configuration
            
        Raises:
            RenterdError: If there is an error fetching the configuration
        """
        response = await self.bus_client.get(f"/autopilot/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)  
    async def update_autopilot(self, id: str, config: Dict[str, Any]) -> None:
        """Updates autopilot configuration.
        
        Args:
            id: Autopilot ID
            config: New configuration
            
        Raises:
            RenterdError: If there is an error updating the configuration
        """
        response = await self.bus_client.put(f"/autopilot/{id}", json=config)
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_contract(self, id: str) -> Dict[str, Any]:
        """Returns contract metadata.
        
        Args:
            id: Contract ID
            
        Returns:
            Contract metadata
            
        Raises:
            RenterdError: If error fetching contract
        """
        response = await self.bus_client.get(f"/contract/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contracts(self, contract_set: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all active contracts.
        
        Args:
            contract_set: Optional contract set to filter by
            
        Returns:
            List of contracts
            
        Raises:
            RenterdError: If error fetching contracts
        """
        params = {"contractset": contract_set} if contract_set else {}
        response = await self.bus_client.get("/contracts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_roots(self, id: str) -> Dict[str, Any]:
        """Returns contract sector roots.
        
        Args:
            id: Contract ID
            
        Returns:
            Contract roots
            
        Raises:
            RenterdError: If error fetching roots
        """
        response = await self.bus_client.get(f"/contract/{id}/roots")
        response.raise_for_status() 
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_size(self, id: str) -> Dict[str, Any]:
        """Returns contract size info.
        
        Args:
            id: Contract ID
            
        Returns:
            Contract size information
            
        Raises:
            RenterdError: If error fetching size
        """
        response = await self.bus_client.get(f"/contract/{id}/size")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_ancestors(self, id: str) -> List[Dict[str, Any]]:
        """Returns contract ancestors.
        
        Args:
            id: Contract ID
            
        Returns:
            List of ancestor contracts
            
        Raises:
            RenterdError: If error fetching ancestors
        """
        response = await self.bus_client.get(f"/contract/{id}/ancestors")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_contract(self, id: str) -> None:
        """Deletes a contract from the bus.
        
        Args:
            id: Contract ID
            
        Raises:
            RenterdError: If error deleting contract
        """
        response = await self.bus_client.delete(f"/contract/{id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_all_contracts(self) -> None:
        """Deletes all contracts from the bus.
        
        Raises:
            RenterdError: If error deleting contracts
        """
        response = await self.bus_client.delete("/contracts/all")
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def acquire_contract(self, id: str, duration: str, priority: int) -> Dict[str, Any]:
        """Acquires a contract lock.
        
        Args:
            id: Contract ID
            duration: Lock duration
            priority: Lock priority
            
        Returns:
            Lock information
            
        Raises:
            RenterdError: If error acquiring lock
        """
        response = await self.bus_client.post(
            f"/contract/{id}/acquire",
            json={"duration": duration, "priority": priority}
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def keepalive_contract(self, id: str, duration: str, priority: int) -> Dict[str, Any]:
        """Extends contract lock duration.
        
        Args:
            id: Contract ID
            duration: Lock extension duration
            priority: Lock priority
            
        Returns:
            Lock information
            
        Raises:
            RenterdError: If error extending lock
        """
        response = await self.bus_client.post(
            f"/contract/{id}/keepalive",
            json={"duration": duration, "priority": priority}
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def release_contract(self, id: str, lock_id: int) -> None:
        """Releases a contract lock.
        
        Args:
            id: Contract ID
            lock_id: Lock ID to release
            
        Raises:
            RenterdError: If error releasing lock
        """
        response = await self.bus_client.post(
            f"/contract/{id}/release",
            json={"lockID": lock_id}
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_consensus_state(self) -> Dict[str, Any]:
        """Returns consensus state info.
        
        Returns:
            Current consensus state
            
        Raises:
            RenterdError: If error fetching state
        """
        response = await self.bus_client.get("/consensus/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_siafund_fee(self, payout: str) -> str:
        """Returns siafund fee for contract payout.
        
        Args:
            payout: Total contract payout
            
        Returns:
            Calculated fee
            
        Raises:
            RenterdError: If error calculating fee
        """
        response = await self.bus_client.get(f"/consensus/siafundfee/{payout}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def accept_block(self, block: Dict[str, Any]) -> None:
        """Accepts a mined block.
        
        Args:
            block: Block data to accept
            
        Raises:
            RenterdError: If error accepting block
        """
        response = await self.bus_client.post("/consensus/acceptblock", json=block)
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_contracts_prunable(self) -> Dict[str, Any]:
        """Returns contract prunable data information.
        
        Returns:
            Contract prunable info
            
        Raises:
            RenterdError: If error fetching prunable info
        """
        response = await self.bus_client.get("/contracts/prunable")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_renewed(self, id: str) -> Dict[str, Any]:
        """Returns renewed contract information.
        
        Args:
            id: Original contract ID
            
        Returns:
            Renewed contract info if exists
            
        Raises:
            RenterdError: If error fetching renewed contract
        """
        response = await self.bus_client.get(f"/contracts/renewed/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_sets(self) -> List[str]:
        """Returns all contract set names.
        
        Returns:
            List of contract set names
            
        Raises:
            RenterdError: If error fetching contract sets
        """
        response = await self.bus_client.get("/contracts/sets")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_contract_set(self, set_name: str, contract_ids: List[str]) -> None:
        """Updates a contract set.
        
        Args:
            set_name: Set name
            contract_ids: Contract IDs in set
            
        Raises:
            RenterdError: If error updating contract set
        """
        response = await self.bus_client.put(
            f"/contracts/set/{set_name}",
            json=contract_ids
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_contract_set(self, set_name: str) -> None:
        """Deletes a contract set.
        
        Args:
            set_name: Set name
            
        Raises:
            RenterdError: If error deleting contract set
        """
        response = await self.bus_client.delete(f"/contracts/set/{set_name}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def update_contracts_spending(self, spending: List[Dict[str, Any]]) -> None:
        """Updates contract spending information.
        
        Args:
            spending: List of spending updates
            
        Raises:
            RenterdError: If error updating spending
        """
        response = await self.bus_client.post("/contracts/spending", json=spending)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_host(self, pubkey: str) -> Dict[str, Any]:
        """Returns host information.
        
        Args:
            pubkey: Host public key
            
        Returns:
            Host information
            
        Raises:
            RenterdError: If error fetching host info
        """
        response = await self.bus_client.get(f"/host/{pubkey}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def reset_host_lost_sectors(self, pubkey: str) -> None:
        """Resets host lost sector count.
        
        Args:
            pubkey: Host public key
            
        Raises:
            RenterdError: If error resetting lost sectors
        """
        response = await self.bus_client.post(f"/host/{pubkey}/resetlostsectors")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_hosts(self, offset: int = 0, limit: int = -1) -> List[Dict[str, Any]]:
        """Returns all known hosts.
        
        Args:
            offset: Starting offset
            limit: Maximum hosts to return
            
        Returns:
            List of host information
            
        Raises:
            RenterdError: If error fetching hosts
        """
        params = {"offset": offset, "limit": limit}
        response = await self.bus_client.get("/hosts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_host_allowlist(self) -> List[str]:
        """Returns host allowlist.
        
        Returns:
            List of allowed host keys
            
        Raises:
            RenterdError: If error fetching allowlist
        """
        response = await self.bus_client.get("/hosts/allowlist")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_host_allowlist(self, input: Dict[str, Any]) -> None:
        """Updates host allowlist.
        
        Args:
            input: Allowlist update parameters
            
        Raises:
            RenterdError: If error updating allowlist
        """
        response = await self.bus_client.put("/hosts/allowlist", json=input)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_host_blocklist(self) -> List[str]:
        """Returns host blocklist.
        
        Returns:
            List of blocked host addresses
            
        Raises:
            RenterdError: If error fetching blocklist
        """
        response = await self.bus_client.get("/hosts/blocklist")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_host_blocklist(self, input: Dict[str, Any]) -> None:
        """Updates host blocklist.
        
        Args:
            input: Blocklist update parameters
            
        Raises:
            RenterdError: If error updating blocklist
        """
        response = await self.bus_client.put("/hosts/blocklist", json=input)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def record_host_interactions(self, interactions: List[Dict[str, Any]]) -> None:
        """Records host interactions.
        
        Args:
            interactions: List of interactions to record
            
        Raises:
            RenterdError: If error recording interactions
        """
        response = await self.bus_client.post("/hosts/interactions", json=interactions)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_contracts_prunable(self) -> Dict[str, Any]:
        """Returns contract prunable data information.
        
        Returns:
            Contract prunable information
            
        Raises:
            RenterdError: If error fetching data
        """
        response = await self.bus_client.get("/contracts/prunable")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def remove_hosts(self, params: Dict[str, Any]) -> int:
        """Removes hosts matching criteria.
        
        Args:
            params: Removal criteria
            
        Returns:
            Number of hosts removed
            
        Raises:
            RenterdError: If error removing hosts
        """
        response = await self.bus_client.post("/hosts/remove", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_scanning_hosts(
        self, 
        offset: int = 0, 
        limit: int = -1,
        last_scan: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Returns hosts for scanning.
        
        Args:
            offset: Pagination offset
            limit: Pagination limit
            last_scan: Last scan cutoff time
            
        Returns:
            List of hosts
            
        Raises:
            RenterdError: If error fetching hosts
        """
        params = {
            "offset": offset,
            "limit": limit
        }
        if last_scan:
            params["lastScan"] = last_scan
            
        response = await self.bus_client.get("/hosts/scanning", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_metrics(
        self,
        key: str,
        start: str,
        interval: int,
        n: int,
        **filters: Any
    ) -> List[Dict[str, Any]]:
        """Returns metrics history.
        
        Args:
            key: Type of metric to fetch
            start: Start time
            interval: Interval length in ms
            n: Number of intervals
            **filters: Additional metric-specific filters
            
        Returns:
            List of metrics
            
        Raises:
            RenterdError: If error fetching metrics
        """
        params = {
            "start": start,
            "interval": interval,
            "n": n,
            **{k:v for k,v in filters.items() if v is not None}
        }
        response = await self.bus_client.get(f"/metric/{key}", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def delete_metrics(self, key: str, cutoff: str) -> None:
        """Deletes metrics before cutoff.
        
        Args:
            key: Type of metric
            cutoff: Cutoff time
            
        Raises:
            RenterdError: If error deleting metrics
        """
        response = await self.bus_client.delete(
            f"/metric/{key}",
            params={"cutoff": cutoff}
        )
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_host(self, public_key: str) -> Dict[str, Any]:
        """Returns host information.
        
        Args:
            public_key: Host's public key
            
        Returns:
            Host information
            
        Raises:
            RenterdError: If error fetching host
        """
        response = await self.bus_client.get(f"/host/{public_key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_hosts(
        self,
        offset: int = 0,
        limit: int = -1
    ) -> List[Dict[str, Any]]:
        """Returns all known hosts.
        
        Args:
            offset: Pagination offset
            limit: Pagination limit
            
        Returns:
            List of hosts
            
        Raises:
            RenterdError: If error fetching hosts
        """
        params = {"offset": offset, "limit": limit}
        response = await self.bus_client.get("/hosts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_allowlist(self) -> List[str]:
        """Returns current allowlist.
        
        Returns:
            List of allowed host public keys
            
        Raises:
            RenterdError: If error fetching allowlist
        """
        response = await self.bus_client.get("/hosts/allowlist")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_allowlist(self, update: Dict[str, Any]) -> None:
        """Updates host allowlist.
        
        Args:
            update: Allowlist updates
            
        Raises:
            RenterdError: If error updating allowlist
        """
        response = await self.bus_client.put("/hosts/allowlist", json=update)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_blocklist(self) -> List[str]:
        """Returns current blocklist.
        
        Returns:
            List of blocked host addresses
            
        Raises:
            RenterdError: If error fetching blocklist
        """
        response = await self.bus_client.get("/hosts/blocklist")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_blocklist(self, update: Dict[str, Any]) -> None:
        """Updates host blocklist.
        
        Args:
            update: Blocklist updates
            
        Raises:
            RenterdError: If error updating blocklist
        """
        response = await self.bus_client.put("/hosts/blocklist", json=update)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def reset_lost_sectors(self, public_key: str) -> None:
        """Resets host's lost sector count.
        
        Args:
            public_key: Host's public key
            
        Raises:
            RenterdError: If error resetting count
        """
        response = await self.bus_client.post(f"/host/{public_key}/resetlostsectors")
        response.raise_for_status()

    @handle_api_errors(RenterdError) 
    async def record_interactions(self, interactions: List[Dict[str, Any]]) -> None:
        """Records host interactions.
        
        Args:
            interactions: List of interactions to record
            
        Raises:
            RenterdError: If error recording interactions
        """
        response = await self.bus_client.post("/hosts/interactions", json=interactions)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_contract_sets(self) -> List[str]:
        """Returns all contract sets.
        
        Returns:
            List of set names
            
        Raises:
            RenterdError: If error fetching sets 
        """
        response = await self.bus_client.get("/contracts/sets")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_contract_set(
        self, 
        name: str,
        contract_ids: List[str]
    ) -> None:
        """Updates a contract set.
        
        Args:
            name: Set name
            contract_ids: Contract IDs to include
            
        Raises:
            RenterdError: If error updating set
        """
        response = await self.bus_client.put(
            f"/contracts/set/{name}",
            json=contract_ids
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_contract_set(self, name: str) -> None:
        """Deletes a contract set.
        
        Args:
            name: Set name
            
        Raises:
            RenterdError: If error deleting set
        """
        response = await self.bus_client.delete(f"/contracts/set/{name}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_renewed_contract(self, id: str) -> Dict[str, Any]:
        """Returns renewed contract info.
        
        Args:
            id: Original contract ID
            
        Returns:
            Renewed contract info
            
        Raises:
            RenterdError: If error fetching contract
        """
        response = await self.bus_client.get(f"/contracts/renewed/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_contract_spending(
        self, 
        updates: List[Dict[str, Any]]
    ) -> None:
        """Updates contract spending.
        
        Args:
            updates: List of spending updates
            
        Raises:
            RenterdError: If error updating spending
        """
        response = await self.bus_client.post(
            "/contracts/spending",
            json=updates
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def create_multipart_upload(self, upload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates multipart upload.
        
        Args:
            upload: Upload parameters
            
        Returns:
            Upload ID info
            
        Raises:
            RenterdError: If error creating upload
        """
        response = await self.bus_client.post("/multipart/create", json=upload)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def abort_multipart_upload(self, abort: Dict[str, Any]) -> None:
        """Aborts multipart upload.
        
        Args:
            abort: Abort parameters
            
        Raises:
            RenterdError: If error aborting upload
        """
        response = await self.bus_client.post("/multipart/abort", json=abort)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def complete_multipart_upload(self, complete: Dict[str, Any]) -> Dict[str, Any]:
        """Completes multipart upload.
        
        Args:
            complete: Complete parameters
            
        Returns:
            Completion info
            
        Raises:
            RenterdError: If error completing upload
        """
        response = await self.bus_client.post("/multipart/complete", json=complete)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError) 
    async def list_multipart_parts(self, parts: Dict[str, Any]) -> Dict[str, Any]:
        """Lists multipart upload parts.
        
        Args:
            parts: List parameters
            
        Returns:
            Parts list
            
        Raises:
            RenterdError: If error listing parts
        """
        response = await self.bus_client.post("/multipart/listparts", json=parts)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_uploads(self, uploads: Dict[str, Any]) -> Dict[str, Any]:
        """Lists multipart uploads.
        
        Args:
            uploads: List parameters
            
        Returns:
            Uploads list
            
        Raises:
            RenterdError: If error listing uploads
        """
        response = await self.bus_client.post("/multipart/listuploads", json=uploads)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_object(
        self,
        key: str,
        bucket: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gets object metadata.
        
        Args:
            key: Object key
            bucket: Optional bucket name
            
        Returns:
            Object metadata
            
        Raises:
            RenterdError: If error getting object
        """
        params = {"bucket": bucket} if bucket else None
        response = await self.bus_client.get(f"/objects/{key}", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_objects(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Lists objects.
        
        Args:
            params: List parameters
            
        Returns:
            Objects list
            
        Raises:
            RenterdError: If error listing objects
        """
        response = await self.bus_client.post("/objects/list", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_object(
        self,
        key: str,
        object: Dict[str, Any],
        bucket: Optional[str] = None
    ) -> None:
        """Puts object metadata.
        
        Args:
            key: Object key
            object: Object metadata
            bucket: Optional bucket name
            
        Raises:
            RenterdError: If error putting object
        """
        params = {"bucket": bucket} if bucket else None
        response = await self.bus_client.put(f"/objects/{key}", json=object, params=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_object(
        self,
        key: str,
        batch: bool = False, 
        bucket: Optional[str] = None
    ) -> None:
        """Deletes object(s).
        
        Args:
            key: Object key
            batch: If true, deletes all objects with prefix
            bucket: Optional bucket name
            
        Raises:
            RenterdError: If error deleting object(s)
        """
        params = {}
        if batch:
            params["batch"] = "true"
        if bucket:
            params["bucket"] = bucket
        
        response = await self.bus_client.delete(f"/objects/{key}", params=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def copy_object(self, copy: Dict[str, Any]) -> None:
        """Copies object.
        
        Args:
            copy: Copy parameters
            
        Raises:
            RenterdError: If error copying object
        """
        response = await self.bus_client.post("/objects/copy", json=copy)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def rename_object(self, rename: Dict[str, Any]) -> None:
        """Renames object(s).
        
        Args:
            rename: Rename parameters
            
        Raises:
            RenterdError: If error renaming object(s)
        """
        response = await self.bus_client.post("/objects/rename", json=rename)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_download_params(self) -> Dict[str, Any]:
        """Gets download parameters.
        
        Returns:
            Download parameters
            
        Raises:
            RenterdError: If error getting parameters
        """
        response = await self.bus_client.get("/params/download")
        response.raise_for_status()
        return response.json()


    @handle_api_errors(RenterdError)
    async def get_download_params(self) -> Dict[str, Any]:
        """Returns download parameters.
        
        Returns:
            Download parameters
            
        Raises:
            RenterdError: If error fetching parameters
        """
        response = await self.bus_client.get("/params/download")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_upload_params(self) -> Dict[str, Any]:
        """Returns upload parameters.
        
        Returns:
            Upload parameters
            
        Raises:
            RenterdError: If error fetching parameters
        """
        response = await self.bus_client.get("/params/upload") 
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_gouging_params(self) -> Dict[str, Any]:
        """Returns gouging parameters.
        
        Returns:
            Gouging parameters
            
        Raises:
            RenterdError: If error fetching parameters
        """
        response = await self.bus_client.get("/params/gouging")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_settings(self) -> List[str]:
        """Returns available settings keys.
        
        Returns:
            List of setting keys
            
        Raises:
            RenterdError: If error fetching settings
        """
        response = await self.bus_client.get("/settings")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_setting(self, key: str) -> Any:
        """Returns setting value.
        
        Args:
            key: Setting key
            
        Returns:
            Setting value
            
        Raises:
            RenterdError: If error fetching setting
        """
        response = await self.bus_client.get(f"/setting/{key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_setting(self, key: str, value: Any) -> None:
        """Updates setting value.
        
        Args:
            key: Setting key
            value: New setting value
            
        Raises:
            RenterdError: If error updating setting
        """
        response = await self.bus_client.put(f"/setting/{key}", json=value)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_setting(self, key: str) -> None:
        """Deletes setting.
        
        Args:
            key: Setting key
            
        Raises:
            RenterdError: If error deleting setting
        """
        response = await self.bus_client.delete(f"/setting/{key}")
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_state(self) -> Dict[str, Any]:
        """Returns bus state info.
        
        Returns:
            State information
            
        Raises:
            RenterdError: If error fetching state
        """
        response = await self.bus_client.get("/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_syncer_address(self) -> str:
        """Returns syncer listening address.
        
        Returns:
            Listening address
            
        Raises:
            RenterdError: If error fetching address
        """
        response = await self.bus_client.get("/syncer/address")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_syncer_peers(self) -> List[str]:
        """Returns connected peers.
        
        Returns:
            List of peer addresses
            
        Raises:
            RenterdError: If error fetching peers
        """
        response = await self.bus_client.get("/syncer/peers")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def connect_peer(self, address: str) -> None:
        """Connects to peer.
        
        Args:
            address: Peer address
            
        Raises:
            RenterdError: If error connecting
        """
        response = await self.bus_client.post("/syncer/connect", json=address)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def broadcast_transaction(self, transaction: Dict[str, Any]) -> None:
        """Broadcasts transaction.
        
        Args:
            transaction: Transaction to broadcast
            
        Raises:
            RenterdError: If error broadcasting
        """
        response = await self.bus_client.post("/txpool/broadcast", json=transaction)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_recommended_fee(self) -> str:
        """Returns recommended transaction fee.
        
        Returns:
            Recommended fee per byte
            
        Raises:
            RenterdError: If error fetching fee
        """
        response = await self.bus_client.get("/txpool/recommendedfee")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_object_stats(self, bucket: Optional[str] = None) -> Dict[str, Any]:
        """Returns object statistics.
        
        Args:
            bucket: Optional bucket name
            
        Returns:
            Object statistics
            
        Raises:
            RenterdError: If error fetching stats
        """
        params = {"bucket": bucket} if bucket else None
        response = await self.bus_client.get("/stats/objects", params=params)
        response.raise_for_status()
        return response.json()


    @handle_api_errors(RenterdError)
    async def get_slab_migrations(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Returns slabs needing migration.
        
        Args:
            params: Migration parameters
            
        Returns:
            List of slabs to migrate
            
        Raises:
            RenterdError: If error fetching migrations
        """
        response = await self.bus_client.post("/slabs/migration", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_partial_slab(
        self, 
        key: str,
        offset: int,
        length: int
    ) -> Optional[Dict[str, Any]]:
        """Returns partial slab data.
        
        Args:
            key: Slab key
            offset: Range start offset
            length: Range length
            
        Returns:
            Partial slab if found
            
        Raises:
            RenterdError: If error fetching slab
        """
        params = {"offset": offset, "length": length}
        response = await self.bus_client.get(f"/slabs/partial/{key}", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def add_partial_slab(
        self,
        min_shards: int,
        total_shards: int,
        contract_set: str
    ) -> Dict[str, Any]:
        """Adds partial slab.
        
        Args:
            min_shards: Minimum shards required
            total_shards: Total shards to create
            contract_set: Contract set to use
            
        Returns:
            Result with slab info and buffer state
            
        Raises:
            RenterdError: If error adding slab
        """
        params = {
            "minShards": min_shards,
            "totalShards": total_shards,
            "contractSet": contract_set
        }
        response = await self.bus_client.post("/slabs/partial", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_slab(self, key: str) -> Optional[Dict[str, Any]]:
        """Returns slab data.
        
        Args:
            key: Slab key
            
        Returns:
            Slab if found
            
        Raises: 
            RenterdError: If error fetching slab
        """
        response = await self.bus_client.get(f"/slab/{key}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_slab_objects(self, key: str) -> List[str]:
        """Returns objects using slab.
        
        Args:
            key: Slab key
            
        Returns:
            List of object paths
            
        Raises:
            RenterdError: If error fetching objects
        """
        response = await self.bus_client.get(f"/slab/{key}/objects")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def update_slab(
        self,
        contract_set: str,
        slab: Dict[str, Any],
        used_contracts: Dict[str, str]
    ) -> None:
        """Updates slab metadata.
        
        Args:
            contract_set: Contract set name
            slab: Updated slab data
            used_contracts: Contract mapping
            
        Raises:
            RenterdError: If error updating slab
        """
        data = {
            "contractSet": contract_set,
            "slab": slab,
            "usedContracts": used_contracts
        }
        response = await self.bus_client.put("/slab", json=data)
        response.raise_for_status()

    @handle_api_errors(RenterdError) 
    async def refresh_health(self) -> None:
        """Refreshes health of all slabs.
        
        Raises:
            RenterdError: If error refreshing health
        """
        response = await self.bus_client.post("/slabs/refreshhealth")
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_object(
        self,
        path: str,
        bucket: Optional[str] = None
    ) -> Dict[str, Any]:
        """Returns object metadata.
        
        Args:
            path: Object path
            bucket: Optional bucket name
            
        Returns:
            Object metadata
            
        Raises:
            RenterdError: If error fetching object
        """
        params = {"bucket": bucket} if bucket else None
        response = await self.bus_client.get(f"/objects/{path}", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_objects(
        self,
        bucket: str,
        limit: int,
        prefix: str = "",
        marker: str = ""
    ) -> Dict[str, Any]:
        """Lists objects from bucket.
        
        Args:
            bucket: Bucket name
            limit: Max objects to return
            prefix: Object name prefix filter
            marker: Pagination marker
            
        Returns:
            Object listing with pagination info
            
        Raises:
            RenterdError: If error listing objects
        """
        data = {
            "bucket": bucket,
            "limit": limit,
            "prefix": prefix,
            "marker": marker
        }
        response = await self.bus_client.post("/objects/list", json=data)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_object(
        self,
        path: str,
        object: Dict[str, Any],
        bucket: Optional[str] = None
    ) -> None:
        """Stores object metadata.
        
        Args:
            path: Object path
            object: Object metadata
            bucket: Optional bucket name
            
        Raises:
            RenterdError: If error storing object
        """ 
        params = {"bucket": bucket} if bucket else None
        response = await self.bus_client.put(f"/objects/{path}", params=params, json=object)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_object(
        self,
        path: str,
        batch: bool = False,
        bucket: Optional[str] = None
    ) -> None:
        """Deletes object(s).
        
        Args:
            path: Object path
            batch: If true, deletes all objects starting with path
            bucket: Optional bucket name
            
        Raises:
            RenterdError: If error deleting object(s)
        """
        params = {}
        if batch:
            params["batch"] = "true"
        if bucket:
            params["bucket"] = bucket
            
        response = await self.bus_client.delete(f"/objects/{path}", params=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def copy_object(self, params: Dict[str, Any]) -> None:
        """Copies object between paths/buckets.
        
        Args:
            params: Copy parameters containing source and destination
            
        Raises:
            RenterdError: If error copying object
        """
        response = await self.bus_client.post("/objects/copy", json=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def rename_object(self, params: Dict[str, Any]) -> None:
        """Renames object or objects.
        
        Args:
            params: Rename parameters
            
        Raises:
            RenterdError: If error renaming object(s)
        """
        response = await self.bus_client.post("/objects/rename", json=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def search_objects(
        self,
        key: str,
        offset: int = 0,
        limit: Optional[int] = None,
        bucket: Optional[str] = None
    ) -> List[str]:
        """Searches for objects containing key.
        
        Args:
            key: Search string
            offset: Pagination offset
            limit: Max results to return
            bucket: Optional bucket to search in
            
        Returns:
            List of matching object paths
            
        Raises:
            RenterdError: If error searching objects
        """
        params = {"key": key, "offset": offset}
        if limit is not None:
            params["limit"] = limit
        if bucket:
            params["bucket"] = bucket
            
        response = await self.bus_client.get("/search/objects", params=params)
        response.raise_for_status()
        return response.json()


    # api/renterd.py - Multipart Handlers

    @handle_api_errors(RenterdError)
    async def create_multipart_upload(
        self,
        bucket: str,
        path: str,
        key: Optional[str] = None,
        generate_key: bool = False
    ) -> Dict[str, str]:
        """Creates new multipart upload.
        
        Args:
            bucket: Bucket name
            path: Object path
            key: Optional encryption key
            generate_key: Whether to generate random key
            
        Returns:
            Upload ID
            
        Raises:
            RenterdError: If error creating upload
        """
        data = {
            "bucket": bucket,
            "path": path,
            "generateKey": generate_key
        }
        if key:
            data["key"] = key
            
        response = await self.bus_client.post("/multipart/create", json=data)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def complete_multipart_upload(self, params: Dict[str, Any]) -> Dict[str, str]:
        """Completes multipart upload.
        
        Args:
            params: Completion parameters
            
        Returns:
            Final object ETag
            
        Raises:
            RenterdError: If error completing upload
        """
        response = await self.bus_client.post("/multipart/complete", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def abort_multipart_upload(
        self,
        bucket: str,
        path: str,
        upload_id: str
    ) -> None:
        """Aborts multipart upload.
        
        Args:
            bucket: Bucket name
            path: Object path
            upload_id: Upload ID
            
        Raises:
            RenterdError: If error aborting upload
        """
        data = {
            "bucket": bucket,
            "path": path,
            "uploadID": upload_id
        }
        response = await self.bus_client.post("/multipart/abort", json=data)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def list_multipart_parts(
        self,
        bucket: str,
        path: str, 
        upload_id: str,
        part_number_marker: int = 0,
        limit: int = 1000
    ) -> Dict[str, Any]:
        """Lists parts of multipart upload.
        
        Args:
            bucket: Bucket name
            path: Object path
            upload_id: Upload ID
            part_number_marker: Part number to start from
            limit: Max parts to return
            
        Returns:
            Parts listing with pagination info
            
        Raises:
            RenterdError: If error listing parts
        """
        data = {
            "bucket": bucket,
            "path": path,
            "uploadID": upload_id,
            "partNumberMarker": part_number_marker,
            "limit": limit
        }
        response = await self.bus_client.post("/multipart/listparts", json=data)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_uploads(
        self,
        bucket: str,
        prefix: str = "",
        path_marker: str = "",
        upload_id_marker: str = "",
        limit: int = 1000
    ) -> Dict[str, Any]:
        """Lists all multipart uploads.
        
        Args:
            bucket: Bucket name
            prefix: Path prefix filter
            path_marker: Path pagination marker
            upload_id_marker: Upload ID pagination marker
            limit: Max uploads to return
            
        Returns:
            Uploads listing
            
        Raises:
            RenterdError: If error listing uploads
        """
        data = {
            "bucket": bucket,
            "prefix": prefix,
            "pathMarker": path_marker,
            "uploadIDMarker": upload_id_marker,
            "limit": limit
        }
        response = await self.bus_client.post("/multipart/listuploads", json=data)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def put_multipart_part(self, params: Dict[str, Any]) -> None:
        """Adds part to multipart upload.
        
        Args:
            params: Part parameters
            
        Raises:
            RenterdError: If error adding part
        """
        response = await self.bus_client.put("/multipart/part", json=params)
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_wallet_info(self) -> Dict[str, Any]:
        """Returns wallet info.
        
        Returns:
            Wallet information
            
        Raises:
            RenterdError: If error fetching info
        """
        response = await self.bus_client.get("/wallet")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_address(self) -> str:
        """Returns wallet address.
        
        Returns:
            Wallet address
            
        Raises:
            RenterdError: If error fetching address
        """
        response = await self.bus_client.get("/wallet/address") 
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_balance(self) -> str:
        """Returns wallet balance.
        
        Returns:
            Current balance
            
        Raises:
            RenterdError: If error fetching balance
        """
        response = await self.bus_client.get("/wallet/balance")
        response.raise_for_status() 
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_outputs(self) -> List[Dict[str, Any]]:
        """Returns wallet outputs.
        
        Returns:
            List of outputs
            
        Raises:
            RenterdError: If error fetching outputs
        """
        response = await self.bus_client.get("/wallet/outputs")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_wallet_transactions(self) -> List[Dict[str, Any]]:
        """Returns wallet transactions.
        
        Returns:
            List of transactions
            
        Raises:
            RenterdError: If error fetching transactions
        """ 
        response = await self.bus_client.get("/wallet/transactions")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_txpool_transactions(self) -> List[Dict[str, Any]]:
        """Returns txpool transactions.
        
        Returns:
            List of unconfirmed transactions
            
        Raises:
            RenterdError: If error fetching transactions
        """
        response = await self.bus_client.get("/txpool/transactions")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_webhooks(self) -> Dict[str, Any]:
        """Returns webhook info.
        
        Returns:
            Webhook information
            
        Raises:
            RenterdError: If error fetching webhooks
        """
        response = await self.bus_client.get("/webhooks")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def register_webhook(self, webhook: Dict[str, Any]) -> None:
        """Registers webhook.
        
        Args:
            webhook: Webhook details
            
        Raises:
            RenterdError: If error registering webhook
        """
        response = await self.bus_client.post("/webhooks", json=webhook)
        response.raise_for_status()

    @handle_api_errors(RenterdError) 
    async def delete_webhook(self, webhook: Dict[str, Any]) -> None:
        """Deletes webhook.
        
        Args:
            webhook: Webhook to delete
            
        Raises:
            RenterdError: If error deleting webhook
        """
        response = await self.bus_client.post("/webhook/delete", json=webhook)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def trigger_webhook(self, action: Dict[str, Any]) -> None:
        """Triggers webhook action.
        
        Args:
            action: Action details
            
        Raises: 
            RenterdError: If error triggering action
        """
        response = await self.bus_client.post("/webhooks/action", json=action)
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def redistribute_wallet(
        self,
        amount: str,
        outputs: int
    ) -> List[str]:
        """Redistributes wallet funds.
        
        Args:
            amount: Amount to redistribute
            outputs: Number of outputs to create
            
        Returns:
            Transaction IDs
            
        Raises:
            RenterdError: If error redistributing
        """
        body = {
            "amount": amount,
            "outputs": outputs
        }
        response = await self.bus_client.post("/wallet/redistribute", json=body)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def sign_transaction(
        self,
        transaction: Dict[str, Any],
        to_sign: List[str],
        covered_fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Signs a transaction.
        
        Args:
            transaction: Transaction to sign
            to_sign: Fields to sign
            covered_fields: Fields covered by signatures
            
        Returns:
            Signed transaction
            
        Raises:
            RenterdError: If error signing
        """
        body = {
            "transaction": transaction,
            "toSign": to_sign,
            "coveredFields": covered_fields
        }
        response = await self.bus_client.post("/wallet/sign", json=body)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def prepare_contract_formation(
        self,
        params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Prepares contract formation.
        
        Args:
            params: Formation parameters
            
        Returns:
            Prepared transactions
            
        Raises:
            RenterdError: If error preparing
        """
        response = await self.bus_client.post("/wallet/prepare/form", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def prepare_contract_renewal(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepares contract renewal.
        
        Args:
            params: Renewal parameters
            
        Returns:
            Prepared transaction data
            
        Raises:
            RenterdError: If error preparing
        """
        response = await self.bus_client.post("/wallet/prepare/renew", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def discard_transaction(
        self,
        transaction: Dict[str, Any]
    ) -> None:
        """Discards a transaction.
        
        Args:
            transaction: Transaction to discard
            
        Raises:
            RenterdError: If error discarding
        """
        response = await self.bus_client.post("/wallet/discard", json=transaction)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def fund_transaction(
        self,
        transaction: Dict[str, Any],
        amount: str
    ) -> Dict[str, Any]:
        """Funds a transaction.
        
        Args:
            transaction: Transaction to fund
            amount: Amount to fund
            
        Returns:
            Funded transaction
            
        Raises:
            RenterdError: If error funding
        """
        body = {
            "transaction": transaction,
            "amount": amount
        }
        response = await self.bus_client.post("/wallet/fund", json=body)
        response.raise_for_status()
        return response.json()



    # api/renterd.py - Multipart and Upload Operations

    @handle_api_errors(RenterdError)
    async def abort_multipart_upload(self, params: Dict[str, Any]) -> None:
        """Aborts a multipart upload.
        
        Args:
            params: Upload to abort
            
        Raises:
            RenterdError: If error aborting upload
        """
        response = await self.bus_client.post("/multipart/abort", json=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def list_multipart_parts(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Lists multipart upload parts.
        
        Args:
            params: Parameters for listing parts
            
        Returns:
            Parts information
            
        Raises:
            RenterdError: If error listing parts
        """
        response = await self.bus_client.post("/multipart/listparts", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError) 
    async def list_multipart_uploads(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Lists unfinished multipart uploads.
        
        Args:
            params: Parameters for listing uploads
            
        Returns:
            List of uploads
            
        Raises:
            RenterdError: If error listing uploads
        """
        response = await self.bus_client.post("/multipart/listuploads", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def create_multipart_upload(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Creates multipart upload.
        
        Args:
            params: Upload creation parameters
            
        Returns:
            Upload creation response
            
        Raises:
            RenterdError: If error creating upload
        """
        response = await self.bus_client.post("/multipart/create", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def complete_multipart_upload(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Completes multipart upload.
        
        Args:
            params: Upload completion parameters
            
        Returns:
            Upload completion response
            
        Raises:
            RenterdError: If error completing upload
        """
        response = await self.bus_client.post("/multipart/complete", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def register_upload(self, id: str) -> None:
        """Registers an upload.
        
        Args:
            id: Upload ID
            
        Raises:
            RenterdError: If error registering
        """
        response = await self.bus_client.post(f"/upload/{id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def unregister_upload(self, id: str) -> None:
        """Unregisters an upload.
        
        Args:
            id: Upload ID
            
        Raises:
            RenterdError: If error unregistering
        """
        response = await self.bus_client.delete(f"/upload/{id}")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def register_upload_sector(
        self,
        id: str,
        sector: Dict[str, Any]
    ) -> None:
        """Registers upload sector.
        
        Args:
            id: Upload ID
            sector: Sector information
            
        Raises:
            RenterdError: If error registering sector
        """
        response = await self.bus_client.post(f"/upload/{id}/sector", json=sector)
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def list_objects(
        self,
        params: Dict[str, Any],
        path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Lists objects or gets single object info.
        
        Args:
            params: Listing parameters
            path: Optional object path
            
        Returns:
            Object listing or info
            
        Raises:
            RenterdError: If error listing objects
        """
        query_params = {
            k: v for k, v in params.items() 
            if v is not None
        }
        
        if path:
            response = await self.bus_client.get(
                f"/objects/{path}",
                params=query_params
            )
        else:
            response = await self.bus_client.post(
                "/objects/list",
                json=params
            )
            
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def store_object(
        self,
        input: Dict[str, Any],
        path: str
    ) -> None:
        """Stores object metadata.
        
        Args:
            input: Object metadata
            path: Object path
            
        Raises:
            RenterdError: If error storing object
        """
        response = await self.bus_client.put(f"/objects/{path}", json=input)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_object(
        self,
        path: str,
        bucket: str = "default",
        batch: bool = False
    ) -> None:
        """Deletes object(s).
        
        Args:
            path: Object path
            bucket: Bucket name
            batch: Whether to delete by prefix
            
        Raises:
            RenterdError: If error deleting
        """
        params = {
            "bucket": bucket,
            "batch": batch
        }
        response = await self.bus_client.delete(f"/objects/{path}", params=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def copy_object(self, params: Dict[str, Any]) -> None:
        """Copies an object.
        
        Args:
            params: Copy parameters
            
        Raises:
            RenterdError: If error copying
        """
        response = await self.bus_client.post("/objects/copy", json=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def rename_object(self, params: Dict[str, Any]) -> None:
        """Renames object(s).
        
        Args:
            params: Rename parameters
            
        Raises:
            RenterdError: If error renaming
        """
        response = await self.bus_client.post("/objects/rename", json=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_consensus_state(self) -> Dict[str, Any]:
        """Returns consensus state.
        
        Returns:
            Current state
            
        Raises:
            RenterdError: If error getting state
        """
        response = await self.bus_client.get("/consensus/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_download_params(self) -> Dict[str, Any]:
        """Returns download parameters.
        
        Returns:
            Default parameters
            
        Raises:
            RenterdError: If error getting parameters
        """
        response = await self.bus_client.get("/params/download")
        response.raise_for_status()
        return response.json()


    @handle_api_errors(RenterdError)
    async def create_multipart_upload(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new multipart upload.
        
        Args:
            input: Upload parameters including bucket, path, key
            
        Returns:
            Upload ID for the new multipart upload
            
        Raises:
            RenterdError: If error creating upload
        """
        response = await self.worker_client.post("/multipart/create", json=input)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError) 
    async def abort_multipart_upload(self, input: Dict[str, Any]) -> None:
        """Aborts an unfinished multipart upload.
        
        Args:
            input: Upload details to abort
            
        Raises:
            RenterdError: If error aborting upload
        """
        response = await self.worker_client.post("/multipart/abort", json=input)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def complete_multipart_upload(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Completes a multipart upload.
        
        Args:
            input: Upload details and parts to complete
            
        Returns:
            ETag of completed upload
            
        Raises:
            RenterdError: If error completing upload
        """
        response = await self.worker_client.post("/multipart/complete", json=input)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_parts(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Lists parts in a multipart upload.
        
        Args:
            input: Upload and pagination parameters
            
        Returns:
            List of upload parts
            
        Raises:
            RenterdError: If error listing parts
        """
        response = await self.worker_client.post("/multipart/listparts", json=input)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def list_multipart_uploads(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Lists all unfinished multipart uploads.
        
        Args:
            input: Bucket and pagination parameters
            
        Returns:
            List of unfinished uploads
            
        Raises:
            RenterdError: If error listing uploads
        """
        response = await self.worker_client.post("/multipart/listuploads", json=input)
        response.raise_for_status()
        return response.json()


    @handle_api_errors(RenterdError)
    async def get_worker_state(self) -> Dict[str, Any]:
        """Gets worker state information.
        
        Returns:
            Worker state details
            
        Raises:
            RenterdError: If error fetching state
        """
        response = await self.worker_client.get("/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_memory(self) -> Dict[str, Any]:
        """Gets worker memory statistics.
        
        Returns:
            Memory usage details
            
        Raises:
            RenterdError: If error fetching memory stats
        """
        response = await self.worker_client.get("/memory")  
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_worker_id(self) -> str:
        """Gets worker's unique identifier.
        
        Returns:
            Worker ID string
            
        Raises:
            RenterdError: If error fetching ID
        """
        response = await self.worker_client.get("/id")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def trigger_maintenance(self, force_scan: bool = False) -> str:
        """Triggers maintenance iteration.
        
        Args:
            force_scan: Whether to force host scanning
            
        Returns:
            Trigger result message
            
        Raises:
            RenterdError: If error triggering maintenance
        """
        response = await self.worker_client.post(
            "/trigger",
            json={"forceScan": force_scan}
        )
        response.raise_for_status()
        return response.json()


    @handle_api_errors(RenterdError)
    async def list_objects(
        self,
        bucket: Optional[str] = None,
        prefix: Optional[str] = None,
        marker: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = -1
    ) -> List[Dict[str, Any]]:
        """Lists objects matching criteria.
        
        Args:
            bucket: Optional bucket name
            prefix: Optional prefix filter
            marker: Optional pagination marker
            offset: Optional pagination offset
            limit: Optional page size limit
            
        Returns:
            List of matching objects
            
        Raises:
            RenterdError: If error listing objects
        """
        params = {
            "bucket": bucket,
            "prefix": prefix,
            "marker": marker,
            "offset": offset,
            "limit": limit
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        response = await self.worker_client.get("/objects/", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def rename_object(
        self,
        from_path: str,
        to_path: str,
        bucket: Optional[str] = None,
        mode: str = "single"
    ) -> None:
        """Renames an object.
        
        Args:
            from_path: Current object path
            to_path: New object path
            bucket: Optional bucket name
            mode: Rename mode ('single' or 'multi')
            
        Raises:
            RenterdError: If error renaming object
        """
        data = {
            "from": from_path,
            "to": to_path,
            "mode": mode
        }
        params = {"bucket": bucket} if bucket else {}
        
        response = await self.worker_client.post(
            "/objects/rename",
            json=data,
            params=params
        )
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def delete_object(
        self,
        path: str,
        bucket: Optional[str] = None, 
        batch: bool = False
    ) -> None:
        """Deletes an object.
        
        Args:
            path: Object path to delete
            bucket: Optional bucket name
            batch: Whether to delete multiple objects matching prefix
            
        Raises:
            RenterdError: If error deleting object
        """
        params = {
            "bucket": bucket,
            "batch": str(batch).lower()
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        response = await self.worker_client.delete(
            f"/objects/{path}",
            params=params
        )
        response.raise_for_status()


    @handle_api_errors(RenterdError)
    async def get_rhp_contracts(self, host_timeout: Optional[int] = None) -> Dict[str, Any]:
        """Returns all active contracts with revisions.
        
        Args:
            host_timeout: Per-host timeout in ms
            
        Returns:
            Active contracts with revisions
            
        Raises:
            RenterdError: If error fetching contracts
        """
        params = {}
        if host_timeout is not None:
            params["hosttimeout"] = host_timeout
            
        response = await self.worker_client.get("/rhp/contracts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def broadcast_contract(self, id: str) -> None:
        """Broadcasts contract revision.
        
        Args:
            id: Contract ID
            
        Raises:
            RenterdError: If error broadcasting
        """
        response = await self.worker_client.post(f"/rhp/contract/{id}/broadcast")
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def prune_contract(self, id: str, timeout: int) -> Dict[str, Any]:
        """Prunes contract data.
        
        Args:
            id: Contract ID
            timeout: Operation timeout in ns
            
        Returns:
            Pruning results
            
        Raises:
            RenterdError: If error pruning
        """
        response = await self.worker_client.post(
            f"/rhp/contract/{id}/prune",
            json={"timeout": timeout}
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_contract_roots(self, id: str) -> List[str]:
        """Returns contract sector roots.
        
        Args:
            id: Contract ID
            
        Returns:
            List of root hashes
            
        Raises:
            RenterdError: If error fetching roots
        """
        response = await self.worker_client.post(f"/rhp/contract/{id}/roots")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def form_contract(
        self,
        end_height: int,
        host_collateral: str,
        host_key: str,
        host_ip: str,
        renter_funds: str,
        renter_address: str
    ) -> Dict[str, Any]:
        """Forms new contract.
        
        Args:
            end_height: Contract end height
            host_collateral: Host collateral amount
            host_key: Host public key
            host_ip: Host IP address
            renter_funds: Renter funds amount
            renter_address: Renter address
            
        Returns:
            Formed contract details
            
        Raises:
            RenterdError: If error forming contract
        """
        data = {
            "endHeight": end_height,
            "hostCollateral": host_collateral,
            "hostKey": host_key,
            "hostIP": host_ip,
            "renterFunds": renter_funds,
            "renterAddress": renter_address
        }
        response = await self.worker_client.post("/rhp/form", json=data)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def fund_account(self, params: Dict[str, Any]) -> None:
        """Fund an ephemeral account.
        
        Args:
            params: Account funding parameters
            
        Raises:
            RenterdError: If error funding account
        """
        response = await self.worker_client.post("/rhp/fund", json=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def renew_contract(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Renew a contract.
        
        Args:
            params: Contract renewal parameters
            
        Returns:
            Renewed contract details
            
        Raises:
            RenterdError: If error renewing contract
        """
        response = await self.worker_client.post("/rhp/renew", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def scan_host(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Scan a host.
        
        Args:
            params: Host scanning parameters
            
        Returns:
            Host scan results
            
        Raises:
            RenterdError: If error scanning host
        """
        response = await self.worker_client.post("/rhp/scan", json=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def sync_account(self, params: Dict[str, Any]) -> None:
        """Sync ephemeral account.
        
        Args:
            params: Account sync parameters
            
        Raises:
            RenterdError: If error syncing account
        """
        response = await self.worker_client.post("/rhp/sync", json=params)
        response.raise_for_status()

    @handle_api_errors(RenterdError)
    async def get_worker_state(self) -> Dict[str, Any]:
        """Get worker state.
        
        Returns:
            Worker state information
            
        Raises:
            RenterdError: If error fetching state
        """
        response = await self.worker_client.get("/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_download_stats(self) -> Dict[str, Any]:
        """Get download statistics.
        
        Returns:
            Download stats
            
        Raises:
            RenterdError: If error fetching stats
        """
        response = await self.worker_client.get("/stats/downloads")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(RenterdError)
    async def get_upload_stats(self) -> Dict[str, Any]:
        """Get upload statistics.
        
        Returns:
            Upload stats
            
        Raises:
            RenterdError: If error fetching stats
        """
        response = await self.worker_client.get("/stats/uploads")
        response.raise_for_status()
        return response.json()
