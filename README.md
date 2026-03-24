# 📚 `testbook`

`testbook` is a Jupyter notebook extension that provides interactive, automated testing and feedback for student code exercises. It integrates seamlessly with Jupyter notebooks using IPython magic commands to validate student solutions with clear, helpful error messages and performance metrics.

## ✨ Features

- **Automatic Test Execution**: Run test cases directly in notebook cells using the `test` magic command (as a line or cell magic)
- **Variable Validation**: Test that students create variables with correct values
- **Function Testing**: Validate student-defined functions with multiple test cases
- **Intelligent Comparison**: Deep equality checking for numbers, strings, lists, dictionaries, and booleans
- **Helpful Error Messages**: Common Python errors (ZeroDivisionError, NameError, etc.) come with plain-English explanations
- **Interactive Hints**: Failed tests can display hints to guide students without giving away solutions
- **Performance Metrics**: Track execution time and memory usage for each test
- **Beautiful UI**: Clean HTML table display with pass/fail indicators and detailed feedback

## 📦 Installation

First, ensure you have Python 3.13 or later installed. Then install the package and its dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## 🚀 Quick Start

### 1. Load the Extension

In a Jupyter notebook cell, load the `testbook` extension:

```python
%load_ext testbook
```

### 2. Define Your Tests

