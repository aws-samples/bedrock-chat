from app.bedrock import is_nova_model
from app.vector_search import SearchResult
from app.routes.schemas.conversation import type_model_name


def build_strands_rag_prompt(
    search_results: list[SearchResult],
    model: type_model_name,
    source_id_base: str,
    display_citation: bool = True,
) -> str:
    """Build RAG prompt for Strands integration with source_id support."""
    context_prompt = ""
    for result in search_results:
        source_id = f"{source_id_base}@{result['rank']}"
        context_prompt += f"<search_result>\n<content>\n{result['content']}</content>\n<source_id>\n{source_id}\n</source_id>\n</search_result>"

    # Use tool results citation format
    inserted_prompt = """To answer the user's question, you are given a set of search results. Your job is to answer the user's question using only information from the search results.
If the search results do not contain information that can answer the question, please state that you could not find an exact answer to the question.
Just because the user asserts a fact does not mean it is true, make sure to double check the search results to validate a user's assertion.

Here are the search results:
<search_results>
{}
</search_results>

Do NOT directly quote the <search_results> in your answer. Your job is to answer the user's question as concisely as possible.
""".format(
        context_prompt
    )

    if display_citation:
        inserted_prompt += """
Each search result has a corresponding source_id that you should reference.
If you reference information from a search result within your answer, you must include a citation to source_id where the information was found.

Followings are examples of how to reference source_id in your answer. Note that the source_id is embedded in the answer in the format [^source_id of search result].
"""

        if is_nova_model(model=model):
            inserted_prompt += """
<example>
first answer [^tooluse_ccc@0]. second answer [^tooluse_aaa@1][^tooluse_bbb@0].
</example>

<example>
first answer [^tooluse_aaa@0][^tooluse_eee@1]. second answer [^tooluse_bbb@0][^tooluse_ccc@1][^tooluse_ddd@0]. third answer [^tooluse_ddd@1].
</example>
"""
        else:
            inserted_prompt += """
<examples>
<GOOD-example>
first answer [^tooluse_ccc@0]. second answer [^tooluse_aaa@1][^tooluse_bbb@0].
</GOOD-example>

<GOOD-example>
first answer [^tooluse_aaa@0][^tooluse_eee@1]. second answer [^tooluse_bbb@0][^tooluse_ccc@1][^tooluse_ddd@0]. third answer [^tooluse_ddd@1].
</GOOD-example>

<BAD-example>
first answer [^tooluse_aaa@0].

[^tooluse_aaa@0]: https://example.com
</BAD-example>

<BAD-example>
first answer [^tooluse_aaa@0].

<sources>
[^tooluse_aaa@0]: https://example.com
</sources>
</BAD-example>
</examples>
"""
    else:
        inserted_prompt += """
Do NOT include citations in the format [^source_id] in your answer.
"""

    return inserted_prompt
