"""
Dynamic tool registry for Strands integration.
Automatically discovers and registers tools without manual maintenance.
"""

import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.repositories.models.custom_bot import BotModel

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
                f"create_{tool_name}_tool",  # e.g., "create_internet_search_tool"
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

    def get_tools_for_bot(self, bot: Optional[BotModel]) -> List[Any]:
        """Get tools for a bot configuration."""
        tools = []

        if not (bot and bot.agent and bot.agent.tools):
            return tools

        # Add knowledge search tool if available
        if bot.knowledge and bot.knowledge.source_urls:
            knowledge_tool = self._load_tool("knowledge")
            if knowledge_tool:
                tools.append(knowledge_tool)
                logger.info("Added knowledge search tool")

        # Process each tool in bot configuration
        for tool_config in bot.agent.tools:
            tool_name = None

            # Determine tool name from configuration
            if hasattr(tool_config, "name") and tool_config.name:
                tool_name = tool_config.name
            elif hasattr(tool_config, "tool_type") and tool_config.tool_type:
                # Map tool_type to tool_name for backward compatibility
                tool_name = self._map_tool_type_to_name(tool_config.tool_type)

            if not tool_name:
                logger.warning(f"Could not determine tool name for: {tool_config}")
                continue

            # Handle special cases that need bot context
            if tool_name == "internet":
                tool = self._load_internet_search_tool(bot)
            else:
                tool = self._load_tool(tool_name)

            if tool:
                tools.append(tool)
                logger.info(f"Added {tool_name} tool")
            else:
                logger.warning(f"Tool not available: {tool_name}")

        # Add Bedrock agent tool if configured
        if hasattr(bot, "bedrock_agent_id") and bot.bedrock_agent_id:
            bedrock_tool = self._load_tool("bedrock_agent")
            if bedrock_tool:
                tools.append(bedrock_tool)
                logger.info("Added bedrock agent tool")

        logger.info(f"Total tools configured: {len(tools)}")
        return tools

    def _map_tool_type_to_name(self, tool_type: str) -> str:
        """Map tool_type to tool_name for backward compatibility."""
        mapping = {
            "plain": "calculator",  # Default plain tools are calculator
            "internet": "internet",
            "bedrock_agent": "bedrock_agent",
            "calculator": "calculator",
        }
        return mapping.get(tool_type, tool_type)

    def _load_internet_search_tool(self, bot: BotModel) -> Optional[Any]:
        """Load internet search tool with bot context."""
        try:
            module = importlib.import_module(
                "app.strands_integration.tools.internet_search_tool_strands"
            )
            if hasattr(module, "create_internet_search_tool"):
                return module.create_internet_search_tool(bot)
        except ImportError as e:
            logger.warning(f"Internet search tool not available: {e}")
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
