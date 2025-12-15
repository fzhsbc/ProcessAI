from app.core.enums import TaskType
from app.services.predictors.tabular import AutoGluonTabularPredictor
from app.services.predictors.timeseries import AutoGluonTimeSeriesPredictor
from app.services.predictors.anomaly import PyTorchAnomalyPredictor

class PredictorFactory:
    @staticmethod
    def get_predictor(task_type: TaskType):
        if task_type == TaskType.TABULAR_REGRESSION:
            return AutoGluonTabularPredictor()
        if task_type == TaskType.TIME_SERIES_FORECAST:
            return AutoGluonTimeSeriesPredictor()
        if task_type == TaskType.ANOMALY_DETECTION:
            return PyTorchAnomalyPredictor()
        raise ValueError(f"Unsupported task type: {task_type}")