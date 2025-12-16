# Industrial AI Platform


## 简介
面向工业数据（Tabular + Curve + TimeSeries）的统一 AI 平台，支持训练、预测、动态阈值、异常检测与可视化，并可扩展至 LLM 编排。


## 启动方式
```bash
export AUTH_TOKEN=your_token
pip install -r requirements.txt
python app/main.py

```run web
 streamlit run app/webpage/web.py

模块说明

FastAPI：统一 API 网关

AutoGluon：Tabular / TimeSeries AutoML

PyTorch：异常检测 / 自定义模型

# Industrial AI Platform

Lightweight backend (FastAPI) + Streamlit frontend for training and
visualizing industrial ML models (tabular, time-series, anomaly detection).

Quick start (development)

1. Install dependencies (Autogluon is heavy; skip if you only need UI):

```bash
pip install -r requirements.txt
# If you don't need Autogluon for quick UI work, you can skip autogluon installs
```

2. Set an API token for local development:

```bash
export AUTH_TOKEN=dev-token-123
```

3. Start the API server:

```bash
python main.py
# or: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Start the Streamlit UI:

```bash
streamlit run app/webpage/web.py
```

Helper scripts

- `scripts/run_sample_training.py --token <TOKEN>` : POST `data/sample_train.csv` to `POST /train` and trigger a demo training run.
- `scripts/repair_registry.py` : fix `model_registry.json` entries by searching `mlruns/` for artifact folders.
- `scripts/create_page.py <page_name>` : scaffold a new Streamlit page in `app/webpage/pages/`.

API notes

- POST `/train` expects a JSON body with two fields: `payload` and `config`.
  - `payload` follows the Pydantic model `app.models.schema.TrainingDataInput` (fields: `data`, `metadata`).
  - `config` follows `app.models.task_config.TabularConfig` (discriminated union).
- GET `/train/{run_id}` returns MLflow run info (status, metrics, params, tags).
- GET `/models` returns registered models from `model_registry.json`.
- GET `/models/{run_id}/download` returns a ZIP archive of saved artifacts for that run.

Developer tips

- The repo uses a small JSON-backed registry at `model_registry.json` (see `app/services/registry/model_registry.py`).
- For quick front-end testing you can use the built-in placeholder predictors; to produce real artifacts install `autogluon` and run training with a longer `time_limit`.
- Streamlit pages live in `app/webpage/pages/`. Add a new page module (no leading underscore). If the module defines a `render()` function the launcher will call it; otherwise top-level Streamlit code will run on import.

If you want I can add a small troubleshooting section (common install problems, Autogluon tips, MLflow setup). 
