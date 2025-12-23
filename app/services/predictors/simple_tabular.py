import typing
import numpy as np
import pandas as pd
import os

from app.models.predictor_base import BasePredictor


class SimpleTabularPredictor(BasePredictor):
    """Very small, dependency-light tabular predictor for MVP use.

    - Uses pandas.get_dummies for categorical encoding
    - Fits linear regression via `np.linalg.lstsq`
    - Saves/loads coefficients with `np.savez`
    This is intentionally minimal and not intended for production accuracy.
    """

    def __init__(self):
        self.coef_: np.ndarray | None = None
        self.columns_: list[str] | None = None
        self.intercept_: float = 0.0

    def _prepare_X_y(self, df: pd.DataFrame, label: str):
        y = df[label].astype(float).to_numpy()
        X = df.drop(columns=[label])
        X = pd.get_dummies(X, drop_first=True)
        cols = list(X.columns)
        X_mat = X.to_numpy(dtype=float)
        # add intercept
        X_mat = np.hstack([np.ones((X_mat.shape[0], 1)), X_mat])
        return X_mat, y, ["__intercept__"] + cols

    def train(self, data: pd.DataFrame, config: typing.Any = None):
        # Expect the caller to pass a dataframe that already contains the label column
        if getattr(config, "label", None) is None:
            raise ValueError("`config.label` must be set for SimpleTabularPredictor")
        label = config.label
        X, y, cols = self._prepare_X_y(data, label)
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        self.coef_ = coef
        self.columns_ = cols
        self.intercept_ = float(coef[0])

    def predict(self, data: pd.DataFrame):
        if self.coef_ is None or self.columns_ is None:
            raise RuntimeError("Model not trained. Call `train` first.")
        X = data.copy()
        X = pd.get_dummies(X, drop_first=True)
        # ensure same columns
        for c in self.columns_[1:]:
            if c not in X.columns:
                X[c] = 0.0
        X = X[self.columns_[1:]]
        X_mat = np.hstack([np.ones((X.shape[0], 1)), X.to_numpy(dtype=float)])
        preds = X_mat.dot(self.coef_)
        return pd.Series(preds, index=data.index, name="prediction")

    def save(self, path: str):
        if self.coef_ is None or self.columns_ is None:
            raise RuntimeError("Model not trained. Nothing to save.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez(path, coef=self.coef_, columns=self.columns_)

    @classmethod
    def load(cls, path: str):
        data = np.load(path, allow_pickle=True)
        coef = data["coef"]
        columns = list(data["columns"])
        obj = cls()
        obj.coef_ = coef
        obj.columns_ = columns
        obj.intercept_ = float(coef[0])
        return obj
