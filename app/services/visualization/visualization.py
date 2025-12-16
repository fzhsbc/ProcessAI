"""Helpers to create Plotly figures from metrics and experiment data.

These helpers are used by the `/visualization` router to return JSON
serializable plotly objects.
"""
from typing import Dict, Any
import plotly.graph_objects as go


def metrics_bar_plot(metrics: Dict[str, float]) -> go.Figure:
	keys = list(metrics.keys())
	vals = [float(metrics[k]) for k in keys]
	fig = go.Figure([go.Bar(x=keys, y=vals)])
	fig.update_layout(title_text="Run metrics")
	return fig


def fig_to_json(fig: go.Figure) -> str:
	return fig.to_json()
