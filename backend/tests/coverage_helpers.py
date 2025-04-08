"""Helper functions for tracking module imports during test execution.

This module provides utilities for tracking which modules are imported
during test execution, which helps diagnose coverage issues.
"""

import sys
import contextlib
from typing import List, Set, Dict, Any, Optional

# Global set to track imported modules
_imported_modules: Set[str] = set()

@contextlib.contextmanager
def track_imports():
    """Context manager that tracks module imports.

    This context manager records which modules are imported during its execution.
    It can be used to track which modules are imported during test setup and execution.
    """
    global _imported_modules
    
    # Save the original import function
    original_import = __builtins__["__import__"]
    
    # Clear the set of imported modules
    _imported_modules.clear()
    
    def tracking_import(name, *args, **kwargs):
        """Wrapper around __import__ that tracks imported modules."""
        # Record the module name
        _imported_modules.add(name)
        
        # Call the original import function
        return original_import(name, *args, **kwargs)
    
    try:
        # Replace the import function with our tracking version
        __builtins__["__import__"] = tracking_import
        yield
    finally:
        # Restore the original import function
        __builtins__["__import__"] = original_import

def get_imported_modules() -> Set[str]:
    """Get the set of modules imported during tracking.

    Returns:
        A set of module names that were imported during tracking.
    """
    return _imported_modules.copy()
