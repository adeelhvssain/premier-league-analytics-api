"""Analytics calculations for the API."""

from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.team import Team


def build_league_table(db: Session, season: str):
    """Compute league table for one season from completed matches."""
    matches = (
        db.query(Match)
        .filter(Match.season == season, Match.status == "completed")
        .all()
    )

    if not matches:
        return []

    team_ids = set()
    for match in matches:
        team_ids.add(match.home_team_id)
        team_ids.add(match.away_team_id)

    teams = db.query(Team.id, Team.name).filter(Team.id.in_(team_ids)).all()
    team_names = {team_id: team_name for team_id, team_name in teams}

    table = defaultdict(
        lambda: {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }
    )

    for match in matches:
        home_stats = table[match.home_team_id]
        away_stats = table[match.away_team_id]

        home_stats["played"] += 1
        away_stats["played"] += 1

        home_stats["goals_for"] += match.home_score
        home_stats["goals_against"] += match.away_score
        away_stats["goals_for"] += match.away_score
        away_stats["goals_against"] += match.home_score

        if match.home_score > match.away_score:
            home_stats["wins"] += 1
            home_stats["points"] += 3
            away_stats["losses"] += 1
        elif match.home_score < match.away_score:
            away_stats["wins"] += 1
            away_stats["points"] += 3
            home_stats["losses"] += 1
        else:
            home_stats["draws"] += 1
            away_stats["draws"] += 1
            home_stats["points"] += 1
            away_stats["points"] += 1

    league_table = []
    for team_id, stats in table.items():
        league_table.append(
            {
                "team_id": team_id,
                "team_name": team_names.get(team_id, ""),
                "played": stats["played"],
                "wins": stats["wins"],
                "draws": stats["draws"],
                "losses": stats["losses"],
                "goals_for": stats["goals_for"],
                "goals_against": stats["goals_against"],
                "goal_difference": stats["goals_for"] - stats["goals_against"],
                "points": stats["points"],
            }
        )

    return sorted(
        league_table,
        key=lambda row: (
            -row["points"],
            -row["goal_difference"],
            -row["goals_for"],
            row["team_name"],
        ),
    )
