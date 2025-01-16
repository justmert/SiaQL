# siaql/graphql/schemas/walletd/syncer.py
from typing import List, Optional
from datetime import datetime
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import Peer, RescanStatus, StartRescanResponse, ConnectPeerResponse, BlockIndex

@strawberry.type
class SyncerQueries(WalletdBaseResolver):
    @strawberry.field
    async def peers(self, info: Info) -> List[Peer]:
        """Returns a list of all connected peers"""
        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_syncer_peers",
            transform_func=lambda peers: [Peer(**peer) for peer in peers]
        )
        return data

    @strawberry.field
    async def rescan_status(self, info: Info) -> Optional[RescanStatus]:
        """Gets the status of an in progress rescan.
        
        This endpoint will error if the index mode is not "personal".
        
        Returns:
            RescanStatus object containing start block, current block, and start time,
            or None if no rescan is in progress
        """
        try:
            data = await WalletdBaseResolver.handle_api_call(info, "get_rescan_status")
            return RescanStatus(
                start_index=BlockIndex(
                    height=data["startIndex"]["height"],
                    id=data["startIndex"]["id"]
                ),
                index=BlockIndex(
                    height=data["index"]["height"],
                    id=data["index"]["id"]
                ),
                start_time=datetime.fromisoformat(data["startTime"].replace("Z", "+00:00"))
            )
        except Exception:
            return None

@strawberry.type
class SyncerMutations(WalletdBaseResolver):
    @strawberry.mutation
    async def start_rescan(self, info: Info, height: int) -> StartRescanResponse:
        """Starts a scan to find state from the specified height.
        
        This endpoint should not be used when in "full" mode.
        
        Args:
            height: Block height to start scanning from
            
        Returns:
            StartRescanResponse indicating success or failure with optional error message
        """
        try:
            await WalletdBaseResolver.handle_api_call(info, "start_rescan", height=height)
            return StartRescanResponse(success=True)
        except Exception as e:
            return StartRescanResponse(success=False, message=str(e))

    @strawberry.mutation
    async def connect_peer(self, info: Info, address: str) -> ConnectPeerResponse:
        """Connect to a new peer"""
        try:
            await WalletdBaseResolver.handle_api_call(
                info,
                "connect_syncer_peer",
                address=address
            )
            return ConnectPeerResponse(success=True)
        except Exception as e:
            return ConnectPeerResponse(success=False, message=str(e))