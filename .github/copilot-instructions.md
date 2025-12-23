<!-- Copilot instructions for ProcessAI (AID_plat) -->
# ProcessAI — Copilot Instructions (condensed, repo-specific)

Purpose: minimal, practical guidance to be productive in this repo:
architecture, dev workflows, conventions, and copy-paste examples.

Big picture
- FastAPI app entry: [main.py](main.py). Routers live under [app/routers/](app/routers) and are mounted from `main.py` (each module exposes a `router`). Protected routes use the auth dependency `app.core.auth.api_token_auth`.
- ML logic: predictor interfaces and configs live in [app/models](app/models) and implementations under [app/services/predictors](app/services/predictors). Predictor instances are created via the factory at [app/services/predictors/factory.py](app/services/predictors/factory.py).
- Artifacts & deployment: model artifacts are written to `mlruns/` (MLflow layout) and a top-level `model_registry.json` tracks registry metadata. Production inference uses [app/deploy/kserve_inference.py](app/deploy/kserve_inference.py) and the Dockerfile at [app/deploy/Dockerfile](app/deploy/Dockerfile).

Quick commands (local)
- Install deps: `pip install -r requirements.txt`.
- Run dev server: `python main.py` or `uvicorn main:app --reload --host 0.0.0.0 --port 8000`.
- Produce example model artifacts: `python scripts/run_sample_training.py` (writes under `mlruns/` and updates `model_registry.json`).

Key repo conventions (practical)
- Routers: each module in `app/routers/` defines `router = APIRouter(...)` and is included by `main.py`. Avoid changing the router-loading approach—add new routers instead.
- Auth: use `app.core.auth.api_token_auth` for endpoint protection; many routers include it as a route-level dependency in `main.py`.
- Predictors: implement `BasePredictor` (`app/models/predictor_base.py`) methods: `train(data, config)`, `predict(data)`, `save(path)`, `@classmethod load(path)`. Register new predictor classes in [app/services/predictors/factory.py](app/services/predictors/factory.py).
- Configs: task configs use discriminated unions in [app/models/task_config.py](app/models/task_config.py) (Field discriminator `task_type`). Follow this pattern when adding task-specific config variants.

Integration & compatibility rules
- Serialization compatibility: if you change predictor save/load serialization, update [app/deploy/kserve_inference.py](app/deploy/kserve_inference.py) and ensure `scripts/run_sample_training.py` still produces compatible artifacts.
- MLflow artifacts: assume `mlruns/` is the authoritative run/artifact location. New training routines should place artifacts under an `artifacts/model/` path consistent with existing runs.
- Registry: update `model_registry.json` only via provided scripts or with careful migration; other components rely on its shape.

Notable files to inspect (start here)
- [main.py](main.py)
- [app/routers/train.py](app/routers/train.py) and other modules in [app/routers/](app/routers)
- [app/models/predictor_base.py](app/models/predictor_base.py), [app/models/task_config.py](app/models/task_config.py)
- [app/services/predictors/factory.py](app/services/predictors/factory.py)
- [app/deploy/kserve_inference.py](app/deploy/kserve_inference.py)
- [scripts/run_sample_training.py](scripts/run_sample_training.py)

Quick copy-paste predictor skeleton
```python
from app.models.predictor_base import BasePredictor

class MyPredictor(BasePredictor):
    def train(self, data, config):
        # save artifacts to path provided by training service
        return {"meta": "ok"}

    def predict(self, data):
        return [0 for _ in data]

    def save(self, path: str):
        # write model files under `path`
        pass

    @classmethod
    def load(cls, path: str):
        return cls()
```

Actionable rules for an AI coding agent
- When adding a predictor: implement `BasePredictor` methods and register the class in [app/services/predictors/factory.py](app/services/predictors/factory.py).
- Prefer adding routers to `app/routers/` instead of altering `main.py` router-loading.
- Update `app/deploy/kserve_inference.py` for any serialization or loading changes to keep deploy compatibility.
- Use `scripts/run_sample_training.py` to validate that a new predictor produces the expected MLflow layout in `mlruns/`.

If anything here is unclear or you want a full example (predictor + registration + run script + test), I can add it—tell me which predictor type to target.
<!-- Copilot instructions for ProcessAI (AID_plat) -->
# ProcessAI — Copilot Instructions (condensed)

Purpose: provide the minimal, repo-specific knowledge an AI coding agent
needs to be productive here: architecture, run commands, conventions, and
small copy-paste examples.

Big picture
- FastAPI backend launched from `main.py`. Routers live in `app/routers/*`
  and are included in `main.py` (each exposes `router`). All API routes are
  mounted with the auth dependency `app.core.auth.api_token_auth`.
- Predictors & ML logic live under `app/models` and `app/services`. Predictor
  implementations are in `app/services/predictors` and instantiated via the
  factory at `app/services/predictors/factory.py`.
- Model serving integration lives in `app/deploy` (see `kserve_inference.py`).

How to run locally (quick)
- Install deps: `pip install -r requirements.txt`.
- Start dev server: `python main.py` or
  `uvicorn main:app --reload --host 0.0.0.0 --port 8000`.
- Produce sample artifacts: run `scripts/run_sample_training.py` (creates
  artifacts under `mlruns/` and `model_registry.json`).

Conventions & patterns (practical)
- Routers: define `router = APIRouter(...)` and include route-level
  dependencies via `app.include_router(..., dependencies=[Depends(api_token_auth)])`.
- Auth: always use `app.core.auth.api_token_auth` for protected endpoints.
- Predictors: subclass `BasePredictor` (`app/models/predictor_base.py`) and
  implement `train(data, config)`, `predict(data)`, `save(path)`, `load(path)`.
  Register new predictors in `app/services/predictors/factory.py`.
- Configs: `app/models/task_config.py` uses a discriminated union
  (`Field(discriminator='task_type')`) — follow this for task-specific configs.

Integration points & artifacts
- MLflow outputs: `mlruns/` contains runs and artifacts; registry file is
  `model_registry.json` at repo root.
- Deployment: `app/deploy/Dockerfile` and `app/deploy/kserve_inference.py` —
  keep save/load compatibility between predictors and `kserve_inference.py`.
- Knowledge graph: `app/services/knowledge` with `storage.py` for persistence.

Practical examples
- Minimal predictor skeleton to copy/paste into `app/services/predictors`:

```python
from app.models.predictor_base import BasePredictor

class MyPredictor(BasePredictor):
    def train(self, data, config):
        # return trained model metadata or save artifacts
        return

    def predict(self, data):
        return [0] * len(data)

    def save(self, path: str):
        # persist model artifacts
        pass

    @classmethod
    def load(cls, path: str):
        return cls()
```

Files to inspect first
- `main.py` — app entry and router mounting
- `app/routers/*` — endpoints (train, models, visualization, llm, deploy, knowledge)
- `app/models/predictor_base.py`, `app/models/task_config.py`
- `app/services/predictors/factory.py` — add new predictors here
- `scripts/run_sample_training.py` — runnable example producing model artifacts

What an AI assistant should do (actionable rules)
- When adding a predictor: implement `BasePredictor` methods and register it
  in `app/services/predictors/factory.py`.
- Avoid changing `main.py` router-loading behavior; add routers instead.
- If changing model serialization, update `app/deploy/kserve_inference.py` and
  ensure `scripts/run_sample_training.py` still produces compatible artifacts.

If anything here is unclear or you want me to expand with a full example
predictor + test, say so and I will add the code and a quick run script.
