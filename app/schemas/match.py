"""Pydantic schemas for the Match resource."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator


class MatchCreate(BaseModel):
    """Payload for creating a match."""

    season: str
    match_date: datetime
    home_team_id: int
    away_team_id: int
    home_score: Optional[int] = 0
    away_score: Optional[int] = 0
    status: str

    @model_validator(mode="after")
    def validate_scores_and_teams(self) -> "MatchCreate":
        if self.home_team_id == self.away_team_id:
            raise ValueError("home_team_id and away_team_id cannot be the same")
        if self.home_score is not None and self.home_score < 0:
            raise ValueError("home_score cannot be negative")
        if self.away_score is not None and self.away_score < 0:
            raise ValueError("away_score cannot be negative")
        return self


class MatchResponse(MatchCreate):
    """Response model for Match ORM objects."""

    id: int

    model_config = ConfigDict(from_attributes=True)
