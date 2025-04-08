"""Base test class with import tracking capabilities."""
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import sys
import traceback
from tests.coverage_helpers import track_imports, get_imported_modules

class ImportTrackingTestCase(unittest.TestCase):
    """
    Base test case that tracks imports.
    
    This class provides infrastructure for tracking which modules are imported
    during test setup and execution, which helps diagnose coverage issues.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up the test class and track imports."""
        super().setUpClass()
        with track_imports():
            # Import the modules needed for this test class
            cls._import_modules()
        
        # Record which modules were successfully imported
        cls.imported_modules = get_imported_modules()
        
    @classmethod
    def _import_modules(cls):
        """
        Import the modules needed for this test class.
        
        Override in subclasses to import specific modules.
        """
        pass

# Re-export the async_test decorator for use in test classes
def async_test(async_func):
    """
    Decorator for async test methods.
    
    This decorator ensures that async test methods have a properly
    configured event loop for execution.
    
    Args:
        async_func: The async test function to decorate.
        
    Returns:
        A wrapper function that executes the async test.
    """
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(async_func(*args, **kwargs))
    return wrapper

class AnalyticsMockFactory:
    """
    Factory for creating mocks for analytics tests.
    
    This factory creates and configures mocks for various components
    used in analytics tests, ensuring consistent mocking across tests.
    """
    
    @staticmethod
    def create_mocks(test_case):
        """
        Create mocks for analytics tests.
        
        Args:
            test_case: The test case instance to set up mocks for.
            
        Returns:
            A dictionary of mock objects.
        """
        mocks = {}
        
        # Create mock for get_table_client
        get_table_mock = patch("app.repositories.group._get_table_client")
        test_case.addCleanup(get_table_mock.stop)
        mocks["table_client"] = table_mock = get_table_mock.start()
        
        # Set up mock table
        mock_table = MagicMock()
        mock_table.query.return_value = {"Items": []}
        table_mock.return_value = mock_table
        
        # Create mock for usage_analysis
        usage_analysis_mock = patch("app.routes.analytics.usage_analysis")
        test_case.addCleanup(usage_analysis_mock.stop)
        mocks["usage_analysis"] = usage_mock = usage_analysis_mock.start()
        
        # Configure async mocks for repository functions
        usage_mock.get_analytics_dashboard_fast = AsyncMock()
        usage_mock.get_top_entities = AsyncMock()
        usage_mock.get_topics_analysis = AsyncMock()
        
        # Create mock for Athena client
        athena_mock = patch("app.repositories.usage_analysis.athena")
        test_case.addCleanup(athena_mock.stop)
        mocks["athena"] = athena_mock.start()
        
        # Create mock for run_athena_query
        run_query_mock = patch(
            "app.repositories.usage_analysis.run_athena_query", 
            new_callable=AsyncMock
        )
        test_case.addCleanup(run_query_mock.stop)
        mocks["run_query"] = query_mock = run_query_mock.start()
        
        # Sample query response
        sample_query_response = {
            "ResultSet": {
                "Rows": [
                    {
                        "Data": [
                            {"VarCharValue": "date"}, 
                            {"VarCharValue": "num_sessions"}, 
                            {"VarCharValue": "num_messages"}, 
                            {"VarCharValue": "input_tokens"}, 
                            {"VarCharValue": "output_tokens"}, 
                            {"VarCharValue": "cost"}
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "2023-01-01"}, 
                            {"VarCharValue": "10"}, 
                            {"VarCharValue": "100"}, 
                            {"VarCharValue": "1000"}, 
                            {"VarCharValue": "800"}, 
                            {"VarCharValue": "1.5"}
                        ]
                    }
                ]
            }
        }
        query_mock.return_value = sample_query_response
        
        return mocks

# MockUser class that matches the User interface
class MockUser:
    """
    Mock implementation of the User class.
    
    This class provides a mock implementation of the User class
    for testing purposes.
    """
    
    def __init__(self, id, name, groups=None, email=None):
        """
        Initialize a new MockUser.
        
        Args:
            id: The user ID.
            name: The user name.
            groups: Optional list of groups the user belongs to.
            email: Optional email address for the user.
        """
        self.id = id
        self.name = name
        self.groups = groups or []
        self.email = email
        
    def is_admin(self):
        """Check if the user is an admin."""
        return "Admin" in self.groups
        
    def is_creating_bot_allowed(self):
        """Check if the user is allowed to create bots."""
        return self.is_admin() or "CreatingBotAllowed" in self.groups
        
    def is_publish_allowed(self):
        """Check if the user is allowed to publish bots."""
        return self.is_admin() or "PublishAllowed" in self.groups
