# siaql/siaql/cli/main.py
import typer
import uvicorn
import os
from rich.console import Console
from rich.prompt import Prompt
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from siaql.graphql.app import create_graphql_app

# Load environment variables from .env file
load_dotenv()

app = typer.Typer(help="SiaQL - GraphQL interface for Sia network components")
console = Console()


@app.command()
def serve(
    host: str = typer.Option(None, help="Host to bind the server to", envvar="HOST"),
    port: int = typer.Option(None, help="Port to bind the server to", envvar="PORT"),
    walletd_url: str = typer.Option(None, help="Walletd API URL", envvar="WALLETD_URL"),
    walletd_password: Optional[str] = typer.Option(None, help="Walletd API password", envvar="WALLETD_PASSWORD"),
    renterd_url: str = typer.Option(None, help="Renterd API URL", envvar="RENTERD_URL"),
    renterd_password: Optional[str] = typer.Option(None, help="Renterd API password", envvar="RENTERD_PASSWORD"),
    hostd_url: str = typer.Option(None, help="Hostd API URL", envvar="HOSTD_URL"),
    hostd_password: Optional[str] = typer.Option(None, help="Hostd API password", envvar="HOSTD_PASSWORD"),
):
    """Start the GraphQL server"""

    # Set defaults
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8000
    DEFAULT_WALLETD_URL = "http://localhost:9980"
    DEFAULT_RENTERD_URL = "http://localhost:9980"
    DEFAULT_HOSTD_URL = "http://localhost:9980"

    # Get values from environment or use defaults
    host = host or os.getenv("HOST") or DEFAULT_HOST
    port = port or int(os.getenv("PORT", "0")) or DEFAULT_PORT

    # Handle URLs in order of precedence: CLI args > env vars > interactive input
    walletd_url = (
        walletd_url or os.getenv("WALLETD_URL") or Prompt.ask("Enter walletd URL", default=DEFAULT_WALLETD_URL)
    )
    renterd_url = (
        renterd_url or os.getenv("RENTERD_URL") or Prompt.ask("Enter renterd URL", default=DEFAULT_RENTERD_URL)
    )
    hostd_url = hostd_url or os.getenv("HOSTD_URL") or Prompt.ask("Enter hostd URL", default=DEFAULT_HOSTD_URL)

    # Handle passwords
    if not walletd_password:
        walletd_password = os.getenv("WALLETD_PASSWORD") or Prompt.ask("Enter walletd API password", password=True)

    if not renterd_password:
        renterd_password = os.getenv("RENTERD_PASSWORD") or Prompt.ask("Enter renterd API password", password=True)

    if not hostd_password:
        hostd_password = os.getenv("HOSTD_PASSWORD") or Prompt.ask("Enter hostd API password", password=True)

    console.print(f"Starting SiaQL server on http://{host}:{port}/graphql")
    console.print(f"GraphiQL interface available at http://{host}:{port}/graphql")

    graphql_app = create_graphql_app(
        walletd_url=walletd_url,
        walletd_password=walletd_password,
        renterd_url=renterd_url,
        renterd_password=renterd_password,
        hostd_url=hostd_url,
        hostd_password=hostd_password,
    )

    uvicorn.run(graphql_app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    app()
