from llm import llm
from models.market_schema import MarketOutput
from utils.file_writer import save_output
from utils.safe_llm import extract_json_safe, safe_validate

MARKET_PROMPT = """
You are a Senior VC Market Analyst + Startup Strategist.

Your job is NOT to generate ideas.
Your job is to critically evaluate if this startup should exist.

Think like:

* A venture capitalist
* A market researcher
* A startup critic

INPUT IDEA:
{idea}

STRICT INSTRUCTIONS:

* Return ONLY valid JSON
* Be realistic
* Focus on reasoning, not storytelling
* Be sharp, critical, and strategic

CRITICAL TYPE RULES:

* confidence MUST be a string such as "0.7", "0.8", "0.9"
* opportunity_score.score MUST be a number
* All arrays must contain strings only
* Do not return markdown
* Do not wrap JSON in code blocks

OUTPUT FORMAT:

{{
"market_overview": {{
"industry": "",
"market_stage": "",
"tams_sams_som": {{
"tam": "",
"sam": "",
"som": ""
}}
}},

"user_analysis": [
{{
"segment": "",
"pain_level": "",
"current_solutions": [],
"unmet_needs": [],
"paying_potential": ""
}}
],

"competitor_analysis": [
{{
"name": "",
"type": "",
"strengths": [],
"weaknesses": []
}}
],

"market_gaps": [],

"trends": [],

"opportunity_score": {{
"score": 0.0,
"reason": ""
}},

"risks": [],

"differentiation_strategy": [],

"pricing_insights": {{
"average_willingness_to_pay": "",
"common_models": []
}},

"verdict": {{
"verdict": "",
"confidence": "0.7",
"reason": ""
}}
}}
"""

def run_market_agent(idea: str):

    prompt = MARKET_PROMPT.format(idea=idea)

    response = llm.invoke(prompt)

    try:
        data = extract_json_safe(response.content)

    except Exception:

        repair_prompt = f"""
Convert the following into VALID JSON only.

Return JSON only.
No explanation.
No markdown.

{response.content}
"""

        repaired = llm.invoke(repair_prompt)

        data = extract_json_safe(repaired.content)

    validated = safe_validate(MarketOutput, data)

    save_output(
        validated.model_dump(),
        "market_output.json"
    )

    return validated