from fastapi import APIRouter


router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/chat")
def chat(payload: dict):
    """
    LLM 接口占位：
    - 即使未配置 LLM，也不影响系统运行
    """
    return {
    "answer": "LLM module not configured",
    "actions": [],
    }