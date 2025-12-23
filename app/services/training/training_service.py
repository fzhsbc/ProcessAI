import os
import uuid
import pandas as pd
import mlflow
# 已移除: import mlflow.autogluon
try:
    from autogluon.tabular import TabularPredictor
except Exception:  # pragma: no cover - autogluon may not be installed
    TabularPredictor = None
from app.services.predictors.simple_tabular import SimpleTabularPredictor
from app.services.feature.curve_extractor import CurveFeatureExtractor
from app.models.task_config import TabularConfig
from app.services.registry.model_registry import register_model
import logging


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

            if TabularPredictor is not None:
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
            else:
                # Fallback lightweight trainer for MVP when AutoGluon isn't installed
                from types import SimpleNamespace

                cfg = SimpleNamespace(label=label, presets=getattr(config, "presets", None), time_limit=getattr(config, "time_limit", None))
                predictor = SimpleTabularPredictor()
                predictor.train(train_df.assign(**{label: train_df[label]}), cfg)
                model_dir = os.path.abspath("./artifacts/simple")
                # Save to a single file path under model_dir
                os.makedirs(model_dir, exist_ok=True)
                save_path = os.path.join(model_dir, "simple_model.npz")
                predictor.save(save_path)
            mlflow.log_artifacts(
                local_dir=model_dir,
                artifact_path="model"
            )

            run_id = mlflow.active_run().info.run_id
            # Prefer to register the MLflow artifact URI (local file path) so
            # that downloads point to the actual stored artifacts.
            try:
                # this returns an artifact URI like file:///abs/path/mlruns/.../artifacts/model
                artifact_uri = mlflow.get_artifact_uri("model")
                if artifact_uri.startswith("file://"):
                    artifact_path = artifact_uri[len("file://"):]
                else:
                    artifact_path = os.path.abspath(model_dir)
            except Exception:
                artifact_path = os.path.abspath(model_dir)

            # register the saved artifact path in the simple registry
            try:
                register_model(run_id, artifact_path, metadata={"label": label})
            except Exception:
                # registry failures shouldn't break training result delivery
                logging.exception("Failed to register model %s in registry", run_id)

            return run_id