"""Analytics endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.analytics import LeagueTableRow
from app.services.analytics import build_league_table

router = APIRouter()


@router.get("/analytics/league-table", response_model=list[LeagueTableRow])
def get_league_table(season: str, db: Session = Depends(get_db)):
    """Return league table for a season based only on completed matches."""
    return build_league_table(db=db, season=season)
