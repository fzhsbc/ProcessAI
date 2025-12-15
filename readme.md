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

MLflow：实验与模型管理

Streamlit：轻量 Web 前端

Knowledge Graph：工业知识管理

HTTP Request (v2)
   ↓
kserve_inference.py
   ↓
原始 JSON → DataFrame
   ↓
CurveFeatureExtractor
   ↓
AutoGluon Predictor.predict()
   ↓
v2 JSON Response
