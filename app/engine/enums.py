from enum import Enum

class Side(str, Enum):
    
    BUY = 'buy'
    SELL = 'sell'

class OrderType(str, Enum):
    
    LIMIT = 'limit'
    MARKET = 'market'

class OrderStatus(str, Enum):

    OPEN = 'open'
    PARTIALLY_FILLED = 'partially filled'
    FILLED = 'filled'
    CANCELLED = 'cancelled'