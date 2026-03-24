"""testbook: Interactive automated testing for Jupyter notebooks.

A Jupyter notebook extension that provides interactive, automated testing and feedback
for student code exercises. It integrates seamlessly with Jupyter notebooks using
IPython magic commands to validate student solutions with clear error messages and
performance metrics.
"""

from .magics import load_ipython_extension
from .compare import compare


__all__ = ["load_ipython_extension", "compare"]
