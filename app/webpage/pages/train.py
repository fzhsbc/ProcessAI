import streamlit as st
import pandas as pd
import json
import requests
from pathlib import Path


def render():
    API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")
    TOKEN = st.secrets.get("AUTH_TOKEN", "")
    HEADERS = {"X-API-TOKEN": TOKEN} if TOKEN else {}

    st.header("训练任务")

    csv_file = st.file_uploader("上传 CSV", type=["csv"])

    if csv_file:
        df = pd.read_csv(csv_file)

        # 把 curve 字符串转成 list
        if "signal" in df.columns:
            try:
                df["signal"] = df["signal"].apply(json.loads)
            except Exception:
                st.warning("Failed to parse 'signal' column as JSON lists; leaving raw")

        st.dataframe(df)

        config = {
            "task_type": "tabular_regression",
            "presets": "medium_quality",
            "time_limit": 60,
        }

        payload = {
            "data": df.to_dict(orient="records"),
            "metadata": {
                "curve_columns": ["signal"],
                "label_column": "label",
            },
        }

        if st.button("开始训练"):
            try:
                body = {"payload": payload, "config": config}
                r = requests.post(
                    f"{API_BASE}/train",
                    json=body,
                    headers=HEADERS,
                    timeout=60,
                )
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")
                return

            try:
                res = r.json()
                st.json(res)
                run_id = res.get("mlflow_run_id")
                if run_id:
                    api_base = API_BASE.rstrip("/")
                    download_url = f"{api_base}/models/{run_id}/download"
                    st.markdown(f"Artifacts for run `{run_id}`: [Download ZIP]({download_url})")
                    # show a button to check status
                    if st.button("Check run status", key=f"status_{run_id}"):
                        try:
                            status_resp = requests.get(f"{api_base}/train/{run_id}", headers=HEADERS, timeout=10)
                            if status_resp.status_code == 200:
                                st.json(status_resp.json())
                            else:
                                st.error(f"Status check failed: {status_resp.status_code} {status_resp.text}")
                        except Exception as e:
                            st.error(f"Status request error: {e}")
            except Exception:
                st.text(r.text)

    # quick sample-train button
    if st.button("Use sample data and train"):
        try:
            sample_path = Path(__file__).parents[2] / "data" / "sample_train.csv"
            if not sample_path.exists():
                st.error("Sample data not found")
            else:
                sample_df = pd.read_csv(sample_path)
                if "signal" in sample_df.columns:
                    try:
                        sample_df["signal"] = sample_df["signal"].apply(json.loads)
                    except Exception:
                        st.warning("Failed to parse 'signal' column in sample data; leaving raw")
                payload = {
                    "data": sample_df.to_dict(orient="records"),
                    "metadata": {"curve_columns": ["signal"], "label_column": "label"},
                }
                # match the API expected shape: {payload: ..., config: ...}
                config = {
                    "task_type": "tabular_regression",
                    "presets": "medium_quality",
                    "time_limit": 60,
                }
                body = {"payload": payload, "config": config}
                try:
                    r = requests.post(f"{API_BASE}/train", json=body, headers=HEADERS, timeout=120)
                except requests.RequestException as e:
                    st.error(f"Request failed: {e}")
                    return
                try:
                    res = r.json()
                    st.json(res)
                    run_id = res.get("mlflow_run_id")
                    if run_id:
                        api_base = API_BASE.rstrip("/")
                        download_url = f"{api_base}/models/{run_id}/download"
                        st.markdown(f"Artifacts for run `{run_id}`: [Download ZIP]({download_url})")
                except Exception:
                    st.text(r.text)
        except Exception as e:
            st.error(f"Failed to train with sample data: {e}")


if __name__ == "__main__":
    render()
