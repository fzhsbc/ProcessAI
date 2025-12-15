import pandas as pd
from app.services.feature.curve_extractor import CurveFeatureExtractor
from app.services.predictors.factory import PredictorFactory


class UnifiedPredictor:


    def __init__(self, task_type, curve_columns: list[str]):
        self.predictor = PredictorFactory.get_predictor(task_type)
        self.extractor = CurveFeatureExtractor(curve_columns)


    def train(self, raw_df: pd.DataFrame, config):
        df = self.extractor.transform(raw_df)
        return self.predictor.train(df, config)


    def predict(self, raw_df: pd.DataFrame):
        df = self.extractor.transform(raw_df)
        return self.predictor.predict(df)