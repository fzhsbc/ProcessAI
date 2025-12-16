"""Post sample_train.csv to the local /train endpoint to trigger training.

Usage:
    python scripts/run_sample_training.py

Reads `data/sample_train.csv`, converts `signal` JSON strings to lists,
and posts to `http://localhost:8000/train` using `AUTH_TOKEN` from env if set.
"""
import os
import json
import pandas as pd
import requests
from pathlib import Path


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="API auth token (overrides AUTH_TOKEN env)")
    parser.add_argument("--api", help="API base URL", default=os.getenv("API_BASE", "http://localhost:8000"))
    parser.add_argument("--presets", help="AutoGluon presets", default="medium_quality")
    parser.add_argument("--time_limit", type=int, help="Time limit in seconds", default=60)
    args = parser.parse_args()

    api_base = args.api
    token = args.token if args.token is not None else os.getenv("AUTH_TOKEN")
    if token is None:
        print("ERROR: No auth token provided. Set AUTH_TOKEN environment variable or pass --token.")
        raise SystemExit(2)
    headers = {"X-API-TOKEN": token}

    sample_path = Path(__file__).parents[1] / "data" / "sample_train.csv"
    if not sample_path.exists():
        print("sample_train.csv not found at", sample_path)
        raise SystemExit(1)

    df = pd.read_csv(sample_path)
    # try to parse signal column
    if "signal" in df.columns:
        def _to_list(x):
            if isinstance(x, str):
                try:
                    return json.loads(x)
                except Exception:
                    return []
            return x
        df["signal"] = df["signal"].apply(_to_list)

    payload = {
        "data": df.to_dict(orient="records"),
        "metadata": {"curve_columns": ["signal"], "label_column": "label"},
    }

    params = {
        "task_type": "tabular_regression",
        "presets": args.presets,
        "time_limit": args.time_limit,
    }

    url = f"{api_base}/train"
    print("Posting to", url)
    # The FastAPI endpoint expects both `payload` and `config` as body params
    body = {"payload": payload, "config": params}
    r = requests.post(url, json=body, headers=headers, timeout=600)
    try:
        print("Response:", r.status_code)
        print(r.json())
    except Exception:
        print(r.text)


if __name__ == "__main__":
    main()
