from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.registry.model_registry import list_models, get_model
from pathlib import Path
import shutil
import tempfile


router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=dict)
def models_list():
    """Return registered models from the simple JSON registry."""
    entries = list_models()
    return {"models": entries}


@router.get("/{run_id}/download")
def download_model(run_id: str):
    """Download artifacts for a registered model run as a ZIP file."""
    entry = get_model(run_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Model not found")

    artifact_path = Path(entry.get("artifact_path"))
    if not artifact_path.exists():
        raise HTTPException(status_code=404, detail="Artifact path not found on disk")

    # Create a temporary zip archive
    tmpdir = tempfile.mkdtemp()
    archive_base = Path(tmpdir) / f"model_{run_id}"
    archive_name = shutil.make_archive(str(archive_base), "zip", root_dir=str(artifact_path))

    return FileResponse(archive_name, media_type="application/zip", filename=f"model_{run_id}.zip")