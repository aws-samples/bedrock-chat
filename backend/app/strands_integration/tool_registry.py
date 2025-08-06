"""
Dynamic tool registry for Strands integration.
Simplified design using tool_type discriminator pattern.
"""

import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.repositories.models.custom_bot import BotModel, InternetToolModel, PlainToolModel, BedrockAgentToolModel

logger = logging.getLogger(__name__)


class StrandsToolRegistry:
    """Registry for dynamically discovering and loading Strands tools."""

    def __init__(self):
        self._tool_cache: Dict[str, Any] = {}
        self._tool_modules: Dict[str, str] = {}
        self._discover_tools()

    def _discover_tools(self):
        """Discover all available Strands tools."""
        tools_dir = Path(__file__).parent / "tools"

        if not tools_dir.exists():
            logger.warning(f"Tools directory not found: {tools_dir}")
            return

        # Scan for tool files
        for tool_file in tools_dir.glob("*_tool_strands.py"):
            tool_name = tool_file.stem.replace("_tool_strands", "")
            module_path = f"app.strands_integration.tools.{tool_file.stem}"
            self._tool_modules[tool_name] = module_path
            logger.debug(f"Discovered tool: {tool_name} -> {module_path}")

    def get_tools_for_bot(self, bot: Optional[BotModel]) -> List[Any]:
        """Get tools for a bot configuration using simplified discriminator-based approach."""
        tools = []

        if not (bot and bot.agent and bot.agent.tools):
            return tools

        # Add knowledge search tool if available
        if bot.knowledge and bot.knowledge.source_urls:
            knowledge_tool = self._load_tool("knowledge")
            if knowledge_tool:
                tools.append(knowledge_tool)
                logger.info("Added knowledge search tool")

        # Process each tool using discriminator pattern
        for tool_config in bot.agent.tools:
            tool = self._create_tool_from_config(tool_config, bot)
            if tool:
                tools.append(tool)
                logger.info(f"Added {tool_config.tool_type} tool: {tool_config.name}")
            else:
                logger.warning(f"Tool not available: {tool_config.tool_type}:{tool_config.name}")

        # Add Bedrock agent tool if configured
        if hasattr(bot, "bedrock_agent_id") and bot.bedrock_agent_id:
            bedrock_tool = self._load_tool("bedrock_agent")
            if bedrock_tool:
                tools.append(bedrock_tool)
                logger.info("Added bedrock agent tool")

        logger.info(f"Total tools configured: {len(tools)}")
        return tools

    def _create_tool_from_config(self, tool_config, bot: BotModel) -> Optional[Any]:
        """Create tool instance from configuration using discriminator pattern."""
        try:
            if isinstance(tool_config, InternetToolModel):
                return self._create_internet_tool(tool_config, bot)
            elif isinstance(tool_config, PlainToolModel):
                return self._create_plain_tool(tool_config)
            elif isinstance(tool_config, BedrockAgentToolModel):
                return self._create_bedrock_agent_tool(tool_config)
            else:
                logger.warning(f"Unknown tool type: {type(tool_config)}")
                return None
        except Exception as e:
            logger.error(f"Error creating tool from config {tool_config}: {e}")
            return None

    def _create_internet_tool(self, tool_config: InternetToolModel, bot: BotModel) -> Optional[Any]:
        """Create internet search tool with bot context."""
        try:
            module = importlib.import_module(
                "app.strands_integration.tools.internet_search_tool_strands"
            )
            if hasattr(module, "create_internet_search_tool"):
                tool_instance = module.create_internet_search_tool(bot)
                logger.debug(f"Created internet search tool instance: {tool_instance}")
                return tool_instance
        except ImportError as e:
            logger.warning(f"Internet search tool not available: {e}")
        except Exception as e:
            logger.error(f"Error creating internet search tool: {e}")
        return None

    def _create_plain_tool(self, tool_config: PlainToolModel) -> Optional[Any]:
        """Create plain tool (calculator, etc.)."""
        # Map common plain tool names
        tool_name_mapping = {
            "calculator": "calculator",
            # Add other plain tools as needed
        }
        
        tool_name = tool_name_mapping.get(tool_config.name, tool_config.name)
        return self._load_tool(tool_name)

    def _create_bedrock_agent_tool(self, tool_config: BedrockAgentToolModel) -> Optional[Any]:
        """Create Bedrock agent tool."""
        return self._load_tool("bedrock_agent")

    def _load_tool(self, tool_name: str) -> Optional[Any]:
        """Load a tool by name."""
        if tool_name in self._tool_cache:
            return self._tool_cache[tool_name]

        if tool_name not in self._tool_modules:
            logger.warning(f"Tool not found: {tool_name}")
            return None

        try:
            module_path = self._tool_modules[tool_name]
            module = importlib.import_module(module_path)

            # Try common tool export names
            tool_exports = [
                tool_name,  # e.g., "calculator"
                f"{tool_name}_tool",  # e.g., "calculator_tool"
            ]

            tool = None
            for export_name in tool_exports:
                if hasattr(module, export_name):
                    tool = getattr(module, export_name)
                    break

            if tool is None:
                logger.error(f"No tool export found in {module_path}")
                return None

            self._tool_cache[tool_name] = tool
            logger.debug(f"Loaded tool: {tool_name}")
            return tool

        except ImportError as e:
            logger.warning(f"Failed to import tool {tool_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading tool {tool_name}: {e}")
            return None

    def list_available_tools(self) -> List[str]:
        """List all available tool names."""
        return list(self._tool_modules.keys())


# Global registry instance
_registry = StrandsToolRegistry()


def get_tools_for_bot(bot: Optional[BotModel]) -> List[Any]:
    """Get tools for a bot configuration using the dynamic registry."""
    return _registry.get_tools_for_bot(bot)


def list_available_tools() -> List[str]:
    """List all available tool names."""
    return _registry.list_available_tools()
