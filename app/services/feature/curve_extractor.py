import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis


class CurveFeatureExtractor:
    def __init__(self, curve_columns: list[str]):
        self.curve_columns = curve_columns
        def transform(self, df: pd.DataFrame) -> pd.DataFrame:
            df = df.copy()
            for col in self.curve_columns:
                curves = df[col]
                df[f"{col}_min"] = curves.apply(np.min)
                df[f"{col}_max"] = curves.apply(np.max)
                df[f"{col}_mean"] = curves.apply(np.mean)
                df[f"{col}_std"] = curves.apply(np.std)
                df[f"{col}_skew"] = curves.apply(skew)
                df[f"{col}_kurt"] = curves.apply(kurtosis)
                df.drop(columns=[col], inplace=True)
            return df