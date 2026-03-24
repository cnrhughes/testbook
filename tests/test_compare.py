"""Tests for the compare function."""
import math
import pytest
from testbook.compare import compare


class TestCompareSimpleTypes:
    """Test compare with simple types: bools, ints, floats, strings."""

    def test_equal_booleans(self):
        passed, msg = compare(True, True)
        assert passed is True
        assert msg == "Success"

    def test_unequal_booleans(self):
        passed, msg = compare(True, False)
        assert passed is False
        assert "Value mismatch" in msg

    def test_bool_type_mismatch(self):
        """Bool vs int should fail even if values look the same."""
        passed, msg = compare(True, 1)
        assert passed is False
        assert "Type mismatch" in msg

    def test_equal_integers(self):
        passed, msg = compare(42, 42)
        assert passed is True

    def test_equal_floats(self):
        passed, msg = compare(3.14, 3.14)
        assert passed is True

    def test_float_tolerance(self):
        """Floats within tolerance should match."""
        passed, msg = compare(1.0, 1.0000000001)
        assert passed is True

    def test_float_outside_tolerance(self):
        """Floats outside tolerance should not match."""
        passed, msg = compare(1.0, 1.1)
        assert passed is False

    def test_equal_strings(self):
        passed, msg = compare("hello", "hello")
        assert passed is True

    def test_unequal_strings(self):
        passed, msg = compare("hello", "world")
        assert passed is False
        assert "Value mismatch" in msg

    def test_nan_equals_nan(self):
        """NaN should equal NaN in this comparison."""
        passed, msg = compare(float('nan'), float('nan'))
        assert passed is True

    def test_nan_vs_number(self):
        """NaN should not equal a regular number."""
        passed, msg = compare(float('nan'), 1.0)
        assert passed is False

    def test_number_vs_nan(self):
        """Regular number should not equal NaN."""
        passed, msg = compare(1.0, float('nan'))
        assert passed is False


class TestCompareCollections:
    """Test compare with lists and dicts."""

    def test_equal_empty_lists(self):
        passed, msg = compare([], [])
        assert passed is True

    def test_equal_lists(self):
        passed, msg = compare([1, 2, 3], [1, 2, 3])
        assert passed is True

    def test_unequal_list_values(self):
        passed, msg = compare([1, 2, 3], [1, 2, 4])
        assert passed is False
        assert "Value mismatch" in msg
        assert "index [2]" in msg

    def test_list_length_mismatch(self):
        passed, msg = compare([1, 2], [1, 2, 3])
        assert passed is False
        assert "Length mismatch" in msg

    def test_list_vs_tuple(self):
        """List vs tuple should fail type check."""
        passed, msg = compare([1, 2], (1, 2))
        assert passed is False
        assert "Type mismatch" in msg

    def test_nested_lists(self):
        passed, msg = compare([[1, 2], [3, 4]], [[1, 2], [3, 4]])
        assert passed is True

    def test_nested_lists_mismatch(self):
        passed, msg = compare([[1, 2], [3, 4]], [[1, 2], [3, 5]])
        assert passed is False
        assert "index [1]" in msg and "index [1]" in msg

    def test_equal_empty_dicts(self):
        passed, msg = compare({}, {})
        assert passed is True

    def test_equal_dicts(self):
        passed, msg = compare({"a": 1, "b": 2}, {"a": 1, "b": 2})
        assert passed is True

    def test_dict_missing_keys(self):
        passed, msg = compare({"a": 1, "b": 2}, {"a": 1})
        assert passed is False
        assert "Missing keys" in msg

    def test_dict_extra_keys(self):
        passed, msg = compare({"a": 1}, {"a": 1, "b": 2})
        assert passed is False
        assert "Extra keys" in msg

    def test_dict_value_mismatch(self):
        passed, msg = compare({"a": 1, "b": 2}, {"a": 1, "b": 3})
        assert passed is False
        assert "Value mismatch" in msg
        assert "key 'b'" in msg

    def test_dict_vs_list(self):
        """Dict vs list should fail type check."""
        passed, msg = compare({"a": 1}, [1, 2])
        assert passed is False
        assert "Type mismatch" in msg

    def test_nested_dicts(self):
        expected = {"user": {"name": "Alice", "age": 30}}
        actual = {"user": {"name": "Alice", "age": 30}}
        passed, msg = compare(expected, actual)
        assert passed is True

    def test_nested_dicts_mismatch(self):
        expected = {"user": {"name": "Alice", "age": 30}}
        actual = {"user": {"name": "Bob", "age": 30}}
        passed, msg = compare(expected, actual)
        assert passed is False
        assert "key 'user'" in msg


