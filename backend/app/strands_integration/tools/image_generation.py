"""
Image generation tool using Amazon Titan Image Generator via Amazon Bedrock.

Generated images are stored in S3 (DOCUMENT_BUCKET) under the `agent-images/`
prefix and returned as a presigned URL valid for 1 hour.
"""

import base64
import json
import logging
import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from app.repositories.models.custom_bot import BotModel
from strands import tool
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DOCUMENT_BUCKET = os.environ.get("DOCUMENT_BUCKET", "")
REGION = os.environ.get("REGION", "us-east-1")
BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")

# Default model — Titan Image Generator V2 is widely available and straightforward.
# Switch to "amazon.nova-canvas-v1:0" if your region supports it and you prefer it.
DEFAULT_IMAGE_MODEL = "amazon.titan-image-generator-v2:0"

# Supported sizes for Titan Image V2
VALID_SIZES = {
    (512, 512),
    (768, 768),
    (1024, 1024),
    (512, 768),
    (768, 512),
    (768, 1152),
    (1152, 768),
    (1024, 768),
    (768, 1024),
}


def _nearest_valid_size(width: int, height: int) -> tuple[int, int]:
    """Return the closest valid (width, height) pair."""
    return min(VALID_SIZES, key=lambda s: abs(s[0] - width) + abs(s[1] - height))


def create_image_generation_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def generate_image(
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
    ) -> str:
        """
        Generate an image from a text description using Amazon Bedrock image generation.

        The generated image is saved to S3 and a time-limited URL is returned.

        Args:
            prompt: Detailed description of the image to generate.
            negative_prompt: Things to avoid in the generated image (optional).
            width: Image width in pixels (default 1024). Will be snapped to the nearest supported size.
            height: Image height in pixels (default 1024). Will be snapped to the nearest supported size.

        Returns:
            str: A presigned URL where the generated image can be viewed (valid for 1 hour),
                 or an error message if generation failed.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        # Snap to nearest valid size
        width, height = _nearest_valid_size(width, height)

        logger.info(
            f"[IMAGE_GEN] Generating {width}x{height} image. Prompt: {prompt[:80]}..."
        )

        # Build the Bedrock request body for Titan Image Generator V2
        request_body: dict = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "width": width,
                "height": height,
                "cfgScale": 8.0,
            },
        }
        if negative_prompt:
            request_body["textToImageParams"]["negativeText"] = negative_prompt

        try:
            bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
            response = bedrock.invoke_model(
                modelId=DEFAULT_IMAGE_MODEL,
                body=json.dumps(request_body),
                contentType="application/json",
                accept="application/json",
            )
            body = json.loads(response["body"].read())

            images: list[str] = body.get("images", [])
            if not images:
                return "Error: Bedrock returned no images."

            image_bytes = base64.b64decode(images[0])

            # Upload to S3
            datestamp = datetime.utcnow().strftime("%Y/%m/%d")
            image_id = str(uuid.uuid4())
            s3_key = f"agent-images/{datestamp}/{image_id}.png"

            s3 = boto3.client("s3", region_name=REGION)
            s3.put_object(
                Bucket=DOCUMENT_BUCKET,
                Key=s3_key,
                Body=image_bytes,
                ContentType="image/png",
            )
            logger.info(
                f"[IMAGE_GEN] Uploaded to s3://{DOCUMENT_BUCKET}/{s3_key}"
            )

            # Generate presigned URL (1 hour)
            presigned_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": DOCUMENT_BUCKET, "Key": s3_key},
                ExpiresIn=3600,
            )

            return (
                f"Image generated successfully ({width}x{height}).\n"
                f"View/download here (link valid for 1 hour):\n{presigned_url}"
            )

        except ClientError as e:
            if e.response["Error"]["Code"] == "ValidationException":
                logger.error(f"[IMAGE_GEN] Validation error: {e}")
                return f"Error: Invalid image generation request — {e}"
            raise
        except Exception as e:
            logger.error(f"[IMAGE_GEN] Error: {e}")
            return f"Error generating image: {e}"

    return generate_image
