# siaql/siaql/cli/main.py
import typer
import uvicorn
import os
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from siaql.graphql.app import create_graphql_app
import httpx
# Load environment variables from .env file
load_dotenv()

app = typer.Typer(help="SiaQL - GraphQL interface for Sia network components")
console = Console()


def validate_url(url: str) -> bool:
    """Check if a URL is alive by making a request"""
    try:
        with httpx.Client() as client:
            response = client.get(url)
            return response.status_code < 500  # Accept any non-server error response
    except:
        return False


def get_endpoint_config(name: str, default_url: str) -> tuple[Optional[str], Optional[str], bool]:
    """Get URL and password for an endpoint with validation"""
    while True:
        url = Prompt.ask(f"Enter {name} URL", default=default_url)

        if not validate_url(url):
            console.print(f"[yellow][bold]WARNING:[/yellow][/bold] {url} seems to be unreachable")
            if Confirm.ask("Would you like to edit the URL?", default=True):
                continue
            if Confirm.ask("Would you like to skip this endpoint?", default=False):
                return None, None, True

        password = Prompt.ask(f"Enter {name} API password", password=True)
        return url, password, False


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
    skip_walletd: bool = typer.Option(False, help="Skip walletd configuration", envvar="SKIP_WALLETD"),
    skip_renterd: bool = typer.Option(False, help="Skip renterd configuration", envvar="SKIP_RENTERD"),
    skip_hostd: bool = typer.Option(False, help="Skip hostd configuration", envvar="SKIP_HOSTD"),
):
    """Start the GraphQL server"""

    # Set defaults
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 9090
    DEFAULT_RENTERD_URL = "http://localhost:9981"
    DEFAULT_WALLETD_URL = "http://localhost:9982"
    DEFAULT_HOSTD_URL = "http://localhost:9983"

    # Get values from environment or use defaults
    host = host or os.getenv("HOST") or DEFAULT_HOST
    port = port or int(os.getenv("PORT", "0")) or DEFAULT_PORT

    # Track skipped endpoints
    skipped_endpoints = {"walletd": False, "renterd": False, "hostd": False}

    # Check enable flags from environment
    enable_walletd = os.getenv("ENABLE_WALLETD", "true").lower() == "true" and not skip_walletd
    enable_renterd = os.getenv("ENABLE_RENTERD", "true").lower() == "true" and not skip_renterd
    enable_hostd = os.getenv("ENABLE_HOSTD", "true").lower() == "true" and not skip_hostd

    # Handle walletd configuration
    if not enable_walletd or skip_walletd:
        skipped_endpoints["walletd"] = True
        walletd_url = None
        walletd_password = None
    elif not (walletd_url and walletd_password):
        walletd_url, walletd_password, skipped_endpoints["walletd"] = get_endpoint_config(
            "walletd", DEFAULT_WALLETD_URL
        )

    # Handle renterd configuration
    if not enable_renterd or skip_renterd:
        skipped_endpoints["renterd"] = True
        renterd_url = None
        renterd_password = None
    elif not (renterd_url and renterd_password):
        renterd_url, renterd_password, skipped_endpoints["renterd"] = get_endpoint_config(
            "renterd", DEFAULT_RENTERD_URL
        )

    # Handle hostd configuration
    if not enable_hostd or skip_hostd:
        skipped_endpoints["hostd"] = True
        hostd_url = None
        hostd_password = None
    elif not (hostd_url and hostd_password):
        hostd_url, hostd_password, skipped_endpoints["hostd"] = get_endpoint_config("hostd", DEFAULT_HOSTD_URL)

    # Check if all endpoints are skipped
    if all(skipped_endpoints.values()):
        console.print(
            "[red][bold]ERROR:[/bold] All services have been skipped. At least one service must be enabled.[/red]"
        )
        sys.exit(1)

    console.print(f"Starting [purple][bold]SiaQL[/bold][/purple] on http://{host}:{port}/graphql")
    console.print(f"GraphiQL interface available at http://{host}:{port}/graphql")
    console.print(
        f"[cyan]Enabled services: {', '.join([key for key, value in skipped_endpoints.items() if not value])}[/cyan]"
    )
    console.print(
        """[green]           
        #############        
   ***               ###     
   ***                  ##   
  ##       =======       ##  
 ##     =============     ## 
 #     =====      ====     # 
 #     ====       ====     # 
 #     =====      ====     # 
 ##     ==============    ## 
  ##      ============   ##  
   ##                   ##   
     ###             ###     
        #############       [/green]
        """
    )
    # Create and display project information table
    table = Table(title="[bold]SiaQL Project Information[/bold]", show_header=False, show_edge=False)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Repository", "[link=https://github.com/justmert/siaql]github.com/justmert/siaql[/link]")
    table.add_row("Documentation", "[link=https://siaql-docs.netlify.app]siaql-docs.netlify.app[/link]")

    console.print()  # Add empty line for spacing
    console.print(table)
    console.print()  # Add empty line for spacing

    graphql_app = create_graphql_app(
        walletd_url=walletd_url,
        walletd_password=walletd_password,
        renterd_url=renterd_url,
        renterd_password=renterd_password,
        hostd_url=hostd_url,
        hostd_password=hostd_password,
        skipped_endpoints=skipped_endpoints,
    )

    uvicorn.run(graphql_app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    app()
