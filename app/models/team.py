"""Team model."""

from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .player import Player


class Team(Base):
    """Premier League team entity."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    short_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    stadium: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    players: Mapped[List["Player"]] = relationship(back_populates="team")
