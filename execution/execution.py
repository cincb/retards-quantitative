from queue import Queue
from events.events import fillEvent, orderEvent

class executionSim:
    def __init__(self, event_queue: Queue, commission: float = 0.0, slippage_bps: float = 0.0):
        self._event_queue = event_queue
        self._commission = commission
        self._slippage_bps = slippage_bps

    def execute(self, order: orderEvent, market_price: float):
        fill_price = self._apply_slippage(order, market_price)

        fill = fillEvent(
            symbol = order.symbol,
            signal = order.signal,
            quantity = order.quantity,
            fill_price = fill_price,
            commission = self._commission
        )

        self._event_queue.put(fill)

    def _apply_slippage(self, order: orderEvent, market_price: float) -> float:
        slippage = self._slippage_bps / 10_000

        if order.signal.name == "BUY":
            return market_price * (1 + slippage)
        if order.signal.name == "SELL":
            return market_price * (1 - slippage)

        return market_price