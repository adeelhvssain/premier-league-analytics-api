"""Player model."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .team import Team
    from .match_event import MatchEvent


class Player(Base):
    """Premier League player entity."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    position: Mapped[str] = mapped_column(String(60), nullable=False)
    nationality: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    shirt_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)

    team: Mapped["Team"] = relationship(back_populates="players")
    events: Mapped[List["MatchEvent"]] = relationship(back_populates="player")
