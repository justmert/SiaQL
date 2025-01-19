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
        # response = await self.client.get(f"/addresses/{address}/events", params={"offset": offset, "limit": limit})
        response = [
  {
    "id": "h:b0a50a2e2f3b6acf1c7a5974989133dcce69696ce174f63fe0344855d519e2d2",
    "index": {
      "height": 76633,
      "id": "bid:00000000afc28d36e868779b57011590c941bb598e6acf993420c88671229bc8"
    },
    "timestamp": "2024-06-28T14:38:52Z",
    "maturityHeight": 76778,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:b0a50a2e2f3b6acf1c7a5974989133dcce69696ce174f63fe0344855d519e2d2",
        "leafIndex": 1673774,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300001173550000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76777
      }
    }
  },
  {
    "id": "h:474478405fa966ddf32c1782374f46a89fc8012c3b37e8d17f010da33619abd7",
    "index": {
      "height": 76631,
      "id": "bid:0000000045be7569ac4dad7346dda6b5a0294b6b9145428c275f92e0689be27d"
    },
    "timestamp": "2024-06-28T14:32:22Z",
    "maturityHeight": 76776,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:474478405fa966ddf32c1782374f46a89fc8012c3b37e8d17f010da33619abd7",
        "leafIndex": 1673431,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300000000000000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76775
      }
    }
  },
  {
    "id": "h:0e1a3157ccb4b50ca90407f696f9d4c25e166872266712d6cf88f561e39c7111",
    "index": {
      "height": 76630,
      "id": "bid:0000000004a1aacfcfb5c696cc763dd629fa20eb58e07ae77ee4db6ad6a2694d"
    },
    "timestamp": "2024-06-28T14:22:42Z",
    "maturityHeight": 76775,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:0e1a3157ccb4b50ca90407f696f9d4c25e166872266712d6cf88f561e39c7111",
        "leafIndex": 1673429,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300001012590000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76774
      }
    }
  },
  {
    "id": "h:f4c6d086b01bffc6b6b750ce3029b4e3a351010a7977fce8475355b6396b541c",
    "index": {
      "height": 76629,
      "id": "bid:00000000c48e6bc7498ddee7e63114f6a982999f7040b67cac6ead9af333575a"
    },
    "timestamp": "2024-06-28T14:13:33Z",
    "maturityHeight": 76774,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:f4c6d086b01bffc6b6b750ce3029b4e3a351010a7977fce8475355b6396b541c",
        "leafIndex": 1673095,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300000000000000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76773
      }
    }
  },
  {
    "id": "h:d8ad9dda724c9ea66dcf0f777f1b5ec482ef71939129aa82c694bd636b86e5a3",
    "index": {
      "height": 76628,
      "id": "bid:00000000e86291aae657d756c3614de6f250524d1b7c833afeca8d33b0e40576"
    },
    "timestamp": "2024-06-28T14:13:11Z",
    "maturityHeight": 76773,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:d8ad9dda724c9ea66dcf0f777f1b5ec482ef71939129aa82c694bd636b86e5a3",
        "leafIndex": 1673093,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300000640970000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76772
      }
    }
  },
  {
    "id": "h:4beedcec5d1d0fafc941f4cb305a712f17672fd2d4829f068dc207b7d03f0ce5",
    "index": {
      "height": 76627,
      "id": "bid:0000000044e4e65d9fe6ba7593e16369162b29531c7b780f6d22606017294cf6"
    },
    "timestamp": "2024-06-28T14:09:22Z",
    "maturityHeight": 76772,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:4beedcec5d1d0fafc941f4cb305a712f17672fd2d4829f068dc207b7d03f0ce5",
        "leafIndex": 1672871,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300000000000000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76771
      }
    }
  },
  {
    "id": "h:3acbfc71fbd088e0f3298bf5422e1948713db90d994aa36a4b6a0f0fc5b7e705",
    "index": {
      "height": 76626,
      "id": "bid:000000003873b3df7e9f9cd157dbb3222307b7bd1c450e6f6076545846b00f91"
    },
    "timestamp": "2024-06-28T14:06:30Z",
    "maturityHeight": 76771,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:3acbfc71fbd088e0f3298bf5422e1948713db90d994aa36a4b6a0f0fc5b7e705",
        "leafIndex": 1672869,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300000307230000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76770
      }
    }
  },
  {
    "id": "h:b2ae335aab760aced353f291b0974233825884aa85e7f99e3a2833636a3119de",
    "index": {
      "height": 76625,
      "id": "bid:000000008f5d8ad18c8948e291e23792d2efceaab13d3f62af89cdc2770efb4d"
    },
    "timestamp": "2024-06-28T14:02:26Z",
    "maturityHeight": 76770,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:b2ae335aab760aced353f291b0974233825884aa85e7f99e3a2833636a3119de",
        "leafIndex": 1672757,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300001640970000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76769
      }
    }
  },
  {
    "id": "h:a012dd2099c2fd8582f5130d4e46f281a364133d721c8510f57b572f1ae8026b",
    "index": {
      "height": 76624,
      "id": "bid:0000000077679d98d24c7f67ecba8eb451c7ccdfa78e833ac6dfda8734cd8fd3"
    },
    "timestamp": "2024-06-28T13:54:43Z",
    "maturityHeight": 76769,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:a012dd2099c2fd8582f5130d4e46f281a364133d721c8510f57b572f1ae8026b",
        "leafIndex": 1672533,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300000948200000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76768
      }
    }
  },
  {
    "id": "h:fdcacbed22f91070b0709337f8df7880db67e53f33bf889e2082f34615e463eb",
    "index": {
      "height": 76623,
      "id": "bid:00000000130939be94450b6eaefc43c3fe8e9f70cc69bcaeb58cb2a3c30563a5"
    },
    "timestamp": "2024-06-28T13:47:14Z",
    "maturityHeight": 76768,
    "type": "miner",
    "data": {
      "siacoinElement": {
        "id": "h:fdcacbed22f91070b0709337f8df7880db67e53f33bf889e2082f34615e463eb",
        "leafIndex": 1672201,
        "merkleProof": None,
        "siacoinOutput": {
          "value": "300000000000000000000000000000",
          "address": "addr:000000000000000000000000000000000000000000000000000000000000000089eb0d6a8a69"
        },
        "maturityHeight": 76767
      }
    }
  }
]
        # response.raise_for_status()
        # return response.json()
        return response

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
