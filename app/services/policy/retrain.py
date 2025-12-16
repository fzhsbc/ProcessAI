"""Simple retraining policy utilities.

These helpers implement a threshold-based decision rule and a placeholder
for scheduling retraining. In production you would replace scheduling with
an async job queue (Celery, RQ, etc.).
"""
from typing import Dict, Any
import logging


def evaluate_retrain(metrics: Dict[str, float], metric_name: str = "score_val", threshold: float = 0.0) -> bool:
	"""Return True when metric is below threshold and retraining is advised."""
	val = metrics.get(metric_name)
	if val is None:
		return False
	try:
		return float(val) < float(threshold)
	except Exception:
		return False


def schedule_retrain(run_id: str, reason: str | None = None) -> None:
	logging.info("Scheduling retrain for %s (%s)", run_id, reason)
	# Placeholder: integrate with background worker or orchestration system.
	return
