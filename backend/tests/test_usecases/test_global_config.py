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


class TestGetDefaultModel(unittest.TestCase):
    """Test cases for get_default_model function."""

    @patch.object(global_config, "DEFAULT_MODEL", "claude-v3.5-sonnet")
    def test_returns_configured_model(self):
        """Test that configured DEFAULT_MODEL is returned."""
        from app.usecases.global_config import get_default_model

        result = get_default_model()
        self.assertEqual(result, "claude-v3.5-sonnet")

    @patch.object(global_config, "DEFAULT_MODEL", None)
    def test_falls_back_to_default_when_none(self):
        """Test that default model is returned when DEFAULT_MODEL is None."""
        from app.usecases.global_config import get_default_model

        result = get_default_model()
        self.assertEqual(result, "claude-v3.7-sonnet")

    @patch.object(global_config, "DEFAULT_MODEL", "")
    def test_falls_back_to_default_when_empty_string(self):
        """Test that default model is returned when DEFAULT_MODEL is empty string."""
        from app.usecases.global_config import get_default_model

        result = get_default_model()
        self.assertEqual(result, "claude-v3.7-sonnet")

    @patch.object(global_config, "DEFAULT_MODEL", "   ")
    def test_falls_back_to_default_when_whitespace(self):
        """Test that default model is returned when DEFAULT_MODEL contains only whitespace."""
        from app.usecases.global_config import get_default_model

        result = get_default_model()
        self.assertEqual(result, "claude-v3.7-sonnet")

    @patch.object(global_config, "DEFAULT_MODEL", "  amazon-nova-pro  ")
    def test_strips_whitespace_from_configured_model(self):
        """Test that whitespace is stripped from configured model."""
        from app.usecases.global_config import get_default_model

        result = get_default_model()
        self.assertEqual(result, "amazon-nova-pro")


class TestGetTitleModel(unittest.TestCase):
    """Test cases for get_title_model function."""

    @patch.object(global_config, "TITLE_MODEL", "claude-v3-haiku")
    @patch.object(global_config, "DEFAULT_MODEL", "claude-v3.7-sonnet")
    def test_returns_title_model_when_set(self):
        """Test that TITLE_MODEL is returned when configured."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "claude-v3-haiku")

    @patch.object(global_config, "TITLE_MODEL", None)
    @patch.object(global_config, "DEFAULT_MODEL", "claude-v3.5-sonnet")
    def test_falls_back_to_default_model_when_title_model_none(self):
        """Test that DEFAULT_MODEL is returned when TITLE_MODEL is None."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "claude-v3.5-sonnet")

    @patch.object(global_config, "TITLE_MODEL", "")
    @patch.object(global_config, "DEFAULT_MODEL", "amazon-nova-lite")
    def test_falls_back_to_default_model_when_title_model_empty(self):
        """Test that DEFAULT_MODEL is returned when TITLE_MODEL is empty string."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "amazon-nova-lite")

    @patch.object(global_config, "TITLE_MODEL", None)
    @patch.object(global_config, "DEFAULT_MODEL", None)
    def test_falls_back_to_haiku_when_both_none(self):
        """Test that claude-v3-haiku is returned when both TITLE_MODEL and DEFAULT_MODEL are None."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "claude-v3-haiku")

    @patch.object(global_config, "TITLE_MODEL", "")
    @patch.object(global_config, "DEFAULT_MODEL", "")
    def test_falls_back_to_haiku_when_both_empty(self):
        """Test that claude-v3-haiku is returned when both TITLE_MODEL and DEFAULT_MODEL are empty."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "claude-v3-haiku")

    @patch.object(global_config, "TITLE_MODEL", "   ")
    @patch.object(global_config, "DEFAULT_MODEL", "   ")
    def test_falls_back_to_haiku_when_both_whitespace(self):
        """Test that claude-v3-haiku is returned when both contain only whitespace."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "claude-v3-haiku")

    @patch.object(global_config, "TITLE_MODEL", "  mistral-7b-instruct  ")
    @patch.object(global_config, "DEFAULT_MODEL", "claude-v3.7-sonnet")
    def test_strips_whitespace_from_title_model(self):
        """Test that whitespace is stripped from TITLE_MODEL."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "mistral-7b-instruct")

    @patch.object(global_config, "TITLE_MODEL", "")
    @patch.object(global_config, "DEFAULT_MODEL", "  llama3-3-70b-instruct  ")
    def test_strips_whitespace_from_default_model_fallback(self):
        """Test that whitespace is stripped from DEFAULT_MODEL when used as fallback."""
        from app.usecases.global_config import get_title_model

        result = get_title_model()
        self.assertEqual(result, "llama3-3-70b-instruct")
