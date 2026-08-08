from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class eventType(Enum):
    MARKET = auto()
    SIGNAL = auto()
    ORDER = auto()
    FILL = auto()

class signalType(Enum):
    BUY = auto()
    SELL = auto()
    HOLD = auto()

class orderType(Enum):
    MARKET = auto()
    LIMIT = auto()

    

@dataclass(slots = True)
class event:
    type: eventType

@dataclass(slots = True)
class marketEvent(event):
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def __init__(self, symbol, timestamp, open_, high, low, close, volume):
        super().__init__(eventType.MARKET)
        self.symbol = symbol
        self.timestamp = timestamp
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

@dataclass(slots = True)
class signalEvent(event):
    symbol: str
    signal: signalType

    def __init__(self, symbol, signal):
        super().__init__(eventType.SIGNAL)
        self.symbol = symbol
        self.signal = signal

@dataclass(slots = True)
class orderEvent(event):
    symbol: str
    order_type: orderType
    signal: signalType
    quantity: int

    def __init__(self, symbol, order_type, signal, quantity):
        super().__init__(eventType.ORDER)
        self.symbol = symbol
        self.order_type = order_type
        self.signal = signal
        self.quantity = quantity

@dataclass(slots = True)
class fillEvent(event):
    symbol: str
    signal: signalType
    quantity: int
    fill_price: float
    commission: float

    def __init__(self, symbol, signal, quantity, fill_price, commission):
        super().__init__(eventType.FILL)
        self.symbol = symbol
        self.signal = signal
        self.quantity = quantity
        self.fill_price = fill_price
        self.commission = commission