class TestCompareComplexNesting:
    """Test compare with deeply nested or mixed structures."""

    def test_list_of_dicts(self):
        expected = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        actual = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        passed, msg = compare(expected, actual)
        assert passed is True

    def test_list_of_dicts_mismatch(self):
        expected = [{"id": 1, "name": "Alice"}]
        actual = [{"id": 1, "name": "Bob"}]
        passed, msg = compare(expected, actual)
        assert passed is False
        assert "index [0]" in msg

    def test_dict_with_list_values(self):
        expected = {"numbers": [1, 2, 3], "letters": ["a", "b"]}
        actual = {"numbers": [1, 2, 3], "letters": ["a", "b"]}
        passed, msg = compare(expected, actual)
        assert passed is True

    def test_dict_with_list_values_mismatch(self):
        expected = {"numbers": [1, 2, 3]}
        actual = {"numbers": [1, 2, 4]}
        passed, msg = compare(expected, actual)
        assert passed is False
        assert "key 'numbers'" in msg and "index [2]" in msg

    def test_deeply_nested_structure(self):
        expected = {
            "data": [
                {"items": [{"value": 1}, {"value": 2}]},
                {"items": [{"value": 3}]},
            ]
        }
        actual = {
            "data": [
                {"items": [{"value": 1}, {"value": 2}]},
                {"items": [{"value": 3}]},
            ]
        }
        passed, msg = compare(expected, actual)
        assert passed is True

    def test_deeply_nested_mismatch(self):
        expected = {"data": [{"items": [{"value": 1}]}]}
        actual = {"data": [{"items": [{"value": 2}]}]}
        passed, msg = compare(expected, actual)
        assert passed is False
        # Should contain path information about where it failed
        assert "data" in msg or "index" in msg or "key" in msg


class TestCompareEdgeCases:
    """Test edge cases and special scenarios."""

    def test_zero_vs_float_zero(self):
        """Int 0 should equal float 0.0 due to numeric comparison."""
        passed, msg = compare(0, 0.0)
        assert passed is True

    def test_empty_string(self):
        passed, msg = compare("", "")
        assert passed is True

    def test_none_values(self):
        passed, msg = compare(None, None)
        assert passed is True

    def test_none_vs_zero(self):
        passed, msg = compare(None, 0)
        assert passed is False

    def test_list_with_none(self):
        passed, msg = compare([1, None, 3], [1, None, 3])
        assert passed is True

    def test_dict_with_none_value(self):
        passed, msg = compare({"key": None}, {"key": None})
        assert passed is True

    def test_infinity_values(self):
        passed, msg = compare(float('inf'), float('inf'))
        assert passed is True

    def test_negative_infinity(self):
        passed, msg = compare(float('-inf'), float('-inf'))
        assert passed is True

    def test_infinity_vs_number(self):
        passed, msg = compare(float('inf'), 1000)
        assert passed is False


class TestPathStringBuilding:
    """Test that path strings are correctly built for nested structures."""

    def test_path_for_list_index(self):
        passed, msg = compare([1, 2], [1, 3])
        assert passed is False
        assert "at index [1]" in msg

    def test_path_for_dict_key(self):
        passed, msg = compare({"a": 1}, {"a": 2})
        assert passed is False
        assert "at key 'a'" in msg

    def test_path_preserves_through_custom_path(self):
        """When custom path is provided, it should be used in messages."""
        passed, msg = compare(1, 2, path=" at result")
        assert passed is False
        assert "at result" in msg

    def test_nested_path_list_then_dict(self):
        expected = [{"value": 1}]
        actual = [{"value": 2}]
        passed, msg = compare(expected, actual)
        assert passed is False
        # Should show path through list index and dict key
        assert ("index [0]" in msg and "key 'value'" in msg) or ("value" in msg)

    def test_nested_path_dict_then_list(self):
        expected = {"items": [1, 2]}
        actual = {"items": [1, 3]}
        passed, msg = compare(expected, actual)
        assert passed is False
        assert ("key 'items'" in msg and "index [1]" in msg) or ("items" in msg)
