import json
import logging
import uuid

from app.repositories.models.custom_bot import BotModel
from strands import tool
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_bedrock_agent_config(bot: BotModel | None):
    """Extract Bedrock Agent configuration from bot."""
    logger.debug(f"_get_bedrock_agent_config called with bot: {bot}")
    logger.debug(f"Bot agent: {bot.agent if bot else None}")
    logger.debug(f"Bot agent tools: {bot.agent.tools if bot and bot.agent else None}")

    if not bot or not bot.agent or not bot.agent.tools:
        logger.debug("Early return: bot, agent, or tools is None/empty")
        return None

    for tool_config in bot.agent.tools:
        logger.debug(f"Checking tool: {tool_config}")
        logger.debug(f"Tool type: {tool_config.tool_type}")
        logger.debug(
            f"Tool bedrockAgentConfig: {getattr(tool_config, 'bedrockAgentConfig', 'NOT_FOUND')}"
        )

        if tool_config.tool_type == "bedrock_agent" and tool_config.bedrockAgentConfig:
            logger.info("Found matching bedrock_agent tool config")
            return tool_config.bedrockAgentConfig

    logger.warning("No matching bedrock_agent tool config found")
    return None


def _invoke_bedrock_agent_standalone(
    agent_id: str, alias_id: str, input_text: str, session_id: str
) -> list[dict[str, str]]:
    """Standalone Bedrock Agent invocation implementation."""
    try:
        from app.utils import get_bedrock_agent_runtime_client

        runtime_client = get_bedrock_agent_runtime_client()

        logger.info(f"Invoking Bedrock Agent: agent_id={agent_id}, alias_id={alias_id}")

        response = runtime_client.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            inputText=input_text,
            sessionId=session_id,
            enableTrace=True,
        )

        # Process response
        result = []
        trace_logs = []

        for event in response["completion"]:
            # Process trace information
            if "trace" in event:
                trace_data = event["trace"]
                trace_logs.append(trace_data)

            if "chunk" in event:
                content = event["chunk"]["bytes"].decode("utf-8")
                # Create data structure for citation support
                result.append(
                    {
                        "content": content,
                        "source_name": f"Agent Final Result({agent_id})",
                        "source_link": "",
                    }
                )

        logger.debug(f"Processed {len(result)} chunks from Bedrock Agent response")
        logger.debug(f"Collected {len(trace_logs)} trace logs")

        # Add trace log information to results
        if trace_logs:
            formatted_traces = _format_trace_for_client_standalone(trace_logs)
            for formatted_trace in formatted_traces:
                trace_type = formatted_trace.get("type")
                trace_input = formatted_trace.get("input")
                recipient = (
                    trace_input.get("recipient", None)
                    if trace_input is not None
                    else None
                )

                if trace_type == "tool_use":
                    if recipient is not None and trace_input is not None:
                        result.append(
                            {
                                "content": json.dumps(
                                    trace_input.get("content"),
                                    default=str,
                                ),
                                "source_name": f"[Trace] Send Message ({agent_id}) -> ({recipient})",
                                "source_link": "",
                            }
                        )
                    elif trace_input is not None:
                        result.append(
                            {
                                "content": json.dumps(
                                    trace_input.get("content"),
                                    default=str,
                                ),
                                "source_name": f"[Trace] Tool Use ({agent_id})",
                                "source_link": "",
                            }
                        )

                elif trace_type == "text":
                    if "<thinking>" in formatted_trace.get("text", ""):
                        result.append(
                            {
                                "content": json.dumps(
                                    formatted_trace.get("text"), default=str
                                ),
                                "source_name": f"[Trace] Agent Thinking({agent_id})",
                                "source_link": "",
                            }
                        )
                    else:
                        result.append(
                            {
                                "content": json.dumps(
                                    formatted_trace.get("text"), default=str
                                ),
                                "source_name": f"[Trace] Agent ({agent_id})",
                                "source_link": "",
                            }
                        )

        return result

    except Exception as e:
        logger.error(f"Error invoking Bedrock Agent: {e}")
        raise e


