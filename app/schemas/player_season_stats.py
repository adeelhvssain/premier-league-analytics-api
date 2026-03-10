"""Pydantic schemas for player season stats."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class PlayerSeasonStatsCreate(BaseModel):
    """Payload for creating a player season stat row."""

    player_id: int
    season: str
    matches: Optional[int] = None
    starts: Optional[int] = None
    mins: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    passes_attempted: Optional[int] = None
    perc_passes_completed: Optional[float] = None
    penalty_goals: Optional[int] = None
    penalty_attempted: Optional[int] = None
    xg: Optional[float] = None
    xa: Optional[float] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None


class PlayerSeasonStatsResponse(PlayerSeasonStatsCreate):
    """Response model for player season stat rows."""

    id: int

    model_config = ConfigDict(from_attributes=True)
