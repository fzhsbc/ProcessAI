import numpy as np
import pandas as pd
from types import SimpleNamespace

from app.services.predictors.simple_tabular import SimpleTabularPredictor


def test_simple_tabular_train_predict_and_save_load(tmp_path):
    # small toy dataset
    df = pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 4.0],
        "b": ["x", "x", "y", "y"],
        "y": [2.0, 3.0, 5.0, 7.0],
    })

    cfg = SimpleNamespace(label="y")
    model = SimpleTabularPredictor()
    model.train(df, cfg)

    X = df.drop(columns=["y"])
    preds = model.predict(X)
    assert len(preds) == len(df)

    # save and load
    save_path = tmp_path / "simple_model.npz"
    model.save(str(save_path))
    assert save_path.exists()

    loaded = SimpleTabularPredictor.load(str(save_path))
    preds2 = loaded.predict(X)

    # numeric comparison
    np.testing.assert_allclose(preds.to_numpy(), preds2.to_numpy(), rtol=1e-6, atol=1e-8)
