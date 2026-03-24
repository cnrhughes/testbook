"""Tests for the IPython magic command."""
import pytest
from unittest.mock import MagicMock, patch, call
from testbook.magics import BookTest, load_ipython_extension, COMMON_ERROR_NUDGES


class TestLoadIPythonExtension:
    """Test the load_ipython_extension function."""

    def test_registers_magics(self):
        """Should register BookTest magics with IPython."""
        mock_ipython = MagicMock()
        load_ipython_extension(mock_ipython)

        mock_ipython.register_magics.assert_called_once_with(BookTest)


class TestTestMagicBasics:
    """Test basic test magic behavior."""

    def test_requires_test_suite_name(self, mock_ipython_shell):
        """Should require a test suite name."""
        magic = BookTest(mock_ipython_shell)

        with patch("builtins.print") as mock_print:
            magic.test("")
            mock_print.assert_called()
            assert "Error" in str(mock_print.call_args)

    def test_test_suite_not_found(self, mock_ipython_shell):
        """Should error if test suite doesn't exist."""
        mock_ipython_shell.user_ns = {}
        magic = BookTest(mock_ipython_shell)

        with patch("builtins.print") as mock_print:
            magic.test("nonexistent_tests")
            mock_print.assert_called()
            assert "not find" in str(mock_print.call_args).lower()

    @patch("testbook.magics.display_test_results")
    def test_returns_none(self, mock_display, mock_ipython_shell):
        """Test magic should return None."""
        mock_ipython_shell.user_ns = {"my_tests": []}
        magic = BookTest(mock_ipython_shell)

        result = magic.test("my_tests")
        assert result is None


