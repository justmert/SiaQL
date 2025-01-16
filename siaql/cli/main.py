# siaql/siaql/cli/main.py
import typer
import uvicorn
from rich.console import Console
from rich.prompt import Prompt
from typing import Optional
from pathlib import Path
from ..graphql.app import create_graphql_app

app = typer.Typer(help="SiaQL - GraphQL interface for Sia network components")
console = Console()

@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
    walletd_url: str = typer.Option("http://localhost:9980", help="Walletd API URL"),
    walletd_password: Optional[str] = typer.Option(
        None, 
        help="Walletd API password. If not provided, will prompt securely.",
        envvar="SIAQL_WALLETD_PASSWORD"
    ),
):
    """Start the GraphQL server"""
    # If password not provided via flag or env var, prompt securely
    if walletd_password is None:
        walletd_password = Prompt.ask(
            "Enter walletd API password",
            password=True,
            console=console
        )

    # Print startup message
    console.print(f"Starting SiaQL server on http://{host}:{port}/graphql")
    console.print(f"GraphiQL interface available at http://{host}:{port}/graphql")
    
    # Create GraphQL app with authentication
    graphql_app = create_graphql_app(
        walletd_url=walletd_url,
        walletd_password=walletd_password
    )
    
    # Start ASGI server
    uvicorn.run(
        graphql_app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    app()