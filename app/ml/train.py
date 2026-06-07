import argparse
import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

from app.models.data_loader import load_train_data

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoders.pkl")
RANDOM_STATE = 42


def _encode_categorical(
    df: pd.DataFrame, encoders: dict | None = None
) -> tuple[pd.DataFrame, dict]:
    df = df.copy()
    if encoders is None:
        encoders = {}
    for col in df.select_dtypes(include="object").columns:
        if col not in encoders:
            le = LabelEncoder()
            df[col] = df[col].astype(str)
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
        else:
            le = encoders[col]
            df[col] = df[col].astype(str)
            # map unseen values to a fallback
            known = set(le.classes_)
            df[col] = df[col].apply(lambda x: x if x in known else le.classes_[0])
            df[col] = le.transform(df[col])
    return df, encoders


def train_model():
    print("Loading training data...")
    df = load_train_data()
    df = df.drop(columns=["id"], errors="ignore")

    target = "subscribe"
    X = df.drop(columns=[target])
    y = df[target]

    print(f"Training samples: {len(X)}, features: {X.shape[1]}")

    X_encoded, encoders = _encode_categorical(X)

    X_train, X_val, y_train, y_val = train_test_split(
        X_encoded, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200, max_depth=15, random_state=RANDOM_STATE, n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]

    acc = accuracy_score(y_val, y_pred)
    auc_score = roc_auc_score((y_val == "yes").astype(int), y_proba)
    report = classification_report(y_val, y_pred)

    print(f"\nAccuracy: {acc:.4f}")
    print(f"AUC: {auc_score:.4f}")
    print(f"\nClassification Report:\n{report}")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(
        model, X_encoded, (y == "yes").astype(int), cv=cv, scoring="roc_auc"
    )
    print(f"5-Fold CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(ENCODER_PATH, "wb") as f:
        pickle.dump({"encoders": encoders, "feature_names": list(X.columns)}, f)

    print(f"\nModel saved: {MODEL_PATH}")
    print(f"Encoders saved: {ENCODER_PATH}")
    return model, encoders


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", action="store_true", help="Skip training if model exists")
    args = parser.parse_args()

    if args.skip and os.path.exists(MODEL_PATH):
        print("Model already exists. Skipping training.")
        return

    train_model()


if __name__ == "__main__":
    main()
