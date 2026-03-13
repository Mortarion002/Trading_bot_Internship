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

app = typer.Typer(help="Binance Futures Testnet Trading Bot", invoke_without_command=True)
console = Console()
logger = setup_logging()


def _print_order_summary(order: OrderRequest) -> None:
    table = Table(title="Order Request Summary", box=box.ROUNDED, show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="white")
    table.add_row("Symbol", order.symbol)
    table.add_row("Side", order.side.value)
    table.add_row("Order Type", order.order_type.value)
    table.add_row("Quantity", str(order.quantity))
    if order.price:
        table.add_row("Price", str(order.price))
    console.print(table)


def _print_order_response(response: dict) -> None:
    table = Table(title="Order Response", box=box.ROUNDED, show_header=False)
    table.add_column("Field", style="bold green")
    table.add_column("Value", style="white")
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
) -> None:
    """Place a market or limit order on Binance Futures Testnet."""

    console.rule("[bold blue]Binance Futures Testnet Bot[/bold blue]")

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

    _print_order_summary(order)
    console.print("\n[yellow]Submitting order to Binance Futures Testnet...[/yellow]")

    try:
        response = place_order(order)
        _print_order_response(response)
        console.print("\n[bold green]✓ Order placed successfully![/bold green]")

    except BinanceAPIException as e:
        console.print(f"\n[bold red]✗ Binance API Error:[/bold red] {e.message}")
        raise typer.Exit(code=1)

    except BinanceRequestException as e:
        console.print(f"\n[bold red]✗ Network Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"\n[bold red]✗ Unexpected Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()