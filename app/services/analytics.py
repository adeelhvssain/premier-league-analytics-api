"""Analytics helpers for player season statistics."""

from sqlalchemy import distinct, func
from sqlalchemy.orm import Session
from typing import Optional

from app.models.player import Player
from app.models.player_season_stats import PlayerSeasonStats
from app.models.team import Team

from app.schemas.analytics import (
    ClubSummaryResponse,
    DisciplineRow,
    TopAssisterRow,
    TopScorerRow,
    TopXGRow,
)


def _to_int(value: Optional[int]) -> int:
    """Convert nullable DB values into safe integers for leaderboard views."""
    return 0 if value is None else int(value)


def _to_float(value: Optional[float]) -> float:
    """Convert nullable DB values into safe floats for leaderboard views."""
    return 0.0 if value is None else float(value)


def get_top_scorers(db: Session, season: str, limit: int) -> list[TopScorerRow]:
    """Return players with the highest goals in a season."""
    rows = (
        db.query(
            Player.id.label("player_id"),
            Player.name.label("player_name"),
            Team.name.label("team_name"),
            func.coalesce(PlayerSeasonStats.goals, 0).label("goals"),
        )
        .join(PlayerSeasonStats, PlayerSeasonStats.player_id == Player.id)
        .join(Team, Player.team_id == Team.id)
        .filter(PlayerSeasonStats.season == season)
        .order_by(func.coalesce(PlayerSeasonStats.goals, 0).desc(), Player.name.asc())
        .limit(limit)
        .all()
    )

    return [
        TopScorerRow(
            player_id=player_id,
            player_name=player_name,
            team_name=team_name,
            goals=_to_int(goals),
        )
        for player_id, player_name, team_name, goals in rows
    ]


def get_top_assisters(db: Session, season: str, limit: int) -> list[TopAssisterRow]:
    """Return players with the highest assists in a season."""
    rows = (
        db.query(
            Player.id.label("player_id"),
            Player.name.label("player_name"),
            Team.name.label("team_name"),
            func.coalesce(PlayerSeasonStats.assists, 0).label("assists"),
        )
        .join(PlayerSeasonStats, PlayerSeasonStats.player_id == Player.id)
        .join(Team, Player.team_id == Team.id)
        .filter(PlayerSeasonStats.season == season)
        .order_by(
            func.coalesce(PlayerSeasonStats.assists, 0).desc(),
            Player.name.asc(),
        )
        .limit(limit)
        .all()
    )

    return [
        TopAssisterRow(
            player_id=player_id,
            player_name=player_name,
            team_name=team_name,
            assists=_to_int(assists),
        )
        for player_id, player_name, team_name, assists in rows
    ]


def get_top_xg(db: Session, season: str, limit: int) -> list[TopXGRow]:
    """Return players with highest expected goals (xG) in a season."""
    rows = (
        db.query(
            Player.id.label("player_id"),
            Player.name.label("player_name"),
            Team.name.label("team_name"),
            func.coalesce(PlayerSeasonStats.xg, 0.0).label("xg"),
        )
        .join(PlayerSeasonStats, PlayerSeasonStats.player_id == Player.id)
        .join(Team, Player.team_id == Team.id)
        .filter(PlayerSeasonStats.season == season)
        .order_by(func.coalesce(PlayerSeasonStats.xg, 0.0).desc(), Player.name.asc())
        .limit(limit)
        .all()
    )

    return [
        TopXGRow(
            player_id=player_id,
            player_name=player_name,
            team_name=team_name,
            xg=_to_float(xg),
        )
        for player_id, player_name, team_name, xg in rows
    ]


def get_top_discipline(db: Session, season: str, limit: int) -> list[DisciplineRow]:
    """Return players with the most disciplinary cards in a season."""
    total_cards = (
        func.coalesce(PlayerSeasonStats.yellow_cards, 0)
        + func.coalesce(PlayerSeasonStats.red_cards, 0)
    ).label("total_cards")

    rows = (
        db.query(
            Player.id.label("player_id"),
            Player.name.label("player_name"),
            Team.name.label("team_name"),
            func.coalesce(PlayerSeasonStats.yellow_cards, 0).label("yellow_cards"),
            func.coalesce(PlayerSeasonStats.red_cards, 0).label("red_cards"),
            total_cards,
        )
        .join(PlayerSeasonStats, PlayerSeasonStats.player_id == Player.id)
        .join(Team, Player.team_id == Team.id)
        .filter(PlayerSeasonStats.season == season)
        .order_by(total_cards.desc(), Player.name.asc())
        .limit(limit)
        .all()
    )

    return [
        DisciplineRow(
            player_id=player_id,
            player_name=player_name,
            team_name=team_name,
            yellow_cards=_to_int(yellow_cards),
            red_cards=_to_int(red_cards),
            total_cards=_to_int(total_cards_value),
        )
        for player_id, player_name, team_name, yellow_cards, red_cards, total_cards_value in rows
    ]


def get_club_summary(db: Session, team_id: int, season: str) -> ClubSummaryResponse:
    """Return aggregated season totals for one team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise ValueError(f"Team {team_id} not found")

    row = (
        db.query(
            func.count(distinct(Player.id)).label("player_count"),
            func.coalesce(func.sum(PlayerSeasonStats.goals), 0).label("total_goals"),
            func.coalesce(func.sum(PlayerSeasonStats.assists), 0).label("total_assists"),
            func.coalesce(func.sum(PlayerSeasonStats.xg), 0.0).label("total_xg"),
            func.coalesce(func.sum(PlayerSeasonStats.xa), 0.0).label("total_xa"),
            func.coalesce(func.sum(PlayerSeasonStats.yellow_cards), 0).label("total_yellow_cards"),
            func.coalesce(func.sum(PlayerSeasonStats.red_cards), 0).label("total_red_cards"),
        )
        .join(Player, Player.id == PlayerSeasonStats.player_id)
        .filter(Player.team_id == team_id, PlayerSeasonStats.season == season)
        .first()
    )

    if row is None:
        return ClubSummaryResponse(
            team_id=team.id,
            team_name=team.name,
            player_count=0,
            total_goals=0,
            total_assists=0,
            total_xg=0.0,
            total_xa=0.0,
            total_yellow_cards=0,
            total_red_cards=0,
        )

    player_count, total_goals, total_assists, total_xg, total_xa, total_yellow, total_red = row
    return ClubSummaryResponse(
        team_id=team.id,
        team_name=team.name,
        player_count=_to_int(player_count),
        total_goals=_to_int(total_goals),
        total_assists=_to_int(total_assists),
        total_xg=_to_float(total_xg),
        total_xa=_to_float(total_xa),
        total_yellow_cards=_to_int(total_yellow),
        total_red_cards=_to_int(total_red),
    )
