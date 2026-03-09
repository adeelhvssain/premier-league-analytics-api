"""Team model."""

from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Team(Base):
    """Premier League team entity."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    short_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    stadium: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
