from ai_agents.llm import llm
from ai_agents.models.competitor_schema import CompetitorOutput
from ai_agents.utils.file_writer import save_output
from ai_agents.utils.safe_llm import extract_json_safe, safe_validate


COMPETITOR_PROMPT = """
You are a Senior Competitive Intelligence Analyst.

You analyze competitors deeply and strategically.

Return ONLY valid JSON.

ABSOLUTE RULES:
- STRICT JSON only (no markdown, no explanation)
- No extra keys outside schema
- All lists must contain only strings
- Be realistic and analytical

INPUT CONTEXT:

IDEA:
{idea}

MARKET INSIGHTS:
{market}

TASK:
Generate deep competitor intelligence for this startup idea.

OUTPUT FORMAT:
{{
  "competitor_landscape": {{
    "direct_competitors": [],
    "indirect_competitors": [],
    "ai_disruptors": []
  }},

  "deep_profiles": [
    {{
      "name": "",
      "category": "",
      "product_strategy": "",
      "strengths": [],
      "weaknesses": [],
      "user_experience": "",
      "pricing_model": "",
      "target_users": []
    }}
  ],

  "feature_matrix": {{ }},

  "market_positioning": {{
    "low_end_players": [],
    "mid_tier": [],
    "high_tier_ai": []
  }},

  "strategy_analysis": [
    {{
      "competitor": "",
      "strategy": ""
    }}
  ],

  "weaknesses": [],

  "user_switch_triggers": [],

  "opportunity_gaps": [],

  "threat_assessment": [
    {{
      "competitor": "",
      "threat_level": "LOW",
      "reason": ""
    }}
  ],

  "final_summary": {{
    "market_saturated": true,
    "winning_factor": "",
    "key_insight": "",
    "recommended_strategy": ""
  }}
}}
"""


def run_competitor_agent(idea_result, market_result):

    idea_context = getattr(idea_result, "summary", "")
    market_context = getattr(market_result, "market_gaps", [])

    prompt = COMPETITOR_PROMPT.format(
        idea=idea_context,
        market=market_context
    )

    response = llm.invoke(prompt)

    try:
        data = extract_json_safe(response.content)

    except Exception:
        repair_prompt = f"""
Convert this into VALID JSON only.

No explanation. No markdown.

{response.content}
"""
        repaired = llm.invoke(repair_prompt)
        data = extract_json_safe(repaired.content)

    validated = safe_validate(CompetitorOutput, data)

    save_output(
        validated.model_dump(),
        "competitor_output.json"
    )

    return validated