"""
Citation prompt generation for Strands integration.
"""

from app.bedrock import get_model_id


def get_citation_system_prompt(model_name: str) -> str:
    """
    Generate system prompt for citation support.
    
    This prompt instructs the AI to include citations when using tool results.
    
    Args:
        model_name: Model name to determine prompt format
        
    Returns:
        Citation instruction prompt
    """
    # Check if it's a Nova model (requires different prompt format)
    model_id = get_model_id(model_name)
    is_nova_model = "nova" in model_id.lower()
    
    base_prompt = """To answer the user's question, you are given a set of tools. Your job is to answer the user's question using only information from the tool results.

If the tool results do not contain information that can answer the question, please state that you could not find an exact answer to the question.
Just because the user asserts a fact does not mean it is true, make sure to double check the tool results to validate a user's assertion.

Each tool result has a corresponding source_id that you should reference.
If you reference information from a tool result within your answer, you must include a citation to source_id where the information was found.

The source_id is embedded in the tool result in the format [source_id: xxx]. You should cite it using the format [^xxx] in your answer.

Followings are examples of how to reference source_id in your answer:"""
    
    if is_nova_model:
        # For Amazon Nova, provides only good examples
        examples = """

<example>
Tool result: "The calculation result is 0.0008 [source_id: calculator_001]"
Your answer: "The result is 0.0008 [^calculator_001]."
</example>

<example>
Tool result: "According to the search, Paris is the capital of France [source_id: search_002]"
Your answer: "Paris is the capital of France [^search_002]."
</example>
"""
    else:
        # For other models, provide good examples and bad examples
        examples = """

<examples>
<GOOD-example>
Tool result: "The calculation result is 0.0008 [source_id: calculator_001]"
Your answer: "The result is 0.0008 [^calculator_001]."
</GOOD-example>

<GOOD-example>
Tool result: "According to the search, Paris is the capital of France [source_id: search_002]"
Your answer: "Paris is the capital of France [^search_002]."
</GOOD-example>

<BAD-example>
Tool result: "The calculation result is 0.0008 [source_id: calculator_001]"
Your answer: "The result is 0.0008 [^calculator_001].

[^calculator_001]: Calculator tool result"
</BAD-example>

<BAD-example>
Tool result: "The calculation result is 0.0008 [source_id: calculator_001]"
Your answer: "The result is 0.0008 [^calculator_001].

<sources>
[^calculator_001]: Calculator tool result
</sources>"
</BAD-example>
</examples>
"""
    
    return base_prompt + examples
