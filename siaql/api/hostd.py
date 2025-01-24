from datetime import datetime
from typing import List, Optional, Dict, Any, Union
import httpx
from siaql.graphql.schemas.types import (
    AddVolumeRequest,
    Alert,
    ChainIndex,
    ConsensusState,
    Contract,
    ContractFilter,
    ContractsResponse,
    FileContractID,
    FundingSource,
    Hash256,
    HostdAccount,
    HostdState,
    IntegrityCheckResult,
    Metrics,
    MetricsInterval,
    Network,
    Peer,
    PinnedSettings,
    HostSettings,
    RegisterWebHookRequest,
    ResizeVolumeRequest,
    SystemDirResponse,
    TransactionID,
    UpdateVolumeRequest,
    VerifySectorResponse,
    Volume,
    VolumeMeta,
    WalletSendSiacoinsRequest,
    Webhook,
    WalletEvent,
    WalletResponse,
    Currency,
)
from siaql.api.utils import APIError, handle_api_errors


class HostdError(Exception):
    """Base exception for Hostd API errors"""

    pass


class HostdClient:
    """Client for interacting with the Hostd REST API"""

    def __init__(self, base_url: str = "http://localhost:9880", api_password: Optional[str] = None):
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
    @handle_api_errors(HostdError)
    async def get_state(self) -> HostdState:
        """Get the current state of the hostd daemon"""
        response = await self.client.get("/state")
        response.raise_for_status()
        return response.json()

    # Consensus endpoints
    @handle_api_errors(HostdError)
    async def get_consensus_tip(self) -> ChainIndex:
        """Get the current consensus tip"""
        response = await self.client.get("/consensus/tip")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_consensus_tip_state(self) -> ConsensusState:
        """Get the current consensus tip state"""
        response = await self.client.get("/consensus/tipstate")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_consensus_network(self) -> Network:
        """Get consensus network parameters"""
        response = await self.client.get("/consensus/network")
        response.raise_for_status()
        return response.json()

    # Syncer endpoints
    @handle_api_errors(HostdError)
    async def get_syncer_address(self) -> str:
        """Get syncer address"""
        response = await self.client.get("/syncer/address")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_syncer_peers(self) -> List[Peer]:
        """Get list of connected peers"""
        response = await self.client.get("/syncer/peers")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def put_syncer_peer(self, address: str) -> None:
        """Connect to a peer"""
        response = await self.client.put("/syncer/peers", json={"address": address})
        response.raise_for_status()

    # Index endpoints
    @handle_api_errors(HostdError)
    async def get_index_tip(self) -> ChainIndex:
        """Get current index tip"""
        response = await self.client.get("/index/tip")
        response.raise_for_status()
        return response.json()

    # Alert endpoints
    @handle_api_errors(HostdError)
    async def get_alerts(self) -> List[Alert]:
        """Get active alerts"""
        response = await self.client.get("/alerts")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def post_alerts_dismiss(self, ids: List[Hash256]) -> None:
        """Dismiss alerts"""
        response = await self.client.post("/alerts/dismiss", json=ids)
        response.raise_for_status()

    # Settings endpoints
    @handle_api_errors(HostdError)
    async def get_settings(self) -> HostSettings:
        """Get host settings"""
        response = await self.client.get("/settings")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def patch_settings(self, settings: HostSettings) -> HostSettings:
        """Update host settings"""
        response = await self.client.patch("/settings", json=settings)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def post_announce(self) -> None:
        """Announce the host"""
        response = await self.client.post("/settings/announce")
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def put_ddns_update(self, force: bool = False) -> None:
        """Update dynamic DNS"""
        response = await self.client.put("/settings/ddns/update", params={"force": force})
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def get_pinned_settings(self) -> PinnedSettings:
        """Get pinned settings"""
        response = await self.client.get("/settings/pinned")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def put_pinned_settings(self, settings: PinnedSettings) -> None:
        """Update pinned settings"""
        response = await self.client.put("/settings/pinned", json=settings)
        response.raise_for_status()

    # Metrics endpoints
    @handle_api_errors(HostdError)
    async def get_metrics(self, timestamp: Optional[datetime] = None) -> Metrics:
        """Get metrics at specified timestamp"""
        params = {}
        if timestamp:
            params["timestamp"] = timestamp.isoformat()
        response = await self.client.get("/metrics", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_period_metrics(self, start: datetime, periods: int, interval: MetricsInterval) -> List[Metrics]:
        """Get metrics for multiple periods"""
        params = {"start": start.isoformat(), "periods": str(periods)}
        response = await self.client.get(f"/metrics/{interval}", params=params)
        response.raise_for_status()
        return response.json()

    # Contract endpoints
    @handle_api_errors(HostdError)
    async def post_contracts(self, filter: ContractFilter) -> ContractsResponse:
        """Get contracts matching filter"""
        response = await self.client.post("/contracts", json=filter)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_contract(self, id: FileContractID) -> Contract:
        """Get specific contract"""
        response = await self.client.get(f"/contracts/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_contract_integrity(self, id: FileContractID) -> IntegrityCheckResult:
        """Get contract integrity check result"""
        response = await self.client.get(f"/contracts/{id}/integrity")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def put_contract_integrity(self, id: FileContractID) -> None:
        """Start contract integrity check"""
        response = await self.client.put(f"/contracts/{id}/integrity")
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def delete_contract_integrity(self, id: FileContractID) -> None:
        """Delete contract integrity check result"""
        response = await self.client.delete(f"/contracts/{id}/integrity")
        response.raise_for_status()

    # Account endpoints
    @handle_api_errors(HostdError)
    async def get_accounts(self, limit: int = 100, offset: int = 0) -> List[HostdAccount]:
        """Get accounts with pagination"""
        params = {"limit": limit, "offset": offset}
        response = await self.client.get("/accounts", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_account_funding(self, account: str) -> List[FundingSource]:
        """Get account funding sources"""
        response = await self.client.get(f"/accounts/{account}/funding")
        response.raise_for_status()
        return response.json()

    # Sector endpoints
    @handle_api_errors(HostdError)
    async def delete_sector(self, root: Hash256) -> None:
        """Delete a sector"""
        response = await self.client.delete(f"/sectors/{root}")
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def get_verify_sector(self, root: Hash256) -> VerifySectorResponse:
        """Verify a sector"""
        response = await self.client.get(f"/sectors/{root}/verify")
        response.raise_for_status()
        return response.json()

    # Volume endpoints
    @handle_api_errors(HostdError)
    async def get_volumes(self) -> List[VolumeMeta]:
        """Get all volumes"""
        response = await self.client.get("/volumes")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def post_volume(self, req: AddVolumeRequest) -> Volume:
        """Add a new volume"""
        response = await self.client.post("/volumes", json=req)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_volume(self, id: int) -> VolumeMeta:
        """Get specific volume"""
        response = await self.client.get(f"/volumes/{id}")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def put_volume(self, id: int, req: UpdateVolumeRequest) -> None:
        """Update volume settings"""
        response = await self.client.put(f"/volumes/{id}", json=req)
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def delete_volume(self, id: int, force: bool = False) -> None:
        """Delete a volume"""
        params = {"force": force}
        response = await self.client.delete(f"/volumes/{id}", params=params)
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def put_volume_resize(self, id: int, req: ResizeVolumeRequest) -> None:
        """Resize a volume"""
        response = await self.client.put(f"/volumes/{id}/resize", json=req)
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def delete_volume_cancel_op(self, id: int) -> None:
        """Cancel ongoing volume operation"""
        response = await self.client.delete(f"/volumes/{id}/cancel")
        response.raise_for_status()

    # System endpoints
    @handle_api_errors(HostdError)
    async def get_system_dir(self, path: str) -> SystemDirResponse:
        """Get directory contents"""
        params = {"path": path}
        response = await self.client.get("/system/dir", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def put_system_dir(self, path: str) -> None:
        """Create a directory"""
        data = {"path": path}
        response = await self.client.put("/system/dir", json=data)
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def post_system_sqlite3_backup(self, path: str) -> None:
        """Create SQLite3 backup"""
        data = {"path": path}
        response = await self.client.post("/system/sqlite3/backup", json=data)
        response.raise_for_status()

    # Wallet endpoints
    @handle_api_errors(HostdError)
    async def get_wallet(self) -> WalletResponse:
        """Get wallet state"""
        response = await self.client.get("/wallet")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_wallet_events(self, limit: int = 100, offset: int = 0) -> List[WalletEvent]:
        """Get wallet events with pagination"""
        params = {"limit": limit, "offset": offset}
        response = await self.client.get("/wallet/events", params=params)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def get_wallet_pending(self) -> List[WalletEvent]:
        """Get pending wallet events"""
        response = await self.client.get("/wallet/pending")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def post_wallet_send(self, req: WalletSendSiacoinsRequest) -> TransactionID:
        """Send siacoins"""
        response = await self.client.post("/wallet/send", json=req)
        response.raise_for_status()
        return response.json()

    # TPool endpoints
    @handle_api_errors(HostdError)
    async def get_tpool_fee(self) -> Currency:
        """Get recommended transaction fee"""
        response = await self.client.get("/tpool/fee")
        response.raise_for_status()
        return response.json()

    # Webhook endpoints
    @handle_api_errors(HostdError)
    async def get_webhooks(self) -> List[Webhook]:
        """Get all webhooks"""
        response = await self.client.get("/webhooks")
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def post_webhooks(self, req: RegisterWebHookRequest) -> Webhook:
        """Register a new webhook"""
        response = await self.client.post("/webhooks", json=req)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def put_webhooks(self, id: int, req: RegisterWebHookRequest) -> Webhook:
        """Update an existing webhook"""
        response = await self.client.put(f"/webhooks/{id}", json=req)
        response.raise_for_status()
        return response.json()

    @handle_api_errors(HostdError)
    async def post_webhooks_test(self, id: int) -> None:
        """Test a webhook"""
        response = await self.client.post(f"/webhooks/{id}/test")
        response.raise_for_status()

    @handle_api_errors(HostdError)
    async def delete_webhooks(self, id: int) -> None:
        """Delete a webhook"""
        response = await self.client.delete(f"/webhooks/{id}")
        response.raise_for_status()
