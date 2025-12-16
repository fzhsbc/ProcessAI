<!-- Copilot instructions for ProcessAI (AID_plat) -->
# ProcessAI — Copilot Instructions

Purpose: give an AI coding agent the minimal, repository-specific knowledge
needed to be productive. Focus on architecture, conventions, run commands,
and small concrete examples.

1) Big picture
- Backend: a FastAPI service started from `main.py`. Routes live under
  `app/routers/*` and are registered in `main.py` (each router exposes a
  `router` object). Authentication is applied via `Depends(api_token_auth)`
  from `app.core.auth`.
- Core: `app/core` contains configuration and enums (`config.py`, `enums.py`) used
  across the project.
- Models: Pydantic schemas and base predictor abstraction live in `app/models`.
  See `predictor_base.py` (defines `BasePredictor`) and `task_config.py`.
- Services: `app/services` implements feature extraction, predictors, training,
  registry, knowledge graph, and visualization. Predictor implementations are
  under `app/services/predictors` and are instantiated via
  `app/services/predictors/factory.py`.
- Deployment: `app/deploy/Dockerfile` and `app/deploy/kserve_inference.py` hold
  deploy-time integration code.

2) Run & build (what actually works from inspected files)
- Install deps: `pip install -r requirements.txt` (project uses `python-dotenv`)
- Run locally (dev):
  - `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
  - or `python main.py` (main uses `uvicorn.run()` when invoked directly).
- Docker: the `app/deploy/Dockerfile` is the single Dockerfile in the repo —
  use it to build an image for serving.

3) Project conventions & patterns (explicit, discoverable)
- Routers: files under `app/routers` export a `router = APIRouter(...)` and are
  included in `main.py`. When adding endpoints, follow existing files like
  `app/routers/train.py`.
- Auth: request-level authentication is applied using `app.core.auth.api_token_auth`.
  New endpoints should accept the same dependency for consistency.
- Predictors: extend `BasePredictor` in `app/models/predictor_base.py` and
  implement `train`, `predict`, `save`, and `load`. Register new predictor
  classes in `app/services/predictors/factory.py` where factory lookup occurs.
  Example:

```python
from app.models.predictor_base import BasePredictor

class MyPredictor(BasePredictor):
    def train(self, data, config):
        # implement training
        return

    def predict(self, data):
        return []

    def save(self, path: str):
        pass

    @classmethod
    def load(cls, path: str):
        return cls()
```

- Pydantic & configs: `app/models/task_config.py` uses a discriminated union
  pattern (`Field(discriminator='task_type')`) — follow that approach when adding
  configuration models.

4) Integration points & external dependencies
- `requirements.txt` lists runtime libs (FastAPI, uvicorn, pydantic, python-dotenv).
- `app/deploy/kserve_inference.py` is the likely integration point for model
  serving — changes to model save/load format should keep this file in mind.
- Knowledge graph code lives under `app/services/knowledge` and uses a local
  storage abstraction in `storage.py` — treat it as a single component when
  changing graph persistence.

5) What an AI assistant should do (actionable rules)
- When adding a new predictor: implement `BasePredictor` methods, add tests,
  and register the class in the `factory.py` so it becomes discoverable.
- Avoid changing global `main.py` behavior — prefer adding routers and
  including them in `main.py` the same way existing routers are included.
- Keep imports explicit and prefer package-level exports (see updated
  `app/models/__init__.py`, `app/services/__init__.py`, `app/core/__init__.py`).

6) Key files to inspect for context
- `main.py` — app entrypoint and router registration
- `app/routers/*` — API endpoints
- `app/core/config.py`, `app/core/auth.py`, `app/core/enums.py` — shared core
- `app/models/predictor_base.py`, `app/models/task_config.py`, `app/models/schema.py`
- `app/services/predictors/factory.py` — predictor registration
- `app/deploy/Dockerfile`, `app/deploy/kserve_inference.py` — deploy

7) When in doubt
- Follow existing file structure and small-file patterns. If you need to
  change serialization or contract between predictor save/load and deploy code,
  update both `predictor` implementations and `app/deploy/kserve_inference.py`.

If anything here is unclear or you want more examples (e.g. a full example
predictor plus registration & a minimal test), tell me which part to expand.
