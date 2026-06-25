from pydantic import BaseModel
from typing import List, Dict


class MarketOutput(BaseModel):
    tam: str
    sam: str
    som: str

    growth_rate_by_segment: list

    industry_trends: list

    market_opportunities: list

    threats_and_risks: list

    market_intelligence_summary: str