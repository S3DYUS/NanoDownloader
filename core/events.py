from queue import Queue, Empty

class EventBus:
    """Bus de eventos thread-safe para comunicar workers → UI"""

    def __init__(self):
        self.q = Queue()

    def emit(self, tipo, valor=None):
        self.q.put((tipo, valor))

    def poll_all(self):
        items = []
        while True:
            try:
                items.append(self.q.get_nowait())
            except Empty:
                break
        return items