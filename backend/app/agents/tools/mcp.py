import json
import logging
import typing
import uuid
from typing import Any, Generator, Iterator

import botocore.awsrequest
import botocore.crt
import botocore.session
import requests
from pydantic import BaseModel, ConfigDict

from app.agents.tools.agent_tool import AgentTool, AgentToolBundle, ToolFunctionResult
from app.repositories.models.conversation import (
    ImageToolResultModel,
    JsonToolResultModel,
    TextToolResultModel,
    type_model_name,
)
from app.repositories.models.custom_bot import BotModel

_logger = logging.getLogger(__name__)


class SigV4AsymAuth(BaseModel):
    service: str
    region: str


class MCPToolBundle(AgentToolBundle):
    """MCPToolBundle is a agent tool bundle, which acts as MCP (Model Context Protocol) client for specified MCP server.
    Only supports MCP server with protocol version 2025-03-26 with Streamable HTTP transport.
    """

    def __init__(
        self,
        name: str,
        description: str,
        url: str,
        *,
        iam_auth: SigV4AsymAuth | None = None,
    ):
        """Initialize MCPToolBundle.
        Args:
            name (str): Name of the tool bundle.
            description (str): Description of the tool bundle.
            url (str): HTTP URL of the MCP server.
            aws_sigv4a_service (str | None): If specified as AWS SigV4a service name, HTTP request is signed.
        """
        super().__init__(name=name, description=description)
        self.url = url
        self.iam_auth = iam_auth
        self._session: requests.Session | None = None

    def get_tools(self) -> list[AgentTool]:
        # MEMO: let GC collect this session
        self._session = requests.Session()

        # initialize session
        # requires protocol version 2025-03-26 support (Streamable HTTP)
        _, session_id = _jsonrpc(
            self._session,
            self.url,
            None,
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "bedrock-claude-chat",
                    "version": "2.9.0",
                },
            },
            iam_auth=self.iam_auth,
        )
        _logger.debug("MCP session initialized: name=%s url=%s", self.name, self.url)

        # prompts and resources are not supported yet
        # list tools
        tools = []
        cursor = None
        while True:
            result, _ = _jsonrpc(
                self._session,
                self.url,
                session_id,
                "tools/list",
                {"cursor": cursor} if cursor else {},
                iam_auth=self.iam_auth,
            )
            tools.extend(result["tools"])
            if not (cursor := result.get("next_cursor")):
                break
        _logger.debug("MCP tools listed: tools=[%s]", ",".join([tool["name"] for tool in tools]))

        return [MCPTool(tool, self._session, self.url, session_id, iam_auth=self.iam_auth) for tool in tools]


class AnyInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class MCPTool(AgentTool):
    """MCPTool is a agent tool, which represents MCP server's single tool."""
    def __init__(
        self,
        tool: dict[str, Any],
        session: requests.Session,
        url: str,
        session_id: str | None,
        *,
        iam_auth: SigV4AsymAuth | None = None,
    ):
        super().__init__(
            name=tool["name"],
            description=tool.get("description", tool["name"]),
            args_schema=AnyInput,  # use JsonSchema directly
            function=self._call_tool,
        )
        self.tool = tool
        self._session = session
        self.url = url
        self.session_id = session_id
        self.iam_auth = iam_auth

    def _generate_input_schema(self) -> dict[str, Any]:
        return self.tool["inputSchema"]

    def _call_tool(
        self,
        tool_input: AnyInput,
        bot: BotModel | None,
        model: type_model_name | None,
    ) -> list[ToolFunctionResult]:
        r, _ = _jsonrpc(
            self._session,
            self.url,
            self.session_id,
            "tools/call",
            {
                "name": self.tool["name"],
                "arguments": tool_input.model_dump(),
            },
            iam_auth=self.iam_auth,
        )
        results: list[ToolFunctionResult] = []
        for c in r["content"]:
            if c.get("type") == "text":
                results.append(
                    TextToolResultModel(text=c["text"]),
                )
            elif c.get("type") == "image":
                results.append(
                    ImageToolResultModel(
                        format=c["mimeType"].removeprefix("image/"),
                        image=c["data"],
                    )
                )
            else:
                # "audio", "resource" types are not supported
                results.append(
                    JsonToolResultModel(
                        json=c,
                    )
                )
        return results


