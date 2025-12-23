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
		import platform, os
		models = list_models()
		server_info = {
			"python_version": platform.python_version(),
			"platform": platform.platform(),
			"model_server_version": os.getenv("MODEL_SERVER_VERSION", "unknown"),
		}
		return {
			"status": "ok",
			"registered_models": len(models),
			"server": server_info,
			"note": "registry inspected; provide MODEL_SERVER_VERSION env var for runtime version",
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
		msg = str(e)
		if "Model not trained" in msg or "not trained" in msg:
			# Attempt a quick fallback: train on provided data, then predict.
			try:
				predictor.train(df)
				preds = predictor.predict(df)
			except Exception as e2:
				return {"error": f"prediction failed after training: {e2}"}
		else:
			return {"error": f"prediction failed: {e}"}

	return {"predictions": preds}
