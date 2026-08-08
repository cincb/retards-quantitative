from queue import Queue
from events.events import fillEvent, orderEvent, signalEvent, signalType, orderType

class Portfolio:
    def __init__(self, event_queue: Queue, init_cash: float, position_size: int):
        self._event_queue = event_queue
        self._cash = init_cash
        self._position_size = position_size
        self._positions: dict[str, int] = {}
        self._average_price: dict[str, float] = {}
        self._realized_pnl = 0.0
        self._equity_curve = []

    def on_signal(self, event: signalEvent, price: float):
        symbol = event.symbol
        current_position = self._positions.get(symbol, 0)

        if event.signal == signalType.BUY:
            if current_position == 0:
                self._create_order(symbol, signalType.BUY, self._position_size)

        elif event.signal == signalType.SELL:
            if current_position > 0:
                self._create_order(symbol, signalType.SELL, current_position)

    def on_fill(self, event: fillEvent):
        symbol = event.symbol
        quantity = event.quantity
        price = event.fill_price
        current_position = self._positions.get(symbol, 0)

        if event.signal == signalType.BUY:
            new_position = current_position + quantity

            if current_position == 0:
                self._average_price[symbol] = price
            else:
                old_value = current_position * self._average_price[symbol]
                new_value = quantity * price

                self._average_price[symbol] = (old_value + new_value) / new_position

            self._positions[symbol] = new_position
            self._cash -= quantity * price + event.commission

        elif event.signal == signalType.SELL:
            if current_position < quantity:
                raise ValueError("Cannot sell more than current position.")

            entry_price = self._average_price[symbol]

            self._realized_pnl += (price - entry_price) * quantity
            self._positions[symbol] -= quantity
            self._cash += quantity * price - event.commission

            if self._positions[symbol] == 0:
                del self._positions[symbol]
                del self._average_price[symbol]

    def _create_order(self, symbol: str, signal: signalType, quantity: int):
        order = orderEvent(symbol = symbol, order_type = orderType.MARKET, signal = signal, quantity = quantity)
        self._event_queue.put(order)

    def update_equity(self, market_price):
        equity = self._cash

        for symbol, quantity in self._positions.items():
            equity += quantity * market_price

        self._equity_curve.append(equity)

    @property
    def cash(self) -> float:
        return self._cash

    @property
    def realized_pnl(self) -> float:
        return self._realized_pnl

    def position(self, symbol: str) -> int:
        return self._positions.get(symbol, 0)