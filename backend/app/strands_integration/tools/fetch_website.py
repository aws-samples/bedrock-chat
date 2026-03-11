"""
Website fetching tool — retrieves the text/markdown content of any URL.

Unlike the existing Firecrawl integration (which requires an API key and
is primarily a search tool), this is a lightweight direct HTTP fetcher
that the agent can use to read arbitrary URLs.
"""

import logging
import re

import requests
from app.repositories.models.custom_bot import BotModel
from strands import tool
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Maximum characters returned to the model to avoid flooding the context window
MAX_CONTENT_CHARS = 8000
REQUEST_TIMEOUT_SECONDS = 15


def _strip_html_tags(html: str) -> str:
    """Very lightweight HTML → plain-text conversion using regex."""
    # Remove script and style blocks entirely
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Replace common block elements with newlines
    html = re.sub(r"<(br|p|div|h[1-6]|li|tr|blockquote)[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Remove remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    # Collapse excessive whitespace
    html = re.sub(r"\n{3,}", "\n\n", html)
    html = re.sub(r"[ \t]+", " ", html)
    return html.strip()


def create_fetch_website_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def fetch_website(url: str, method: str = "GET", body: str = "") -> str:
        """
        Fetch the content of a web page or HTTP endpoint.

        Useful for reading documentation, articles, or API responses that the
        agent needs in order to answer a question or complete a task.

        Args:
            url: The full URL to fetch (must start with http:// or https://).
            method: HTTP method to use — GET (default), POST, PUT, DELETE, HEAD, OPTIONS, PATCH.
            body: Optional request body for POST/PUT/PATCH requests (send as plain text or JSON string).

        Returns:
            str: The text content of the response (up to 8,000 characters), or an error message.
        """
        allowed_methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}
        method = method.upper()
        if method not in allowed_methods:
            return f"Error: Unsupported HTTP method '{method}'. Must be one of: {', '.join(sorted(allowed_methods))}."

        if not url.startswith(("http://", "https://")):
            return "Error: URL must start with http:// or https://."

        logger.info(f"[FETCH_WEBSITE] {method} {url}")

        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (compatible; BedrockChatAgent/1.0; "
                    "+https://github.com/aws-samples/bedrock-claude-chat)"
                ),
                "Accept": "text/html,application/xhtml+xml,application/json,text/plain,*/*",
                "Accept-Language": "en-US,en;q=0.9",
            }

            request_kwargs: dict = {
                "url": url,
                "headers": headers,
                "timeout": REQUEST_TIMEOUT_SECONDS,
                "allow_redirects": True,
            }
            if body and method in ("POST", "PUT", "PATCH"):
                request_kwargs["data"] = body.encode("utf-8")

            response = requests.request(method, **request_kwargs)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if "json" in content_type:
                text = response.text
            elif "html" in content_type or "xml" in content_type:
                text = _strip_html_tags(response.text)
            else:
                text = response.text

            # Truncate if necessary
            if len(text) > MAX_CONTENT_CHARS:
                text = text[:MAX_CONTENT_CHARS] + f"\n\n[Content truncated — {len(text)} characters total]"

            logger.info(
                f"[FETCH_WEBSITE] Retrieved {len(text)} characters from {url} "
                f"(HTTP {response.status_code})"
            )
            return text

        except requests.exceptions.Timeout:
            return f"Error: Request to {url} timed out after {REQUEST_TIMEOUT_SECONDS} seconds."
        except requests.exceptions.ConnectionError as e:
            return f"Error: Could not connect to {url} — {e}"
        except requests.exceptions.HTTPError as e:
            return f"Error: HTTP {e.response.status_code} from {url} — {e}"
        except Exception as e:
            logger.error(f"[FETCH_WEBSITE] Unexpected error: {e}")
            return f"Error fetching {url}: {e}"

    return fetch_website
