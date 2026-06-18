from pydantic import BaseModel
from typing import List, Dict


class UserSegment(BaseModel):
    segment: str
    pain_level: str
    current_solutions: List[str]
    unmet_needs: List[str]
    paying_potential: str


class Competitor(BaseModel):
    name: str
    type: str
    strengths: List[str]
    weaknesses: List[str]


class OpportunityScore(BaseModel):
    score: float
    reason: str


class PricingInsights(BaseModel):
    average_willingness_to_pay: str
    common_models: List[str]


from typing import Literal

class Verdict(BaseModel):
    verdict: str
    confidence: float   # 0.0 to 1.0
    reason: str


class MarketOutput(BaseModel):

    market_overview: Dict

    user_analysis: List[UserSegment]

    competitor_analysis: List[Competitor]

    market_gaps: List[str]

    trends: List[str]

    opportunity_score: OpportunityScore

    risks: List[str]

    differentiation_strategy: List[str]

    pricing_insights: PricingInsights

    verdict: Verdict