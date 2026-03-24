"""Shared test fixtures and configuration."""
import pytest
from unittest.mock import MagicMock
from traitlets.config.loader import Config
from IPython.core.interactiveshell import InteractiveShell


@pytest.fixture
def mock_ipython_shell():
    """Create a mock IPython shell for testing."""
    # Use MagicMock but set critical attributes to real types
    shell = MagicMock(spec=InteractiveShell)
    shell.user_ns = {}
    shell.run_cell = MagicMock(return_value=MagicMock(error_in_exec=None))
    shell.config = Config()
    shell.parent = None
    return shell
