# mcp_client.py
import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, server_script: str = "mcp_server.py"):        
        self._server_script = server_script
        self._session: ClientSession | None = None
        self._exit_stack = None
        self._tools: list = []
        self._bedrock_schemas: list = []

    async def start(self):         
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        params = StdioServerParameters(
            command="python",
            args=[self._server_script],
            env=dict(os.environ),
        )

        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(params)
        )
        read, write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        await self._session.initialize()

        response = await self._session.list_tools()
        self._tools = response.tools
        self._bedrock_schemas = [_to_bedrock_schema(t) for t in self._tools]

        print(f"[mcp] Connected — {len(self._tools)} tools registered:")
        for t in self._tools:
            print(f"       • {t.name}")

    async def stop(self):
        if self._exit_stack:
            await self._exit_stack.aclose()
            self._exit_stack = None
            self._session = None

    def list_tool_schemas(self) -> list[dict]:
        print("Tools")
        return self._bedrock_schemas

    async def call_tool(self, name: str, tool_input: dict) -> str:
        if not self._session:
            raise RuntimeError("MCPClient is not started. Call await client.start() first.")
        print(f"{name} {tool_input}")
        result = await self._session.call_tool(name, tool_input)
        print(f"{name} result {result}")
        parts = []
        for block in result.content:
            if hasattr(block, "text"):
                parts.append(block.text)
            else:
                parts.append(json.dumps(block))

        return "\n".join(parts) if parts else json.dumps({"result": "ok"})


# ── Schema conversion ─────────────────────────────────────────────────────────

def _to_bedrock_schema(tool) -> dict:
    raw_schema = tool.inputSchema if tool.inputSchema else {}

    if hasattr(raw_schema, "model_dump"):
        raw_schema = raw_schema.model_dump()

    # Ensure it's a plain dict copy so we can safely mutate it
    raw_schema = dict(raw_schema)

    # Bedrock requires "properties" key if type is "object"
    if raw_schema.get("type") == "object" and "properties" not in raw_schema:
        raw_schema["properties"] = {}

    # Strip keys Bedrock doesn't accept
    for key in ("title", "$schema", "additionalProperties"):
        raw_schema.pop(key, None)
    print(f"{tool.name} {tool.description} {json.dumps(raw_schema)}")
    # Bedrock Nova Sonic requires inputSchema.json to be a JSON *string*, not a dict
    return {
        "toolSpec": {
            "name":        tool.name,
            "description": tool.description or "",
            "inputSchema": {
                "json": json.dumps(raw_schema)
            },
        }
    }