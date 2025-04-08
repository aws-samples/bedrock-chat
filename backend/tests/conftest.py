import warnings
import pytest
import sys
import os

# Filter deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="schemathesis.generation.coverage")

# Make sure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import modules to ensure coverage tracking
def pytest_configure(config):
    """
    Import modules to ensure they are tracked for coverage.
    
    This function runs before testing begins.
    """
    try:
        from app.repositories import usage_analysis
    except ImportError:
        pass

    try:
        from app.routes import analytics, metadata
    except ImportError:
        pass

    try:
        from app.repositories import metadata_repository
    except ImportError:
        pass

    # Import the tracking helpers
    try:
        from tests.coverage_helpers import track_imports, get_imported_modules
    except ImportError:
        pass