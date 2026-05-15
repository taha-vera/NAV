import time
import hashlib
import json
from collections import deque
from datetime import datetime, timedelta

class AggregationWindow:
    def __init__(self, window_size_hours=6):
        self.window_size = timedelta(hours=window_size_hours)
        self.buffer = deque()
        self.window_start = None
        self.is_open = False

    def open_window(self):
        self.window_start = datetime.now()
        self.is_open = True
        self.buffer.clear()
        print(f"[{self.window_start}] Window opened (H6)")
        return self.window_start

    def add_point(self, timestamp, value):
        if not self.is_open:
            raise RuntimeError("Window is closed")
        if timestamp < self.window_start:
            raise ValueError("Timestamp before window start")
        if timestamp > self.window_start + self.window_size:
            raise ValueError("Timestamp exceeds window size (H6)")
        self.buffer.append({
            'timestamp': timestamp.isoformat(),
            'value': value,
            'hash': hashlib.sha256(f'{timestamp}{value}'.encode()).hexdigest()[:8]
        })
        return len(self.buffer)

    def close_window(self):
        if not self.is_open:
            return None
        self.is_open = False
        window_end = self.window_start + self.window_size
        result = {
            'window_start': self.window_start.isoformat(),
            'window_end': window_end.isoformat(),
            'duration_hours': self.window_size.total_seconds() / 3600,
            'points_count': len(self.buffer),
            'data': list(self.buffer),
            'hash': hashlib.sha256(json.dumps(self.buffer, sort_keys=True).encode()).hexdigest()
        }
        print(f"[{datetime.now()}] Window closed — {len(self.buffer)} points")
        return result
