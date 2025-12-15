import pandas as pd
from fastapi import APIRouter
from app.services.predictors.unified import UnifiedPredictor
from app.models.schema import TrainingDataInput
from app.core.enums import TaskType

router = APIRouter(prefix="/predict", tags=["predict"])

# ⚠️ 示例：真实系统应从 run_id / model_path 加载
_predictor = None

@router.post("")
def predict(payload: TrainingDataInput):
    global _predictor

    df = pd.DataFrame(payload.data)

    if _predictor is None:
        _predictor = UnifiedPredictor(
            task_type=TaskType.TABULAR_REGRESSION,
            curve_columns=payload.metadata.curve_columns,
        )
        # 这里未来换成 MLflow / 本地 load
        _predictor.predictor.load("./artifacts/autogluon")

    result = _predictor.predict(df)
    return {"prediction": result}
