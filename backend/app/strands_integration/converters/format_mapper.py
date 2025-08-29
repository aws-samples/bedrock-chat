"""
Format mapping utilities for Strands integration.
"""

import logging

from strands.types.media import DocumentFormat, ImageFormat

logger = logging.getLogger(__name__)


def map_to_image_format(media_type: str) -> ImageFormat:
    """Map media type to Strands ImageFormat."""
    # Extract format from media type (e.g., "image/png" -> "png")
    format_str = media_type.split("/")[-1].lower()

    # Map to valid ImageFormat values
    if format_str in ["png", "jpeg", "jpg", "gif", "webp"]:
        if format_str == "jpg":
            return "jpeg"
        return format_str  # type: ignore
    else:
        # Default to png for unsupported formats
        logger.warning(f"Unsupported image format: {format_str}, defaulting to png")
        return "png"


def map_to_document_format(file_name: str) -> DocumentFormat:
    """Map file extension to Strands DocumentFormat."""
    # Extract extension from filename
    if "." not in file_name:
        return "txt"

    ext = file_name.split(".")[-1].lower()

    # Map to valid DocumentFormat values
    valid_formats = ["pdf", "csv", "doc", "docx", "xls", "xlsx", "html", "txt", "md"]
    if ext in valid_formats:
        return ext  # type: ignore
    else:
        # Default to txt for unsupported formats
        logger.warning(f"Unsupported document format: {ext}, defaulting to txt")
        return "txt"
