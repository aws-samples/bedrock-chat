"""
Content conversion utilities for Strands integration.
"""

import re
import urllib.parse
from pathlib import Path

from app.repositories.models.conversation import AttachmentContentModel
from strands.types.content import ContentBlock


def convert_attachment_to_content_block(
    content: AttachmentContentModel,
) -> ContentBlock:
    """Convert AttachmentContentModel to Strands ContentBlock format."""
    # Use decoded filename for format detection
    try:
        decoded_name = urllib.parse.unquote(content.file_name)
    except:
        decoded_name = content.file_name

    # Extract format and name like legacy implementation
    format = Path(decoded_name).suffix[1:]  # Remove the dot
    name = Path(decoded_name).stem

    # Convert to valid file name (matching legacy)
    def _convert_to_valid_file_name(file_name: str) -> str:
        file_name = re.sub(r"[^a-zA-Z0-9\s\-\(\)\[\]]", "", file_name)
        file_name = re.sub(r"\s+", " ", file_name)
        return file_name.strip()

    valid_name = _convert_to_valid_file_name(name)

    return {
        "document": {
            "format": format,  # type: ignore
            "name": valid_name,
            "source": {"bytes": content.body},  # Use body directly (already base64)
        }
    }
