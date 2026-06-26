from ai_agents.llm import llm
from ai_agents.models.roadmap_schema import RoadmapOutput
from ai_agents.utils.file_writer import save_output
from ai_agents.utils.safe_llm import extract_json_safe, safe_validate


# -----------------------------
# PROMPT BUILDER (SAFE)
# -----------------------------
def build_prompt(idea_result, market_result, competitor_result):

    return f"""
You are an experienced Startup Product Manager and VC Advisor.

Generate a practical startup execution roadmap.

========================
Startup Information
========================

Product:
{idea_result.product_name}

Category:
{idea_result.category}

Problem:
{idea_result.problem_statement}

Solution:
{idea_result.recommended_solution}

Target Users:
{idea_result.target_users}

Market Summary:
{market_result.market_intelligence_summary}

Market Opportunities:
{market_result.market_opportunities}

Competitor Market Gaps:
{competitor_result.market_gap_analysis}

========================
REQUIREMENTS
========================

Create EXACTLY FIVE phases:

1. Research & Validation
2. MVP Build
3. Closed Beta
4. Public Launch
5. Scale & Institutional

Each phase must include:
- phase
- duration
- 4-6 deliverables

Also generate:
- Timeline overview (5 entries)
- 5-6 key milestones
- weekly/monthly deliverables

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================

Return ONLY JSON:

{{
  "roadmap": [
    {{
      "phase": "",
      "duration": "",
      "deliverables": []
    }}
  ],
  "timeline_overview": [
    {{
      "stage": "",
      "duration": ""
    }}
  ],
  "key_milestones": [
    {{
      "milestone": "",
      "timeline": ""
    }}
  ],
  "weekly_monthly_deliverables": [
    {{
      "period": "",
      "tasks": []
    }}
  ]
}}

NO markdown.
NO explanation.
ONLY JSON.
"""


# -----------------------------
# NORMALIZER
# -----------------------------
def normalize_roadmap(data):
    if not isinstance(data, dict):
        return {}

    return {
        "roadmap": data.get("roadmap", []),
        "timeline_overview": data.get("timeline_overview", []),
        "key_milestones": data.get("key_milestones", []),
        "weekly_monthly_deliverables": data.get("weekly_monthly_deliverables", []),
    }


# -----------------------------
# VALIDATION
# -----------------------------
def is_bad_output(data):

    if not isinstance(data, dict):
        return True

    if len(data.get("roadmap", [])) != 5:
        return True

    if len(data.get("timeline_overview", [])) < 5:
        return True

    if len(data.get("key_milestones", [])) < 5:
        return True

    if len(data.get("weekly_monthly_deliverables", [])) < 5:
        return True

    return False


# -----------------------------
# MAIN AGENT
# -----------------------------
def run_roadmap_agent(idea_result, market_result, competitor_result):

    prompt = build_prompt(
        idea_result,
        market_result,
        competitor_result
    )

    data = {}

    for attempt in range(5):

        response = llm.invoke(prompt)

        try:
            data = extract_json_safe(response.content)

        except Exception:

            repair = llm.invoke(
                "Convert this into ONLY valid JSON:\n\n" + response.content
            )

            data = extract_json_safe(repair.content)

        if not is_bad_output(data):
            break

        prompt += "\n\nFix: Return complete JSON with all 5 phases properly filled."

    fixed = normalize_roadmap(data)

    print("\n===== ROADMAP OUTPUT =====")
    print(fixed)
    print("=========================\n")

    validated = safe_validate(RoadmapOutput, fixed)

    save_output(validated.model_dump(), "roadmap_output.json")

    return validated