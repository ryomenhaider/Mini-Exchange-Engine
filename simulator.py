import random
import time
import uuid
from orderbook import OrderBook


class Simulator:
    def __init__(self, mid_price: float = 100.0):
        self.orderbook = OrderBook()
        self.mid_price = mid_price
        self.spoof_order_ids = []
        self.spoof_active = False
        self.last_spoof_reason = ""
        self._seed_book()

    def _seed_book(self):
        for _ in range(10):
            bid_price = self.mid_price * (1 - random.uniform(0.001, 0.02))
            bid_vol = random.uniform(0.5, 5.0)

            self.orderbook.add_order(
                order_id=uuid.uuid4().hex,
                side="bid",
                price=round(bid_price, 2),
                volume=round(bid_vol, 2),
            )

            ask_price = self.mid_price * (1 + random.uniform(0.001, 0.02))
            ask_vol = random.uniform(0.5, 5.0)

            self.orderbook.add_order(
                order_id=uuid.uuid4().hex,
                side="ask",
                price=round(ask_price, 2),
                volume=round(ask_vol, 2),
            )

    def tick(self):
        action = random.choice(["add", "cancel", "trade"])

        if action == "add":
            side = random.choice(["bid", "ask"])

            price_shift = random.uniform(0.001, 0.02)
            if side == "bid":
                price = self.mid_price * (1 - price_shift)
            else:
                price = self.mid_price * (1 + price_shift)

            volume = random.uniform(0.5, 5.0)

            self.orderbook.add_order(
                order_id=uuid.uuid4().hex,
                side=side,
                price=round(price, 2),
                volume=round(volume, 2),
            )

        elif action == "cancel":
            if self.orderbook.orders:
                order_id = random.choice(list(self.orderbook.orders.keys()))
                self.orderbook.cancel_order(order_id)

        elif action == "trade":
            side = random.choice(["bid", "ask"])

            if side == "bid":
                price = self.orderbook.best_bid()
                book = self.orderbook.bids
            else:
                price = self.orderbook.best_ask()
                book = self.orderbook.asks

            if price is not None and price in book:
                trade_volume = random.uniform(0.1, book[price])
                book[price] -= trade_volume

                if book[price] <= 0:
                    del book[price]

        # --- UPDATE MID PRICE ---
        new_mid = self.orderbook.mid_price()
        if new_mid is not None:
            self.mid_price = new_mid

    def inject_spoof(self, side: str, price: float, volume: float):
        order_id = uuid.uuid4().hex
        self.orderbook.add_order(
            order_id=order_id, side=side, price=round(price, 2), volume=round(volume, 2)
        )
        self.spoof_order_ids.append(order_id)
        self.spoof_active = True
        return order_id

    def cancel_spoof(self):
        for order_id in self.spoof_order_ids[:]:
            self.orderbook.cancel_order(order_id)
            self.spoof_order_ids.remove(order_id)
        self.spoof_active = False

    def _execute_trade(self):
        side = random.choice(["bid", "ask"])

        if side == "bid":
            price = self.orderbook.best_bid()
            book = self.orderbook.bids
        else:
            price = self.orderbook.best_ask()
            book = self.orderbook.asks

        if price is None or price not in book:
            return

        trade_volume = random.uniform(0.1, 1.0)
        book[price] -= trade_volume

        if book[price] <= 0:
            del book[price]
