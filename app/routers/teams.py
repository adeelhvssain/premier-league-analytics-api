"""Team API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate


router = APIRouter(tags=["Teams"])
COMMON_RESPONSES = {
    401: {"description": "Missing or invalid API key."},
    429: {"description": "Rate limit exceeded."},
}


@router.post(
    "/teams",
    response_model=TeamResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create team",
    description="Creates a new user-created team.",
    responses=COMMON_RESPONSES,
)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    """Create a team."""
    payload = team.model_dump()
    payload["is_user_created"] = True
    db_team = Team(**payload)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get(
    "/teams",
    response_model=list[TeamResponse],
    summary="List teams",
    description="Returns all teams in the database.",
    responses=COMMON_RESPONSES,
)
def list_teams(db: Session = Depends(get_db)):
    """List all teams."""
    return db.query(Team).all()


@router.get(
    "/teams/{team_id}",
    response_model=TeamResponse,
    summary="Get team by ID",
    description="Returns one team by its ID.",
    responses={**COMMON_RESPONSES, 404: {"description": "Team not found."}},
)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a team by ID."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.put(
    "/teams/{team_id}",
    response_model=TeamResponse,
    summary="Update team",
    description="Updates a user-created team. Imported teams cannot be updated.",
    responses={
        **COMMON_RESPONSES,
        403: {"description": "Imported teams cannot be updated."},
        404: {"description": "Team not found."},
    },
)
def update_team(
    team_id: int, team_update: TeamUpdate, db: Session = Depends(get_db)
):
    """Update a user-created team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    if not team.is_user_created:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Imported teams cannot be updated",
        )

    update_data = team_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(team, field, value)

    db.commit()
    db.refresh(team)
    return team


@router.delete(
    "/teams/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete team",
    description="Deletes a user-created team. Imported teams cannot be deleted.",
    responses={
        **COMMON_RESPONSES,
        403: {"description": "Imported teams cannot be deleted."},
        404: {"description": "Team not found."},
        409: {"description": "Team is referenced by existing players."},
    },
)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """Delete a user-created team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    if not team.is_user_created:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Imported teams cannot be deleted",
        )

    db.delete(team)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team cannot be deleted because it is referenced by players",
        )

    return None
