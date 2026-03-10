"""Schemas for analytics responses."""

from pydantic import BaseModel


class LeagueTableRow(BaseModel):
    """One row in the league table."""

    team_id: int
    team_name: str
    played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
