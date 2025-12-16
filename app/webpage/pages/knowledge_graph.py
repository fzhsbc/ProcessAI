import streamlit as st
import requests
from pathlib import Path


def render():
    API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")
    TOKEN = st.secrets.get("AUTH_TOKEN", "")
    headers = {"X-API-TOKEN": TOKEN} if TOKEN else {}

    st.header("工业 AI 平台控制台")
    st.write("Use this page to check basic service health and registered models.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("检查服务状态"):
            try:
                r = requests.get(f"{API_BASE.rstrip('/')}/models", headers=headers, timeout=10)
                r.raise_for_status()
                data = r.json()
                st.success("Service reachable")
                st.json(data)
            except Exception as e:
                st.error(f"Service check failed: {e}")
    with col2:
        st.write("Models registry file:")
        reg_path = Path(__file__).parents[2].parent / "model_registry.json"
        st.write(str(reg_path))


if __name__ == "__main__":
    render()