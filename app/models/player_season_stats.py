"""Player season stats model."""

from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PlayerSeasonStats(Base):
    """Player season statistics for a single competition season."""

    __tablename__ = "player_season_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    season: Mapped[str] = mapped_column(String(20), nullable=False)
    matches: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    starts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mins: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    goals: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    assists: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    passes_attempted: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    perc_passes_completed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    penalty_goals: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    penalty_attempted: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    xg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    xa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    yellow_cards: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    red_cards: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    player: Mapped["Player"] = relationship("Player", back_populates="season_stats")
