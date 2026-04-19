from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"
TABLE_DIR = REPORT_DIR / "tables"
FIG_DIR = REPORT_DIR / "figures"
ARTIFACT_DIR = PROJECT_ROOT / "ml-service" / "artifacts"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def load_processed_data() -> tuple[pd.DataFrame, dict]:
    data_path = PROCESSED_DIR / "student_performance_clean.csv"
    feature_config_path = PROCESSED_DIR / "feature_config.json"
    if not data_path.exists():
        raise FileNotFoundError(f"Thiếu file dữ liệu sạch: {data_path}")
    if not feature_config_path.exists():
        raise FileNotFoundError(f"Thiếu cấu hình biến: {feature_config_path}")

    df = pd.read_csv(data_path)
    feature_config = json.loads(feature_config_path.read_text(encoding="utf-8"))
    return df, feature_config


def compute_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict[str, float]:
    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": mse,
        "rmse": float(mse ** 0.5),
        "r2": float(r2_score(y_true, y_pred)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Huấn luyện mô hình hồi quy tuyến tính cho Student Performance.")
    parser.add_argument(
        "--scenario",
        choices=["reference", "early_warning", "web_minimal"],
        default="web_minimal",
        help="Bộ biến dùng để train model.",
    )
    parser.add_argument("--test-size", type=float, default=0.2, help="Tỷ lệ test set.")
    parser.add_argument("--random-state", type=int, default=42, help="Random state cho train/test split.")
    args = parser.parse_args()

    df, feature_config = load_processed_data()
    target = feature_config.get("target", "G3")
    scenarios = feature_config.get("scenarios", {})
    if args.scenario not in scenarios:
        raise ValueError(f"Không tìm thấy scenario '{args.scenario}' trong feature_config.json")

    feature_names = scenarios[args.scenario]
    missing_cols = [col for col in feature_names + [target] if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dữ liệu thiếu các cột cần thiết: {missing_cols}")

    X = df[feature_names].copy()
    y = df[target].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    train_metrics = compute_metrics(y_train, pd.Series(train_pred))
    test_metrics = compute_metrics(y_test, pd.Series(test_pred))

    created_at = datetime.now(timezone.utc).isoformat()

    bundle = {
        "model": model,
        "scenario": args.scenario,
        "feature_names": feature_names,
        "target": target,
        "test_size": args.test_size,
        "random_state": args.random_state,
        "created_at": created_at,
        "test_indices": X_test.index.tolist(),
        "train_indices": X_train.index.tolist(),
        "metrics": {
            "train": train_metrics,
            "test": test_metrics,
        },
    }

    scenario_model_path = ARTIFACT_DIR / f"model_{args.scenario}.joblib"
    default_model_path = ARTIFACT_DIR / "model.joblib"
    joblib.dump(bundle, scenario_model_path)
    joblib.dump(bundle, default_model_path)

    metrics_path = TABLE_DIR / f"metrics_{args.scenario}.json"
    metrics_payload = {
        "scenario": args.scenario,
        "feature_names": feature_names,
        "target": target,
        "rows_used": int(len(df)),
        "created_at": created_at,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "coefficients": {name: float(coef) for name, coef in zip(feature_names, model.coef_)},
        "intercept": float(model.intercept_),
    }
    metrics_path.write_text(json.dumps(metrics_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    predictions_df = pd.DataFrame({
        "index": X_test.index,
        "actual_G3": y_test.values,
        "predicted_G3": test_pred,
    }).sort_values("index")
    predictions_path = TABLE_DIR / f"predictions_{args.scenario}.csv"
    predictions_df.to_csv(predictions_path, index=False)

    print(f"Đã lưu model theo scenario: {scenario_model_path}")
    print(f"Đã cập nhật model mặc định: {default_model_path}")
    print(f"Đã lưu metrics: {metrics_path}")
    print(f"Đã lưu dự đoán test set: {predictions_path}")
    print("\nTest metrics:")
    for key, value in test_metrics.items():
        print(f"- {key}: {value:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
