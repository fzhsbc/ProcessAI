import typing
import pandas as pd
import numpy as np

from app.models.predictor_base import BasePredictor


class PyTorchAnomalyPredictor(BasePredictor):
    """A small, dependency-light anomaly predictor used as a placeholder.

    This implementation computes per-feature mean and std on `train`, then
    flags rows as anomalous when any feature exceeds `k * std` from the mean.
    It's intentionally simple — replace with a real PyTorch model when needed.
    """

    def __init__(self, k: float = 3.0):
        self.k = k
        self.stats: typing.Dict[str, typing.Tuple[float, float]] | None = None

    def train(self, data: pd.DataFrame, config: typing.Any = None):
        # compute mean/std per numeric column
        numeric = data.select_dtypes(include=[np.number])
        self.stats = {
            col: (numeric[col].mean(), numeric[col].std(ddof=0) or 1.0)
            for col in numeric.columns
        }

    def predict(self, data: pd.DataFrame):
        if self.stats is None:
            raise RuntimeError("Model not trained. Call `train` first.")
        numeric = data.select_dtypes(include=[np.number])
        anomalies = []
        for _, row in numeric.iterrows():
            is_anom = False
            for col, (m, s) in self.stats.items():
                if abs(row.get(col, 0.0) - m) > self.k * s:
                    is_anom = True
                    break
            anomalies.append(is_anom)
        return pd.Series(anomalies, index=data.index, name="is_anomaly")

    def save(self, path: str):
        if self.stats is None:
            raise RuntimeError("Model not trained. Nothing to save.")
        # simple numpy savez for the placeholder stats
        cols = list(self.stats.keys())
        means = np.array([self.stats[c][0] for c in cols])
        stds = np.array([self.stats[c][1] for c in cols])
        np.savez(path, cols=cols, means=means, stds=stds, k=np.array([self.k]))

    @classmethod
    def load(cls, path: str):
        data = np.load(path, allow_pickle=True)
        cols = list(data["cols"])
        means = data["means"]
        stds = data["stds"]
        k = float(data["k"][0])
        obj = cls(k=k)
        obj.stats = {cols[i]: (float(means[i]), float(stds[i])) for i in range(len(cols))}
        return obj
