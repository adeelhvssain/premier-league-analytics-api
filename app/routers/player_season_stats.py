"""Player season stats endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.player import Player
from app.models.player_season_stats import PlayerSeasonStats
from app.schemas.player_season_stats import (
    PlayerSeasonStatsCreate,
    PlayerSeasonStatsResponse,
)


router = APIRouter(tags=["Player Season Stats"])
COMMON_RESPONSES = {
    401: {"description": "Missing or invalid API key."},
    429: {"description": "Rate limit exceeded."},
}


@router.post(
    "/player-season-stats",
    response_model=PlayerSeasonStatsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create player season stats",
    description="Creates one season stats record for a player.",
    responses={**COMMON_RESPONSES, 404: {"description": "Player not found."}},
)
def create_player_season_stats(
    stats: PlayerSeasonStatsCreate, db: Session = Depends(get_db)
):
    """Create a player season stats row."""
    player = db.query(Player).filter(Player.id == stats.player_id).first()
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    db_stats = PlayerSeasonStats(**stats.model_dump())
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats


@router.get(
    "/player-season-stats",
    response_model=list[PlayerSeasonStatsResponse],
    summary="List player season stats",
    description="Returns all player season stats records.",
    responses=COMMON_RESPONSES,
)
def list_player_season_stats(db: Session = Depends(get_db)):
    """List all player season stats rows."""
    return db.query(PlayerSeasonStats).all()


@router.get(
    "/player-season-stats/{stat_id}",
    response_model=PlayerSeasonStatsResponse,
    summary="Get player season stats by ID",
    description="Returns one player season stats record by its ID.",
    responses={**COMMON_RESPONSES, 404: {"description": "Player season stats not found."}},
)
def get_player_season_stats(stat_id: int, db: Session = Depends(get_db)):
    """Get a player season stats row by ID."""
    stats = db.query(PlayerSeasonStats).filter(PlayerSeasonStats.id == stat_id).first()
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player season stats not found"
        )
    return stats


@router.get(
    "/players/{player_id}/season-stats",
    response_model=list[PlayerSeasonStatsResponse],
    summary="List season stats for player",
    description="Returns all season stats rows for the given player ID.",
    responses={**COMMON_RESPONSES, 404: {"description": "Player not found."}},
)
def list_stats_for_player(player_id: int, db: Session = Depends(get_db)):
    """List all season stats for one player."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    return db.query(PlayerSeasonStats).filter(
        PlayerSeasonStats.player_id == player_id
    ).all()
