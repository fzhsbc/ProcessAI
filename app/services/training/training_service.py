import os
import uuid
import pandas as pd
import mlflow
# 已移除: import mlflow.autogluon
from autogluon.tabular import TabularPredictor
from app.services.feature.curve_extractor import CurveFeatureExtractor
from app.models.task_config import TabularConfig


class TrainingService:
    """
    工业级训练服务：
    - 不捕获 AutoGluon / MLflow 异常
    - 每次训练 = 一个独立 MLflow Run
    """
    def __init__(self, mlflow_tracking_uri: str | None = None):
        if mlflow_tracking_uri:
            mlflow.set_tracking_uri(mlflow_tracking_uri)

    def train_tabular(
        self,
        raw_df: pd.DataFrame,
        label: str,
        curve_columns: list[str],
        config: TabularConfig,
    ) -> str:
        run_name = f"tabular-train-{uuid.uuid4().hex[:8]}"

        extractor = CurveFeatureExtractor(curve_columns)
        train_df = extractor.transform(raw_df)

        with mlflow.start_run(run_name=run_name):
            mlflow.log_params({
                "task_type": config.task_type,
                "presets": config.presets,
                "time_limit": config.time_limit,
            })

            predictor = TabularPredictor(label=label)
            predictor.fit(
                train_df,
                presets=config.presets,
                time_limit=config.time_limit,
            )

            leaderboard = predictor.leaderboard(silent=True)
            best_row = leaderboard.iloc[0].to_dict()

            for k, v in best_row.items():
                if isinstance(v, (int, float)):
                    mlflow.log_metric(k, float(v))
            model_dir = os.path.abspath("./artifacts/autogluon")
            predictor.save(model_dir)
            mlflow.log_artifacts(
                local_dir=model_dir,
                artifact_path="model"
            )

            return mlflow.active_run().info.run_id