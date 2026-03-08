import time
from app.utils.logger import logger

class LatencyTracker:
    def __init__(self):
        self.start_time = None
        self.events = {}

    def start(self):
        """Called exactly when the user finishes speaking"""
        self.start_time = time.perf_counter()
        self.events = {}

    def log_event(self, event_name: str):
        """Logs a specific stage and calculates elapsed time in ms"""
        if self.start_time is not None:
            elapsed = (time.perf_counter() - self.start_time) * 1000
            self.events[event_name] = f"{elapsed:.2f}ms"
            logger.info(f"LATENCY: {event_name} -> {elapsed:.2f}ms")

    def get_summary(self):
        return self.events