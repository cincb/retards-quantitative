from abc import ABC, abstractmethod
from queue import Queue
from events.events import marketEvent

class strategy(ABC):
    def __init__(self, event_queue: Queue):
        self._event_queue = event_queue

    @abstractmethod
    def on_market(self, event: marketEvent) -> None:
        pass