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
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.walletd_client = WalletdClient(base_url=walletd_url, api_password=walletd_password)
        self.renterd_client = RenterdClient(base_url=renterd_url, api_password=renterd_password)
        self.hostd_client = HostdClient(base_url=hostd_url, api_password=hostd_password)

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
        }
        return context


def create_graphql_app(
    walletd_url: str,
    walletd_password: str,
    renterd_url: str,
    renterd_password: str,
    hostd_url: str,
    hostd_password: str,
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
        graphiql=True,
        debug=True,
    )
