import json
import logging
import uuid
from typing import Any, Generator, Iterator

import botocore.awsrequest
import botocore.crt
import botocore.session
import requests
from pydantic import BaseModel, ConfigDict

from app.agents.tools.agent_tool import (
    AgentTool,
    AgentToolBundle,
    BotModel,
    ToolFunctionResult,
    type_model_name,
)

_logger = logging.getLogger(__name__)


class MCPToolBundle(AgentToolBundle):
    """MCPToolBundle is a agent tool bundle, which acts as MCP (Model Context Protocol) client for specified MCP server.
    Only supports MCP server with protocol version 2025-03-26 with Streamable HTTP transport.
    """

    def __init__(
        self,
        name: str,
        description: str,
        url: str,
        aws_sigv4a_service: str | None = None,
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
        self.aws_sigv4a_service = aws_sigv4a_service
        self._session: requests.Session | None = None

    def get_tools(self) -> list[AgentTool]:
        # MEMO: let GC collect this session
        self._session = requests.Session()

        # initialize session
        # requires protocol version 2025-03-26 support (Streamable HTTP)
        _ = _jsonrpc(
            self._session,
            self.url,
            self.aws_sigv4a_service,
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "bedrock-claude-chat",
                    "version": "2.9.0",
                },
            },
        )
        _logger.debug("MCP session initialized: name=%s url=%s", self.name, self.url)

        # prompts and resources are not supported yet
        # list tools
        tools = []
        cursor = None
        while True:
            result = _jsonrpc(
                self._session,
                self.url,
                self.aws_sigv4a_service,
                "tools/list",
                {"cursor": cursor},
            )
            tools.extend(result["tools"])
            if not (cursor := result.get("next_cursor")):
                break
        _logger.debug("MCP tools listed: tools=[%s]", ",".join([tool["name"] for tool in tools]))

        return [MCPTool(tool, self._session, self.url, self.aws_sigv4a_service) for tool in tools]


class AnyInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class MCPTool(AgentTool):
    """MCPTool is a agent tool, which represents MCP server's single tool."""
    def __init__(
        self,
        tool: dict[str, Any],
        session: requests.Session,
        url: str,
        aws_sigv4a_service: str | None = None,
    ):
        super().__init__(
            name=tool["name"],
            description=tool["description"],
            args_schema=AnyInput,  # use JsonSchema directly
            function=self._call_tool,
        )
        self.tool = tool
        self._session = session
        self.url = url
        self.aws_sigv4a_service = aws_sigv4a_service

    def _generate_input_schema(self) -> dict[str, Any]:
        return self.tool["inputSchema"]

    def _call_tool(
        self,
        tool_input: AnyInput,
        bot: BotModel | None,
        model: type_model_name | None,
    ) -> ToolFunctionResult:
        r = _jsonrpc(
            self._session,
            self.url,
            self.aws_sigv4a_service,
            "tools/call",
            {
                "name": self.tool["name"],
                "arguments": tool_input.model_dump(),
            },
        )
        return {
            "content": r,
        }


def _jsonrpc(
    session: requests.Session,
    url: str,
    aws_sigv4a_service: str | None,
    method: str,
    params: dict,
) -> Any:
    """Do JSON-RPC 2.0 request on MCP HTTP transport."""
    # set up headers
    # MEMO: `session.headers` may have `Mcp-Session-Id`
    headers = dict(session.headers)
    headers.update(
        {
            "Content-Type": "application/json-rpc",
            "Accept": "application/json, text/event-stream",
        }
    )

    # set up JSON-RPC 2.0 request
    request_id = uuid.uuid4().hex
    rpc_request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params,
    }
    body = json.dumps(rpc_request, ensure_ascii=False, separators=(",", ":"))

    if aws_sigv4a_service:
        # handle AWS SigV4a signing
        headers["x-amz-content-sha256"] = "UNSIGNED-PAYLOAD"
        request = botocore.awsrequest.AWSRequest(
            method="POST",
            url=url,
            data=body,
            headers=headers,
        )
        request.context["payload_signing_enabled"] = False

        signer = botocore.crt.auth.CrtSigV4AsymAuth(  # type: ignore
            botocore.session.Session().get_credentials(), aws_sigv4a_service, "*"
        )
        signer.add_auth(request)

        prepared = request.prepare()
        url = prepared.url
        headers = (
            prepared.headers
        )  # wrong type, should be botocore.awsrequest.HeadersDict

    # Send HTTP request
    _logger.debug("MCP request: object=\"%s\"", str(rpc_request)[:1000])
    http_response = session.post(url, headers=headers, data=body, stream=True, timeout=10.0)  # type: ignore

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

    if "Mcp-Session-Id" in http_response.headers:
        session.headers["Mcp-Session-Id"] = http_response.headers["Mcp-Session-Id"]

    return rpc_response["result"]


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
