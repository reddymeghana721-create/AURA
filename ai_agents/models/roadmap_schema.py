from pydantic import BaseModel, Field
from typing import List


class RoadmapPhase(BaseModel):
    phase: str = Field(..., description="Phase name")
    duration: str = Field(..., description="Time duration")
    deliverables: List[str] = Field(default_factory=list)


class TimelineOverview(BaseModel):
    stage: str = Field(..., description="Stage name")
    duration: str = Field(..., description="Duration")


class KeyMilestone(BaseModel):
    milestone: str = Field(..., description="Milestone description")
    timeline: str = Field(..., description="When it happens")


class WeeklyMonthlyDeliverable(BaseModel):
    period: str = Field(..., description="Week or month range")
    tasks: List[str] = Field(default_factory=list)


class RoadmapOutput(BaseModel):
    roadmap: List[RoadmapPhase] = Field(default_factory=list)
    timeline_overview: List[TimelineOverview] = Field(default_factory=list)
    key_milestones: List[KeyMilestone] = Field(default_factory=list)
    weekly_monthly_deliverables: List[WeeklyMonthlyDeliverable] = Field(default_factory=list)