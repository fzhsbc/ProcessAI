"""Simple file-backed storage for the knowledge graph.

This module provides helper functions to persist and restore a NetworkX
graph using node-link JSON format. Keep in mind this is a minimal
implementation for local development and not intended for production.
"""
from typing import Any
from pathlib import Path
import json
import networkx as nx
from networkx.readwrite import json_graph


def save_graph(graph: nx.Graph, path: str) -> None:
	p = Path(path)
	p.parent.mkdir(parents=True, exist_ok=True)
	data = json_graph.node_link_data(graph)
	p.write_text(json.dumps(data, indent=2))


def load_graph(path: str) -> nx.Graph:
	p = Path(path)
	if not p.exists():
		return nx.MultiDiGraph()
	data = json.loads(p.read_text())
	return json_graph.node_link_graph(data)
