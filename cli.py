from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich import box
from pydantic import ValidationError
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.validators import OrderRequest, OrderSide, OrderType
from bot.orders import place_order
from bot.logging_config import setup_logging

# Typer app instance — invoke_without_command=True allows the app to run
# directly without requiring a subcommand (e.g. just `python cli.py --symbol ...`)
app = typer.Typer(help="Binance Futures Testnet Trading Bot", invoke_without_command=True)

# Rich console for styled terminal output (tables, colors, rules)
console = Console()


def _print_order_summary(order: OrderRequest) -> None:
    """
    Print a formatted table summarising the order before submission.
    Gives the user a chance to verify inputs before the API call is made.
    """
    table = Table(title="Order Request Summary", box=box.ROUNDED, show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row("Symbol", order.symbol)
    table.add_row("Side", order.side.value)
    table.add_row("Order Type", order.order_type.value)
    table.add_row("Quantity", str(order.quantity))

    # Price is only relevant for LIMIT orders — skip it for MARKET orders
    if order.price:
        table.add_row("Price", str(order.price))

    console.print(table)


def _print_order_response(response: dict) -> None:
    """
    Print a formatted table of the Binance API response after order placement.
    Only shows fields that are present and non-empty in the response.
    """
    table = Table(title="Order Response", box=box.ROUNDED, show_header=False)
    table.add_column("Field", style="bold green")
    table.add_column("Value", style="white")

    # Map Binance API response keys to human-readable labels
    fields = {
        "orderId": "Order ID",
        "status": "Status",
        "executedQty": "Executed Qty",
        "avgPrice": "Avg Price",
        "symbol": "Symbol",
        "side": "Side",
        "type": "Type",
        "origQty": "Orig Qty",
        "price": "Price",
    }

    for key, label in fields.items():
        value = response.get(key)
        # Skip fields that are missing or empty strings in the response
        if value is not None and value != "":
            table.add_row(label, str(value))

    console.print(table)


@app.command()
def main(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair, e.g. BTCUSDT"),
    side: OrderSide = typer.Option(..., "--side", help="BUY or SELL"),
    order_type: OrderType = typer.Option(..., "--type", "-t", help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Amount to trade"),
    price: Optional[float] = typer.Option(
        None, "--price", "-p", help="Limit price (required for LIMIT orders)"
    ),
    log_file: str = typer.Option(
        "trading_bot.log", "--log-file", "-l", help="Log output file path"
    ),
) -> None:
    """Place a market or limit order on Binance Futures Testnet."""

    # Initialise logger with the specified log file
    # Defaults to trading_bot.log — override with --log-file to separate logs
    # e.g. --log-file market_order.log or --log-file limit_order.log
    logger = setup_logging(log_file)

    console.rule("[bold blue]Binance Futures Testnet Bot[/bold blue]")

    # --- Step 1: Validate user inputs via Pydantic ---
    # Catches issues like missing price on LIMIT, invalid symbol format, etc.
    try:
        order = OrderRequest(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
    except ValidationError as e:
        console.print("\n[bold red]Validation Error:[/bold red]")
        for err in e.errors():
            field = " -> ".join(str(f) for f in err["loc"])
            console.print(f"  [red]• {field}:[/red] {err['msg']}")
        logger.error("Validation failed: %s", e)
        raise typer.Exit(code=1)

    # --- Step 2: Show order summary before submitting ---
    _print_order_summary(order)
    console.print("\n[yellow]Submitting order to Binance Futures Testnet...[/yellow]")

    # --- Step 3: Place the order and handle API responses ---
    try:
        response = place_order(order)
        _print_order_response(response)
        console.print("\n[bold green]✓ Order placed successfully![/bold green]")

    except BinanceAPIException as e:
        # Binance rejected the order (e.g. insufficient margin, bad symbol, min notional)
        console.print(f"\n[bold red]✗ Binance API Error:[/bold red] {e.message}")
        raise typer.Exit(code=1)

    except BinanceRequestException as e:
        # Network-level failure — could not reach the testnet API
        console.print(f"\n[bold red]✗ Network Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

    except Exception as e:
        # Catch-all for any unexpected errors
        console.print(f"\n[bold red]✗ Unexpected Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()