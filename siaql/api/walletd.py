# siaql/siaql/api/walletd.py
from typing import Dict, List, Optional, Any
import httpx
from datetime import datetime
from siaql.api.utils import handle_api_errors, APIError

class WalletdError(APIError):
    """Specific exception for Walletd API errors"""
    pass


class WalletdClient:
    def __init__(
        self, 
        base_url: str = "http://localhost:9980",
        api_password: Optional[str] = None
    ):
        # Ensure base_url doesn't have trailing slash and has /api
        self.base_url = f"{base_url.rstrip('/')}/api"
        if api_password:
            auth = httpx.BasicAuth(username="", password=api_password)
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                auth=auth,
                timeout=30.0
            )
        else:
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0
            )

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    @handle_api_errors(WalletdError)
    async def get_address_balance(self, address: str) -> Dict[str, Any]:
        """Get balance of an individual address"""
        url = f"/addresses/{address}/balance"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_address_events(
        self, 
        address: str, 
        limit: Optional[int] = 100,
        offset: Optional[int] = 0
    ) -> List[Dict[str, Any]]:
        """Get events for a specific address"""
        params = {"limit": limit, "offset": offset}
        response = await self.client.get(
            f"/addresses/{address}/events",
            params=params
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_address_unconfirmed_events(
        self, 
        address: str, 
        limit: Optional[int] = 100,
        offset: Optional[int] = 0
    ) -> List[Dict[str, Any]]:
        """Get unconfirmed events for a specific address"""
        params = {"limit": limit, "offset": offset}
        response = await self.client.get(
            f"/addresses/{address}/events/unconfirmed",
            params=params
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_address_siacoin_outputs(
        self, 
        address: str, 
        limit: Optional[int] = 100,
        offset: Optional[int] = 0
    ) -> List[Dict[str, Any]]:
        """Get Siacoin UTXOs owned by the address"""
        params = {"limit": limit, "offset": offset}
        response = await self.client.get(
            f"/addresses/{address}/outputs/siacoin",
            params=params
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_address_siafund_outputs(
        self, 
        address: str, 
        limit: Optional[int] = 10,
        offset: Optional[int] = 0
    ) -> List[Dict[str, Any]]:
        """Get Siafund UTXOs owned by the address"""
        params = {"limit": limit, "offset": offset}
        response = await self.client.get(
            f"/addresses/{address}/outputs/siafund",
            params=params
        )
        response.raise_for_status()
        return response.json()

    # Consensus endpoints
    @handle_api_errors(WalletdError)
    async def get_consensus_network(self) -> Dict[str, Any]:
        """Returns the current network parameters"""
        response = await self.client.get("/consensus/network")
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors(WalletdError)
    async def get_consensus_tip(self) -> Dict[str, Any]:
        """Returns the height and ID of the current block"""
        response = await self.client.get("/consensus/tip")
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors(WalletdError)
    async def get_consensus_tipstate(self) -> Dict[str, Any]:
        """Returns the current consensus state"""
        response = await self.client.get("/consensus/tipstate")
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors(WalletdError)
    async def get_consensus_index(self, height: int) -> Dict[str, Any]:
        """Returns the chain index at a specified height"""
        response = await self.client.get(f"/consensus/index/{height}")
        response.raise_for_status()
        return response.json()

    # Syncer endpoints
    @handle_api_errors(WalletdError)
    async def get_syncer_peers(self) -> List[Dict[str, Any]]:
        """Returns a list of all connected peers and metadata associated with them"""
        response = await self.client.get("/syncer/peers")
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors(WalletdError)
    async def connect_syncer_peer(self, address: str) -> None:
        """Connect to a new peer"""
        response = await self.client.post("/syncer/connect", json=address)
        response.raise_for_status()

    # Transaction pool endpoints
    @handle_api_errors(WalletdError)
    async def get_txpool_transactions(self) -> Dict[str, Any]:
        """Returns all transactions currently in the transaction pool"""
        response = await self.client.get("/txpool/transactions")
        response.raise_for_status()
        return response.json()
    
    @handle_api_errors(WalletdError)
    async def get_txpool_fee(self) -> str:
        """Returns the current fee to broadcast a transaction in Hastings per byte"""
        response = await self.client.get("/txpool/fee")
        response.raise_for_status()
        # API returns the fee as a JSON string, so we need to parse it
        return response.json()
    
    @handle_api_errors(WalletdError)
    async def broadcast_transaction_set(
        self,
        transactions: Optional[List[Dict[str, Any]]] = None,
        v2transactions: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """Broadcasts a set of transactions to the network.
        
        Args:
            transactions: List of v1 transactions to broadcast
            v2transactions: List of v2 transactions to broadcast
        
        Returns:
            None on success, raises WalletdError on failure
        """
        payload = {
            "transactions": transactions or [],
            "v2transactions": v2transactions or []
        }
        response = await self.client.post("/txpool/broadcast", json=payload)
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def get_event(self, event_id: str) -> Dict[str, Any]:
        """Returns data on a confirmed event"""
        response = await self.client.get(f"/events/{event_id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_state(self) -> Dict[str, Any]:
        """Gets the current state of the running walletd node"""
        response = await self.client.get("/state")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallets(self) -> List[Dict[str, Any]]:
        """Returns a list of all created wallets.
        
        Returns:
            List of wallet objects containing id, name, description, creation date,
            last update date, and metadata.
        """
        response = await self.client.get("/wallets")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def add_wallet(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Adds a new wallet.
        
        Args:
            name: Optional name for the wallet
            description: Optional description for the wallet
            metadata: Optional metadata for the wallet
            
        Returns:
            Dict containing the created wallet information
        """
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if metadata is not None:
            payload["metadata"] = metadata
            
        response = await self.client.post("/wallets", json=payload)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_addresses(self, wallet_id: str) -> List[Dict[str, Any]]:
        """Returns a list of addresses associated with the wallet.
        
        Args:
            wallet_id: ID of the wallet to get addresses for
            
        Returns:
            List of address objects containing the address string, description,
            and optional metadata.
            
        Raises:
            WalletdError: If the wallet is not found or other API error occurs
        """
        response = await self.client.get(f"/wallets/{wallet_id}/addresses")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def add_wallet_address(
        self,
        wallet_id: str,
        address: str,
        description: Optional[str] = None,
        spend_policy: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Adds an address for the wallet to watch.
        
        Args:
            wallet_id: ID of the wallet to add the address to
            address: The address to add (required)
            description: Optional description for the address
            spend_policy: Optional spend policy for tracking public keys
            metadata: Optional metadata for the address
            
        Note:
            After registering one or more addresses, the blockchain may need
            to be rescanned using the subscribe endpoint.
            
        Raises:
            WalletdError: If the wallet is not found or other API error occurs
        """
        payload = {"address": address}
        if description is not None:
            payload["description"] = description
        if spend_policy is not None:
            payload["spendPolicy"] = spend_policy
        if metadata is not None:
            payload["metadata"] = metadata
            
        response = await self.client.put(f"/wallets/{wallet_id}/addresses", json=payload)
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def delete_wallet_address(self, wallet_id: str, address: str) -> None:
        """Removes an address from a wallet.
        
        This will disassociate any events or UTXOs not referencing another address.
        The address will continue to be tracked even if not registered to another wallet.
        
        Args:
            wallet_id: ID of the wallet to remove the address from
            address: The address to remove
            
        Raises:
            WalletdError: If the wallet or address is not found, or other API error occurs
        """
        response = await self.client.delete(f"/wallets/{wallet_id}/addresses/{address}")
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def construct_transaction(
        self,
        wallet_id: str,
        siacoins: Optional[List[Dict[str, Any]]] = None,
        siafunds: Optional[List[Dict[str, Any]]] = None,
        change_address: str = None
    ) -> Dict[str, Any]:
        """Constructs a transaction sending siacoins and siafunds to the recipients.
        
        Args:
            wallet_id: ID of the wallet to use for funding
            siacoins: List of siacoin recipients with address and value
            siafunds: List of siafund recipients with address and value
            change_address: Address to send change to
            
        Returns:
            Dict containing the constructed transaction details
        """
        payload = {
            "siacoins": siacoins or [],
            "siafunds": siafunds or [],
            "changeAddress": change_address
        }
        response = await self.client.post(f"/wallets/{wallet_id}/construct/transaction", json=payload)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def construct_v2_transaction(
        self,
        wallet_id: str,
        siacoins: Optional[List[Dict[str, Any]]] = None,
        siafunds: Optional[List[Dict[str, Any]]] = None,
        change_address: str = None
    ) -> Dict[str, Any]:
        """Constructs a V2 transaction sending siacoins and siafunds to the recipients.
        
        Args:
            wallet_id: ID of the wallet to use for funding
            siacoins: List of siacoin recipients with address and value
            siafunds: List of siafund recipients with address and value
            change_address: Address to send change to
            
        Returns:
            Dict containing the constructed transaction details
        """
        payload = {
            "siacoins": siacoins or [],
            "siafunds": siafunds or [],
            "changeAddress": change_address
        }
        response = await self.client.post(f"/wallets/{wallet_id}/construct/v2/transaction", json=payload)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def delete_wallet(self, wallet_id: str) -> None:
        """Removes a wallet from walletd.
        
        Note: Addresses that were previously added will continue to be tracked
        even if they are no longer connected to any wallets.
        
        Args:
            wallet_id: ID of the wallet to delete
            
        Raises:
            WalletdError: If the wallet is not found or other API error occurs
        """
        response = await self.client.delete(f"/wallets/{wallet_id}")
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def get_unconfirmed_events(self, wallet_id: str) -> List[Dict[str, Any]]:
        """Returns any unconfirmed events relevant to the wallet.
        
        Args:
            wallet_id: ID of the wallet to get unconfirmed events for
            
        Returns:
            List of unconfirmed event objects containing transaction details,
            maturity height, relevant addresses, etc.
            
        Raises:
            WalletdError: If the wallet is not found or other API error occurs
        """
        response = await self.client.get(f"/wallets/{wallet_id}/events/unconfirmed")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_balance(self, wallet_id: str) -> Dict[str, Any]:
        """Returns the current balance of the wallet.
        
        Args:
            wallet_id: ID of the wallet to get balance for
            
        Returns:
            Dict containing:
                siacoins: Current confirmed siacoin balance
                immatureSiacoins: Siacoins that are not yet mature
                siafunds: Current siafund balance
            
        Raises:
            WalletdError: If the wallet is not found or other API error occurs
        """
        response = await self.client.get(f"/wallets/{wallet_id}/balance")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_siacoin_utxos(
        self, wallet_id: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Returns a paginated list of Siacoin UTXOs for the wallet.
        
        Args:
            wallet_id: ID of the wallet to get UTXOs for
            limit: Maximum number of UTXOs to return
            offset: Number of UTXOs to skip
            
        Returns:
            List of UTXOs, each containing:
                id: UTXO ID
                leafIndex: Index in the merkle tree
                merkleProof: List of hashes forming the merkle proof
                siacoinOutput: Dict containing value and address
                maturityHeight: Block height at which the UTXO matures
            
        Raises:
            WalletdError: If the wallet is not found or other API error occurs
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
            
        response = await self.client.get(
            f"/wallets/{wallet_id}/outputs/siacoin",
            params=params
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_siafund_utxos(
        self, wallet_id: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Returns a paginated list of Siafund UTXOs for the wallet.
        
        Args:
            wallet_id: ID of the wallet to get UTXOs for
            limit: Maximum number of UTXOs to return
            offset: Number of UTXOs to skip
            
        Returns:
            List of UTXOs sorted by value descending, each containing:
                id: UTXO ID
                leafIndex: Index in the merkle tree
                merkleProof: List of hashes forming the merkle proof
                siafundOutput: Dict containing value and address
                claimStart: The amount of siacoins that have been earned by all siafunds
                          before this output was created
            
        Raises:
            WalletdError: If the wallet is not found or other API error occurs
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
            
        response = await self.client.get(
            f"/wallets/{wallet_id}/outputs/siafund",
            params=params
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def fund_transaction(
        self, 
        wallet_id: str, 
        transaction: Dict[str, Any],
        amount: str,
        change_address: str
    ) -> Dict[str, Any]:
        """Funds a transaction using UTXOs from the wallet.
        
        The UTXOs are locked for future use. If the transaction is not going to be broadcast,
        call the release endpoint to free the UTXOs. Signatures must be added externally
        in order to broadcast the transaction.
        
        Args:
            wallet_id: ID of the wallet to use for funding
            transaction: Dict containing:
                siacoinOutputs: List of outputs, each with value and address
                minerFees: List of miner fees
            amount: Total amount needed for the transaction (including fees)
            change_address: Address to send any remaining funds to
            
        Returns:
            Dict containing:
                transaction: The funded transaction with inputs and outputs
                toSign: List of parent IDs that need to be signed
                dependsOn: Optional list of transactions this one depends on
            
        Raises:
            WalletdError: If the wallet is not found, insufficient funds, or other API error
        """
        payload = {
            "transaction": transaction,
            "amount": amount,
            "changeAddress": change_address
        }
        
        response = await self.client.post(
            f"/wallets/{wallet_id}/fund",
            json=payload
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def reserve_utxos(
        self,
        wallet_id: str,
        siacoin_outputs: List[str],
        siafund_outputs: List[str],
        duration: Optional[int] = None
    ) -> None:
        """Reserves UTXOs preventing them from being used by the fund endpoint.
        
        To unlock the UTXOs and allow other transactions to use them, call the release endpoint.
        Duration is the time to lock the UTXOs in nanoseconds. If duration is zero or None,
        the outputs will be locked for 10 minutes.
        
        Args:
            wallet_id: ID of the wallet
            siacoin_outputs: List of siacoin output IDs to reserve
            siafund_outputs: List of siafund output IDs to reserve
            duration: Time to lock the UTXOs in nanoseconds. If None or 0, defaults to 10 minutes
            
        Raises:
            WalletdError: If the wallet is not found or other API error
        """
        payload = {
            "siacoinOutputs": siacoin_outputs,
            "siafundOutputs": siafund_outputs,
            "duration": duration or 0
        }
        
        response = await self.client.post(
            f"/wallets/{wallet_id}/reserve",
            json=payload
        )
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def release_utxos(
        self,
        wallet_id: str,
        siacoin_outputs: List[str],
        siafund_outputs: List[str]
    ) -> None:
        """Release unlocks UTXOs so they can be used to fund transactions.
        
        This endpoint unlocks previously reserved UTXOs, making them available
        for use with the fund endpoint.
        
        Args:
            wallet_id: ID of the wallet
            siacoin_outputs: List of siacoin output IDs to release
            siafund_outputs: List of siafund output IDs to release
            
        Raises:
            WalletdError: If the wallet is not found or other API error
        """
        payload = {
            "siacoinOutputs": siacoin_outputs,
            "siafundOutputs": siafund_outputs
        }
        
        response = await self.client.post(
            f"/wallets/{wallet_id}/release",
            json=payload
        )
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def get_rescan_status(self) -> Dict[str, Any]:
        """Gets the status of an in progress rescan.
        
        This endpoint will error if the index mode is not "personal".
        
        Returns:
            Dict containing:
                startIndex: Dict with height and id of the starting block
                index: Dict with height and id of the current block
                startTime: ISO timestamp of when the rescan started
            
        Raises:
            WalletdError: If index mode is not personal or other API error
        """
        response = await self.client.get("/rescan")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def start_rescan(self, height: int) -> None:
        """Starts a scan to find state from the specified height.
        
        This endpoint should not be used when in "full" mode.
        
        Args:
            height: Block height to start scanning from
            
        Raises:
            WalletdError: If in full mode or other API error
        """
        response = await self.client.post(
            "/rescan",
            json=height
        )
        response.raise_for_status()