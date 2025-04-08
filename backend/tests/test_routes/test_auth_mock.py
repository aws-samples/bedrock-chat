from app.routes.metadata import router as metadata_router
import unittest
from unittest.mock import patch

class TestAuthMock(unittest.TestCase):
    def setUp(self):
        self.mock_is_authorized_patcher = patch("app.usecases.group.is_user_authorized", return_value=True)
        self.mock_is_authorized = self.mock_is_authorized_patcher.start()

    def tearDown(self):
        self.mock_is_authorized_patcher.stop()

    def test_auth_mock_works(self):
        """Test that our authorization mocking works."""
        from app.usecases.group import is_user_authorized
        self.assertTrue(is_user_authorized("test-user", "test-permission"))

if __name__ == "__main__":
    unittest.main()
