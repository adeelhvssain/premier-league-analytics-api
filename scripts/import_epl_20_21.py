"""Import EPL 2020/21 player season stats from CSV into PostgreSQL."""

from pathlib import Path
import sys

import pandas as pd
from sqlalchemy.exc import IntegrityError

# Allow running this file directly with `python scripts/import_epl_20_21.py`
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import SessionLocal
from app.database import engine
from app.models.base import Base
from app.models.player import Player
from app.models.player_season_stats import PlayerSeasonStats
from app.models.team import Team


SEASON = "2020/21"


def _find_csv(path_name: str) -> Path:
    """Find the CSV in project root or data folder."""
    cwd = Path.cwd()
    candidates = [cwd / path_name, cwd / "data" / path_name]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Could not find {path_name} in project root or data folder."
    )


def _to_optional_int(value):
    """Convert numbers safely, returning None for NaN/blank."""
    if pd.isna(value):
        return None
    return int(value)


def _to_optional_float(value):
    """Convert numbers safely, returning None for NaN/blank."""
    if pd.isna(value):
        return None
    return float(value)


def _make_unique_short_name(session, club_name: str) -> str:
    """Generate a unique short_name for a team."""
    if not club_name:
        base = "UNK"
    else:
        lowered = club_name.lower()
        if "manchester city" in lowered:
            base = "MCI"
        elif "manchester united" in lowered:
            base = "MUN"
        else:
            base = "".join(part[0] for part in club_name.split() if part).upper()
            if len(base) < 3:
                base = club_name[:3].upper()

    short_name = base
    suffix = 1
    while session.query(Team).filter(Team.short_name == short_name).first() is not None:
        short_name = f"{base}{suffix}"
        suffix += 1

    return short_name


def _reset_database() -> None:
    """Drop and recreate all tables to start with a clean database."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _get_or_create_team(session, club_name: str, stats_counts: dict) -> Team:
    """Get existing team by name, or create a new one."""
    team = session.query(Team).filter(Team.name == club_name).first()
    if team is not None:
        return team

    short_name = _make_unique_short_name(session, club_name)
    team = Team(
        name=club_name,
        short_name=short_name,
        city=None,
        stadium=None,
        founded_year=None,
    )
    session.add(team)
    session.flush()
    stats_counts["teams_created"] += 1
    return team


def _get_or_create_player(
    session, name: str, nationality: str, position: str, team_id: int, stats_counts: dict
) -> Player:
    """Get existing player by name + team, or create a new one."""
    player = (
        session.query(Player)
        .filter(Player.name == name, Player.team_id == team_id)
        .first()
    )
    if player is not None:
        return player

    player = Player(
        name=name,
        position=position or "Unknown",
        nationality=(nationality if pd.notna(nationality) else None),
        shirt_number=None,
        team_id=team_id,
    )
    session.add(player)
    session.flush()
    stats_counts["players_created"] += 1
    return player


def _get_or_create_stats(session, player_id: int, row, stats_counts: dict) -> None:
    """Create one PlayerSeasonStats row if it does not already exist."""
    existing = (
        session.query(PlayerSeasonStats)
        .filter(
            PlayerSeasonStats.player_id == player_id,
            PlayerSeasonStats.season == SEASON,
        )
        .first()
    )
    if existing is not None:
        return

    stats = PlayerSeasonStats(
        player_id=player_id,
        season=SEASON,
        matches=_to_optional_int(row.get("Matches")),
        starts=_to_optional_int(row.get("Starts")),
        mins=_to_optional_int(row.get("Mins")),
        goals=_to_optional_int(row.get("Goals")),
        assists=_to_optional_int(row.get("Assists")),
        passes_attempted=_to_optional_int(row.get("Passes_Attempted")),
        perc_passes_completed=_to_optional_float(row.get("Perc_Passes_Completed")),
        penalty_goals=_to_optional_int(row.get("Penalty_Goals")),
        penalty_attempted=_to_optional_int(row.get("Penalty_Attempted")),
        xg=_to_optional_float(row.get("xG")),
        xa=_to_optional_float(row.get("xA")),
        yellow_cards=_to_optional_int(row.get("Yellow_Cards")),
        red_cards=_to_optional_int(row.get("Red_Cards")),
    )
    session.add(stats)
    stats_counts["stats_created"] += 1


def main() -> None:
    """Run the CSV import."""
    _reset_database()
    csv_path = _find_csv("EPL_20_21.csv")
    df = pd.read_csv(csv_path)

    stats_counts = {
        "teams_created": 0,
        "players_created": 0,
        "stats_created": 0,
    }

    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            club = str(row.get("Club", "")).strip()
            name = str(row.get("Name", "")).strip()
            if not club or not name:
                continue

            team = _get_or_create_team(session, club, stats_counts)

            nationality = row.get("Nationality")
            position = (
                str(row.get("Position", "Unknown")).strip()
                if pd.notna(row.get("Position"))
                else "Unknown"
            )
            player = _get_or_create_player(
                session,
                name=name,
                nationality=nationality,
                position=position,
                team_id=team.id,
                stats_counts=stats_counts,
            )
            _get_or_create_stats(session, player.id, row, stats_counts)

        session.commit()
        print(f"Teams created: {stats_counts['teams_created']}")
        print(f"Players created: {stats_counts['players_created']}")
        print(f"Stats rows created: {stats_counts['stats_created']}")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as exc:
        print(exc)
    except IntegrityError as exc:
        print(f"Database integrity error: {exc}")
