from collections import deque
from events.events import marketEvent, signalEvent, signalType
from strategy.base import strategy

class movingAverageStrategy(strategy):
    def __init__(self, event_queue, fast_period: int = 10, slow_period: int = 30):
        super().__init__(event_queue)

        if fast_period >= slow_period:
            raise ValueError("The fast period should be smaller than the slow period.")

        self._fast_period = fast_period
        self._slow_period = slow_period
        self._prices = deque(maxlen = slow_period)
        self._current_signal = signalType.HOLD

    def on_market(self, event: marketEvent) -> None:
        self._prices.append(event.close)

        if len(self._prices) < self._slow_period:
            return

        fast_ma = sum(list(self._prices)[-self._fast_period:]) / self._fast_period
        slow_ma = sum(self._prices) / self._slow_period

        if fast_ma > slow_ma and self._current_signal != signalType.BUY:
            self._current_signal = signalType.BUY

            self._event_queue.put(
                signalEvent(
                    symbol = event.symbol,
                    signal = signalType.BUY
                )
            )

        elif fast_ma < slow_ma and self._current_signal != signalType.SELL:
            self._current_signal = signalType.SELL

            self._event_queue.put(
                signalEvent(
                    symbol = event.symbol,
                    signal = signalType.SELL
                )
            )