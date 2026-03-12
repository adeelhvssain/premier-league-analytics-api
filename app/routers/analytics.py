"""Analytics endpoints for the player-season dataset."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.analytics import (
    ClubSummaryResponse,
    DisciplineRow,
    TopAssisterRow,
    TopScorerRow,
    TopXGRow,
)
from app.services.analytics import (
    get_club_summary,
    get_top_assisters,
    get_top_discipline,
    get_top_scorers,
    get_top_xg,
)

router = APIRouter(tags=["Analytics"])
COMMON_RESPONSES = {
    401: {"description": "Missing or invalid API key."},
    429: {"description": "Rate limit exceeded."},
}


@router.get(
    "/analytics/top-scorers",
    response_model=list[TopScorerRow],
    summary="Top goal scorers",
    description="Returns top goal scorers for the selected season.",
    responses=COMMON_RESPONSES,
)
def top_scorers(season: str = "2020/21", limit: int = 10, db: Session = Depends(get_db)):
    """Top goalscorers for a season."""
    return get_top_scorers(db=db, season=season, limit=limit)


@router.get(
    "/analytics/top-assisters",
    response_model=list[TopAssisterRow],
    summary="Top assist providers",
    description="Returns top assist providers for the selected season.",
    responses=COMMON_RESPONSES,
)
def top_assisters(
    season: str = "2020/21", limit: int = 10, db: Session = Depends(get_db)
):
    """Top assist providers for a season."""
    return get_top_assisters(db=db, season=season, limit=limit)


@router.get(
    "/analytics/top-xg",
    response_model=list[TopXGRow],
    summary="Top expected goals (xG)",
    description="Returns players with highest xG for the selected season.",
    responses=COMMON_RESPONSES,
)
def top_xg(season: str = "2020/21", limit: int = 10, db: Session = Depends(get_db)):
    """Top xG performers for a season."""
    return get_top_xg(db=db, season=season, limit=limit)


@router.get(
    "/analytics/discipline",
    response_model=list[DisciplineRow],
    summary="Discipline leaderboard",
    description="Returns players with most cards for the selected season.",
    responses=COMMON_RESPONSES,
)
def discipline(
    season: str = "2020/21", limit: int = 10, db: Session = Depends(get_db)
):
    """Players with the most disciplinary cards for a season."""
    return get_top_discipline(db=db, season=season, limit=limit)


@router.get(
    "/analytics/club-summary/{team_id}",
    response_model=ClubSummaryResponse,
    summary="Club summary",
    description="Returns aggregated season totals for one club.",
    responses={**COMMON_RESPONSES, 404: {"description": "Team not found."}},
)
def club_summary(team_id: int, season: str = "2020/21", db: Session = Depends(get_db)):
    """Season club summary totals."""
    try:
        return get_club_summary(db=db, team_id=team_id, season=season)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
