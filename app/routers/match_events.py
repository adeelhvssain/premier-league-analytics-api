"""MatchEvent API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.match import Match
from app.models.match_event import MatchEvent
from app.schemas.match_event import ALLOWED_EVENT_TYPES, MatchEventCreate, MatchEventResponse


router = APIRouter()


@router.post("/events", response_model=MatchEventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: MatchEventCreate, db: Session = Depends(get_db)):
    """Create a match event."""
    if event.event_type not in ALLOWED_EVENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid event_type"
        )
    if event.minute < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="minute cannot be negative"
        )
    if event.extra_minute is not None and event.extra_minute < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="extra_minute cannot be negative",
        )

    match = db.query(Match).filter(Match.id == event.match_id).first()
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match not found"
        )

    db_event = MatchEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/events", response_model=list[MatchEventResponse])
def list_events(db: Session = Depends(get_db)):
    """List all match events."""
    return db.query(MatchEvent).all()


@router.get("/events/{event_id}", response_model=MatchEventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get an event by ID."""
    event = db.query(MatchEvent).filter(MatchEvent.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MatchEvent not found"
        )
    return event


@router.get("/matches/{match_id}/events", response_model=list[MatchEventResponse])
def list_match_events(match_id: int, db: Session = Depends(get_db)):
    """List all events for a match."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match not found"
        )
    return db.query(MatchEvent).filter(MatchEvent.match_id == match_id).all()
