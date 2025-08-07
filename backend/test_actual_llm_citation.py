#!/usr/bin/env python3
"""
Test script to verify actual LLM citation behavior with simple_list_tool.
This test makes actual LLM calls to verify that citations work end-to-end.
"""

import json
import logging
import os
import sys
import time

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_actual_strands_agent_with_calculator():
    """Test actual Strands agent with calculator_tool and citation"""
    print("=" * 80)
    print("TEST: Actual Strands Agent with calculator_tool and Citation")
    print("=" * 80)
    
    try:
        # Import required modules
        from strands import Agent
        from strands.models import BedrockModel
        from app.strands_integration.tools.calculator_tool_strands import calculator
        from app.strands_integration.tool_registry import _add_citation_support
        from app.strands_integration.citation_prompt import get_citation_system_prompt
        from app.bedrock import get_model_id, BEDROCK_REGION
        
        # Create citation-enhanced calculator tool
        enhanced_calculator = _add_citation_support(calculator, "calculator")
        
        # Create Bedrock model using the same configuration as the project
        model_name = "claude-v3.5-sonnet"
        model_id = get_model_id(model_name)
        
        model = BedrockModel(
            model_id=model_id,
            region=BEDROCK_REGION
        )
        
        print(f"Using model: {model_id} in region: {BEDROCK_REGION}")
        
        # Create system prompt with citation instructions
        citation_prompt = get_citation_system_prompt("claude-v3.5-sonnet")
        system_prompt = f"""You are a helpful assistant. When using tools, always cite your sources properly.

{citation_prompt}"""
        
        print("System prompt:")
        print(system_prompt)
        print("\n" + "=" * 40)
        
        # Create agent with citation-enhanced tool
        agent = Agent(
            model=model,
            tools=[enhanced_calculator],
            system_prompt=system_prompt
        )
        
        # Test query that should trigger calculator tool
        test_query = "What is 15 * 23 + 7? Please show me the calculation."
        
        print(f"Test query: {test_query}")
        print("\nCalling agent...")
        
        # Call agent
        start_time = time.time()
        result = agent(test_query)
        end_time = time.time()
        
        print(f"Agent call completed in {end_time - start_time:.2f} seconds")
        print(f"Result type: {type(result)}")
        
        # Extract response message
        if hasattr(result, 'message'):
            if isinstance(result.message, dict):
                # Extract text from message dict
                content = result.message.get('content', [])
                if content and isinstance(content, list) and len(content) > 0:
                    response_text = content[0].get('text', str(result.message))
                else:
                    response_text = str(result.message)
            else:
                response_text = result.message
        else:
            response_text = str(result)
        
        print("\n" + "=" * 40)
        print("LLM Response:")
        print("=" * 40)
        print(response_text)
        
        # Analyze citations in response
        print("\n" + "=" * 40)
        print("Citation Analysis:")
        print("=" * 40)
        
        import re
        
        # Extract all citations
        citations = re.findall(r'\[\^([^\]]+)\]', response_text)
        print(f"Found citations: {citations}")
        
        # Check citation patterns
        proper_citations = []
        numbered_citations = []
        
        for citation in citations:
            if citation.isdigit():
                numbered_citations.append(citation)
            else:
                proper_citations.append(citation)
        
        print(f"Proper source_id citations: {proper_citations}")
        print(f"Numbered citations (problematic): {numbered_citations}")
        
        # Determine success
        if proper_citations and not numbered_citations:
            print("✅ SUCCESS: LLM used proper source_id citations!")
            return True, response_text, citations
        elif proper_citations and numbered_citations:
            print("⚠️  PARTIAL: LLM used both proper and numbered citations")
            return False, response_text, citations
        else:
            print("❌ FAILURE: LLM only used numbered citations")
            return False, response_text, citations
            
    except Exception as e:
        print(f"❌ Error during agent test: {e}")
        import traceback
        traceback.print_exc()
        return False, None, []


def test_calculator_tool_inspection():
    """Inspect what the calculator tool actually returns to the LLM"""
    print("\n" + "=" * 80)
    print("TEST: Calculator Tool Result Inspection")
    print("=" * 80)
    
    try:
        from app.strands_integration.tools.calculator_tool_strands import calculator
        from app.strands_integration.tool_registry import _add_citation_support
        
        # Create citation-enhanced tool
        enhanced_tool = _add_citation_support(calculator, "calculator")
        
        # Call the tool directly
        result = enhanced_tool(expression="15 * 23 + 7")
        
        print("Direct tool call result:")
        print(f"Type: {type(result)}")
        print(f"Content: {result}")
        
        # Check if result contains source_id information
        if isinstance(result, str) and '[source_id:' in result:
            print("✅ Tool result contains embedded source_id")
            
            # Extract source_id
            import re
            source_ids = re.findall(r'\[source_id: ([^\]]+)\]', result)
            if source_ids:
                print(f"✅ Found source_id: {source_ids[0]}")
            else:
                print("❌ Could not extract source_id")
        else:
            print("❌ Tool result does not contain embedded source_id")
            
        return result
        
    except Exception as e:
        print(f"❌ Error during tool inspection: {e}")
        import traceback
        traceback.print_exc()
        return None
