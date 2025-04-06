import asyncio
import contextlib
import json
import sys
import time
import unittest
from threading import Thread
from typing import Any, Callable, Generator

import fastapi
import uvicorn

sys.path.append(".")
from app.agents.tools.mcp import MCPToolBundle


def _app_echo(echo_impl: Callable | None) -> fastapi.FastAPI:
    app = fastapi.FastAPI()

    @app.post("/mcp")
    async def mcp(request: fastapi.Request, response: fastapi.Response) -> Any:
        body = await request.json()
        if body.get("method") == "initialize":
            response.headers["Mcp-Session-Id"] = "dummy-session-id"
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                },
            }
        elif body.get("method") == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "echo",
                            "description": "Echoes the input back",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "input": {
                                        "type": "string",
                                        "description": "Input to echo",
                                    },
                                },
                                "required": ["input"],
                            },
                        }
                    ]
                },
            }
        elif (
            body.get("method") == "tools/call"
            and body.get("params", {}).get("name") == "echo"
        ):
            input = body.get("params", {}).get("arguments", {}).get("input")
            if echo_impl:
                return await echo_impl(request, response, body.get("id"), input)
            else:
                # Default echo implementation
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": input,
                            }
                        ],
                    },
                }
        else:
            raise fastapi.HTTPException(status_code=400)

    return app


def app_echo_json() -> fastapi.FastAPI:
    return _app_echo(None)


def app_echo_sse() -> fastapi.FastAPI:
    async def echo_impl(request: fastapi.Request, response: fastapi.Response, request_id: str | int, input: str) -> Any:
        event = json.dumps({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": input,
                    }
                ],
            },
        }, ensure_ascii=False, separators=(",", ": "))
        return fastapi.Response(
            status_code=202,
            media_type="text/event-stream",
            content=f"data: {event}\n\n",
        )
    return _app_echo(echo_impl)


def app_echo_sse_with_notification() -> fastapi.FastAPI:
    async def echo_impl(request: fastapi.Request, response: fastapi.Response, request_id: str | int, input: str) -> Any:
        event = json.dumps({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": input,
                    }
                ],
            },
        }, ensure_ascii=False, separators=(",", ": "))
        notification = json.dumps({
            "jsonrpc": "2.0",
            "method": "notification",
            "params": {
                "message": "This is a notification",
            },
        }, ensure_ascii=False, separators=(",", ": "))

        async def streamer():
            yield f"data: {notification}\n\n"
            await asyncio.sleep(0.1)
            yield f"data: {event}\n\n"
            await asyncio.sleep(0.1)
            yield f"data: {notification}\n\n"
            while True:
                await asyncio.sleep(1)

        return fastapi.responses.StreamingResponse(
            status_code=202,
            media_type="text/event-stream",
            content=streamer(),
        )
    return _app_echo(echo_impl)


class TestMCPTool(unittest.TestCase):
    @contextlib.contextmanager
    def _with_server(self, entry: str) -> Generator[int, None, None]:
        config = uvicorn.Config(entry, factory=True, port=0, log_level="warning")
        server = uvicorn.Server(config)

        thread = Thread(target=server.run, daemon=True)
        thread.start()
        try:
            for _ in range(20):
                if server.started:
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError("Server failed to start")

            yield server.servers[0].sockets[0].getsockname()[1]
        finally:
            server.should_exit = True
            thread.join(timeout=1.0)

    def _test_mcp_tool(self, entry: str):
        with self._with_server(entry) as port:
            tool_bundle = MCPToolBundle(
                name="test_mcp",
                description="Test MCP Tool",
                url=f"http://localhost:{port}/mcp",
            )

            tools = tool_bundle.get_tools()
            self.assertEqual(len(tools), 1)
            self.assertEqual(tools[0].name, "echo")

            response = tools[0].run(
                tool_use_id="dummy",
                input={"input": "Hello, World!"},
                model="claude-v3.5-sonnet-v2",
            )
            self.assertIsInstance(response["related_documents"], list)
            self.assertEqual(response["status"], "success")

    def test_mcp_tool_json(self):
        self._test_mcp_tool("test_mcp:app_echo_json")

    def test_mcp_tool_sse(self):
        self._test_mcp_tool("test_mcp:app_echo_sse")

    def test_mcp_tool_sse_with_notification(self):
        self._test_mcp_tool("test_mcp:app_echo_sse_with_notification")


if __name__ == "__main__":
    unittest.main()
