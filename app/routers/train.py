import pandas as pd
from fastapi import APIRouter
from app.models.schema import TrainingDataInput
from app.models.task_config import TabularConfig
from app.services.training.training_service import TrainingService


router = APIRouter(prefix="/train", tags=["training"])


@router.post("", response_model=dict)
def train_tabular(payload: TrainingDataInput, config: TabularConfig):
    df = pd.DataFrame(payload.data)


    service = TrainingService()
    run_id = service.train_tabular(
        raw_df=df,
        label=payload.metadata.label_column,
        curve_columns=payload.metadata.curve_columns,
        config=config,
        )


    return {"status": "success", "mlflow_run_id": run_id}