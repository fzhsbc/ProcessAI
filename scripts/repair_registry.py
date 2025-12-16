"""Repair registry entries by pointing artifact_path to mlruns artifacts if possible.

Run this after training runs to fix artifact paths that point to missing locations.
"""
import json
from pathlib import Path
import os

REGISTRY = Path(os.getenv("MODEL_REGISTRY_FILE", "./model_registry.json"))
MLRUNS = Path(os.getenv("MLFLOW_RUNS_DIR", "./mlruns"))


def load():
    if not REGISTRY.exists():
        print('registry not found')
        return {}
    return json.loads(REGISTRY.read_text())


def save(data):
    REGISTRY.write_text(json.dumps(data, indent=2))


def find_mlruns_path_for(run_id: str):
    # search mlruns tree for the run id
    for root, dirs, files in os.walk(str(MLRUNS)):
        for d in dirs:
            if d == run_id:
                candidate = Path(root) / d / "artifacts" / "model"
                if candidate.exists():
                    return str(candidate.resolve())
    return None


def main():
    data = load()
    changed = False
    for run_id, entry in list(data.items()):
        path = entry.get('artifact_path')
        if path and Path(path).exists():
            continue
        print('trying to repair', run_id)
        newp = find_mlruns_path_for(run_id)
        if newp:
            data[run_id]['artifact_path'] = newp
            print('updated', run_id, '->', newp)
            changed = True
        else:
            print('no mlruns artifact found for', run_id)
    if changed:
        save(data)
        print('registry updated')
    else:
        print('no changes')


if __name__ == '__main__':
    main()
