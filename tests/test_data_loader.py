import os
import tempfile
from unittest.mock import patch

import pandas as pd
import pytest

from app.models.data_loader import (
    MISSING_MARKERS,
    get_categorical_features,
    get_feature_columns,
    get_numeric_features,
    load_test_data,
    load_train_data,
)


class TestLoadTrainData:
    def test_returns_dataframe(self):
        df = load_train_data()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "subscribe" in df.columns

    def test_file_not_found(self):
        with patch("app.models.data_loader._resolve_data_path") as mock_path:
            mock_path.return_value = "/nonexistent/path/file.csv"
            with pytest.raises(FileNotFoundError):
                load_train_data()

    def test_empty_file_raises(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("col1,col2\n")  # header only, no data rows
            tmp = f.name
        try:
            with patch("app.models.data_loader._resolve_data_path") as mock_path:
                mock_path.return_value = tmp
                with pytest.raises(ValueError, match="empty"):
                    load_train_data()
        finally:
            os.unlink(tmp)


class TestLoadTestData:
    def test_returns_dataframe(self):
        df = load_test_data()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_file_not_found(self):
        with patch("app.models.data_loader._resolve_data_path") as mock_path:
            mock_path.return_value = "/nonexistent/path/file.csv"
            with pytest.raises(FileNotFoundError):
                load_test_data()


class TestMissingMarkers:
    def test_missing_markers_replaced_with_na(self):
        df = load_train_data()
        for marker in MISSING_MARKERS:
            for col in df.select_dtypes(include="object").columns:
                mask = df[col] == marker
                assert not mask.any(), f"Column {col} still contains '{marker}'"


class TestFeatureColumns:
    def test_excludes_id_and_target(self):
        cols = get_feature_columns()
        assert "id" not in cols
        assert "subscribe" not in cols
        assert len(cols) > 0


class TestCategoricalFeatures:
    def test_excludes_id_and_target(self):
        cats = get_categorical_features()
        for c in cats:
            assert c not in ("id", "subscribe")


class TestNumericFeatures:
    def test_excludes_id_and_target(self):
        nums = get_numeric_features()
        for n in nums:
            assert n not in ("id", "subscribe")
