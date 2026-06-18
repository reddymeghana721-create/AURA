from llm import llm
from backend.models.idea_schema import IdeaOutput
from backend.utils.file_writer import save_output
from backend.utils.safe_llm import extract_json_safe, safe_validate


IDEA_PROMPT = """
You are an expert startup analyst.

Return ONLY valid JSON (no markdown, no explanation).

Analyze this idea:
{idea}

You MUST return:
- product_name
- summary
- industry
- goal
- problem_statement (list)
- target_users (list of strings only)
- value_proposition
- usp
- market_category
- monetization_models (list)
- competitors (list)
- suggested_mvp_features (list)
- assumptions (list)
- success_metrics (list)
- product_vision
- complexity_level
- reasoning_summary (2-3 lines)
- deep_analysis (detailed 5-8 lines)
- raw_idea

CRITICAL TYPE RULES:
- complexity_level MUST be one of: "Low", "Medium", "High"
- All lists must be arrays of strings only
"""


def run_idea_agent(user_input: str):

    prompt = IDEA_PROMPT.format(idea=user_input)

    response = llm.invoke(prompt)

    try:
        data = extract_json_safe(response.content)

    except Exception:
        repair_prompt = (
            "Convert the following into valid JSON only. "
            "Do not add explanations.\n\n"
            + response.content
        )

        repaired = llm.invoke(repair_prompt)

        data = extract_json_safe(repaired.content)

    validated = safe_validate(IdeaOutput, data)

    save_output(
        validated.model_dump(),
        "idea_output.json"
    )

    return validated