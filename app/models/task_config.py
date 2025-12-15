from pydantic import BaseModel, Field
from typing import Union, Annotated
from app.core.enums import TaskType

class BaseModelConfig(BaseModel):
    task_type: TaskType

class TabularConfig(BaseModelConfig):
    task_type: TaskType = Field(TaskType.TABULAR_REGRESSION, frozen=True)
    presets: str
    time_limit: int

class TimeSeriesConfig(BaseModelConfig):
    task_type: TaskType = Field(TaskType.TIME_SERIES_FORECAST, frozen=True)
    prediction_length: int
    seasonality: int | None = None

class AnomalyConfig(BaseModelConfig):
    task_type: TaskType = Field(TaskType.ANOMALY_DETECTION, frozen=True)
    contamination: float
    threshold_method: str

ModelConfig = Annotated[
    Union[TabularConfig, TimeSeriesConfig, AnomalyConfig],
    Field(discriminator="task_type")
    ]