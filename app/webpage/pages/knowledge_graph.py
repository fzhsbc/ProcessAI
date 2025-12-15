import streamlit as st
import requests


API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")
TOKEN = st.secrets.get("AUTH_TOKEN", "")


headers = {"X-API-TOKEN": TOKEN}


st.set_page_config(page_title="Industrial AI Platform", layout="wide")


st.title("工业 AI 平台控制台")


if st.button("检查服务状态"):
    r = requests.get(f"{API_BASE}/models", headers=headers)
    st.json(r.json())