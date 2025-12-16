from fastapi import APIRouter

router = APIRouter(prefix="/deploy", tags=["deploy"])

@router.get("/health")
def deploy_health():
	"""Simple health endpoint for deployment router."""
	return {"status": "ok"}

@router.get("/info")
def deploy_info():
	"""Return basic deploy info and registry summary.

	TODO: extend with model server metadata, version, and runtime stats.
	"""
	try:
		from app.services.registry.model_registry import list_models
		models = list_models()
		return {
			"status": "ok",
			"registered_models": len(models),
			"note": "TODO: add server version and runtime metrics",
		}
	except Exception as e:
		return {"status": "ok", "warning": f"failed to inspect registry: {e}"}


from fastapi import Body, Query
from app.models.schema import TrainingDataInput
from app.core.enums import TaskType
from app.services.predictors.factory import PredictorFactory
from app.services.feature.curve_extractor import CurveFeatureExtractor
from app.services.registry.model_registry import get_model


@router.post("/predict")
def deploy_predict(payload: TrainingDataInput = Body(...), run_id: str | None = Query(None), task_type: TaskType = Query(TaskType.TABULAR_REGRESSION)):
	"""Predict using a model registered in `model_registry.json`.

	- `run_id` (optional): if provided, the registry will be used to locate artifacts and load the model.
	- `task_type`: determines which predictor implementation to use for loading.
	"""
	# convert payload to DataFrame
	import pandas as pd
	df = pd.DataFrame(payload.data)

	# load model from registry when run_id is provided
	predictor = PredictorFactory.get_predictor(task_type)
	if run_id:
		entry = get_model(run_id)
		if not entry:
			return {"error": "run_id not found in registry"}
		artifact_path = entry.get("artifact_path")
		try:
			predictor = type(predictor).load(artifact_path)
		except Exception as e:
			return {"error": f"failed to load model: {e}"}

	# apply curve extractor if payload has curve columns
	curve_cols = payload.metadata.curve_columns if hasattr(payload, "metadata") else []
	if curve_cols:
		extractor = CurveFeatureExtractor(curve_cols)
		df = extractor.transform(df)

	try:
		preds = predictor.predict(df)
	except Exception as e:
		return {"error": f"prediction failed: {e}"}

	return {"predictions": preds}
