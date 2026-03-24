# src/testbook/compare.py
import math
from typing import Any


def compare(expected: Any, actual: Any, path: str = "") -> tuple[bool, str]:
    # 1. Strict Boolean Check
    if isinstance(expected, bool) or isinstance(actual, bool):
        if type(expected) != type(actual):
            return (
                False,
                f"Type mismatch{path}: Expected {type(expected).__name__}, but got {type(actual).__name__}.",
            )
        if expected != actual:
            return (
                False,
                f"Value mismatch{path}: Expected {expected}, but got {actual}.",
            )
        return True, "Success"

    # 2. Existing Numeric Check
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        # Handle NaN case: math.isclose returns False for two NaNs
        if math.isnan(expected) and math.isnan(actual):
            return True, "Success"

        if math.isclose(expected, actual, rel_tol=1e-09, abs_tol=1e-09):
            return True, "Success"
        return False, f"Value mismatch{path}: Expected {expected}, but got {actual}."

    # 3. Handle Lists
    if isinstance(expected, list):
        # Prevent crashes if the student didn't return a list at all
        if not isinstance(actual, list):
            return (
                False,
                f"Type mismatch{path}: Expected a list, but got {type(actual).__name__}.",
            )

        if len(expected) != len(actual):
            return (
                False,
                f"Length mismatch{path}: Expected a list with {len(expected)} items, but your list has {len(actual)} items.",
            )

        for i, (e, a) in enumerate(zip(expected, actual)):
            passed, msg = compare(e, a, path=f"{path} at index [{i}]")
            if not passed:
                return False, msg
        return True, "Success"

    # 4. Handle Dictionaries
    if isinstance(expected, dict):
        # Prevent crashes if the student didn't return a dictionary at all
        if not isinstance(actual, dict):
            return (
                False,
                f"Type mismatch{path}: Expected a dict, but got {type(actual).__name__}.",
            )

        missing_keys = set(expected.keys()) - set(actual.keys())
        if missing_keys:
            return (
                False,
                f"Missing keys{path}: Your dictionary is missing {list(missing_keys)}.",
            )

        extra_keys = set(actual.keys()) - set(expected.keys())
        if extra_keys:
            return (
                False,
                f"Extra keys{path}: Your dictionary has unexpected keys {list(extra_keys)}.",
            )

        for key in expected:
            passed, msg = compare(
                expected[key], actual[key], path=f"{path} at key '{key}'"
            )
            if not passed:
                return False, msg
        return True, "Success"

    # 5. General Type Mismatch Catch-All
    # If they are different types and didn't trigger the int/float allowance above
    if type(expected) != type(actual):
        return (
            False,
            f"Type mismatch{path}: Expected {type(expected).__name__}, but got {type(actual).__name__}.",
        )

    # 6. Exact match fallback
    if expected == actual:
        return True, "Success"

    return False, f"Value mismatch{path}: Expected {expected}, but got {actual}."
