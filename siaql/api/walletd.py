# siaql/siaql/api/walletd.py
from typing import Dict, List, Optional, Any
import httpx
from datetime import datetime

class WalletdError(Exception):
    """Base exception for Walletd API errors"""
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




    async def get_address_balance(self, address: str) -> Dict[str, Any]:
        """Get balance of an individual address"""
        try:
            url = f"/addresses/{address}/balance"
            print(f"Requesting: {self.base_url}{url}")  # Debug print
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise WalletdError(f"Failed to fetch address balance: {str(e)}")
        except Exception as e:
            raise WalletdError(f"Unexpected error: {str(e)}")

    async def get_address_events(
        self, 
        address: str, 
        limit: Optional[int] = 100,
        offset: Optional[int] = 0
    ) -> List[Dict[str, Any]]:
        """Get events for a specific address"""
        try:
            params = {"limit": limit, "offset": offset}
            response = await self.client.get(
                f"/addresses/{address}/events",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise WalletdError(f"Failed to fetch address events: {str(e)}")
        except Exception as e:
            raise WalletdError(f"Unexpected error: {str(e)}")

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

    async def get_address_siafund_outputs(
        self,
        address: str,
        limit: Optional[int] = 100,
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

    async def get_event(self, event_id: str) -> Dict[str, Any]:
        """Get a specific event by ID"""
        response = await self.client.get(f"/events/{event_id}")
        response.raise_for_status()
        return response.json()