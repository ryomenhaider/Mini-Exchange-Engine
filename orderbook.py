from sortedcontainers import SortedDict
from collections import defaultdict
import time

class OrderBook:
    def __init__(self):
        
        self.bids = SortedDict()
        self.asks = SortedDict()
        self.orders = {}

    def add_order(self, order_id: str, side: str, price: float, volume: float):
        
        self.orders[order_id] = {
            'side': side,
            'price': price,
            'volume': volume
        }
        
        if side == 'ask':
            book = self.asks
        elif side == 'bid':
            book = self.bids
        else: 
            raise ValueError('sides should be ask or bid')
        
        if price in book:
            book[price] += volume
        else:
            book[price] = volume


    def cancel_order(self, order_id: str):
        
        order = self.orders.pop(order_id, None)

        side   = order['side']
        price  = order['price']
        volume = order['volume']

        if side == 'ask':
            book = self.asks
        elif side == 'bid':
            book = self.bids

        if price in book:
            book[price] -= volume

            if book[price] >= 0:
                del book[price]


    def best_bid(self) -> float:
        
        if not self.bids:
            return None
        return max(self.bids.keys())


    def best_ask(self) -> float:
        if not self.asks:
            return None
        return min(self.asks.key())
        

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
        
        bid = list(reversed(self.bids.items()))[:levels]
        ask = list(self.asks.items())[:levels]

        return bid, ask
