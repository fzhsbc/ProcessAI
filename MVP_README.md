# MVP Quickstart — Industrial AI Platform (MVP)

Purpose: minimal, actionable steps to get an MVP running locally and to extend the project.

Prerequisites
- Python 3.10+ (virtualenv recommended)
- Docker (optional, for container smoke tests)

Local setup
1. Create and activate a virtualenv, install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set an API token used by protected endpoints:

```bash
export AUTH_TOKEN="changeme"
```

Run the dev server

```bash
# option A (simple)
python main.py
# option B (recommended for dev)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Smoke-test training (example)

1. Ensure the server is running and `AUTH_TOKEN` is exported.
2. Post the sample dataset to the `/train` endpoint (the script uses `AUTH_TOKEN`):

```bash
python scripts/run_sample_training.py --token "$AUTH_TOKEN"
```

Expected results
- A new MLflow run will be created under `mlruns/` and artifacts saved under `artifacts/model/` (or `artifacts/simple/` when running the lightweight fallback).
- `model_registry.json` will be updated by the registry helper.

Where to look in the code
- App entry and routers: [main.py](main.py) and [app/routers/](app/routers)
- Training flow: [app/services/training/training_service.py](app/services/training/training_service.py)
- Predictor patterns: [app/models/predictor_base.py](app/models/predictor_base.py) and [app/services/predictors/](app/services/predictors)
- Predictor factory: [app/services/predictors/factory.py](app/services/predictors/factory.py)
- Deployment / inference helper: [app/deploy/kserve_inference.py](app/deploy/kserve_inference.py)
- Sample training client: [scripts/run_sample_training.py](scripts/run_sample_training.py)

Adding a new predictor (quick)
1. Implement a subclass of `BasePredictor` in `app/services/predictors/` implementing `train`, `predict`, `save`, `@classmethod load`.
2. Register the class in [app/services/predictors/factory.py](app/services/predictors/factory.py).
3. Validate by running `python scripts/run_sample_training.py` and confirming artifacts in `mlruns/`.

Container / Docker (smoke test)

```bash
docker build -f app/deploy/Dockerfile -t aid_plat:dev .
docker run -e AUTH_TOKEN="$AUTH_TOKEN" -p 8000:8000 aid_plat:dev
```

Notes & gotchas
- AutoGluon heavy dependency: the repo ships a lightweight `SimpleTabularPredictor` fallback so training can run without AutoGluon for MVP/dev. Production use should install AutoGluon.
- MLflow local storage: artifacts and mlruns are written to the repo `mlruns/` folder by default. Keep this directory persisted if you want reproducible artifacts.
- Registry shape: `model_registry.json` is used by tools in `app/services/registry/`. Modify it only via scripts or helper functions to avoid breaking assumptions.

Checklist (MVP)
- [ ] Create virtualenv and install deps
- [ ] Start server and verify root page (`/`)
- [ ] Run `scripts/run_sample_training.py` and confirm `mlruns/` updates
- [ ] Inspect `model_registry.json` for a new entry
- [ ] Add a new predictor and register it (if extending)
- [ ] Build and run Docker container (optional)

If you want, I can: add a runnable unit test that exercises `SimpleTabularPredictor`, or create a full example predictor implementation and CI job.