def test_actual_strands_agent_with_simple_list():
    """Test actual Strands agent with simple_list_tool and citation"""
    print("=" * 80)
    print("TEST: Actual Strands Agent with simple_list_tool and Citation")
    print("=" * 80)
    
    try:
        # Import required modules
        from strands import Agent
        from strands.models import BedrockModel
        from app.strands_integration.tools.simple_list_tool_strands import simple_list
        from app.strands_integration.tool_registry import _add_citation_support
        from app.strands_integration.citation_prompt import get_citation_system_prompt
        
        # Create citation-enhanced simple_list tool
        enhanced_simple_list = _add_citation_support(simple_list, "simple_list")
        
        # Create Bedrock model using the same configuration as the project
        from app.bedrock import get_model_id, BEDROCK_REGION
        
        model_name = "claude-v3.5-sonnet"
        model_id = get_model_id(model_name)
        
        model = BedrockModel(
            model_id=model_id,
            region=BEDROCK_REGION
        )
        
        print(f"Using model: {model_id} in region: {BEDROCK_REGION}")
        
        # Create system prompt with citation instructions
        citation_prompt = get_citation_system_prompt("claude-v3.5-sonnet")
        system_prompt = f"""You are a helpful assistant. When using tools, always cite your sources properly.

{citation_prompt}"""
        
        print("System prompt:")
        print(system_prompt)
        print("\n" + "=" * 40)
        
        # Create agent with citation-enhanced tool
        agent = Agent(
            model=model,
            tools=[enhanced_simple_list],
            system_prompt=system_prompt
        )
        
        # Test query that should trigger simple_list tool
        test_query = "Can you give me a list of 3 colors and tell me about each one?"
        
        print(f"Test query: {test_query}")
        print("\nCalling agent...")
        
        # Call agent
        start_time = time.time()
        result = agent(test_query)
        end_time = time.time()
        
        print(f"Agent call completed in {end_time - start_time:.2f} seconds")
        print(f"Result type: {type(result)}")
        
        # Extract response message
        if hasattr(result, 'message'):
            if isinstance(result.message, dict):
                # Extract text from message dict
                content = result.message.get('content', [])
                if content and isinstance(content, list) and len(content) > 0:
                    response_text = content[0].get('text', str(result.message))
                else:
                    response_text = str(result.message)
            else:
                response_text = result.message
        else:
            response_text = str(result)
        
        print("\n" + "=" * 40)
        print("LLM Response:")
        print("=" * 40)
        print(response_text)
        
        # Analyze citations in response
        print("\n" + "=" * 40)
        print("Citation Analysis:")
        print("=" * 40)
        
        import re
        
        # Extract all citations
        citations = re.findall(r'\[\^([^\]]+)\]', response_text)
        print(f"Found citations: {citations}")
        
        # Check citation patterns
        proper_citations = []
        numbered_citations = []
        
        for citation in citations:
            if citation.isdigit():
                numbered_citations.append(citation)
            else:
                proper_citations.append(citation)
        
        print(f"Proper source_id citations: {proper_citations}")
        print(f"Numbered citations (problematic): {numbered_citations}")
        
        # Determine success
        if proper_citations and not numbered_citations:
            print("✅ SUCCESS: LLM used proper source_id citations!")
            return True, response_text, citations
        elif proper_citations and numbered_citations:
            print("⚠️  PARTIAL: LLM used both proper and numbered citations")
            return False, response_text, citations
        else:
            print("❌ FAILURE: LLM only used numbered citations")
            return False, response_text, citations
            
    except Exception as e:
        print(f"❌ Error during agent test: {e}")
        import traceback
        traceback.print_exc()
        return False, None, []


