"""
Tests for Strands integration context management.
"""

import pytest
from unittest.mock import Mock

from app.strands_integration.context import (
    get_current_bot,
    get_current_user,
    strands_context,
)


@pytest.fixture
def mock_bot():
    """Create a mock bot for testing."""
    bot = Mock()
    bot.id = "test-bot-123"
    return bot


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    user = Mock()
    user.id = "test-user-456"
    return user


def test_basic_context_management(mock_bot, mock_user):
    """Test basic context management with context manager."""
    # Initially no context
    assert get_current_bot() is None
    assert get_current_user() is None
    
    # Use context manager
    with strands_context(mock_bot, mock_user):
        # Context should be set inside the manager
        assert get_current_bot() == mock_bot
        assert get_current_user() == mock_user
    
    # Context should be automatically cleared after exiting
    assert get_current_bot() is None
    assert get_current_user() is None


def test_context_manager(mock_bot, mock_user):
    """Test automatic context management with context manager."""
    # Initially no context
    assert get_current_bot() is None
    assert get_current_user() is None
    
    # Use context manager
    with strands_context(mock_bot, mock_user):
        # Context should be set inside the manager
        assert get_current_bot() == mock_bot
        assert get_current_user() == mock_user
    
    # Context should be automatically cleared after exiting
    assert get_current_bot() is None
    assert get_current_user() is None


def test_context_manager_with_exception(mock_bot, mock_user):
    """Test that context is cleared even when exception occurs."""
    # Initially no context
    assert get_current_bot() is None
    assert get_current_user() is None
    
    # Use context manager with exception
    with pytest.raises(ValueError):
        with strands_context(mock_bot, mock_user):
            # Context should be set
            assert get_current_bot() == mock_bot
            assert get_current_user() == mock_user
            # Raise exception
            raise ValueError("Test exception")
    
    # Context should still be cleared after exception
    assert get_current_bot() is None
    assert get_current_user() is None


def test_context_with_none_bot(mock_user):
    """Test context manager with None bot."""
    with strands_context(None, mock_user):
        assert get_current_bot() is None
        assert get_current_user() == mock_user
    
    # Context should be cleared
    assert get_current_bot() is None
    assert get_current_user() is None