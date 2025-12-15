from fastapi import APIRouter
import os


router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=dict)
def list_models():
    """
    列出已注册 / 可用模型（最小实现，文件系统级）
    """
    base_dir = os.getenv("MODEL_REGISTRY_DIR", "./artifacts")
    if not os.path.exists(base_dir):
        return {"models": []}


    models = []
    for root, dirs, _ in os.walk(base_dir):
        for d in dirs:
            models.append(os.path.join(root, d))
            break


    return {"models": models}