def test_tool_result_inspection():
    """Inspect what the tool actually returns to the LLM"""
    print("\n" + "=" * 80)
    print("TEST: Tool Result Inspection")
    print("=" * 80)
    
    try:
        from app.strands_integration.tools.simple_list_tool_strands import simple_list
        from app.strands_integration.tool_registry import _add_citation_support
        
        # Create citation-enhanced tool
        enhanced_tool = _add_citation_support(simple_list, "simple_list")
        
        # Call the tool directly
        result = enhanced_tool(topic="colors", count=3)
        
        print("Direct tool call result:")
        print(f"Type: {type(result)}")
        print(f"Content: {result}")
        
        # Check if result contains source_id information
        if isinstance(result, dict) and 'source_id' in result:
            print(f"✅ Tool result contains source_id: {result['source_id']}")
            
            # Check if content can be parsed
            content = result.get('content', '')
            try:
                parsed_content = json.loads(content)
                if 'items' in parsed_content:
                    print(f"✅ Content contains {len(parsed_content['items'])} items")
                    for i, item in enumerate(parsed_content['items']):
                        print(f"  Item {i}: {item.get('name', 'Unknown')}")
                else:
                    print("❌ Content does not contain 'items' key")
            except json.JSONDecodeError:
                print("❌ Content is not valid JSON")
        else:
            print("❌ Tool result does not contain source_id")
            
        return result
        
    except Exception as e:
        print(f"❌ Error during tool inspection: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_citation_prompt_effectiveness():
    """Test if the citation prompt is effective"""
    print("\n" + "=" * 80)
    print("TEST: Citation Prompt Effectiveness")
    print("=" * 80)
    
    from app.strands_integration.citation_prompt import get_citation_system_prompt
    
    citation_prompt = get_citation_system_prompt("claude-v3.5-sonnet")
    
    print("Citation prompt being used:")
    print("-" * 40)
    print(citation_prompt)
    print("-" * 40)
    
    # Check if prompt mentions the correct format
    key_phrases = [
        "source_id",
        "[^xxx]",
        "[source_id:",
        "tool result"
    ]
    
    missing_phrases = []
    for phrase in key_phrases:
        if phrase not in citation_prompt:
            missing_phrases.append(phrase)
    
    if missing_phrases:
        print(f"❌ Citation prompt missing key phrases: {missing_phrases}")
        return False
    else:
        print("✅ Citation prompt contains all key phrases")
        return True


if __name__ == "__main__":
    print("Testing actual LLM citation behavior...")
    print("This test will make actual calls to Amazon Bedrock.")
    
    # Check if AWS credentials are available
    try:
        import boto3
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        print("✅ AWS credentials available")
    except Exception as e:
        print(f"❌ AWS credentials not available: {e}")
        print("Please configure AWS credentials to run this test.")
        sys.exit(1)
    
    try:
        # Run tests
        print("\n" + "🔍 Step 1: Inspecting tool results...")
        tool_result = test_tool_result_inspection()
        
        print("\n" + "🔍 Step 2: Inspecting calculator tool results...")
        calc_result = test_calculator_tool_inspection()
        
        print("\n" + "🔍 Step 3: Checking citation prompt...")
        prompt_ok = test_citation_prompt_effectiveness()
        
        print("\n" + "🔍 Step 4: Testing actual LLM call with simple_list...")
        success1, response1, citations1 = test_actual_strands_agent_with_simple_list()
        
        print("\n" + "🔍 Step 5: Testing actual LLM call with calculator...")
        success2, response2, citations2 = test_actual_strands_agent_with_calculator()
        
        # Final summary
        print("\n" + "=" * 80)
        print("FINAL RESULTS")
        print("=" * 80)
        
        if success1 and success2:
            print("🎉 SUCCESS: Citation fix is working correctly for both tools!")
            print(f"✅ simple_list citations: {citations1}")
            print(f"✅ calculator citations: {citations2}")
            print("✅ No numbered citations found")
            print("✅ Tool results contain proper source_ids")
        elif success1 or success2:
            print("⚠️  PARTIAL SUCCESS: Citation fix works for some tools")
            if success1:
                print(f"✅ simple_list citations: {citations1}")
            else:
                print(f"❌ simple_list citations failed: {citations1}")
            if success2:
                print(f"✅ calculator citations: {citations2}")
            else:
                print(f"❌ calculator citations failed: {citations2}")
        else:
            print("❌ FAILURE: Citation fix needs more work")
            if citations1:
                print(f"simple_list citations found: {citations1}")
            if citations2:
                print(f"calculator citations found: {citations2}")
        
        print("\nNext steps:")
        if success1 and success2:
            print("- Test with actual chat_with_strands integration")
            print("- Verify frontend citation display")
            print("- Test with other tools (internet_search, knowledge_base)")
        else:
            print("- Debug why some tools are not using proper source_ids")
            print("- Check if citation prompt needs adjustment for different tool types")
            print("- Verify tool result format consistency")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
