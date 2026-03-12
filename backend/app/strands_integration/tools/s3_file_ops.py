"""
S3-backed file operation tools for agent workspace.

All paths are sandboxed under the `agent-workspace/` prefix in DOCUMENT_BUCKET,
keeping them isolated from bot knowledge-base files.
"""

import logging
import os
import posixpath

import boto3
from botocore.exceptions import ClientError
from app.repositories.models.custom_bot import BotModel
from strands import tool
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DOCUMENT_BUCKET = os.environ.get("DOCUMENT_BUCKET", "")
REGION = os.environ.get("REGION", "us-east-1")
WORKSPACE_PREFIX = "agent-workspace"


def _s3_client():
    return boto3.client("s3", region_name=REGION)


def _safe_key(path: str) -> str:
    """Normalise a user-supplied path into a sandboxed S3 key.

    Any path traversal attempts (e.g. `../../secrets`) are collapsed so that
    the result always starts with `agent-workspace/`.
    """
    # Strip leading slashes so posixpath.normpath behaves predictably
    clean = posixpath.normpath(path.lstrip("/"))
    # Remove any leading ../ segments that escaped the workspace
    parts = clean.split("/")
    safe_parts = [p for p in parts if p not in (".", "..")]
    return f"{WORKSPACE_PREFIX}/{'/'.join(safe_parts)}"


def create_s3_file_ops_tools(bot: BotModel | None = None) -> list[StrandsAgentTool]:
    """Return all S3 file-operation tools."""
    return [
        create_write_file_tool(bot),
        create_read_file_tool(bot),
        create_list_files_tool(bot),
        create_move_file_tool(bot),
        create_delete_file_tool(bot),
    ]


def create_write_file_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def write_file(path: str, content: str) -> str:
        """
        Write text content to a file in the agent workspace on S3.

        Creates the file (and any implied directory structure) if it does not exist,
        or overwrites it if it does. Paths are relative to the agent workspace root.

        Args:
            path: Relative file path within the workspace, e.g. "reports/summary.txt"
            content: Text content to write to the file.

        Returns:
            str: Confirmation message with the S3 key the file was written to.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        key = _safe_key(path)
        logger.info(f"[WRITE_FILE] Writing to s3://{DOCUMENT_BUCKET}/{key}")

        try:
            _s3_client().put_object(
                Bucket=DOCUMENT_BUCKET,
                Key=key,
                Body=content.encode("utf-8"),
                ContentType="text/plain; charset=utf-8",
            )
            return f"Successfully wrote {len(content)} characters to '{key}'."
        except Exception as e:
            logger.error(f"[WRITE_FILE] Error: {e}")
            return f"Error writing file: {e}"

    return write_file


def create_read_file_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def read_file(path: str) -> str:
        """
        Read the text content of a file from the agent workspace on S3.

        Args:
            path: Relative file path within the workspace, e.g. "reports/summary.txt"

        Returns:
            str: The text content of the file, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        key = _safe_key(path)
        logger.info(f"[READ_FILE] Reading s3://{DOCUMENT_BUCKET}/{key}")

        try:
            response = _s3_client().get_object(Bucket=DOCUMENT_BUCKET, Key=key)
            content = response["Body"].read().decode("utf-8")
            logger.info(f"[READ_FILE] Read {len(content)} characters from '{key}'")
            return content
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return f"Error: File '{path}' does not exist in the workspace."
            raise
        except Exception as e:
            logger.error(f"[READ_FILE] Error: {e}")
            return f"Error reading file: {e}"

    return read_file


def create_list_files_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def list_files(path: str = "") -> str:
        """
        List files and folders inside a directory within the agent workspace on S3.

        Args:
            path: Relative directory path to list, e.g. "reports/" or "" for the workspace root.

        Returns:
            str: Newline-separated list of keys relative to the workspace root, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        prefix = _safe_key(path) + "/"
        logger.info(f"[LIST_FILES] Listing s3://{DOCUMENT_BUCKET}/{prefix}")

        try:
            s3 = _s3_client()
            paginator = s3.get_paginator("list_objects_v2")
            keys: list[str] = []
            for page in paginator.paginate(Bucket=DOCUMENT_BUCKET, Prefix=prefix):
                for obj in page.get("Contents", []):
                    # Return paths relative to the workspace prefix
                    relative = obj["Key"][len(WORKSPACE_PREFIX) + 1 :]
                    keys.append(relative)

            if not keys:
                return f"No files found under '{path or '/'}'."
            return "\n".join(keys)
        except Exception as e:
            logger.error(f"[LIST_FILES] Error: {e}")
            return f"Error listing files: {e}"

    return list_files


def create_move_file_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def move_file(source: str, destination: str) -> str:
        """
        Move (rename) a file within the agent workspace on S3.

        Args:
            source: Relative path of the file to move, e.g. "drafts/report.txt"
            destination: Relative destination path, e.g. "reports/final.txt"

        Returns:
            str: Confirmation message, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        src_key = _safe_key(source)
        dst_key = _safe_key(destination)
        logger.info(
            f"[MOVE_FILE] Moving s3://{DOCUMENT_BUCKET}/{src_key} -> {dst_key}"
        )

        try:
            s3 = _s3_client()
            s3.copy_object(
                Bucket=DOCUMENT_BUCKET,
                CopySource={"Bucket": DOCUMENT_BUCKET, "Key": src_key},
                Key=dst_key,
            )
            s3.delete_object(Bucket=DOCUMENT_BUCKET, Key=src_key)
            return f"Successfully moved '{source}' to '{destination}'."
        except Exception as e:
            logger.error(f"[MOVE_FILE] Error: {e}")
            return f"Error moving file: {e}"

    return move_file


def create_delete_file_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def delete_file(path: str) -> str:
        """
        Delete a file from the agent workspace on S3.

        Args:
            path: Relative file path within the workspace, e.g. "drafts/old_report.txt"

        Returns:
            str: Confirmation message, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        key = _safe_key(path)
        logger.info(f"[DELETE_FILE] Deleting s3://{DOCUMENT_BUCKET}/{key}")

        try:
            _s3_client().delete_object(Bucket=DOCUMENT_BUCKET, Key=key)
            return f"Successfully deleted '{path}' from the workspace."
        except Exception as e:
            logger.error(f"[DELETE_FILE] Error: {e}")
            return f"Error deleting file: {e}"

    return delete_file
