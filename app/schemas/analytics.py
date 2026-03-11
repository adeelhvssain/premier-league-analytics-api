"""Schemas for analytics responses."""

from pydantic import BaseModel


class TopScorerRow(BaseModel):
    """One row for the top scorers leaderboard."""

    player_id: int
    player_name: str
    team_name: str
    goals: int


class TopAssisterRow(BaseModel):
    """One row for the top assist providers leaderboard."""

    player_id: int
    player_name: str
    team_name: str
    assists: int


class TopXGRow(BaseModel):
    """One row for the top expected goals leaderboard."""

    player_id: int
    player_name: str
    team_name: str
    xg: float


class DisciplineRow(BaseModel):
    """One row for the discipline leaderboard."""

    player_id: int
    player_name: str
    team_name: str
    yellow_cards: int
    red_cards: int
    total_cards: int


class ClubSummaryResponse(BaseModel):
    """Aggregate view for one team in one season."""

    team_id: int
    team_name: str
    player_count: int
    total_goals: int
    total_assists: int
    total_xg: float
    total_xa: float
    total_yellow_cards: int
    total_red_cards: int