def _format_trace_for_client_standalone(trace_logs: list) -> list[dict]:
    """Format trace log information for the client."""
    try:
        traces = []

        for trace in trace_logs:
            trace_data = trace.get("trace", {})

            # Skip to the next trace if required keys are missing
            if "orchestrationTrace" not in trace_data:
                continue

            orch = trace_data["orchestrationTrace"]
            if "modelInvocationOutput" not in orch:
                continue

            model_output = orch["modelInvocationOutput"]
            if "rawResponse" not in model_output:
                continue

            raw_response = model_output["rawResponse"]
            if "content" not in raw_response:
                continue

            content = raw_response["content"]
            if not isinstance(content, str):
                continue

            # Parse JSON string
            try:
                parsed_content = json.loads(content)
                content_list = parsed_content.get("content", [])
            except Exception as e:
                logger.warning(f"Issue with parsing content, it is not valid JSON {e}")
                parsed_content = content
                content_list = []

            logger.info(f"parsed_content: {parsed_content}")

            # Process content list
            for model_invocation_content in content_list:
                logger.info(f"model_invocation_content: {model_invocation_content}")
                if isinstance(model_invocation_content, dict):
                    traces.append(
                        {
                            "type": model_invocation_content.get("type"),
                            "input": model_invocation_content.get("input"),
                            "text": model_invocation_content.get("text"),
                        }
                    )
        return traces
    except Exception as e:
        logger.error(f"Error formatting trace for client: {e}")
        import traceback

        logger.error(traceback.format_exc())
        raise e


def create_bedrock_agent_tool(bot: BotModel | None) -> StrandsAgentTool:
    """Create a Bedrock Agent tool with bot context captured in closure."""

    @tool
    def bedrock_agent(query: str) -> dict:
        """
        Invoke Bedrock Agent for specialized tasks.

        Args:
            query: Query to send to the agent

        Returns:
            list: Agent response for citation support
        """
        logger.debug(f"[BEDROCK_AGENT_V3] Starting invocation: query={query}")

        try:
            # # Bot is captured on closure
            current_bot = bot

            if not current_bot:
                logger.warning("[BEDROCK_AGENT_V3] No bot context available")
                return {
                    "status": "error",
                    "content": [
                        {
                            "text": f"Bedrock Agent requires bot configuration. Query was: {query}"
                        }
                    ],
                }

            # Fetch Bedrock Agent configuration from bot settings
            agent_config = _get_bedrock_agent_config(current_bot)

            if (
                not agent_config
                or not agent_config.agent_id
                or not agent_config.alias_id
            ):
                logger.warning("[BEDROCK_AGENT_V3] Bot has no Bedrock Agent configured")
                return {
                    "status": "error",
                    "content": [
                        {
                            "text": f"Bot does not have a Bedrock Agent configured. Query was: {query}"
                        }
                    ],
                }

            # Generate a session ID
            session_id = str(uuid.uuid4())

            logger.debug(
                f"[BEDROCK_AGENT_V3] Using agent_id: {agent_config.agent_id}, alias_id: {agent_config.alias_id}"
            )
            # Invoke Bedrock Agent
            results = _invoke_bedrock_agent_standalone(
                agent_id=agent_config.agent_id,
                alias_id=agent_config.alias_id,
                input_text=query,
                session_id=session_id,
            )

            logger.debug(f"[BEDROCK_AGENT_V3] Invocation completed successfully")
            return {
                "status": "success",
                "content": [{"json": result} for result in results],
            }

        except Exception as e:
            logger.error(f"[BEDROCK_AGENT_V3] Bedrock Agent error: {e}")
            return {
                "status": "error",
                "content": [
                    {
                        "text": f"An error occurred during Bedrock Agent invocation: {str(e)}"
                    }
                ],
            }

    # Update tool description dynamically to reflect the actual agent's purpose.
    # This ensures the LLM selects the correct tool based on the agent's specific capabilities
    # rather than using a generic description that may lead to inappropriate tool selection.
    logger.debug(f"create_bedrock_agent_tool called with bot: {bot is not None}")
    if bot:
        logger.debug("Bot exists, getting agent config...")
        agent_config = _get_bedrock_agent_config(bot)
        logger.debug(f"Agent config: {agent_config}")
        if agent_config and agent_config.agent_id:
            logger.debug(f"Agent config valid, agent_id: {agent_config.agent_id}")
            try:
                from app.utils import get_bedrock_agent_client

                client = get_bedrock_agent_client()
                response = client.get_agent(agentId=agent_config.agent_id)
                description = response.get("agent", {}).get(
                    "description", "Bedrock Agent"
                )

                # Dynamically update tool description
                bedrock_agent._tool_spec["description"] = description
                logger.info(f"Updated bedrock_agent tool description to: {description}")

            except Exception as e:
                logger.error(f"Failed to update bedrock_agent tool description: {e}")

    return bedrock_agent
