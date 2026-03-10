"""MatchEvent model."""

from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .match import Match
    from .player import Player
    from .team import Team


class MatchEvent(Base):
    """Event that occurs during a match."""

    __tablename__ = "match_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(20), nullable=False)
    minute: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_minute: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    match: Mapped["Match"] = relationship(back_populates="events")
    player: Mapped["Player"] = relationship(back_populates="events")
    team: Mapped["Team"] = relationship(back_populates="events")

    __table_args__ = (
        CheckConstraint("minute >= 0", name="ck_match_event_minute_non_negative"),
        CheckConstraint(
            "extra_minute IS NULL OR extra_minute >= 0",
            name="ck_match_event_extra_minute_non_negative",
        ),
    )
