from fastapi import APIRouter, HTTPException
from app.services.knowledge.graph_manager import KnowledgeGraphManager
from app.services.knowledge import storage
from app.services.knowledge.schema import NodeModel, RelationModel
from pathlib import Path
import logging

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

# simple singleton manager
_GRAPH_PATH = Path("./data/knowledge_graph.json")
_manager = KnowledgeGraphManager()

# try to load persisted graph at startup
try:
    g = storage.load_graph(str(_GRAPH_PATH))
    _manager.graph = g
except Exception as e:
    logging.exception("Failed to load persisted knowledge graph: %s", e)


@router.post("/node")
def add_node(node: NodeModel):
    _manager.add_entity(node.id, **node.attrs)
    try:
        storage.save_graph(_manager.graph, str(_GRAPH_PATH))
    except Exception:
        logging.exception("Failed to persist graph after adding node %s", node.id)
    return {"status": "ok", "node": node.id}


@router.post("/relation")
def add_relation(rel: RelationModel):
    _manager.add_relation(rel.src, rel.dst, rel.relation)
    try:
        storage.save_graph(_manager.graph, str(_GRAPH_PATH))
    except Exception:
        logging.exception("Failed to persist graph after adding relation %s->%s", rel.src, rel.dst)
    return {"status": "ok", "relation": rel.relation}


@router.get("/neighbors/{node_id}")
def neighbors(node_id: str):
    try:
        n = _manager.query_neighbors(node_id)
    except Exception:
        raise HTTPException(status_code=404, detail="node not found")
    return {"neighbors": n}


@router.get("/export")
def export_graph():
    try:
        data = storage.load_graph(str(_GRAPH_PATH))
        # return node count and edge count as summary
        return {"nodes": data.number_of_nodes(), "edges": data.number_of_edges()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
