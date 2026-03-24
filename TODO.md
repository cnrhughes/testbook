# 📋 testbook To-Dos

## High Priority

### 🛡️ Timeout Handling for Test Execution
Add a configurable timeout mechanism to prevent infinite loops and long-running code from hanging Jupyter notebooks.

**Rationale:** Students writing infinite loops or inefficient algorithms can lock up the notebook, disrupting the learning experience.

**Implementation Notes:**
- Add timeout parameter to test configuration (per-suite or global)
- Use `signal.alarm()` (Unix) or `threading` approach for timeout
- Display clear message when timeout is exceeded
- Consider default timeout (e.g., 5-10 seconds)

**Example Usage:**
```python
test_suite = [
    {
        "function_name": "factorial",
        "cases": [...],
        "timeout": 2  # seconds
    }
]
```

---

### 📤 Test Result Export/Persistence
Allow instructors to save and export test results for grading, analytics, and record-keeping.

**Rationale:** Enables batch grading workflows, student progress tracking, and data analysis across submissions.

**Implementation Notes:**
- Add export function(s) to output JSON, CSV, or similar formats
- Include metadata (timestamp, student ID, notebook name, etc.)
- Store results with test case details and performance metrics
- Consider adding a results aggregator for multiple submissions

**Export Formats:**
- **JSON:** Structured data with full details (for programmatic analysis)
- **CSV:** Flat format for spreadsheet import (for grade entry)

---

## Medium Priority

### 🎨 Output/Print Capture Testing
Enable instructors to write tests that validate what students print to stdout, not just function return values.

**Rationale:** Many students print results instead of returning them. Having explicit print-capture tests teaches proper function design.

**Implementation Notes:**
- Capture `sys.stdout` during test execution
- Add `expected_output` field to test case schema
- Support partial matches or regex patterns for flexibility
- Display diff-like output when print test fails

**Example Usage:**
```python
print_tests = [
    {
        "code": "print('Hello, World!')",
        "expected_output": "Hello, World!",
        "hint": "Make sure your print statement matches exactly"
    }
]
```

---

### ⚙️ Test Configuration & Customization Options
Allow per-notebook or per-test configuration to customize testbook behavior.

**Rationale:** Different assignments may have different requirements (show/hide hints, custom messages, disable metrics, etc.).

**Implementation Notes:**
- Add configuration dict parameter to magic command
- Support test-level overrides (hints, messages, display options)
- Consider a notebook-wide config block
- Options could include:
  - `show_hints` (bool)
  - `show_metrics` (bool)
  - `custom_error_message` (str)
  - `timeout` (int)
  - `strict_type_checking` (bool)

**Example Usage:**
```python
%%test my_suite --config {'show_hints': False, 'timeout': 5}
# student code
```

---

### 🔧 Custom Comparison Functions
Allow instructors to define custom comparison logic for specialized data types or domain-specific equality.

**Rationale:** Some comparisons (floating-point tolerances, custom objects, approximate matches) need more flexibility than the built-in deep equality checker.

**Implementation Notes:**
- Add `comparator` field to test configuration
- Pass comparator function to compare module
- Support lambda functions or named functions
- Provide common comparators (tolerance-based, fuzzy string matching, etc.)
- Validate comparator signature

**Example Usage:**
```python
import math

def approx_equal(expected, actual):
    return math.isclose(expected, actual, rel_tol=1e-5)

tests = [
    {
        "function_name": "sqrt",
        "cases": [{"input": [4], "expected": 2.0}],
        "comparator": approx_equal
    }
]
```

---

## Low Priority / Nice-to-Have

### 🎯 Multi-Test Execution & Aggregation
Run multiple test suites sequentially with a unified summary view.

**Rationale:** Complex assignments may benefit from organizing tests into suites (basic, intermediate, advanced) and running them all at once.

**Implementation Notes:**
- Extend magic command to accept multiple suite names
- Aggregate results into summary table
- Show pass rate across all suites
- Highlight which suites passed/failed

---

### 📊 Performance Analytics & Visualization
Track performance metrics over time and provide visualization for instructors.

**Rationale:** Helps identify bottleneck assignments, track student improvement, and spot performance regressions.

**Implementation Notes:**
- Store historical performance data (with student/timestamp)
- Generate performance reports/charts
- Identify slowest test cases
- Alert on unexpected performance degradation

---

### 🔍 Enhanced Debugging & Verbose Mode
Add optional verbose logging for troubleshooting test failures.

**Rationale:** When tests fail in unexpected ways, detailed logs help both students and instructors understand what went wrong.

**Implementation Notes:**
- Add `--verbose` flag to magic command
- Log execution steps, variable states, comparison details
- Optional debug output for comparison logic
- Capture and display full tracebacks for complex failures

---

### 🏷️ Test Filtering & Selective Execution
Run only specific tests from a suite by name or tag.

**Rationale:** Useful for iterative development or focusing on specific test categories.

**Implementation Notes:**
- Add naming/tagging system for test cases
- Filter syntax: `%%test suite_name --filter "basic"`
- Support multiple filters (AND/OR logic)

**Example Usage:**
```python
tests = [
    {"name": "basic_1", "expected_state": {...}},
    {"name": "basic_2", "expected_state": {...}},
    {"name": "advanced_1", "expected_state": {...}},
]

# Run only basic tests
%%test tests --filter "basic"
```

---

### 🔐 Async/Await Support
Enable testing of async functions for students learning concurrent programming.

**Rationale:** Modern Python education includes async patterns; testbook should support them.

**Implementation Notes:**
- Detect if student function is async
- Use `asyncio.run()` to execute async code
- Handle async context managers
- Support both sync and async test cases


---

## Notes

- **Prioritization:** High-priority items (timeouts, export) directly improve usability and instructor workflows
- **Scope:** Medium-priority items add power and flexibility without major architectural changes
- **Testing:** Each feature should include comprehensive tests in `tests/`
- **Documentation:** Update README and docstrings for each new feature
- **Backward Compatibility:** All changes should maintain compatibility with existing test suites
