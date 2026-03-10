"""Pydantic schemas for the MatchEvent resource."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator


ALLOWED_EVENT_TYPES = {
    "goal",
    "assist",
    "yellow_card",
    "red_card",
    "sub_on",
    "sub_off",
}


class MatchEventCreate(BaseModel):
    """Payload for creating a match event."""

    match_id: int
    player_id: int
    team_id: int
    event_type: str
    minute: int
    extra_minute: Optional[int] = None

    @model_validator(mode="after")
    def validate_event(self) -> "MatchEventCreate":
        if self.event_type not in ALLOWED_EVENT_TYPES:
            raise ValueError("Invalid event_type")
        if self.minute < 0:
            raise ValueError("minute cannot be negative")
        if self.extra_minute is not None and self.extra_minute < 0:
            raise ValueError("extra_minute cannot be negative")
        return self


class MatchEventResponse(MatchEventCreate):
    """Response model for MatchEvent ORM objects."""

    id: int

    model_config = ConfigDict(from_attributes=True)
