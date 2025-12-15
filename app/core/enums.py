from enum import Enum


class TaskType(str, Enum):
    TABULAR_REGRESSION = "tabular_regression"
    TIME_SERIES_FORECAST = "time_series_forecast"
    ANOMALY_DETECTION = "anomaly_detection"