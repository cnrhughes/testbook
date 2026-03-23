# src/testbook/__init__.py
from .magics import load_ipython_extension
from .compare import compare


# This ensures that if someone wants to use the compare function
# directly in a script, it is easy to find.
__all__ = ["load_ipython_extension", "compare"]
