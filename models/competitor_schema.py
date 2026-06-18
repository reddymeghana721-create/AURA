from pydantic import BaseModel
from typing import List, Dict, Any


class CompetitorProfile(BaseModel):
    name: str
    category: str
    product_strategy: str
    strengths: List[str]
    weaknesses: List[str]
    user_experience: str
    pricing_model: str
    target_users: List[str]


class ThreatAssessment(BaseModel):
    competitor: str
    threat_level: str
    reason: str


class FinalSummary(BaseModel):
    market_saturated: bool
    winning_factor: str
    key_insight: str
    recommended_strategy: str


class CompetitorOutput(BaseModel):
    competitor_landscape: Dict[str, List[str]]
    deep_profiles: List[Dict[str, Any]]
    feature_matrix: Dict[str, Any]
    market_positioning: Dict[str, List[str]]
    strategy_analysis: List[Dict[str, str]]
    weaknesses: List[str]
    user_switch_triggers: List[str]
    opportunity_gaps: List[str]
    threat_assessment: List[ThreatAssessment]
    final_summary: FinalSummary