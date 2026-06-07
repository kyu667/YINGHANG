import pytest

from app.models.predictor import Predictor


class TestPredictor:
    def test_model_not_loaded_before_training(self):
        p = Predictor()
        if not p.model_loaded:
            assert True
        else:
            pytest.skip("Model already exists, cannot test absence")

    def test_predict_without_model_raises(self):
        p = Predictor()
        if not p.model_loaded:
            with pytest.raises(FileNotFoundError, match="模型文件不存在"):
                p.predict({"job": "admin.", "marital": "married"})

    def test_missing_feature_raises(self):
        p = Predictor()
        if not p.model_loaded:
            pytest.skip("Model file not available")
        p._load()
        with pytest.raises(ValueError, match="缺少特征"):
            p.predict({"age": 30})

    def test_predict_returns_dict(self):
        p = Predictor()
        if not p.model_loaded:
            pytest.skip("Model file not available")
        p._load()
        features = {}
        for col in p._feature_names:
            if col in p._encoders:
                features[col] = p._encoders[col].classes_[0]
            else:
                features[col] = 30.0
        result = p.predict(features)
        assert "subscribe" in result
        assert "probability" in result
        assert "confidence" in result
        assert isinstance(result["subscribe"], bool)
        assert 0 <= result["probability"] <= 1
        assert result["confidence"] in ("高", "中", "低")

    def test_response_time_under_1s(self):
        p = Predictor()
        if not p.model_loaded:
            pytest.skip("Model file not available")
        p._load()
        features = {}
        for col in p._feature_names:
            if col in p._encoders:
                features[col] = p._encoders[col].classes_[0]
            else:
                features[col] = 30.0
        result = p.predict(features)
        assert result["response_time_ms"] < 1000
