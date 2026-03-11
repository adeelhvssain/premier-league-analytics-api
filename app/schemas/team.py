"""Pydantic schemas for the Team resource."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class TeamCreate(BaseModel):
    """Payload for creating a team."""

    name: str
    short_name: str
    city: Optional[str] = None
    stadium: Optional[str] = None
    founded_year: Optional[int] = None


class TeamUpdate(BaseModel):
    """Payload for updating a team."""

    name: Optional[str] = None
    short_name: Optional[str] = None
    city: Optional[str] = None
    stadium: Optional[str] = None
    founded_year: Optional[int] = None


class TeamResponse(TeamCreate):
    """Response model for Team ORM objects."""

    id: int
    is_user_created: bool

    model_config = ConfigDict(from_attributes=True)
