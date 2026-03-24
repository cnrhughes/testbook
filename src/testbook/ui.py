# src/testbook/ui.py
from typing import Any
from IPython.display import display, HTML


def display_test_results(results: list[dict[str, Any]], duration_ms: float, memory_mib: float) -> None:
    """Display test results as an interactive HTML table with performance metrics.

    Builds and renders a formatted HTML table showing the results of each test case,
    including pass/fail status, detailed feedback messages, and clickable hints.
    Also displays execution time and peak memory usage at the bottom.

    Args:
        results: List of test result dictionaries, each containing:
            - var_name (str): The variable or function name being tested.
            - passed (bool): Whether the test passed.
            - message (str): Feedback message explaining the result.
            - hint (str, optional): Hint text to display on failure.
        duration_ms: Total execution time in milliseconds.
        memory_mib: Peak memory usage in Mebibytes (MiB).

    Returns:
        None. Displays output directly in the Jupyter notebook.
    """

    # 1. Define clean, unintimidating CSS
    html = [
        "<style>",
        # Removed max-width and added overflow-x so it can stretch safely
        "  .testbook-container { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin-top: 15px; width: 100%; overflow-x: auto; }",
        "  .testbook-table { width: 100%; border-collapse: collapse; text-align: left; }",
        "  .testbook-table th { padding: 10px; border-bottom: 2px solid #ccc; background-color: #f8f9fa; }",
        "  .testbook-table td { padding: 10px; border-bottom: 1px solid #eee; vertical-align: top; }",
        # Added white-space: nowrap to prevent the long arrays from breaking onto new lines
        "  .testbook-table code { font-family: monospace; background-color: #f1f3f5; padding: 2px 4px; border-radius: 3px; white-space: nowrap; }",
        "  .pass { color: #28a745; font-weight: bold; }",
        "  .fail { color: #dc3545; font-weight: bold; }",
        "  .feedback { color: #333; }",
        "  .hint-box { margin-top: 8px; font-size: 0.9em; background: #f8f9fa; padding: 8px; border-left: 4px solid #0d6efd; border-radius: 0 4px 4px 0; }",
        "  summary { font-weight: bold; color: #0d6efd; cursor: pointer; outline: none; }",
        "  .metrics-footer { margin-top: 10px; font-size: 0.85em; color: #6c757d; display: flex; gap: 15px; }",
        "  .metric-badge { background-color: #e9ecef; padding: 4px 8px; border-radius: 12px; }",
        "</style>",
        "<div class='testbook-container'>",
        "  <table class='testbook-table'>",
        "    <tr><th>Variable</th><th>Status</th><th>Feedback</th></tr>",
    ]

    # 2. Build a row for every test result
    for res in results:
        var_name = res.get("var_name", "Unknown")
        passed = res.get("passed", False)
        message = res.get("message", "")
        hint = res.get("hint", None)

        if passed:
            status_html = "<span class='pass'>PASS</span>"
            feedback_html = f"<span class='feedback'>✅ {message}</span>"
        else:
            status_html = "<span class='fail'>FAIL</span>"
            feedback_html = f"<span class='feedback'>❌ {message}</span>"

            # Inject the interactive hint ONLY if it failed and a hint exists
            if hint:
                feedback_html += f"<details class='hint-box'><summary>💡 Show Hint</summary><div style='margin-top: 5px;'>{hint}</div></details>"

        html.append(
            f"    <tr><td><code>{var_name}</code></td><td>{status_html}</td><td>{feedback_html}</td></tr>"
        )

    html.append("  </table>")

    # 3. Add the performance metrics footer
    time_str = f"{duration_ms:.2f} ms"
    mem_str = f"{memory_mib:.2f} MiB"
    html.append("  <div class='metrics-footer'>")
    html.append(f"    <span class='metric-badge'>⏱️ {time_str}</span>")
    html.append(f"    <span class='metric-badge'>💾 {mem_str}</span>")
    html.append("  </div>")
    html.append("</div>")

    # 4. Render the final HTML
    display(HTML("".join(html)))


def display_nudge(error_name: str, nudge_text: str) -> None:
    """Display a friendly error explanation box for runtime errors.

    Shows a styled alert box with a plain-English explanation of a common Python error.
    Designed to be displayed immediately after the Jupyter traceback to provide
    helpful context without overwhelming students with technical jargon.

    Args:
        error_name: The name of the exception (e.g., "ZeroDivisionError").
        nudge_text: A plain-English explanation of what the error means and
            how to fix it.

    Returns:
        None. Displays output directly in the Jupyter notebook.
    """

    html = [
        "<div style='margin-top: 10px; max-width: 800px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;'>",
        "  <div style='background-color: #e7f1ff; border-left: 5px solid #0d6efd; padding: 12px 15px; border-radius: 4px; color: #084298;'>",
        f"    <strong style='font-size: 1.1em;'>💡 Heads up! ({error_name})</strong>",
        f"    <p style='margin: 8px 0 0 0; line-height: 1.4;'>{nudge_text}</p>",
        "  </div>",
        "</div>",
    ]

    display(HTML("".join(html)))
