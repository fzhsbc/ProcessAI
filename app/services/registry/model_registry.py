import json
from pathlib import Path
import threading
from typing import Dict, Any, List
import os

_lock = threading.Lock()
REGISTRY_FILE = Path(os.getenv("MODEL_REGISTRY_FILE", "./model_registry.json"))


def _load() -> Dict[str, Any]:
    if not REGISTRY_FILE.exists():
        return {}
    try:
        return json.loads(REGISTRY_FILE.read_text())
    except Exception:
        return {}


def _save(data: Dict[str, Any]):
    tmp = REGISTRY_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(REGISTRY_FILE)


def register_model(run_id: str, artifact_path: str, metadata: Dict[str, Any] | None = None):
    """Register a model by MLflow run id and artifact path."""
    with _lock:
        data = _load()
        data[run_id] = {
            "artifact_path": str(artifact_path),
            "metadata": metadata or {},
        }
        _save(data)


def list_models() -> List[Dict[str, Any]]:
    with _lock:
        data = _load()
        return [
            {"run_id": k, "artifact_path": v.get("artifact_path"), "metadata": v.get("metadata", {})}
            for k, v in data.items()
        ]


def get_model(run_id: str) -> Dict[str, Any] | None:
    with _lock:
        data = _load()
        return data.get(run_id)
