# src/testbook/metrics.py
import time
import tracemalloc


class PerformanceTracker:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.peak_memory = 0

    def __enter__(self):
        # Start the stopwatch using a highly precise performance counter
        self.start_time = time.perf_counter()

        # Start tracking every memory allocation behind the scenes
        tracemalloc.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Stop the stopwatch exactly when the code block finishes or crashes
        self.end_time = time.perf_counter()

        # tracemalloc.get_traced_memory() returns a tuple: (current_memory, peak_memory)
        # We only care about the peak (the maximum RAM used at any one time)
        current, peak = tracemalloc.get_traced_memory()
        self.peak_memory = peak

        # Clean up and stop tracking so we don't slow down the rest of the notebook
        tracemalloc.stop()

    @property
    def duration_ms(self):
        # Convert seconds to milliseconds
        return (self.end_time - self.start_time) * 1000

    @property
    def memory_mib(self):
        # Convert bytes to Mebibytes (MiB) for a clean, readable number in the UI
        return self.peak_memory / (1024 * 1024)
