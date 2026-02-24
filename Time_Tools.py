from project_utils import safe_load_json, atomic_write_json

class TotalTimeTracker:
    def __init__(self, persist_file: str = None):
        self._persist_file = persist_file
        self._total_seconds = 0.0
        self._lock = None  # Assuming some lock mechanism is used

    @property
    def total_seconds(self) -> float:
        with self._lock:
            return self._total_seconds

    @total_seconds.setter
    def total_seconds(self, value: float) -> None:
        with self._lock:
            self._total_seconds = value

    def save(self) -> None:
        if not self._persist_file:
            raise ValueError("No persist_file specified")
        data = {"total_seconds": self.total_seconds}
        try:
            atomic_write_json(self._persist_file, data)
        except Exception:
            pass

    def load(self) -> None:
        if not self._persist_file:
            return
        try:
            data = safe_load_json(self._persist_file) or {}
            secs = float(data.get("total_seconds", 0.0))
            with self._lock:
                self._total_seconds = secs
        except Exception:
            pass