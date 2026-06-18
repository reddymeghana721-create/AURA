from ai_agents.llm import llm
from backend.models.roadmap_schema import RoadmapOutput
from backend.utils.file_writer import save_output
from backend.utils.safe_llm import extract_json_safe, safe_validate


# -----------------------------
# NORMALIZER (UNCHANGED)
# -----------------------------
def normalize_roadmap(data: dict):
    if not isinstance(data, dict):
        return {}

    def safe_list(value):
        if isinstance(value, list):
            return [
                item if isinstance(item, dict) else {"value": str(item)}
                for item in value
            ]
        return []

    def safe_dict(value):
        return value if isinstance(value, dict) else {}

    return {
        "executive_summary": safe_dict(data.get("executive_summary")),
        "development_phases": safe_list(data.get("development_phases")),
        "sprints": safe_list(data.get("sprints")),
        "feature_dependencies": safe_list(data.get("feature_dependencies")),
        "milestones": safe_list(data.get("milestones")),
        "resource_plan": safe_dict(data.get("resource_plan")),
        "risk_plan": safe_list(data.get("risk_plan")),
        "mvp_features": safe_list(data.get("mvp_features")),
        "post_mvp_features": safe_list(data.get("post_mvp_features")),
        "launch_checklist": safe_list(data.get("launch_checklist")),
        "timeline": safe_dict(data.get("timeline")),
        "priority_matrix": safe_list(data.get("priority_matrix")),
    }


# -----------------------------
# 🔥 STRONG PROMPT (FIXED)
# -----------------------------
ROADMAP_PROMPT = """
You are a Senior Startup Product Manager.

You are generating a REAL execution roadmap.

INPUT:
IDEA: {idea}
MARKET: {market}
COMPETITOR: {competitor}

-------------------------
STRICT RULES
-------------------------
- DO NOT leave any field empty
- DO NOT return placeholders
- MUST be realistic and actionable
- Think like a real startup PM

MANDATORY:
- product name must be specific
- ≥ 3 development phases
- ≥ 3 sprints
- ≥ 5 MVP features
- ≥ 3 risks
- non-empty priority matrix

Return ONLY valid JSON.
"""


# -----------------------------
# QUALITY CHECK (STRICT)
# -----------------------------
def is_bad_output(data: dict):
    if not isinstance(data, dict):
        return True

    exec_sum = data.get("executive_summary", {})
    if not exec_sum.get("product"):
        return True

    if len(data.get("sprints", [])) < 3:
        return True

    if len(data.get("mvp_features", [])) < 5:
        return True

    if len(data.get("risk_plan", [])) < 3:
        return True

    if len(data.get("priority_matrix", [])) < 2:
        return True

    return False


# -----------------------------
# MAIN AGENT
# -----------------------------
def run_roadmap_agent(idea_result, market_result, competitor_result):

    idea_context = {
        "product_name": getattr(idea_result, "product_name", ""),
        "summary": getattr(idea_result, "summary", ""),
        "target_users": getattr(idea_result, "target_users", [])
    }

    market_context = {
        "market_gaps": getattr(market_result, "market_gaps", []),
        "risks": getattr(market_result, "risks", [])
    }

    competitor_context = {
        "opportunity_gaps": getattr(competitor_result, "opportunity_gaps", []),
        "weaknesses": getattr(competitor_result, "weaknesses", [])
    }

    prompt = ROADMAP_PROMPT.format(
        idea=str(idea_context),
        market=str(market_context),
        competitor=str(competitor_context)
    )

    # -----------------------------
    # RETRY LOOP (FIXED)
    # -----------------------------
    data = {}

    for _ in range(3):
        response = llm.invoke(prompt)

        try:
            data = extract_json_safe(response.content)
        except Exception:
            repaired = llm.invoke(f"Fix JSON only:\n\n{response.content}")
            data = extract_json_safe(repaired.content)

        if not is_bad_output(data):
            break
        else:
            prompt += "\n\n⚠️ Previous output was weak. Fill ALL fields properly."

    # -----------------------------
    # FINAL PIPELINE
    # -----------------------------
    fixed = normalize_roadmap(data)
    validated = safe_validate(RoadmapOutput, fixed)

    save_output(validated.model_dump(), "roadmap_output.json")

    return validated