Create a Python file (e.g., `my_tests.py`) that defines test suites. See the [Writing Tests](#writing-tests) section below for details.

### 3. Import and Run Tests

In your notebook, import your tests and use the `test` magic command. It can be used as a line magic (`%test`) or cell magic (`%%test`):

```python
from my_tests import my_test_suite

# As a cell magic (for code blocks):
%%test my_test_suite
# Student code goes here

# Or as a line magic (for single-line execution):
%test my_test_suite
```

## 🧪 Writing Tests

Tests are defined as Python data structures (lists of dictionaries) in a separate `.py` file. There are two types of tests:

### Type 1: Variable Tests

Test that students create a variable with the expected value.

```python
# my_tests.py
list_cleaning_tests = [
    {
        "expected_state": {
            "fruits": ["apple", "banana", "cherry"]
        },
        "hint": "Make sure your list is in alphabetical order and contains only three fruits."
    }
]
```

**Fields:**
- `expected_state` (required dict): Maps variable names to their expected values
- `hint` (optional string): A hint displayed when the test fails

### Type 2: Function Tests

Test that students define a function and that it produces correct outputs for given inputs.

```python
# my_tests.py
add_numbers_tests = [
    {
        "function_name": "add",
        "cases": [
            {"input": [1, 2], "expected": 3},
            {"input": [10, 20], "expected": 30},
            {"input": [-5, 5], "expected": 0},
        ],
        "hint": "Your function should take two arguments and return their sum."
    }
]
```

**Fields:**
- `function_name` (required string): Name of the function to test
- `cases` (required list): Array of test cases with:
  - `input` (required list): Arguments to pass to the function (unpacked as `func(*input)`)
  - `expected` (required): Expected return value
- `hint` (optional string): Displayed when any case fails

### Complete Example Test File

```python
# my_tests.py

# Test 1: Variable validation
list_cleaning_tests = [
    {
        "expected_state": {"fruits": ["apple", "banana", "cherry"]},
        "hint": "Filter the list and sort alphabetically.",
    }
]

# Test 2: Function testing
add_numbers_tests = [
    {
        "function_name": "add",
        "cases": [
            {"input": [1, 2], "expected": 3},
            {"input": [10, 20], "expected": 30},
            {"input": [-5, 5], "expected": 0},
        ],
        "hint": "Your function should take two arguments and return their sum.",
    }
]

# Test 3: Multiple assertions in one test
dictionary_tests = [
    {
        "expected_state": {
            "user_data": {
                "name": "Alice",
                "age": 30,
                "scores": [85, 90, 88]
            }
        },
        "hint": "Make sure all values are correct, including nested data.",
    }
]
```

## 📓 Using Tests in a Notebook

### Variable Test Example

```python
# Cell 1: Load extension and import tests
%load_ext testbook
from my_tests import list_cleaning_tests

# Cell 2: Student code (using cell magic)
%%test list_cleaning_tests

unfiltered_fruits = ["mango", "banana", "orange", "apple", "cherry", "grape"]
fruits = [element for element in unfiltered_fruits if element in {"apple", "banana", "cherry"}]
fruits = sorted(fruits)
```

### Function Test Example

```python
# Cell 1: Load extension and import tests
%load_ext testbook
from my_tests import add_numbers_tests

# Cell 2: Student code (using cell magic)
%%test add_numbers_tests

def add(a, b):
    return a + b
```

## ⚖️ Comparison Logic

`testbook` compares expected and actual values with intelligent type checking:

| Type | Behavior |
|------|----------|
| **Numbers** (int, float) | Compares with floating-point tolerance (1e-9) |
| **Booleans** | Requires exact type and value match |
| **Strings** | Exact string matching |
| **Lists** | Same length, all elements match recursively |
| **Dictionaries** | Same keys, all values match recursively |
| **Nested structures** | Recursively validates nested lists/dicts |

## ⚠️ Error Handling

When student code crashes, `testbook` catches the error and displays:

1. The standard Jupyter traceback
2. A friendly blue box with a plain-English explanation of the error

### Common Error Messages

- **ZeroDivisionError**: "Check your denominators!"
- **NameError**: "Did you forget to run a previous cell or is there a typo?"
- **TypeError**: "Did you try to perform an operation on the wrong kind of data?"
- **IndexError**: "Remember, Python starts counting at 0!"
- **KeyError**: "Check that the key exists in your dictionary!"
- **SyntaxError**: "Check for missing colons, unclosed brackets, or typos in keywords."

## 📊 Test Output

When a test runs, students see an interactive HTML table with:

- **Variable column**: The variable or function name being tested
- **Status column**: PASS (green) or FAIL (red)
- **Feedback column**:
  - Success message for passing tests
  - Detailed error message for failures
  - Clickable hint (if provided) that appears on failed tests
- **Metrics footer**: Execution time and peak memory usage

## 🔧 API Reference

### Comparison Function

While primarily used internally, the `compare` function can be imported and used directly:

```python
from testbook import compare

passed, message = compare(expected, actual)
print(message)  # "Success" or detailed error message
```

### Performance Tracker

Monitor execution performance:

```python
from testbook.metrics import PerformanceTracker

with PerformanceTracker() as tracker:
    # Your code here
    pass

print(f"Time: {tracker.duration_ms:.2f} ms")
print(f"Memory: {tracker.memory_mib:.2f} MiB")
```

## 📁 Project Structure

```
testbook/
├── src/testbook/
│   ├── __init__.py           # Package exports
│   ├── magics.py             # IPython magic command & test execution (typed)
│   ├── compare.py            # Comparison logic for values (typed)
│   ├── ui.py                 # HTML rendering for results (typed)
│   └── metrics.py            # Performance tracking (typed)
├── tests/                    # Comprehensive pytest test suite
│   ├── test_compare.py
│   ├── test_metrics.py
│   ├── test_ui.py
│   └── test_magics.py
├── pyproject.toml            # Project configuration
└── README.md                 # README
```

## 🔑 Key Components

### magics.py
Implements the `%%test` cell magic. When executed:
1. Retrieves the named test suite from the notebook namespace
2. Executes the student's code
3. Compares student variables/functions against expected values
4. Displays results in an interactive HTML table

### compare.py
Provides deep equality checking that handles:
- Type mismatches with clear error messages
- Floating-point tolerance for numeric comparisons
- Recursive validation of nested data structures
- Specific error reporting (missing keys, wrong length, etc.)

### ui.py
Renders test results as interactive HTML with:
- Color-coded pass/fail status
- Clickable hints for failed tests
- Performance metrics (time and memory)
- Clean, accessible styling

### metrics.py
Tracks performance using:
- `time.perf_counter()` for high-resolution timing
- `tracemalloc` for peak memory usage
- Context manager pattern for easy integration

## 💡 Tips for Instructors

1. **Keep hints concise**: Hints should guide without giving away the solution
2. **Test edge cases**: Include multiple test cases to catch incomplete solutions
3. **Clear error messages**: Use descriptive names and expected states
4. **Provide examples**: Show working notebook examples before students write code
5. **Start simple**: Begin with variable tests before function tests
6. **Incremental complexity**: Build up from basic exercises to more complex ones

## 🔍 Troubleshooting

### "Error: Please provide a test suite name"
Make sure you're using the `test` magic correctly:
```python
%%test test_name  # Cell magic: include the test name!
%test test_name   # Or use line magic
```

### "Error: Could not find tests named 'test_name'"
The test variable isn't imported or doesn't exist:
```python
from my_tests import test_name  # Must import first
```

### "Your function returned None"
Student used `print()` instead of `return`:
```python
def add(a, b):
    return a + b  # Use return, not print!
```

### Function signature doesn't match
Ensure student function takes the right number of arguments:
```python
# If test has: {"input": [1, 2], "expected": 3}
def add(a, b):  # Must accept 2 arguments
    return a + b
```

## 🧬 Testing

The project includes a comprehensive test suite using pytest. Run tests with:

```bash
# Using uv
uv run pytest

# Or using pip
pytest
```

Test coverage includes:
- `tests/test_compare.py`: Comparison logic validation
- `tests/test_metrics.py`: Performance tracking
- `tests/test_ui.py`: HTML rendering
- `tests/test_magics.py`: IPython magic command functionality

## 🛠️ Development

### Dependencies

- `ipykernel>=7.2.0`: For Jupyter notebook support
- Python 3.13+: For the core implementation and type hints
- `pytest`: For running the test suite

## 📄 License

This project is open source and available for educational use.
