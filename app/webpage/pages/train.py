import streamlit as st
import pandas as pd
import json
import requests

API_BASE = st.secrets["API_BASE"]
TOKEN = st.secrets["AUTH_TOKEN"]
HEADERS = {"X-API-TOKEN": TOKEN}

st.title("训练任务")

csv_file = st.file_uploader("上传 CSV", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)

    # 把 curve 字符串转成 list
    df["signal"] = df["signal"].apply(json.loads)

    st.dataframe(df)

    config = {
        "task_type": "tabular_regression",
        "presets": "medium_quality",
        "time_limit": 60
    }

    payload = {
        "data": df.to_dict(orient="records"),
        "metadata": {
            "curve_columns": ["signal"],
            "label_column": "label"
        }
    }

    if st.button("开始训练"):
        r = requests.post(
            f"{API_BASE}/train",
            json=payload,
            params=config,
            headers=HEADERS,
        )
        st.json(r.json())
