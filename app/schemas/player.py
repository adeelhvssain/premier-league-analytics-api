"""Pydantic schemas for the Player resource."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class PlayerCreate(BaseModel):
    """Payload for creating a player."""

    name: str
    position: str
    nationality: Optional[str] = None
    shirt_number: Optional[int] = None
    team_id: int


class PlayerResponse(PlayerCreate):
    """Response model for Player ORM objects."""

    id: int

    model_config = ConfigDict(from_attributes=True)
