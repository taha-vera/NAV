import json
import hashlib
from collections import deque
from datetime import datetime, timedelta

class NAVBuffer:
    """Non-volatile buffer for VERA aggregation node"""

    def __init__(self, max_windows=168):
        self.windows = deque(maxlen=max_windows)
        self.last_commit = None

    def commit_window(self, window_data):
        """Commit a closed aggregation window to buffer"""
        window_data['committed_at'] = datetime.now().isoformat()
        window_data['seq'] = len(self.windows)
        self.windows.append(window_data)
        self.last_commit = datetime.now()
        print(f"Window committed — Seq #{window_data[\"seq\"]}")
        return window_data["seq"]

    def get_window(self, seq):
        """Retrieve window by sequence number"""
        if seq < 0 or seq >= len(self.windows):
            return None
        return self.windows[seq]

    def get_windows_since(self, timestamp):
        """Get all windows after given timestamp"""
        result = []
        for w in self.windows:
            if datetime.fromisoformat(w['window_start']) >= timestamp:
                result.append(w)
        return result

    def verify_integrity(self, seq):
        """Verify hash chain integrity for a window"""
        if seq >= len(self.windows):
            return False, "Window not found"

        window = self.windows[seq]
        computed = hashlib.sha256(json.dumps(window['data'], sort_keys=True).encode()).hexdigest()

        if computed != window['hash']:
            return False, "Hash mismatch — data corrupted"

        if seq > 0:
            prev = self.windows[seq-1]
            if window['window_start'] <= prev['window_start']:
                return False, "Sequence violation — window order"

        return True, "OK"

    def export_chain(self):
        """Export full chain for VERA transmission"""
        return {
            'chain_length': len(self.windows),
            'last_seq': len(self.windows) - 1 if self.windows else -1,
            'last_commit': self.last_commit.isoformat() if self.last_commit else None,
            'windows': list(self.windows),
            'chain_hash': hashlib.sha256(json.dumps(list(self.windows), sort_keys=True).encode()).hexdigest()
        }
