# siaql/siaql/graphql/app.py
from typing import Optional, Union, Dict, Any
from strawberry.asgi import GraphQL
from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.responses import Response
from .schema import schema
from ..api.walletd import WalletdClient

class SiaQLGraphQL(GraphQL):
    def __init__(
        self,
        walletd_url: str,
        walletd_password: str,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        # Initialize the client with auth
        self.walletd_client = WalletdClient(
            base_url=walletd_url,
            api_password=walletd_password
        )

    async def get_context(
        self, 
        request: Union[Request, WebSocket], 
        response: Optional[Response] = None
    ) -> Dict[str, Any]:
        """Provides the context for GraphQL resolvers"""
        context = {
            "request": request,
            "response": response,
            "walletd_client": self.walletd_client
        }
        return context

def create_graphql_app(
    walletd_url: str,
    walletd_password: str
) -> GraphQL:
    """Creates and configures the GraphQL application"""
    return SiaQLGraphQL(
        schema=schema,
        walletd_url=walletd_url,
        walletd_password=walletd_password,
        graphiql=True,
        debug=True
    )