"""Team API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate


router = APIRouter()


@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    """Create a team."""
    payload = team.model_dump()
    payload["is_user_created"] = True
    db_team = Team(**payload)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/teams", response_model=list[TeamResponse])
def list_teams(db: Session = Depends(get_db)):
    """List all teams."""
    return db.query(Team).all()


@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a team by ID."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.put("/teams/{team_id}", response_model=TeamResponse)
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


@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
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
