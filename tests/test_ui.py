"""Tests for the UI display functions."""
import pytest
from unittest.mock import patch, call
from testbook.ui import display_test_results, display_nudge


class TestDisplayTestResults:
    """Test the display_test_results function."""

    @patch("testbook.ui.display")
    def test_displays_html(self, mock_display):
        """Should call display with HTML."""
        results = [{"var_name": "x", "passed": True, "message": "OK", "hint": None}]
        display_test_results(results, 10.5, 2.3)

        mock_display.assert_called_once()
        # Check that it was called with an HTML object
        call_args = mock_display.call_args[0]
        assert len(call_args) == 1

    @patch("testbook.ui.display")
    def test_includes_variable_names(self, mock_display):
        """HTML output should include variable names."""
        results = [
            {"var_name": "result", "passed": True, "message": "OK", "hint": None}
        ]
        display_test_results(results, 0, 0)

        html_obj = mock_display.call_args[0][0]
        html_str = html_obj.data
        assert "result" in html_str

    @patch("testbook.ui.display")
    def test_includes_pass_status(self, mock_display):
        """HTML should include PASS for passing tests."""
        results = [{"var_name": "x", "passed": True, "message": "Good", "hint": None}]
        display_test_results(results, 0, 0)

        html_str = mock_display.call_args[0][0].data
        assert "PASS" in html_str
        assert "pass" in html_str  # CSS class

    @patch("testbook.ui.display")
    def test_includes_fail_status(self, mock_display):
        """HTML should include FAIL for failing tests."""
        results = [{"var_name": "x", "passed": False, "message": "Wrong", "hint": None}]
        display_test_results(results, 0, 0)

        html_str = mock_display.call_args[0][0].data
        assert "FAIL" in html_str
        assert "fail" in html_str  # CSS class

    @patch("testbook.ui.display")
    def test_includes_messages(self, mock_display):
        """HTML should include feedback messages."""
        results = [
            {"var_name": "x", "passed": True, "message": "Correct answer!", "hint": None}
        ]
        display_test_results(results, 0, 0)

        html_str = mock_display.call_args[0][0].data
        assert "Correct answer!" in html_str

    @patch("testbook.ui.display")
    def test_includes_hints_when_failed(self, mock_display):
        """HTML should include hint when provided and test failed."""
        results = [
            {
                "var_name": "x",
                "passed": False,
                "message": "Wrong",
                "hint": "Try a different approach",
            }
        ]
        display_test_results(results, 0, 0)

        html_str = mock_display.call_args[0][0].data
        assert "Try a different approach" in html_str
        assert "details" in html_str  # Should use <details> for hint

    @patch("testbook.ui.display")
    def test_no_hints_when_passed(self, mock_display):
        """HTML should not include hint if test passed."""
        results = [
            {
                "var_name": "x",
                "passed": True,
                "message": "Good",
                "hint": "This hint should not appear",
            }
        ]
        display_test_results(results, 0, 0)

        html_str = mock_display.call_args[0][0].data
        assert "This hint should not appear" not in html_str

    @patch("testbook.ui.display")
    def test_includes_duration_metrics(self, mock_display):
        """HTML should include duration in milliseconds."""
        results = []
        display_test_results(results, 42.5, 0)

        html_str = mock_display.call_args[0][0].data
        assert "42.50" in html_str or "42.5" in html_str
        assert "ms" in html_str

    @patch("testbook.ui.display")
    def test_includes_memory_metrics(self, mock_display):
        """HTML should include memory in MiB."""
        results = []
        display_test_results(results, 0, 15.7)

        html_str = mock_display.call_args[0][0].data
        assert "15.70" in html_str or "15.7" in html_str
        assert "MiB" in html_str

    @patch("testbook.ui.display")
    def test_multiple_results(self, mock_display):
        """Should handle multiple test results."""
        results = [
            {"var_name": "a", "passed": True, "message": "Good", "hint": None},
            {"var_name": "b", "passed": False, "message": "Bad", "hint": None},
            {"var_name": "c", "passed": True, "message": "Good", "hint": None},
        ]
        display_test_results(results, 0, 0)

        html_str = mock_display.call_args[0][0].data
        assert "a" in html_str
        assert "b" in html_str
        assert "c" in html_str

    @patch("testbook.ui.display")
    def test_empty_results(self, mock_display):
        """Should handle empty results list."""
        display_test_results([], 0, 0)

        mock_display.assert_called_once()
        html_str = mock_display.call_args[0][0].data
        # Should still have table structure
        assert "table" in html_str

    @patch("testbook.ui.display")
    def test_html_structure(self, mock_display):
        """HTML should have proper structure."""
        results = []
        display_test_results(results, 0, 0)

        html_str = mock_display.call_args[0][0].data
        assert "<style>" in html_str
        assert "</style>" in html_str
        assert "<table" in html_str
        assert "</table>" in html_str
        assert "testbook-" in html_str  # CSS classes


class TestDisplayNudge:
    """Test the display_nudge function."""

    @patch("testbook.ui.display")
    def test_displays_html_for_nudge(self, mock_display):
        """Should call display with HTML."""
        display_nudge("ValueError", "Check your input")

        mock_display.assert_called_once()
        call_args = mock_display.call_args[0]
        assert len(call_args) == 1

    @patch("testbook.ui.display")
    def test_includes_error_name(self, mock_display):
        """HTML should include the error name."""
        display_nudge("TypeError", "Wrong data type")

        html_str = mock_display.call_args[0][0].data
        assert "TypeError" in html_str

    @patch("testbook.ui.display")
    def test_includes_nudge_text(self, mock_display):
        """HTML should include the nudge message."""
        display_nudge("Error", "Try something different")

        html_str = mock_display.call_args[0][0].data
        assert "Try something different" in html_str

    @patch("testbook.ui.display")
    def test_includes_bulb_emoji(self, mock_display):
        """HTML should include the bulb emoji hint."""
        display_nudge("Error", "Message")

        html_str = mock_display.call_args[0][0].data
        assert "💡" in html_str

    @patch("testbook.ui.display")
    def test_has_styling(self, mock_display):
        """HTML should include styling."""
        display_nudge("Error", "Message")

        html_str = mock_display.call_args[0][0].data
        assert "style=" in html_str
        assert "background" in html_str.lower()

    @patch("testbook.ui.display")
    def test_blue_background_for_nudge(self, mock_display):
        """Nudge should have blue-ish background."""
        display_nudge("Error", "Message")

        html_str = mock_display.call_args[0][0].data
        # Should have blue color (e7f1ff is light blue)
        assert "#e7f1ff" in html_str or "#0d6efd" in html_str

    @patch("testbook.ui.display")
    def test_different_error_names(self, mock_display):
        """Should handle different error names."""
        for error_name in ["ValueError", "TypeError", "KeyError", "IndexError"]:
            mock_display.reset_mock()
            display_nudge(error_name, "Message")

            html_str = mock_display.call_args[0][0].data
            assert error_name in html_str
