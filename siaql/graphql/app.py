# siaql/siaql/graphql/app.py
from typing import Optional, Union, Dict, Any
from strawberry.asgi import GraphQL
from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.responses import Response
from siaql.graphql.schema import schema
from siaql.api.walletd import WalletdClient
from siaql.api.renterd import RenterdClient
from siaql.api.hostd import HostdClient


class SiaQLGraphQL(GraphQL):
    def __init__(
        self,
        walletd_url: str,
        walletd_password: str,
        renterd_url: str,
        renterd_password: str,
        hostd_url: str,
        hostd_password: str,
        skipped_endpoints: Dict[str, bool],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.skipped_endpoints = skipped_endpoints

        # Initialize clients only for non-skipped endpoints
        self.walletd_client = (
            None if skipped_endpoints["walletd"] else WalletdClient(base_url=walletd_url, api_password=walletd_password)
        )
        self.renterd_client = (
            None if skipped_endpoints["renterd"] else RenterdClient(base_url=renterd_url, api_password=renterd_password)
        )
        self.hostd_client = (
            None if skipped_endpoints["hostd"] else HostdClient(base_url=hostd_url, api_password=hostd_password)
        )

    async def get_context(
        self, request: Union[Request, WebSocket], response: Optional[Response] = None
    ) -> Dict[str, Any]:
        """Provides the context for GraphQL resolvers"""
        context = {
            "request": request,
            "response": response,
            "walletd_client": self.walletd_client,
            "renterd_client": self.renterd_client,
            "hostd_client": self.hostd_client,
            "skipped_endpoints": self.skipped_endpoints,
        }
        return context


def create_graphql_app(
    walletd_url: str,
    walletd_password: str,
    renterd_url: str,
    renterd_password: str,
    hostd_url: str,
    hostd_password: str,
    skipped_endpoints: Dict[str, bool],
) -> GraphQL:
    """Creates and configures the GraphQL application"""
    return SiaQLGraphQL(
        schema=schema,
        walletd_url=walletd_url,
        walletd_password=walletd_password,
        renterd_url=renterd_url,
        renterd_password=renterd_password,
        hostd_url=hostd_url,
        hostd_password=hostd_password,
        skipped_endpoints=skipped_endpoints,
        graphiql=True,
        debug=True,
    )
