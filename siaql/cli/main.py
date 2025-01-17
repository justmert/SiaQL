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
    host: str = typer.Option(
        os.getenv("HOST", "127.0.0.1"), 
        help="Host to bind the server to",
        envvar="HOST"
    ),
    port: int = typer.Option(
        int(os.getenv("PORT", "8000")), 
        help="Port to bind the server to",
        envvar="PORT"
    ),
    walletd_url: str = typer.Option(
        os.getenv("SIAQL_WALLETD_URL", "http://localhost:9980"), 
        help="Walletd API URL",
        envvar="SIAQL_WALLETD_URL"
    ),
    walletd_password: Optional[str] = typer.Option(
        None, 
        help="Walletd API password. If not provided, will prompt securely.",
        envvar="SIAQL_WALLETD_PASSWORD"
    ),
    renterd_url: str = typer.Option(
        os.getenv("SIAQL_RENTERD_URL", "http://localhost:9980"), 
        help="Renterd API URL",
        envvar="SIAQL_RENTERD_URL"
    ),
    renterd_password: Optional[str] = typer.Option(
        None,
        help="Renterd API password. If not provided, will prompt securely.",
        envvar="SIAQL_RENTERD_PASSWORD"
    ),
):
    """Start the GraphQL server"""
    if walletd_password is None:
        walletd_password = Prompt.ask("Enter walletd API password", password=True, console=console)
    
    if renterd_password is None:
        renterd_password = Prompt.ask("Enter renterd API password", password=True, console=console)

    console.print(f"Starting SiaQL server on http://{host}:{port}/graphql")
    console.print(f"GraphiQL interface available at http://{host}:{port}/graphql")
    
    graphql_app = create_graphql_app(
        walletd_url=walletd_url,
        walletd_password=walletd_password,
        renterd_url=renterd_url,
        renterd_password=renterd_password
    )
    
    uvicorn.run(graphql_app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    app()