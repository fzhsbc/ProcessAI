"""Pydantic models for knowledge graph entities and relations."""
from pydantic import BaseModel
from typing import Any, Dict


class NodeModel(BaseModel):
	id: str
	attrs: Dict[str, Any] = {}


class RelationModel(BaseModel):
	src: str
	dst: str
	relation: str
	attrs: Dict[str, Any] = {}