def _jsonrpc(
    session: requests.Session,
    url: str,
    session_id: str | None,
    method: str,
    params: dict,
    *,
    iam_auth: SigV4AsymAuth | None = None,
) -> tuple[Any, str | None]:
    """Do JSON-RPC 2.0 request on MCP HTTP transport."""
    # set up headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id

    # set up JSON-RPC 2.0 request
    request_id = uuid.uuid4().hex
    rpc_request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params,
    }
    body = json.dumps(rpc_request, ensure_ascii=False, separators=(",", ":"))

    if iam_auth:
        # handle AWS SigV4a signing
        request = botocore.awsrequest.AWSRequest(
            method="POST",
            url=url,
            data=body,
            headers=headers,
        )

        signer = botocore.crt.auth.CrtSigV4AsymAuth(  # type: ignore
            botocore.session.Session().get_credentials(), iam_auth.service, iam_auth.region
        )
        signer.add_auth(request)

        prepared = request.prepare()
        url = prepared.url
        headers = typing.cast(dict, prepared.headers)

    # Send HTTP request
    _logger.debug("MCP request: object=\"%s\"", str(rpc_request)[:1000])
    http_response = session.post(url, headers=headers, data=body, stream=True, timeout=10.0)

    # handle HTTP response
    with http_response:
        if not 200 <= http_response.status_code < 300:
            _logger.error("Unsuccessful HTTP response: status_code=%s", http_response.status_code)
            raise Exception(f"Unsuccessful HTTP response: status_code={http_response.status_code}")

        if http_response.headers.get("content-type", "").startswith("text/event-stream"):
            events = _parse_sse(http_response.iter_lines())
        elif http_response.headers.get("content-type", "").startswith("application/json"):
            events = [http_response.content]
        else:
            _logger.error("Invalid content type: content-type=\"%s\"", http_response.headers.get("content-type"))
            raise Exception(f"Invalid content type: content-type=\"{http_response.headers.get('content-type')}\"")

        rpc_response: dict | None = None
        for event in events:
            try:
                event = json.loads(event)
            except json.JSONDecodeError:
                _logger.error("Invalid JSON response: content=\"%s\"", str(event)[:1000], exc_info=True)
                raise Exception("Invalid JSON response")

            # handle JSON-RPC 2.0 Request/Response objects (may be batched)
            objects = event if isinstance(event, list) else [event]
            for obj in objects:
                if not isinstance(obj, dict):
                    _logger.error("Invalid JSON response: not a object: content=\"%s\"", str(obj)[:1000])
                    raise Exception("Invalid JSON-RPC response: not a object")
                if "jsonrpc" not in obj or obj["jsonrpc"] != "2.0":
                    _logger.error("Unexpected JSON-RPC version: jsonrpc=\"%s\"", obj.get("jsonrpc"))
                    raise Exception(f"Unexpected JSON-RPC version: jsonrpc=\"{obj.get("jsonrpc")}\"")
                if "id" in obj and obj["id"] == request_id:
                    _logger.debug("MCP response: object=\"%s\"", str(obj)[:1000])
                    rpc_response = obj
                else:
                    _logger.info("MCP message: object=\"%s\"", str(obj)[:1000])
            
            if rpc_response is not None:
                # early exit if we received the response
                break
        
    if rpc_response is None:
        _logger.error("No JSON-RPC response received: status_code=%s", http_response.status_code)
        raise Exception(f"No JSON-RPC response received: status_code={http_response.status_code}")

    if "error" in rpc_response:
        code = rpc_response["error"].get("code")
        message = rpc_response["error"].get("message")
        data = rpc_response["error"].get("data")
        _logger.error("JSON-RPC error: code=%s message=\"%s\" data=\"%s\"", code, message, str(data)[:1000] if data is not None else "")
        raise Exception(f"JSON-RPC error: code={code} message=\"{message}\"")

    return rpc_response["result"], http_response.headers.get("Mcp-Session-Id")


def _parse_sse(line_iterator: Iterator[bytes]) -> Generator[bytes, None, None]:
    """Parse Server-Sent Events (SSE) from line iterator."""
    lines: list[bytes] = []
    for line in line_iterator:
        if not line:
            yield b"".join(lines)
            lines = []
        elif line.startswith(b"data:"):
            lines.append(line[5:])
        # ignore event name
    if lines:
        yield b"".join(lines)
