from pydantic import BaseModel, Field
from typing import Any, Dict, List

Scalar = int | float | str
Curve = List[float]
class DatasetMetadata(BaseModel):
    curve_columns: List[str]
    label_column: str
class TrainingDataInput(BaseModel):
    data: List[Dict[str, Scalar | Curve]]
    metadata: DatasetMetadata