"""Model package public exports.

Expose the base predictor and common config/schema helpers used across
the codebase.
"""

from .predictor_base import BasePredictor
from .schema import DatasetMetadata, TrainingDataInput
from .task_config import ModelConfig

__all__ = ["BasePredictor", "DatasetMetadata", "TrainingDataInput", "ModelConfig"]
