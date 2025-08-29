import sys

sys.path.insert(0, ".")
import unittest
from unittest.mock import patch

from app.usecases import global_config
from app.usecases.global_config import get_global_available_models


class TestGetGlobalAvailableModels(unittest.TestCase):
    """Test cases for get_global_available_models function."""

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", None)
    def test_no_environment_variable_returns_empty_list(self):
        """Test that when no GLOBAL_AVAILABLE_MODELS env var is set, empty list is returned."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", "")
    def test_empty_environment_variable_returns_empty_list(self):
        """Test that when GLOBAL_AVAILABLE_MODELS is empty string, empty list is returned."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", "[]")
    def test_empty_json_array_returns_empty_list(self):
        """Test that empty JSON array returns empty list."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(
        global_config,
        "GLOBAL_AVAILABLE_MODELS",
        '["claude-v3.7-sonnet", "claude-v3.5-sonnet", "amazon-nova-pro"]',
    )
    def test_valid_json_array_returns_models(self):
        """Test that valid JSON array returns the list of models."""
        result = get_global_available_models()
        self.assertEqual(
            result, ["claude-v3.7-sonnet", "claude-v3.5-sonnet", "amazon-nova-pro"]
        )

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", "invalid json")
    def test_invalid_json_returns_empty_list(self):
        """Test that invalid JSON returns empty list."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", '{"not": "an array"}')
    def test_json_object_instead_of_array_returns_empty_list(self):
        """Test that JSON object (not array) returns empty list."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", '"string instead of array"')
    def test_json_string_instead_of_array_returns_empty_list(self):
        """Test that JSON string (not array) returns empty list."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", "true")
    def test_json_boolean_instead_of_array_returns_empty_list(self):
        """Test that JSON boolean (not array) returns empty list."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", '[""]')
    def test_empty_string_models_filtered_out(self):
        """Test that empty string models are filtered out from the array."""
        result = get_global_available_models()
        self.assertEqual(result, [])

    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", '[null, "valid-model"]')
    def test_null_values_filtered_out(self):
        """Test that null values are filtered out from the array."""
        result = get_global_available_models()
        self.assertEqual(result, ["valid-model"])

    @patch.object(
        global_config, "GLOBAL_AVAILABLE_MODELS", '["model1", "", null, "model2", ""]'
    )
    def test_mixed_valid_and_invalid_values_filtered(self):
        """Test that empty strings and null values are filtered out, keeping only valid models."""
        result = get_global_available_models()
        self.assertEqual(result, ["model1", "model2"])

    @patch("app.usecases.global_config.logger")
    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", '["test-model"]')
    def test_logging_for_valid_models(self, mock_logger):
        """Test that appropriate log message is generated for valid models."""
        result = get_global_available_models()
        mock_logger.info.assert_called_with(
            "Global available models (JSON): ['test-model']"
        )
        self.assertEqual(result, ["test-model"])

    @patch("app.usecases.global_config.logger")
    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", None)
    def test_logging_for_no_config(self, mock_logger):
        """Test that appropriate log message is generated when no config is set."""
        result = get_global_available_models()
        mock_logger.info.assert_called_with(
            "No global available models configured - all models are available"
        )
        self.assertEqual(result, [])

    @patch("app.usecases.global_config.logger")
    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", "invalid json")
    def test_logging_for_invalid_json(self, mock_logger):
        """Test that error is logged for invalid JSON."""
        result = get_global_available_models()
        mock_logger.error.assert_called_with(
            "Failed to parse GLOBAL_AVAILABLE_MODELS as JSON"
        )
        self.assertEqual(result, [])

    @patch("app.usecases.global_config.logger")
    @patch.object(global_config, "GLOBAL_AVAILABLE_MODELS", '{"not": "array"}')
    def test_logging_for_non_array_type(self, mock_logger):
        """Test that error is logged for non-array JSON types."""
        result = get_global_available_models()
        mock_logger.error.assert_called_with(
            "GLOBAL_AVAILABLE_MODELS must be a JSON array, got <class 'dict'>"
        )
        self.assertEqual(result, [])
