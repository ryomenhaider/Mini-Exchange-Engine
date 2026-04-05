import os
import sys
import time
import threading
import random
from datetime import datetime
from simulator import Simulator

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    from rich.layout import Layout
except ImportError:
    print("Installing rich...")
    os.system("uv add rich")
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    from rich.layout import Layout


class OrderBookUI:
    def __init__(self):
        self.console = Console()
        self.sim = Simulator(mid_price=100.0)
        self.running = True
        self.spoof_injected = False
        self.spoof_side = None
        self.spoof_price = 0
        self.spoof_volume = 0
        self.spoof_start_time = None
        self.detection_events = []
        self.stats = {
            "spreads": [],
            "mid_moves": [],
            "spoof_trades": 0,
            "price_impact": 0,
        }

    def get_detection_info(self):
        """Analyze the order book and provide spoof detection insights"""
        info = []

        bid_prices = list(self.sim.orderbook.bids.keys())
        ask_prices = list(self.sim.orderbook.asks.keys())

        if not bid_prices or not ask_prices:
            return ["No data"]

        best_bid = max(bid_prices)
        best_ask = min(ask_prices)
        spread = best_ask - best_bid
        mid = (best_ask + best_bid) / 2

        info.append(f"Spread: {spread:.2f} ({spread / mid * 100:.2f}%)")
        info.append(f"Mid Price: {mid:.2f}")

        if self.spoof_injected:
            elapsed = time.time() - self.spoof_start_time
            info.append(f"Spoof Active: {elapsed:.1f}s")

            if self.spoof_side == "bid":
                spoof_orders = [
                    (pid, self.sim.orderbook.orders[pid])
                    for pid in self.sim.spoof_order_ids
                ]
                for oid, order in spoof_orders:
                    vol_ratio = order["volume"] / 5.0
                    info.append(
                        f"SPOOF: {order['side'].upper()} {order['price']} vol={order['volume']:.1f} ({vol_ratio:.1f}x normal)"
                    )
            else:
                spoof_orders = [
                    (pid, self.sim.orderbook.orders[pid])
                    for pid in self.sim.spoof_order_ids
                ]
                for oid, order in spoof_orders:
                    vol_ratio = order["volume"] / 5.0
                    info.append(
                        f"SPOOF: {order['side'].upper()} {order['price']} vol={order['volume']:.1f} ({vol_ratio:.1f}x normal)"
                    )

        if spread > 2.0:
            info.append("[!] Wide spread detected - possible spoof!")

        return info

    def get_detection_explanation(self):
        """Explain why spoof detection works"""
        lines = []
        lines.append("=" * 50)
        lines.append("WHY SPOOF DETECTION WORKS")
        lines.append("=" * 50)
        lines.append("")
        lines.append("1. VOLUME ANOMALY")
        lines.append("   Spoof orders are 10-20x larger than normal")
        lines.append("   Normal volume: 0.5-5.0 | Spoof: 50-100+")
        lines.append("")
        lines.append("2. PRICE IMMOBILE")
        lines.append("   Spoof never executes - it's fake!")
        lines.append("   Watch: price approaches then retreats")
        lines.append("")
        lines.append("3. TEMPORAL PATTERN")
        lines.append("   Spoof appears -> price moves -> spoof vanishes")
        lines.append("   Typical lifespan: 2-10 seconds")
        lines.append("")
        lines.append("4. LAYERING EFFECT")
        lines.append("   Spoof creates wall to push price direction")
        lines.append("   Then cancels when price moves away")
        lines.append("=" * 50)
        return "\n".join(lines)

    def render_orderbook(self):
        """Render the current order book state"""
        bids = sorted(self.sim.orderbook.bids.items(), key=lambda x: -x[0])
        asks = list(self.sim.orderbook.asks.items())

        console = self.console
        console.clear()

        title = f"ORDER BOOK SIMULATOR | Mid: {self.sim.mid_price:.2f}"
        if self.spoof_injected:
            title += " | [SPOOF ACTIVE]"

        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("BID SIZE", justify="right", style="green")
        table.add_column("BID Px", justify="right", style="green")
        table.add_column("ASK Px", justify="left", style="red")
        table.add_column("ASK SIZE", justify="left", style="red")

        max_rows = 15
        for i in range(max_rows):
            bid_vol = ""
            bid_px = ""
            ask_px = ""
            ask_vol = ""

            if i < len(bids):
                px, vol = bids[i]
                bid_px = f"{px:.2f}"
                bid_vol = f"{vol:.2f}"

                is_spoof = False
                if self.spoof_injected and self.spoof_side == "bid":
                    for oid in self.sim.spoof_order_ids:
                        if self.sim.orderbook.orders.get(oid, {}).get("price") == px:
                            is_spoof = True
                            bid_vol = f"[bold yellow]{vol:.2f}[/bold yellow] ⚠️"
                            break

                if is_spoof:
                    bid_vol = (
                        f"[bold yellow on black]{vol:.2f}[/bold yellow on black] 🔽"
                    )

            if i < len(asks):
                px, vol = asks[i]
                ask_px = f"{px:.2f}"
                ask_vol = f"{vol:.2f}"

                is_spoof = False
                if self.spoof_injected and self.spoof_side == "ask":
                    for oid in self.sim.spoof_order_ids:
                        if self.sim.orderbook.orders.get(oid, {}).get("price") == px:
                            is_spoof = True
                            ask_vol = f"[bold yellow]{vol:.2f}[/bold yellow] ⚠️"
                            break

                if is_spoof:
                    ask_vol = (
                        f"[bold yellow on black]{vol:.2f}[/bold yellow on black] 🔼"
                    )

            table.add_row(bid_vol, bid_px, ask_px, ask_vol)

        console.print(table)
        console.print()

        info = self.get_detection_info()
        panel = Panel("\n".join(info), title="Detection Info", border_style="blue")
        console.print(panel)
        console.print()

        if self.spoof_injected:
            console.print(
                Panel(
                    self.get_detection_explanation(),
                    title="Why Detection Works",
                    border_style="yellow",
                )
            )
            console.print()

        console.print("[bold cyan]Controls:[/bold cyan]")
        console.print("  [B] Inject BUY Spoof Wall   [S] Inject SELL Spoof Wall")
        console.print("  [C] Cancel Spoof            [Q] Quit")
        console.print("  [SPACE] Step Simulation")

        if self.spoof_injected:
            console.print()
            console.print("[bold yellow]⚠️ SPOOF DETECTION TRIGGERED![/bold yellow]")
            console.print("Watch how price moves toward spoof, then spoof vanishes!")

    def inject_spoof_buy(self):
        """Inject a large buy order (spoof)"""
        if self.spoof_injected:
            return

        best_ask = self.sim.orderbook.best_ask()
        if best_ask:
            spoof_price = best_ask - 0.01
            spoof_volume = random.uniform(40, 80)

            self.sim.inject_spoof("bid", spoof_price, spoof_volume)
            self.spoof_injected = True
            self.spoof_side = "bid"
            self.spoof_start_time = time.time()

            self.console.print(
                f"[yellow]Injected BUY spoof: {spoof_price:.2f} x {spoof_volume:.1f}[/yellow]"
            )

    def inject_spoof_sell(self):
        """Inject a large sell order (spoof)"""
        if self.spoof_injected:
            return

        best_bid = self.sim.orderbook.best_bid()
        if best_bid:
            spoof_price = best_bid + 0.01
            spoof_volume = random.uniform(40, 80)

            self.sim.inject_spoof("ask", spoof_price, spoof_volume)
            self.spoof_injected = True
            self.spoof_side = "ask"
            self.spoof_start_time = time.time()

            self.console.print(
                f"[yellow]Injected SELL spoof: {spoof_price:.2f} x {spoof_volume:.1f}[/yellow]"
            )

    def cancel_spoof(self):
        """Cancel the spoof order"""
        if not self.spoof_injected:
            return

        self.sim.cancel_spoof()
        self.spoof_injected = False
        elapsed = time.time() - self.spoof_start_time

        self.console.print(f"[red]Spoof cancelled after {elapsed:.2f}s[/red]")

        if self.spoof_side == "bid":
            direction = "upward"
        else:
            direction = "downward"

        self.console.print(
            f"[dim]Price was pushed {direction}, spoof vanished - classic spoof pattern![/dim]"
        )

    def simulation_step(self):
        """Run one simulation tick"""
        if self.spoof_injected:
            for _ in range(3):
                self.sim.tick()
        else:
            self.sim.tick()

    def run(self):
        """Main loop with keyboard input"""
        self.console.print("[bold green]Order Book Spoof Simulator[/bold green]")
        self.console.print("Watch how spoof walls manipulate price, then disappear!\n")

        while self.running:
            self.render_orderbook()

            self.console.print("\n[cyan]Press key...[/cyan]", end="")

            key = self.console.input()

            if key.lower() == "b":
                self.inject_spoof_buy()
            elif key.lower() == "s":
                self.inject_spoof_sell()
            elif key.lower() == "c":
                self.cancel_spoof()
            elif key.lower() == "q":
                self.running = False
            elif key == " ":
                self.simulation_step()
            else:
                self.simulation_step()

            time.sleep(0.3)

        self.console.print("\n[green]Goodbye![/green]")


def main():
    ui = OrderBookUI()
    ui.run()


if __name__ == "__main__":
    main()
