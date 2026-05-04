"""
Custom model configurations for AWS Bedrock models.

This module contains model configurations that extend the upstream bedrock-chat
to support additional models available in AWS Bedrock before they are added
to the upstream repository.

NOTE: This is a custom extension maintained separately from upstream bedrock-chat.

To add a new model:
1. Add the model ID to CUSTOM_MODEL_IDS
2. Add global inference profile to CUSTOM_GLOBAL_INFERENCE_PROFILES (if supported)
3. Add regional inference profile to CUSTOM_REGIONAL_INFERENCE_PROFILES (if supported)
4. Add pricing to CUSTOM_PRICING
5. Update backend/app/routes/schemas/conversation.py - add to type_model_name
6. Update backend/app/bedrock.py - add to feature support functions if needed
7. Update frontend/src/constants/index.ts - add to AVAILABLE_MODEL_KEYS
8. Update frontend/src/hooks/useModel.ts - add model details
9. Update frontend/src/i18n/en/index.ts - add translations

Claude 4.6 was added here ahead of upstream support; upstream v3.16.0 now
provides 4.6 natively, so the entries were removed to avoid shallow-merge
overwrites of upstream's broader region/pricing data.
"""

# Model name to AWS Bedrock model ID mapping
CUSTOM_MODEL_IDS: dict[str, str] = {}

# Global inference profiles for cross-region inference
# Reference: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html
CUSTOM_GLOBAL_INFERENCE_PROFILES: dict[str, dict] = {}

# Regional inference profiles
# Reference: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html
CUSTOM_REGIONAL_INFERENCE_PROFILES: dict[str, dict] = {}

# Pricing configuration (per 1K tokens)
# Reference: https://aws.amazon.com/bedrock/pricing/
CUSTOM_PRICING: dict[str, dict] = {}


def get_custom_model_ids():
    """Return custom model IDs to merge with BASE_MODEL_IDS."""
    return CUSTOM_MODEL_IDS.copy()


def get_custom_global_inference_profiles():
    """Return custom global inference profiles."""
    return CUSTOM_GLOBAL_INFERENCE_PROFILES.copy()


def get_custom_regional_inference_profiles():
    """Return custom regional inference profiles."""
    return CUSTOM_REGIONAL_INFERENCE_PROFILES.copy()


def get_custom_pricing():
    """Return custom pricing configuration."""
    return CUSTOM_PRICING.copy()
