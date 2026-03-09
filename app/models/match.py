"""Match model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .team import Team


class Match(Base):
    """Premier League match entity."""

    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    season: Mapped[str] = mapped_column(String(20), nullable=False)
    match_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    home_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    away_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(30), nullable=False)

    home_team: Mapped["Team"] = relationship(
        "Team", foreign_keys=[home_team_id], back_populates="home_matches"
    )
    away_team: Mapped["Team"] = relationship(
        "Team", foreign_keys=[away_team_id], back_populates="away_matches"
    )

    __table_args__ = (
        CheckConstraint("home_score >= 0", name="ck_home_score_non_negative"),
        CheckConstraint("away_score >= 0", name="ck_away_score_non_negative"),
    )
