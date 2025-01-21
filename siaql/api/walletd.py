# siaql/siaql/api/walletd.py
from typing import Dict, List, Optional, Any
import httpx
from datetime import datetime
from siaql.api.utils import handle_api_errors, APIError
from siaql.graphql.schemas.types import (
    Transaction,
    V2Transaction,
    ChainIndex,
    Block,
    SiacoinElement,
    SiafundElement,
    StateResponse,
    RescanResponse,
    ConsensusState,
    Network,
    BalanceResponse,
)


class WalletdError(APIError):
    """Specific exception for Walletd API errors"""

    pass


class WalletdClient:
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

    # State endpoints
    @handle_api_errors(WalletdError)
    async def get_state(self) -> StateResponse:
        """Get the current state of the walletd daemon"""
        response = await self.client.get("/state")
        response.raise_for_status()
        return response.json()

    # Consensus endpoints
    @handle_api_errors(WalletdError)
    async def get_consensus_network(self) -> Network:
        """Get consensus network parameters"""
        response = await self.client.get("/consensus/network")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_consensus_tip(self) -> ChainIndex:
        """Get current consensus tip"""
        response = await self.client.get("/consensus/tip")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_consensus_tip_state(self) -> ConsensusState:
        """Get current consensus tip state"""
        response = await self.client.get("/consensus/tipstate")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_consensus_index(self, height: int) -> ChainIndex:
        """Get consensus index at specified height"""
        response = await self.client.get(f"/consensus/index/{height}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_consensus_updates(self, index: ChainIndex, limit: int = 10) -> Dict[str, Any]:
        """Get consensus updates since specified index"""
        response = await self.client.get(f"/consensus/updates/{index}?limit={limit}")
        response.raise_for_status()
        return response.json()

    # Syncer endpoints

    @handle_api_errors(WalletdError)
    async def get_syncer_peers(self) -> List[Dict[str, Any]]:
        """Get list of connected peers"""
        response = await self.client.get("/syncer/peers")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_syncer_connect(self, addr: str) -> None:
        """Connect to a peer"""
        response = await self.client.post("/syncer/connect", json=addr)
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def post_syncer_broadcast_block(self, block: Block) -> None:
        """Broadcast a block to all peers"""
        response = await self.client.post("/syncer/broadcast/block", json=block)
        response.raise_for_status()

    # Transaction Pool endpoints

    @handle_api_errors(WalletdError)
    async def get_txpool_transactions(self) -> Dict[str, Any]:
        """Get all transactions in the transaction pool"""
        response = await self.client.get("/txpool/transactions")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_txpool_fee(self) -> Dict[str, Any]:
        """Get the recommended transaction fee"""
        response = await self.client.get("/txpool/fee")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_txpool_broadcast(
        self, basis: ChainIndex, transactions: List[Transaction], v2transactions: List[V2Transaction]
    ) -> None:
        """Broadcast transactions to the network"""
        data = {"basis": basis, "transactions": transactions, "v2transactions": v2transactions}
        response = await self.client.post("/txpool/broadcast", json=data)
        response.raise_for_status()

    # Wallet endpoints

    @handle_api_errors(WalletdError)
    async def get_wallets(self) -> List[Dict[str, Any]]:
        """Get all wallets"""
        response = await self.client.get("/wallets")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_add_wallet(self, wallet_update: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new wallet"""
        response = await self.client.post("/wallets", json=wallet_update)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_update_wallet(self, wallet_id: str, wallet_update: Dict[str, Any]) -> Dict[str, Any]:
        """Update a wallet"""
        response = await self.client.post(f"/wallets/{wallet_id}", json=wallet_update)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def delete_wallet(self, wallet_id: str) -> None:
        """Delete a wallet"""
        response = await self.client.delete(f"/wallets/{wallet_id}")
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def get_wallet_addresses(self, wallet_id: str) -> List[Dict[str, Any]]:
        """Get addresses for a wallet"""
        response = await self.client.get(f"/wallets/{wallet_id}/addresses")
        response.raise_for_status()
        return response.json()

    # Wallet-specific operations
    @handle_api_errors(WalletdError)
    async def put_wallet_address(self, wallet_id: str, address: Dict[str, Any]) -> None:
        """Add an address to a wallet"""
        response = await self.client.put(f"/wallets/{wallet_id}/addresses", json=address)
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def delete_wallet_address(self, wallet_id: str, address: str) -> None:
        """Remove an address from a wallet"""
        response = await self.client.delete(f"/wallets/{wallet_id}/addresses/{address}")
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def get_wallet_balance(self, wallet_id: str) -> Dict[str, Any]:
        """Get wallet balance"""
        response = await self.client.get(f"/wallets/{wallet_id}/balance")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_events(self, wallet_id: str, offset: int = 0, limit: int = 500) -> List[Dict[str, Any]]:
        """Get wallet events"""
        response = await self.client.get(f"/wallets/{wallet_id}/events", params={"offset": offset, "limit": limit})
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_unconfirmed_events(self, wallet_id: str) -> List[Dict[str, Any]]:
        """Get unconfirmed wallet events"""
        response = await self.client.get(f"/wallets/{wallet_id}/events/unconfirmed")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_siacoin_outputs(
        self, wallet_id: str, offset: int = 0, limit: int = 100
    ) -> List[SiacoinElement]:
        """Get wallet siacoin outputs"""
        response = await self.client.get(f"/wallets/{wallet_id}/outputs/siacoin?offset={offset}&limit={limit}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_wallet_siafund_outputs(
        self, wallet_id: str, offset: int = 0, limit: int = 100
    ) -> List[SiafundElement]:
        """Get wallet siafund outputs"""
        response = await self.client.get(f"/wallets/{wallet_id}/outputs/siafund?offset={offset}&limit={limit}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_wallet_reserve(self, wallet_id: str, reserve_request: Dict[str, Any]) -> None:
        """Reserve outputs"""
        response = await self.client.post(f"/wallets/{wallet_id}/reserve", json=reserve_request)
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def post_wallet_release(self, wallet_id: str, release_request: Dict[str, Any]) -> None:
        """Release outputs"""
        response = await self.client.post(f"/wallets/{wallet_id}/release", json=release_request)
        response.raise_for_status()

    @handle_api_errors(WalletdError)
    async def post_wallet_fund(self, wallet_id: str, fund_request: Dict[str, Any]) -> Dict[str, Any]:
        """Fund a transaction"""
        response = await self.client.post(f"/wallets/{wallet_id}/fund", json=fund_request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_wallet_fund_siafund(self, wallet_id: str, fund_request: Dict[str, Any]) -> Dict[str, Any]:
        """Fund a siafund transaction"""
        response = await self.client.post(f"/wallets/{wallet_id}/fundsf", json=fund_request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_wallet_construct(self, wallet_id: str, construct_request: Dict[str, Any]) -> Dict[str, Any]:
        """Construct a transaction"""
        response = await self.client.post(f"/wallets/{wallet_id}/construct/transaction", json=construct_request)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def post_wallet_construct_v2(self, wallet_id: str, construct_request: Dict[str, Any]) -> Dict[str, Any]:
        """Construct a v2 transaction"""
        response = await self.client.post(f"/wallets/{wallet_id}/construct/v2/transaction", json=construct_request)
        response.raise_for_status()
        return response.json()

    # Address-related endpoints

    @handle_api_errors(WalletdError)
    async def get_address_balance(self, address: str) -> BalanceResponse:
        """Get balance for address"""
        response = await self.client.get(f"/addresses/{address}/balance")
        response.raise_for_status()
        return response.json()


    @handle_api_errors(WalletdError)
    async def get_address_events(self, address: str, offset: int = 0, limit: int = 500) -> List[Dict[str, Any]]:
        """Get events for an address"""
        response = await self.client.get(f"/addresses/{address}/events", params={"offset": offset, "limit": limit})
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_address_unconfirmed_events(self, address: str) -> List[Dict[str, Any]]:
        """Get unconfirmed events for an address"""
        response = await self.client.get(f"/addresses/{address}/events/unconfirmed")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_address_siacoin_outputs(
        self, address: str, offset: int = 0, limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get siacoin outputs for an address"""
        response = await self.client.get(
            f"/addresses/{address}/outputs/siacoin", params={"offset": offset, "limit": limit}
        )
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def get_address_siafund_outputs(
        self, address: str, offset: int = 0, limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get siafund outputs for an address"""
        response = await self.client.get(
            f"/addresses/{address}/outputs/siafund", params={"offset": offset, "limit": limit}
        )
        response.raise_for_status()
        return response.json()

    # Event-related endpoints
    @handle_api_errors(WalletdError)
    async def get_event(self, event_id: str) -> Dict[str, Any]:
        """Get a specific event"""
        response = await self.client.get(f"/events/{event_id}")
        response.raise_for_status()
        return response.json()

    # newly added
    # Rescan endpoints
    @handle_api_errors(WalletdError)
    async def get_rescan_status(self) -> RescanResponse:
        """Get rescan status"""
        response = await self.client.get("/rescan")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(WalletdError)
    async def start_rescan(self, height: int) -> None:
        """Start rescan from height"""
        response = await self.client.post("/rescan", json=height)
        response.raise_for_status()
