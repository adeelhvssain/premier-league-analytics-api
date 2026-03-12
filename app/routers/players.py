"""Player API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.player import Player
from app.models.team import Team
from app.schemas.player import PlayerCreate, PlayerResponse


router = APIRouter(tags=["Players"])
COMMON_RESPONSES = {
    401: {"description": "Missing or invalid API key."},
    429: {"description": "Rate limit exceeded."},
}


@router.post(
    "/players",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create player",
    description="Creates a new player linked to an existing team.",
    responses={**COMMON_RESPONSES, 404: {"description": "Team not found."}},
)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """Create a player."""
    team = db.query(Team).filter(Team.id == player.team_id).first()
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    db_player = Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


@router.get(
    "/players",
    response_model=list[PlayerResponse],
    summary="List players",
    description="Returns all players in the database.",
    responses=COMMON_RESPONSES,
)
def list_players(db: Session = Depends(get_db)):
    """List all players."""
    return db.query(Player).all()


@router.get(
    "/players/{player_id}",
    response_model=PlayerResponse,
    summary="Get player by ID",
    description="Returns one player by its ID.",
    responses={**COMMON_RESPONSES, 404: {"description": "Player not found."}},
)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Get a player by ID."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player


@router.get(
    "/teams/{team_id}/players",
    response_model=list[PlayerResponse],
    summary="List players for team",
    description="Returns all players belonging to the given team ID.",
    responses={**COMMON_RESPONSES, 404: {"description": "Team not found."}},
)
def list_players_for_team(team_id: int, db: Session = Depends(get_db)):
    """List all players for a team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    return db.query(Player).filter(Player.team_id == team_id).all()
