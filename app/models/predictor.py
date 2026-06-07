import os
import pickle
import time

import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "model", "model.pkl")
ENCODER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "ml", "model", "encoders.pkl"
)


class Predictor:
    def __init__(self):
        self._model = None
        self._encoders = None
        self._feature_names = None

    @property
    def model_loaded(self) -> bool:
        return os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH)

    @property
    def feature_names(self) -> list[str]:
        if self._feature_names is None and self.model_loaded:
            self._load()
        return self._feature_names or []

    def _load(self):
        with open(MODEL_PATH, "rb") as f:
            self._model = pickle.load(f)
        with open(ENCODER_PATH, "rb") as f:
            bundle = pickle.load(f)
        self._encoders = bundle["encoders"]
        self._feature_names = bundle["feature_names"]

    def predict(self, features: dict) -> dict:
        if not self.model_loaded:
            raise FileNotFoundError("模型文件不存在,请先执行训练脚本 python -m app.ml.train")

        if self._model is None:
            self._load()

        start = time.perf_counter()
        row = {}
        for col in self._feature_names:
            val = features.get(col)
            if val is None:
                raise ValueError(f"缺少特征: {col}")
            if col in self._encoders:
                le = self._encoders[col]
                val_str = str(val)
                if val_str in le.classes_:
                    row[col] = le.transform([val_str])[0]
                else:
                    row[col] = 0
            else:
                row[col] = float(val)

        df = pd.DataFrame([row], columns=self._feature_names)
        proba = self._model.predict_proba(df)[0]
        yes_idx = list(self._model.classes_).index("yes")
        prob = proba[yes_idx]

        subscribe = prob >= 0.5
        if prob >= 0.7:
            confidence = "高"
        elif prob >= 0.4:
            confidence = "中"
        else:
            confidence = "低"

        elapsed = time.perf_counter() - start
        return {
            "subscribe": bool(subscribe),
            "probability": float(prob),
            "confidence": confidence,
            "response_time_ms": round(elapsed * 1000, 2),
        }
