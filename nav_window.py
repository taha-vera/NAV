
import threading
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional
from enum import Enum

WINDOW_TIMEOUT_SEC = 3600
K_MIN = 100
MAX_SIGNALS = 10_000

class WindowState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    EXPIRED = "expired"
    CONSUMED = "consumed"

class AggregationWindow:
    def __init__(self, window_id):
        self.window_id = window_id
        self._signals = []
        self._seen_devices = set()  # H1: track device contributions
        self._lock = threading.Lock()
        self._state = WindowState.OPEN
        self._opened_at = datetime.now(timezone.utc)

    def add_signal(self, value, device_id=None):
        # H1: max_per_device=1 — one signal per SIM per window
        # Single lock block to prevent race condition between H1 check and state check
        with self._lock:
            if self._state != WindowState.OPEN: return False
            if device_id is not None:
                if device_id in self._seen_devices:
                    raise ValueError(f'H1 violation: device {device_id} already contributed')
                self._seen_devices.add(device_id)
            if len(self._signals) >= MAX_SIGNALS: return False
            if not (0.0 <= value <= 1.0): return False
            self._signals.append(value)
            return True

    def close(self):
        with self._lock:
            if self._state == WindowState.OPEN:
                self._state = WindowState.CLOSED
            return {"n": len(self._signals), "state": self._state}

    def get_signals(self):
        with self._lock:
            if self._state != WindowState.CLOSED:
                raise RuntimeError("Fenetre doit etre CLOSED")
            return list(self._signals)

    @property
    def is_ready(self):
        with self._lock:
            return self._state == WindowState.CLOSED and len(self._signals) >= K_MIN

    @property
    def signal_count(self):
        with self._lock:
            return len(self._signals)
