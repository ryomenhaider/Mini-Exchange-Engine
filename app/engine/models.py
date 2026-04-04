class Order:
    
    def __init__(self, id, user_id, price, quantity, remaining_quantity, order_type):
        
        self.id = id
        self.user_id = user_id
        self.price = price
        self.quantity = quantity
        self.remaining_quantity = remaining_quantity
        self.order_type = order_type

class Trade:

    def __init__(self, buy_order_id, sell_order_id, quantity, price, timestamps):
        
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.quantity = quantity
        self.price = price
        self.timestamps = timestamps

class OrderBookEntry:

    def __init__(self, order, timestamps):
        
        self.order = order
        self.timestamps = timestamps
