from dataclasses import dataclass
from typing import Optional

from enums import Side, OrderType, OrderStatus
from order_book import Order, OrderBook


@dataclass
class Trade:
    trade_id: str
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: float
    timestamp: float


class MatchingEngine:
    def __init__(self, order_book: OrderBook):
        self.order_book = order_book
        self.trades: list[Trade] = []

    def process_order(self, order: Order) -> list[Trade]:
        # Match against opposite side (price-time priority)
        # For partial fills: update order.quantity, set status to PARTIALLY_FILLED
        # For full fills: set status to FILLED
        # If limit order with remaining quantity: add to order book
        
        pass

    def execute_trade(
        self,
        buy_order: Order,
        sell_order: Order,
        quantity: float,
        price: float,
    ) -> Trade:
        # Create and return a Trade object
        # Update buy/sell order statuses and quantities
        pass

    def cancel_order(self, order_id: str) -> Optional[Order]:
        # Set order status to CANCELLED
        # Remove from order book
        pass