class TestVariableTesting:
    """Test variable comparison testing."""

    @patch("testbook.magics.display_test_results")
    def test_variable_exact_match(self, mock_display, mock_ipython_shell):
        """Should pass when variable matches expected value."""
        test_cases = [{"expected_state": {"x": 42}}]
        mock_ipython_shell.user_ns = {"x": 42, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        # Check that results were displayed
        mock_display.assert_called_once()
        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is True

    @patch("testbook.magics.display_test_results")
    def test_variable_mismatch(self, mock_display, mock_ipython_shell):
        """Should fail when variable doesn't match."""
        test_cases = [{"expected_state": {"x": 42}}]
        mock_ipython_shell.user_ns = {"x": 10, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is False

    @patch("testbook.magics.display_test_results")
    def test_missing_variable(self, mock_display, mock_ipython_shell):
        """Should fail if required variable is missing."""
        test_cases = [{"expected_state": {"missing_var": 10}}]
        mock_ipython_shell.user_ns = {"my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is False
        assert "missing" in results[0]["message"].lower()

    @patch("testbook.magics.display_test_results")
    def test_multiple_variables(self, mock_display, mock_ipython_shell):
        """Should test multiple variables."""
        test_cases = [
            {"expected_state": {"a": 1, "b": 2, "c": 3}}
        ]
        mock_ipython_shell.user_ns = {
            "a": 1,
            "b": 2,
            "c": 3,
            "my_tests": test_cases,
        }
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert len(results) == 3
        assert all(r["passed"] for r in results)

    @patch("testbook.magics.display_test_results")
    def test_variable_with_hint(self, mock_display, mock_ipython_shell):
        """Should include hint in result if provided."""
        test_cases = [
            {
                "expected_state": {"x": 42},
                "hint": "Try multiplying by 6",
            }
        ]
        mock_ipython_shell.user_ns = {"x": 10, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["hint"] == "Try multiplying by 6"


class TestFunctionTesting:
    """Test function comparison testing."""

    @patch("testbook.magics.display_test_results")
    def test_function_exists_check(self, mock_display, mock_ipython_shell):
        """Should fail if required function is missing."""
        test_cases = [{"function_name": "add", "cases": []}]
        mock_ipython_shell.user_ns = {"my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is False
        assert "define" in results[0]["message"].lower()

    @patch("testbook.magics.display_test_results")
    def test_function_correct_output(self, mock_display, mock_ipython_shell):
        """Should pass when function output is correct."""
        def add(a, b):
            return a + b

        test_cases = [
            {
                "function_name": "add",
                "cases": [
                    {"input": [2, 3], "expected": 5},
                ],
            }
        ]
        mock_ipython_shell.user_ns = {"add": add, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is True

    @patch("testbook.magics.display_test_results")
    def test_function_wrong_output(self, mock_display, mock_ipython_shell):
        """Should fail when function output is wrong."""
        def add(a, b):
            return a - b  # Wrong!

        test_cases = [
            {
                "function_name": "add",
                "cases": [
                    {"input": [2, 3], "expected": 5},
                ],
            }
        ]
        mock_ipython_shell.user_ns = {"add": add, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is False

    @patch("testbook.magics.display_test_results")
    def test_function_returns_none(self, mock_display, mock_ipython_shell):
        """Should catch print instead of return."""
        def print_instead():
            print("result")
            # No return!

        test_cases = [
            {
                "function_name": "print_instead",
                "cases": [
                    {"input": [], "expected": "result"},
                ],
            }
        ]
        mock_ipython_shell.user_ns = {"print_instead": print_instead, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is False
        assert "print" in results[0]["message"].lower()

    @patch("testbook.magics.display_test_results")
    def test_function_multiple_test_cases(self, mock_display, mock_ipython_shell):
        """Should run multiple test cases for one function."""
        def square(x):
            return x * x

        test_cases = [
            {
                "function_name": "square",
                "cases": [
                    {"input": [2], "expected": 4},
                    {"input": [3], "expected": 9},
                    {"input": [0], "expected": 0},
                ],
            }
        ]
        mock_ipython_shell.user_ns = {"square": square, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert len(results) == 3
        assert all(r["passed"] for r in results)

    @patch("testbook.magics.display_test_results")
    def test_function_runtime_error(self, mock_display, mock_ipython_shell):
        """Should catch runtime errors in function."""
        def bad_func():
            return 1 / 0  # ZeroDivisionError

        test_cases = [
            {
                "function_name": "bad_func",
                "cases": [
                    {"input": [], "expected": 0},
                ],
            }
        ]
        mock_ipython_shell.user_ns = {"bad_func": bad_func, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["passed"] is False
        assert "Error" in results[0]["message"]

    @patch("testbook.magics.display_test_results")
    def test_function_with_hint(self, mock_display, mock_ipython_shell):
        """Should include hint if provided."""
        def add(a, b):
            return a - b

        test_cases = [
            {
                "function_name": "add",
                "cases": [
                    {"input": [2, 3], "expected": 5},
                ],
                "hint": "Remember to add, not subtract",
            }
        ]
        mock_ipython_shell.user_ns = {"add": add, "my_tests": test_cases}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        results = mock_display.call_args[0][0]
        assert results[0]["hint"] == "Remember to add, not subtract"


class TestCellExecution:
    """Test execution of cell code."""

    @patch("testbook.magics.display_test_results")
    def test_cell_code_executed(self, mock_display, mock_ipython_shell):
        """Should execute cell code if provided."""
        mock_ipython_shell.user_ns = {"my_tests": []}
        mock_ipython_shell.run_cell = MagicMock(
            return_value=MagicMock(error_in_exec=None)
        )
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests", cell="x = 10")

        mock_ipython_shell.run_cell.assert_called_once_with("x = 10")

    @patch("testbook.magics.display_nudge")
    def test_cell_error_handling(self, mock_nudge, mock_ipython_shell):
        """Should display nudge if cell has error."""
        error = ValueError("Invalid input")
        result = MagicMock(error_in_exec=error)
        mock_ipython_shell.user_ns = {"my_tests": []}
        mock_ipython_shell.run_cell = MagicMock(return_value=result)
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests", cell="bad code")

        mock_nudge.assert_called_once()
        args = mock_nudge.call_args[0]
        assert "ValueError" in args[0]

    @patch("testbook.magics.display_nudge")
    def test_common_error_nudge(self, mock_nudge, mock_ipython_shell):
        """Should use common error nudge for known errors."""
        error = ZeroDivisionError("division by zero")
        result = MagicMock(error_in_exec=error)
        mock_ipython_shell.user_ns = {"my_tests": []}
        mock_ipython_shell.run_cell = MagicMock(return_value=result)
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests", cell="x = 1/0")

        args = mock_nudge.call_args[0]
        assert "ZeroDivisionError" in args[0]
        assert "zero" in args[1].lower()


class TestCommonErrorNudges:
    """Test that common error nudges exist and make sense."""

    def test_zero_division_nudge_exists(self):
        assert "ZeroDivisionError" in COMMON_ERROR_NUDGES
        assert "zero" in COMMON_ERROR_NUDGES["ZeroDivisionError"].lower()

    def test_name_error_nudge_exists(self):
        assert "NameError" in COMMON_ERROR_NUDGES

    def test_type_error_nudge_exists(self):
        assert "TypeError" in COMMON_ERROR_NUDGES

    def test_index_error_nudge_exists(self):
        assert "IndexError" in COMMON_ERROR_NUDGES

    def test_key_error_nudge_exists(self):
        assert "KeyError" in COMMON_ERROR_NUDGES

    def test_attribute_error_nudge_exists(self):
        assert "AttributeError" in COMMON_ERROR_NUDGES

    def test_syntax_error_nudge_exists(self):
        assert "SyntaxError" in COMMON_ERROR_NUDGES


class TestPerformanceTracking:
    """Test that performance metrics are tracked."""

    @patch("testbook.magics.display_test_results")
    def test_duration_and_memory_passed(self, mock_display, mock_ipython_shell):
        """Should pass duration and memory to display_test_results."""
        mock_ipython_shell.user_ns = {"my_tests": []}
        magic = BookTest(mock_ipython_shell)

        magic.test("my_tests")

        # Check that display_test_results was called with metrics
        assert mock_display.called
        args = mock_display.call_args[0]
        # args[0] = results, args[1] = duration_ms, args[2] = memory_mib
        assert len(args) == 3
        assert isinstance(args[1], float)  # duration_ms
        assert isinstance(args[2], float)  # memory_mib
