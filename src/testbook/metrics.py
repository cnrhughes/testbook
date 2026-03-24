"""Performance tracking utilities for test execution.

Provides context manager for measuring execution time and peak memory usage
during test execution.
"""

import time
import tracemalloc


class PerformanceTracker:
    """Context manager for tracking execution time and peak memory usage.

    Measures high-resolution execution time and peak memory consumption for a
    code block. Use as a context manager to automatically start and stop tracking.

    Attributes:
        start_time (float): Timestamp when tracking started (seconds).
        end_time (float): Timestamp when tracking ended (seconds).
        peak_memory (int): Peak memory usage during execution (bytes).

    Example:
        >>> with PerformanceTracker() as tracker:
        ...     result = sum(range(1000))
        >>> print(f"Time: {tracker.duration_ms:.2f} ms")
        >>> print(f"Memory: {tracker.memory_mib:.2f} MiB")
    """

    def __init__(self) -> None:
        self.start_time: float = 0
        self.end_time: float = 0
        self.peak_memory: int = 0

    def __enter__(self) -> "PerformanceTracker":
        """Start tracking execution time and memory usage.

        Returns:
            Self for use as a context manager.
        """
        # Start the stopwatch using a highly precise performance counter
        self.start_time = time.perf_counter()

        # Start tracking every memory allocation behind the scenes
        tracemalloc.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Stop tracking and record final metrics.

        Args:
            exc_type: Exception type if an exception occurred, None otherwise.
            exc_val: Exception instance if an exception occurred, None otherwise.
            exc_tb: Exception traceback if an exception occurred, None otherwise.
        """
        # Stop the stopwatch exactly when the code block finishes or crashes
        self.end_time = time.perf_counter()

        # tracemalloc.get_traced_memory() returns a tuple: (current_memory, peak_memory)
        # We only care about the peak (the maximum RAM used at any one time)
        current, peak = tracemalloc.get_traced_memory()
        self.peak_memory = peak

        # Clean up and stop tracking so we don't slow down the rest of the notebook
        tracemalloc.stop()

    @property
    def duration_ms(self) -> float:
        """Execution duration in milliseconds.

        Returns:
            float: Time elapsed between __enter__ and __exit__ in milliseconds.
        """
        # Convert seconds to milliseconds
        return (self.end_time - self.start_time) * 1000

    @property
    def memory_mib(self) -> float:
        """Peak memory usage in Mebibytes.

        Returns:
            float: Peak memory consumed during execution in MiB.
        """
        # Convert bytes to Mebibytes (MiB) for a clean, readable number in the UI
        return self.peak_memory / (1024 * 1024)
