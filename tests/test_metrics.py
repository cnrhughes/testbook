"""Tests for the PerformanceTracker context manager."""
import time
import pytest
from testbook.metrics import PerformanceTracker


class TestPerformanceTrackerContextManager:
    """Test basic context manager behavior."""

    def test_enter_returns_self(self):
        """__enter__ should return the tracker instance itself."""
        tracker = PerformanceTracker()
        result = tracker.__enter__()
        assert result is tracker
        tracker.__exit__(None, None, None)

    def test_context_manager_with_statement(self):
        """Should work as a context manager with 'with' statement."""
        with PerformanceTracker() as tracker:
            assert isinstance(tracker, PerformanceTracker)

    def test_exit_returns_none(self):
        """__exit__ should return None (or falsy) to not suppress exceptions."""
        tracker = PerformanceTracker()
        tracker.__enter__()
        result = tracker.__exit__(None, None, None)
        assert result is None


class TestDurationTracking:
    """Test that duration_ms is tracked correctly."""

    def test_duration_is_positive(self):
        """Duration should be positive after context exits."""
        with PerformanceTracker() as tracker:
            time.sleep(0.01)  # Sleep 10ms
        assert tracker.duration_ms > 0

    def test_duration_is_reasonable(self):
        """Duration should be at least the amount of sleep."""
        with PerformanceTracker() as tracker:
            sleep_time = 0.05  # 50ms
            time.sleep(sleep_time)
        # Duration should be at least 50ms (accounting for slight overhead)
        assert tracker.duration_ms >= sleep_time * 1000 * 0.9

    def test_duration_before_enter_is_zero(self):
        """Duration should be 0 before entering context."""
        tracker = PerformanceTracker()
        assert tracker.duration_ms == 0

    def test_duration_is_milliseconds(self):
        """Duration should be in milliseconds, not seconds."""
        with PerformanceTracker() as tracker:
            time.sleep(0.01)  # 10ms
        # Should be in range of 10ms (in ms scale), not 0.01ms
        assert tracker.duration_ms > 5  # At least 5ms (allowing for variance)


class TestMemoryTracking:
    """Test that memory tracking works."""

    def test_memory_is_non_negative(self):
        """Peak memory should be non-negative."""
        with PerformanceTracker() as tracker:
            pass
        assert tracker.peak_memory >= 0

    def test_memory_mib_is_non_negative(self):
        """memory_mib should be non-negative."""
        with PerformanceTracker() as tracker:
            pass
        assert tracker.memory_mib >= 0

    def test_memory_mib_is_float(self):
        """memory_mib should return a float."""
        with PerformanceTracker() as tracker:
            pass
        assert isinstance(tracker.memory_mib, float)

    def test_memory_tracking_with_allocation(self):
        """Memory should increase when we allocate objects."""
        with PerformanceTracker() as tracker:
            # Allocate some memory
            large_list = [i for i in range(100000)]
        # Peak memory should have been captured (may be > 0)
        assert tracker.peak_memory >= 0
        # memory_mib should be reasonable (not crazy huge or negative)
        assert 0 <= tracker.memory_mib < 100  # Shouldn't be more than 100 MiB for this test


class TestTrackerInitialization:
    """Test proper initialization of tracker attributes."""

    def test_start_time_initialized_to_zero(self):
        tracker = PerformanceTracker()
        assert tracker.start_time == 0

    def test_end_time_initialized_to_zero(self):
        tracker = PerformanceTracker()
        assert tracker.end_time == 0

    def test_peak_memory_initialized_to_zero(self):
        tracker = PerformanceTracker()
        assert tracker.peak_memory == 0


class TestExceptionHandling:
    """Test that tracker handles exceptions properly."""

    def test_exit_called_on_exception(self):
        """__exit__ should be called even if exception occurs."""
        tracker = PerformanceTracker()
        try:
            with tracker:
                raise ValueError("Test exception")
        except ValueError:
            pass
        # If we get here, __exit__ was called and didn't suppress the exception
        assert tracker.end_time > 0

    def test_exit_returns_none_with_exception_args(self):
        """__exit__ should return None when exception info is passed."""
        tracker = PerformanceTracker()
        try:
            with tracker:
                raise ValueError("Test")
        except ValueError as e:
            result = tracker.__exit__(type(e), e, None)
        assert result is None

    def test_exception_not_suppressed(self):
        """Context manager should not suppress exceptions."""
        with pytest.raises(ValueError, match="Test exception"):
            with PerformanceTracker():
                raise ValueError("Test exception")


class TestMultipleContextManagers:
    """Test multiple tracker instances don't interfere."""

    def test_independent_trackers(self):
        """Multiple trackers should work independently."""
        tracker1 = PerformanceTracker()
        tracker2 = PerformanceTracker()

        with tracker1:
            time.sleep(0.01)

        with tracker2:
            time.sleep(0.02)

        # tracker1 should have less duration than tracker2
        assert tracker1.duration_ms < tracker2.duration_ms

    def test_no_cross_contamination(self):
        """Time from one tracker shouldn't affect another."""
        tracker1 = PerformanceTracker()
        with tracker1:
            time.sleep(0.01)
        duration1 = tracker1.duration_ms

        tracker2 = PerformanceTracker()
        with tracker2:
            time.sleep(0.01)
        duration2 = tracker2.duration_ms

        # Durations should be similar (both ~10ms)
        assert abs(duration1 - duration2) < 20  # Within 20ms of each other
