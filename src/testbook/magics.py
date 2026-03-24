# src/testbook/magics.py
from typing import Any
from IPython.core.magic import Magics, magics_class, line_cell_magic
from .compare import compare
from .metrics import PerformanceTracker
from .ui import display_test_results, display_nudge


# A dictionary mapping common Python errors to plain-English explanations
COMMON_ERROR_NUDGES = {
    "ZeroDivisionError": "A ZeroDivisionError happens when you try to divide a number by zero. Check your denominators!",
    "NameError": "A NameError usually means you are using a variable that hasn't been defined yet. Did you forget to run a previous cell or is there a typo?",
    "TypeError": "TypeErrors occur when you try to perform an operation on the wrong kind of data, like trying to add a number to a string.",
    "IndexError": "An IndexError means you are trying to access a position in a list that doesn't exist. Remember, Python starts counting at 0!",
    "KeyError": "A KeyError happens when you try to grab a key from a dictionary that isn't there. Check your spelling!",
    "AttributeError": "An AttributeError usually means you are trying to use a method that doesn't belong to that object.",
    "SyntaxError": "A SyntaxError means Python couldn't understand your code. Check for missing colons, unclosed brackets, or typos in keywords.",
}


@magics_class
class TestBook(Magics):

    # Changed from @cell_magic to @line_cell_magic
    @line_cell_magic
    def test(self, line: str, cell: str | None = None) -> None:
        # 1. Setup: Figure out which test suite to use
        test_suite_name = line.strip()
        notebook_memory = self.shell.user_ns

        if not test_suite_name:
            print("Error: Please provide a test suite name, like '%%test my_tests'.")
            return

        if test_suite_name not in notebook_memory:
            print(
                f"Error: Could not find tests named '{test_suite_name}'. Did you import them into the notebook?"
            )
            return

        test_cases = notebook_memory[test_suite_name]

        # 2. Execution: Run the student's code and track performance
        with PerformanceTracker() as tracker:
            # Only try to run the cell if the user actually wrote code inside it
            if cell:
                result = self.shell.run_cell(cell)

                # 3. Error Handling
                if result.error_in_exec:
                    error_name = type(result.error_in_exec).__name__
                    nudge = COMMON_ERROR_NUDGES.get(
                        error_name,
                        "Check the traceback above to see what went wrong. Debugging is a core part of programming!",
                    )
                    display_nudge(error_name, nudge)
                    return

        # 4. Evaluation: Check the student's variables or functions against the expected state
        results = list()

        for case in test_cases:
            hint = case.get("hint", None)

            # --- Function Testing Logic ---
            if "function_name" in case:
                func_name = case.get("function_name")

                # Did they define the requested function?
                if func_name not in notebook_memory:
                    results.append(
                        {
                            "var_name": func_name,
                            "passed": False,
                            "message": f"You need to define a function named '{func_name}'.",
                            "hint": hint,
                        }
                    )
                    continue

                student_func = notebook_memory[func_name]
                function_cases = case.get("cases", list())

                # Run through all the input/output pairs provided in the test suite
                for test_case in function_cases:
                    inputs = test_case.get("input", list())
                    expected = test_case.get("expected")

                    # NEW: Use repr() to perfectly preserve inner lists and dictionaries
                    # while creating a clean (arg1, arg2) string for the UI table
                    input_str = f"({', '.join(repr(arg) for arg in inputs)})"
                    display_name = f"{func_name}{input_str}"

                    try:
                        # Unpack the inputs and call the student's function
                        actual = student_func(*inputs)

                        # Catch a "print instead of return" mistake
                        if actual is None and expected is not None:
                            results.append(
                                {
                                    "var_name": display_name,
                                    "passed": False,
                                    "message": "Your function returned None. Did you use print() instead of return?",
                                    "hint": hint,
                                }
                            )
                            continue

                        passed, message = compare(expected, actual)

                        results.append(
                            {
                                "var_name": display_name,
                                "passed": passed,
                                "message": message,
                                "hint": hint,
                            }
                        )
                    except Exception as e:
                        # Catch runtime errors that occur specifically inside the student's function
                        results.append(
                            {
                                "var_name": display_name,
                                "passed": False,
                                "message": f"Error running function: {type(e).__name__} - {e}",
                                "hint": hint,
                            }
                        )

            # --- Variable Testing Logic ---
            elif "expected_state" in case:
                expected_state = case.get("expected_state", dict())

                for var_name, expected_value in expected_state.items():

                    # Did they even create the required variable?
                    if var_name not in notebook_memory:
                        results.append(
                            {
                                "var_name": var_name,
                                "passed": False,
                                "message": f"You need to create a variable named '{var_name}'.",
                                "hint": hint,
                            }
                        )
                        continue

                    # If they did, compare it to the answer key
                    actual_value = notebook_memory[var_name]
                    passed, message = compare(expected_value, actual_value)

                    results.append(
                        {
                            "var_name": var_name,
                            "passed": passed,
                            "message": message,
                            "hint": hint,
                        }
                    )

        # 5. UI: Send the final results and the metrics to the canvas to be drawn
        display_test_results(results, tracker.duration_ms, tracker.memory_mib)


# This function tells IPython how to load our custom magic command
def load_ipython_extension(ipython: Any) -> None:
    ipython.register_magics(TestBook)
