import random
import time
import uuid
from orderbook import OrderBook

class Simulator:
    def __init__(self, mid_price: float = 100.0):
        # create an OrderBook instance
        # store mid_price as starting reference price
        # seed the book by calling _seed_book()
        
        self.orderbook = OrderBook()
        self.mid_price = mid_price
        self._seed_book()
        

    def _seed_book(self):
        # place ~10 realistic bid orders below mid_price
        # place ~10 realistic ask orders above mid_price
        # prices should be random but close to mid_price (within 2%)
        # volumes should be random floats between 0.5 and 5.0
        # use uuid.uuid4().hex as order_id for each
        for _ in range(10):
            
            bid_price = self.mid_price * (1 - random.uniform(0.001, 0.02))
            bid_vol   = random.uniform(0.5,5.0)

            self.orderbook.add_order(
                order_id=uuid.uuid4().hex,
                side='bid',
                price=round(bid_price, 2),
                volume=round(bid_vol, 2)
            ) 
            ask_price = self.mid_price * (1 - random.uniform(0.001, 0.02))
            ask_vol   = random.uniform(0.5,5.0)

            self.orderbook.add_order(
                order_id=uuid.uuid4().hex,
                side='ask',
                price=round(ask_price, 2),
                volume=round(ask_vol, 2)
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
                volume=round(volume, 2)
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
        # place a large order (volume should be 10-20x normal)
        # store its order_id in spoof_order_ids
        # return the order_id
        large_order = {
            spoof_vol = volume * (random.uniform(10, 20)),

        }

    def cancel_spoof(self):
        # cancel all orders in spoof_order_ids
        # clear the list after
        pass

    def _execute_trade(self):
        # pick best bid or best ask randomly
        # reduce its volume by a small random amount (0.1 to 1.0)
        # if volume hits 0, remove that price level
        # hint: you'll need to find the order_id for that price level
        #       look through self.ob.orders to find it
        pass