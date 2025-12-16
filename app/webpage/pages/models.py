import streamlit as st
import requests
from typing import List


def render():
    st.header("Models Registry")

    API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")
    TOKEN = st.secrets.get("AUTH_TOKEN", "")
    headers = {"X-API-TOKEN": TOKEN} if TOKEN else {}

    if st.button("Refresh models list"):
        try:
            r = requests.get(f"{API_BASE}/models", headers=headers, timeout=10)
            data = r.json()
        except Exception as e:
            st.error(f"Failed to fetch models: {e}")
            return

        models = data.get("models", []) if isinstance(data, dict) else []
        if not models:
            st.info("No models found in registry")
            return

        st.write(f"Found {len(models)} model(s)")
        import io

        for entry in models:
            run_id = entry.get("run_id")
            path = entry.get("artifact_path")
            meta = entry.get("metadata", {})
            st.subheader(run_id)
            st.code(path)
            st.write(meta)

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(f"Download ZIP ({run_id})"):
                    try:
                        # stream download with auth header
                        download_resp = requests.get(f"{API_BASE.rstrip('/')}/models/{run_id}/download", headers=headers, stream=True, timeout=120)
                        if download_resp.status_code != 200:
                            st.error(f"Download failed: {download_resp.status_code} {download_resp.text}")
                        else:
                            bio = io.BytesIO(download_resp.content)
                            bio.seek(0)
                            st.download_button("Save ZIP", data=bio, file_name=f"model_{run_id}.zip", mime="application/zip")
                    except Exception as e:
                        st.error(f"Download error: {e}")
            with col2:
                st.write(" ")


if __name__ == "__main__":
    render()
