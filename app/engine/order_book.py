import heapq
from dataclasses import dataclass
from typing import Optional

from enums import Side, OrderType, OrderStatus


@dataclass
class Order:
    order_id: str
    price: float
    quantity: float
    side: Side
    order_type: OrderType
    status: OrderStatus
    timestamp: float


class OrderBook:
    def __init__(self):
        self._bids: list[tuple[float, float, Order]] = [] 
        self._asks: list[tuple[float, float, Order]] = [] 
        self._orders: dict[str, Order] = {}
        self._cancelled: set[str] = set()

    def add_order(self, order: Order) -> None:
        self._orders[order.order_id] = order
        if order.side == 'bid':
            heapq.heappush(self._bids,(-order.price, order.timestamp, order))
        elif order.side == 'ask':
            heapq.heappush(self._asks, (order.price, order.timestamp, order))

    def remove_order(self, order_id: str) -> None:
        if order_id in self._orders:
            self._cancelled.add(order_id)
            del self._orders[order_id]

    def _purge(self, heap:list) -> None:
        while heap and heap[0][2].order_id in self._cancelled:
            heapq.heappop(heap)

    def get_best_bid(self) -> Optional[Order]:
        self._purge(self._bids)
        if self._bids:
            return self._bids[0][2]
        return None

    def get_best_ask(self) -> Optional[Order]:
        self._purge(self._purge)
        if self._asks:
            return self._asks[0][2]
        return None

    def get_snapshot(self) -> dict:
        active_bids = sorted(
            [o for o in self._orders.values() if o.side == 'bid'],
            key=lambda o: -o.price,
        )
        active_asks = sorted(
            [o for o in self._orders.values() if o.side == 'ask'],
            key= lambda o: o.price,
        )
        return{
            'bids': [(o.price, o.quantity, o.order_id) for o in active_bids],
            'asks': [(o.price, o.quantity, o.order_id) for o in active_asks],
            'best_bid': active_asks[0].price if active_bids else None,
            'best_ask': active_bids[0].price if active_asks else None,   
        }