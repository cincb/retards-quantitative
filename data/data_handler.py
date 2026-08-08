from queue import Queue
import pandas as pd
from events.events import marketEvent

class dataHandler:
    def __init__(self, data: pd.DataFrame, event_queue: Queue):
        self._data = data
        self._event_queue = event_queue
        self._current_bar = 0

    def has_next(self) -> bool:
        return self._current_bar < len(self._data)

    def next(self) -> None:
        if not self.has_next():
            return

        bar = self._data.iloc[self._current_bar]

        event = marketEvent(
            symbol = bar["symbol"],
            timestamp = bar["timestamp"],
            open_ = bar["open"],
            high = bar["high"],
            low = bar["low"],
            close = bar["close"],
            volume = bar["volume"]
        )

        self._event_queue.put(event)
        self._current_bar += 1