import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import mlflow
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



@router.get("/{run_id}")
def get_run_status(run_id: str):
    """Return MLflow run info (status, metrics, start/end times) for a run_id."""
    try:
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(run_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    info = run.info
    data = run.data
    resp = {
        "run_id": info.run_id,
        "status": info.status,
        "start_time": info.start_time,
        "end_time": info.end_time,
        "metrics": data.metrics,
        "params": data.params,
        "tags": data.tags,
    }
    return JSONResponse(resp)