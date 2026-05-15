
import threading
from nav_window import AggregationWindow, WindowState, K_MIN
import uuid

class NAVBuffer:
    def __init__(self):
        self._lock = threading.Lock()
        self._active = None
        self._queue = []
        self._total_signals = 0

    def receive(self, value, device_id=""):
        with self._lock:
            if self._active is None:
                self._active = AggregationWindow(str(uuid.uuid4())[:8])
            ok = self._active.add_signal(value)
            if ok:
                self._total_signals += 1
            return ok

    def close_active(self):
        with self._lock:
            if self._active is None:
                return None
            meta = self._active.close()
            if self._active.is_ready:
                self._queue.append(self._active)
            self._active = None
            return meta

    def next_ready(self):
        with self._lock:
            return self._queue.pop(0) if self._queue else None

    @property
    def queue_size(self):
        with self._lock:
            return len(self._queue)

    @property
    def active_count(self):
        with self._lock:
            return self._active.signal_count if self._active else 0
