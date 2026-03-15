from unittest import TestCase
from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor


class AlphabetPredictor(Predictor):
    def predict(self, fixture: Fixture) -> Prediction:
        if str(fixture.home_team).lower() < str(fixture.away_team).lower():
            return Prediction(outcome=Outcome.HOME)
        elif str(fixture.home_team).lower() > str(fixture.away_team).lower():
            return Prediction(outcome=Outcome.AWAY)
        else:
            return Prediction(outcome=Outcome.DRAW)