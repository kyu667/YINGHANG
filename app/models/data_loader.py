import os

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
TARGET_COL = "subscribe"
MISSING_MARKERS = ["unknown", "nonexistent"]


def _resolve_data_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def _replace_missing(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].replace(MISSING_MARKERS, pd.NA)
    return df


def load_train_data() -> pd.DataFrame:
    path = _resolve_data_path("train.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Training data not found: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Training data is empty")
    return _replace_missing(df)


def load_test_data() -> pd.DataFrame:
    path = _resolve_data_path("test.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Test data not found: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Test data is empty")
    return _replace_missing(df)


def get_feature_columns() -> list[str]:
    df = load_train_data()
    exclude = ["id", TARGET_COL]
    return [c for c in df.columns if c not in exclude]


def get_categorical_features() -> list[str]:
    df = load_train_data()
    exclude = ["id", TARGET_COL]
    return [c for c in df.select_dtypes(include="object").columns if c not in exclude]


def get_numeric_features() -> list[str]:
    df = load_train_data()
    exclude = ["id", TARGET_COL]
    return [c for c in df.select_dtypes(include="number").columns if c not in exclude]
