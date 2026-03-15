import csv
from typing import Dict, Callable, List, Optional, cast

import requests

from matchpredictor.matchresults.result import Result, Fixture, Team, Outcome


def training_results(
        csv_location: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True,
) -> List[Result]:
    return load_results(csv_location, lambda r: result_filter(r) and r.season < year)


def validation_results(
        csv_location: str,
        year: int,
        result_filter: Callable[[Result], bool] = lambda result: True
) -> List[Result]:
    return load_results(csv_location, lambda r: result_filter(r) and r.season == year)


def load_results(
        csv_location: str,
        result_filter: Callable[[Result], bool] = lambda result: True,
) -> List[Result]:
    def match_outcome(home_goals: int, away_goals: int) -> Outcome:
        if home_goals > away_goals:
            return Outcome.HOME
        if away_goals > home_goals:
            return Outcome.AWAY
        return Outcome.DRAW

    def result_from_row(row: Dict[str, str]) -> Optional[Result]:
        try:
            home_goals = int(row['score1'])
            away_goals = int(row['score2'])

            return Result(
                fixture=Fixture(
                    home_team=Team(row['team1']),
                    away_team=Team(row['team2']),
                    league=row['league']
                ),
                outcome=match_outcome(home_goals, away_goals),
                home_goals=home_goals,
                away_goals=away_goals,
                season=int(row['season'])
            )
        except (KeyError, ValueError):
            return None

    # Determine if csv_location is a URL or a local file path
    try:
        # Read data from URL or local file
        if csv_location.startswith(('http://', 'https://')):
            response = requests.get(csv_location)
            response.raise_for_status()
            csv_data = response.text
        else:
            with open(csv_location, 'r', encoding='utf-8') as f:
                csv_data = f.read()

        rows = csv.DictReader(csv_data.splitlines())
        results = []
        for row in rows:
            try:
                r = result_from_row(row)
                if isinstance(r, Result) and result_filter(r):
                    results.append(r)
            except Exception:
                # Skip any row that fails to parse
                continue
        return results
    except Exception:
        # Catch any error (network, file not found, malformed CSV, etc.)
        return []