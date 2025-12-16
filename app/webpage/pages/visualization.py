import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from pathlib import Path


def render():
	st.header("Visualization")

	uploaded = st.file_uploader("Upload CSV with a `signal` column (JSON list)", type=["csv"]) 
	sample = st.checkbox("Use sample data from data/sample_train.csv")

	df = None
	if uploaded:
		df = pd.read_csv(uploaded)
	elif sample:
		sample_path = Path(__file__).parents[2] / "data" / "sample_train.csv"
		if sample_path.exists():
			df = pd.read_csv(sample_path)
		else:
			st.warning("Sample file not found: data/sample_train.csv")

	if df is None:
		st.info("Upload a CSV or enable sample data to visualize signals.")
		return

	# ensure 'signal' column is list-like
	if "signal" in df.columns:
		def _to_list(x):
			if isinstance(x, str):
				try:
					return json.loads(x)
				except Exception:
					return []
			return x

		df["signal_parsed"] = df["signal"].apply(_to_list)
	else:
		st.error("No 'signal' column in CSV")
		return

	st.write("Rows:", len(df))

	idx = st.number_input("Row index to plot", min_value=0, max_value=max(0, len(df) - 1), value=0)

	row = df.iloc[int(idx)]
	sig = row["signal_parsed"]
	if not sig:
		st.warning("Selected row has empty or invalid signal data.")
		return

	fig, ax = plt.subplots()
	ax.plot(sig, label="signal")
	ax.set_title(f"Signal (row {idx})")
	ax.legend()

	st.pyplot(fig)

	# basic stats
	import numpy as np
	arr = np.array(sig)
	st.write({
		"min": float(arr.min()),
		"max": float(arr.max()),
		"mean": float(arr.mean()),
		"std": float(arr.std()),
	})

	# allow downloading the parsed signal as JSON
	st.download_button("Download signal JSON", json.dumps(sig), file_name=f"signal_{idx}.json")
