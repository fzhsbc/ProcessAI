from fastapi import APIRouter, HTTPException
import mlflow
import pandas as pd
import plotly.graph_objects as go


router = APIRouter(prefix="/visualization", tags=["visualization"])


@router.get("/{run_id}")
def visualize_run(run_id: str):
    """
    返回 AutoGluon 训练结果的 Plotly JSON
    """
    client = mlflow.tracking.MlflowClient()


    try:
        run = client.get_run(run_id)
    except Exception:
        raise HTTPException(status_code=404, detail="MLflow run not found")


    metrics = run.data.metrics
    fig = go.Figure([
    go.Bar(x=list(metrics.keys()), y=list(metrics.values()))
    ])


    return {"plotly_json": fig.to_json()}