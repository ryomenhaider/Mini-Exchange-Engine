from sortedcontainers import SortedDict
from collections import defaultdict
import time


class OrderBook:
    def __init__(self):

        self.bids = SortedDict()
        self.asks = SortedDict()
        self.orders = {}

    def add_order(self, order_id: str, side: str, price: float, volume: float):

        self.orders[order_id] = {"side": side, "price": price, "volume": volume}

        if side == "ask":
            book = self.asks
        elif side == "bid":
            book = self.bids
        else:
            raise ValueError("sides should be ask or bid")

        if price in book:
            book[price] += volume
        else:
            book[price] = volume

    def cancel_order(self, order_id: str):
        order = self.orders.pop(order_id, None)
        if order is None:
            return

        side = order["side"]
        price = order["price"]
        volume = order["volume"]

        if side == "ask":
            book = self.asks
        elif side == "bid":
            book = self.bids
        else:
            return

        if price in book:
            book[price] -= volume

            if book[price] <= 0:
                del book[price]

    def best_bid(self) -> float:

        if not self.bids:
            return None
        return max(self.bids.keys())

    def best_ask(self) -> float:
        if not self.asks:
            return None
        return min(self.asks.keys())

    def spread(self) -> float:

        best_bid = self.best_bid()
        best_ask = self.best_ask()

        if best_bid is None or best_ask is None:
            return None

        return best_ask - best_bid

    def mid_price(self) -> float:

        best_ask = self.best_ask()
        best_bid = self.best_bid()

        if best_bid is None or best_ask is None:
            return None

        return (best_ask + best_bid) / 2

    def get_depth(self, levels: int = 10):

        bid = sorted(self.bids.items(), key=lambda x: -x[0])[:levels]
        ask = list(self.asks.items())[:levels]

        return bid, ask


if __name__ == "__main__":
    ob = OrderBook()
    ob.add_order("o1", "bid", 100.0, 5.0)
    ob.add_order("o2", "bid", 99.5, 3.0)
    ob.add_order("o3", "ask", 101.0, 4.0)
    ob.add_order("o4", "ask", 101.5, 2.0)

    print(ob.best_bid())  # 100.0
    print(ob.best_ask())  # 101.0
    print(ob.spread())  # 1.0
    print(ob.mid_price())  # 100.5

    ob.cancel_order("o1")
    print(ob.best_bid())  # 99.5

    print(ob.get_depth(2))
