"""Small helpers for converting kserve-style JSON inputs into DataFrame
and running a predictor's `predict` method.

This module is intentionally small: integration layers can import
`predict_from_request` to implement a server adapter.
"""
from typing import Any, Dict
import pandas as pd


def payload_to_dataframe(payload: Dict[str, Any]) -> pd.DataFrame:
	"""Convert a kserve-style JSON payload into a pandas DataFrame.

	Expected shape: {'instances': [ {col: val, ...}, ... ] }
	or fallback to a dict with key 'data' or raw list of records.
	"""
	if not payload:
		return pd.DataFrame()

	if "instances" in payload and isinstance(payload["instances"], list):
		return pd.DataFrame(payload["instances"])

	if "data" in payload and isinstance(payload["data"], list):
		return pd.DataFrame(payload["data"])

	# If payload is already a list of records
	if isinstance(payload, list):
		return pd.DataFrame(payload)

	# fallback: interpret keys as columns with scalar values
	return pd.DataFrame([payload])


def predict_from_request(payload: Dict[str, Any], predictor) -> Dict[str, Any]:
	"""Run `predictor.predict` on the DataFrame converted from payload.

	`predictor` must expose a `predict(dataframe)` method. Return value is
	wrapped into a dict for JSON serialization.
	"""
	df = payload_to_dataframe(payload)
	preds = predictor.predict(df)
	return {"predictions": preds}

