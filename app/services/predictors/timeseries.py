import pandas as pd
import numpy as np
from autogluon.timeseries import TimeSeriesPredictor
from app.models.predictor_base import BasePredictor


class AutoGluonTimeSeriesPredictor(BasePredictor):
    def train(self, data: pd.DataFrame, config):
        self.freq = data.index.freq
        self.model = TimeSeriesPredictor(
        prediction_length=config.prediction_length,
        freq=self.freq
        )
        self.model.fit(data)


    def predict(self, data: pd.DataFrame, sensitivity_factor: float = 1.0):
        if data.index.freq != self.freq:
            raise ValueError("Time frequency mismatch")
        forecast = self.model.predict(data)
        return self.generate_dynamic_threshold(forecast, sensitivity_factor)


    def generate_dynamic_threshold(self, forecast_df, k: float):
        mean = forecast_df["mean"]
        std = forecast_df["std"]
        return {
        "mean": mean,
        "upper": mean + k * std,
        "lower": mean - k * std,
        }


    def save(self, path: str):
        self.model.save(path)


    @classmethod
    def load(cls, path: str):
        obj = cls()
        obj.model = TimeSeriesPredictor.load(path)
        return obj