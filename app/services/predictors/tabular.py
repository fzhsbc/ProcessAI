import pandas as pd
from typing import Any

try:
    from autogluon.tabular import TabularPredictor
except Exception:  # pragma: no cover - autogluon may not be installed in dev env
    TabularPredictor = None

from app.models.predictor_base import BasePredictor


class AutoGluonTabularPredictor(BasePredictor):
    """Thin wrapper around AutoGluon TabularPredictor.

    If AutoGluon isn't available the methods raise informative errors to
    make debugging easier in minimalist environments.
    """

    def __init__(self):
        self.model = None

    def train(self, data: pd.DataFrame, config: Any):
        if TabularPredictor is None:
            raise ImportError("autogluon.tabular is required for AutoGluonTabularPredictor")
        label = getattr(config, "label", None)
        self.model = TabularPredictor(label=label)
        fit_kwargs = {}
        if hasattr(config, "presets"):
            fit_kwargs["presets"] = config.presets
        if hasattr(config, "time_limit"):
            fit_kwargs["time_limit"] = config.time_limit
        self.model.fit(data, **fit_kwargs)

    def predict(self, data: pd.DataFrame):
        if self.model is None:
            raise RuntimeError("Model not trained. Call `train` first.")
        return self.model.predict(data)

    def save(self, path: str):
        if self.model is None:
            raise RuntimeError("Model not trained. Nothing to save.")
        self.model.save(path)

    @classmethod
    def load(cls, path: str):
        if TabularPredictor is None:
            raise ImportError("autogluon.tabular is required to load saved models")
        obj = cls()
        obj.model = TabularPredictor.load(path)
        return obj
