import logging
import pprint
from typing import List, Dict, Any

import httpx
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
from strands.types.tools import AgentTool as StrandsAgentTool
from app.repositories.models.custom_bot import MCPAgentToolModel, MCPConfigModel, MCPServerModel


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def create_mcp_tools(bot) -> list[StrandsAgentTool]:
    """
    Create MCP tools based on the bot's configuration.
    
    Args:
        bot: The bot object containing MCP configuration
        
    Returns:
        list: All selected MCP tools from all configured MCP servers
    """
    logger.debug(f"create_mcp_tools called with bot: {bot.id}; Agent: {bot.agent}; Agent tools: {bot.agent.tools}")

    mcp_config: MCPConfigModel | None = get_mcp_config(bot)

    logger.debug(f"mcp_config: {pprint.pformat(mcp_config)}")

    # Check if mcp_config has mcp_servers attribute
    if mcp_config is None or not mcp_config.mcp_servers:
        logger.debug("No MCP servers configured")
        return []

    # Iterate through each MCP server
    selected_tools: list[StrandsAgentTool] = []
    for mcp_server in mcp_config.mcp_servers:
        available_tools=connect_to_mcp_server_and_list_tools(mcp_server)

        mcp_server.tools.available = [
            MCPAgentToolModel.from_agent_tool(tool) for tool in available_tools
        ]

        for tool in available_tools:
            for selected_tool in mcp_server.tools.selected:
                if tool.tool_name == selected_tool:
                    selected_tools.append(tool)

    return selected_tools

def get_mcp_config(bot) -> MCPConfigModel | None:
    """Extract MCP configuration from bot."""
    logger.debug(f"get_mpc_config called with bot: {bot.id}")
    
    if not bot or not bot.agent or not bot.agent.tools:
        logger.debug("Early return: bot, agent, or tools is None/empty")
        return MCPConfigModel(
            tool_type="mcp",
            name="mcp",
            description="",
            mcp_servers=[]
        )
    
    for tool_config in bot.agent.tools:
        logger.debug(f"Checking tool: {tool_config}")
        logger.debug(f"Tool type: {tool_config.tool_type}")
        logger.debug(f"Tool MCP servers: {getattr(tool_config, 'mcp_servers', 'NOT_FOUND')}")

        if tool_config.tool_type == "mcp" and isinstance(tool_config, MCPConfigModel):
                logger.info("Found matching bedrock_agent tool config")
                return tool_config
    
    logger.info("No matching bedrock_agent tool config found")
    return None

class MCPAuth(httpx.Auth):
    def __init__(self, api_key, auth_type="bearer"):
        self.api_key = api_key
        self.auth_type = auth_type.lower()

    def auth_flow(self, request):
        if self.auth_type == "bearer":
            request.headers["Authorization"] = f"Bearer {self.api_key}"
        elif self.auth_type == "api-key":
            request.headers["X-API-Key"] = self.api_key
        else:
            # Custom header
            request.headers[self.auth_type] = self.api_key
        yield request

def connect_to_mcp_server_and_list_tools(mcp_server: MCPServerModel) -> List[StrandsAgentTool]:
    """
    Connection to a remote MCP server.

    Args:
        mcp_server: The MCP server object containing the API endpoint and API key

    Returns:
        list: All available tools
    """
    try:
        logger.debug(f"Connecting to remote MCP server: {mcp_server.name} at {mcp_server.endpoint}")

        auth = None
        if mcp_server.api_key:
            auth = MCPAuth(api_key=mcp_server.api_key, auth_type="bearer")

        mcp_client = MCPClient(lambda: streamablehttp_client(url=mcp_server.endpoint, auth=auth))

        # Get available tools from the MCP server
        with mcp_client as client:
            tools = client.list_tools_sync()
            logger.debug(f"Found {len(tools)} tools from MCP server {mcp_server.name}")

            for tool in tools:
                logger.debug(vars(tool))
                log_tool(tool)

            return tools            
                
    except Exception as e:
        logger.error(f"Error connecting to MCP server {mcp_server.name} at {mcp_server.endpoint}: {e}")
        return []

def log_tool(tool):
    """Log a tool using dir() instead of vars()."""
    logger.debug(f"Tool type: {type(tool)}")
    
    # Get all attributes
    attributes = dir(tool)
    
    # Filter out private attributes and methods
    public_attrs = [attr for attr in attributes if not attr.startswith('_')]
    
    # Log each attribute and its value
    for attr in public_attrs:
        try:
            value = getattr(tool, attr)
            # Skip methods
            if callable(value):
                continue
            logger.debug(f"  {attr}: {value}")
        except Exception as e:
            logger.debug(f"  {attr}: Error accessing - {e}")
