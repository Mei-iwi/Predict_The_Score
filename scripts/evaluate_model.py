from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"
TABLE_DIR = REPORT_DIR / "tables"
FIG_DIR = REPORT_DIR / "figures"
ARTIFACT_DIR = PROJECT_ROOT / "ml-service" / "artifacts"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


def compute_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict[str, float]:
    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": mse,
        "rmse": float(mse ** 0.5),
        "r2": float(r2_score(y_true, y_pred)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Đánh giá model đã train và sinh hình minh họa.")
    parser.add_argument(
        "--model-path",
        type=Path,
        default=ARTIFACT_DIR / "model.joblib",
        help="Đường dẫn tới file model bundle.",
    )
    args = parser.parse_args()

    if not args.model_path.exists():
        raise FileNotFoundError(f"Không tìm thấy model: {args.model_path}")

    processed_path = PROCESSED_DIR / "student_performance_clean.csv"
    if not processed_path.exists():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu sạch: {processed_path}")

    df = pd.read_csv(processed_path)
    bundle = joblib.load(args.model_path)

    model = bundle["model"]
    feature_names = bundle["feature_names"]
    target = bundle.get("target", "G3")
    scenario = bundle.get("scenario", "unknown")
    test_indices = bundle.get("test_indices", [])

    if not test_indices:
        raise ValueError("Model bundle không có test_indices để đánh giá lại.")

    test_df = df.loc[test_indices].copy()
    X_test = test_df[feature_names]
    y_test = test_df[target]
    y_pred = model.predict(X_test)

    metrics = compute_metrics(y_test, pd.Series(y_pred))
    evaluation_payload = {
        "scenario": scenario,
        "feature_names": feature_names,
        "target": target,
        "model_path": str(args.model_path),
        "rows_in_test_set": int(len(test_df)),
        "metrics": metrics,
    }

    evaluation_path = TABLE_DIR / f"evaluation_{scenario}.json"
    evaluation_path.write_text(json.dumps(evaluation_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    detail_df = pd.DataFrame({
        "index": test_df.index,
        "actual_G3": y_test.values,
        "predicted_G3": y_pred,
        "abs_error": (y_test.values - y_pred).astype(float).__abs__(),
    }).sort_values("index")
    detail_path = TABLE_DIR / f"evaluation_detail_{scenario}.csv"
    detail_df.to_csv(detail_path, index=False)

    plt.figure(figsize=(6, 5))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.xlabel("Giá trị thật G3")
    plt.ylabel("Giá trị dự đoán G3")
    plt.title(f"Actual vs Predicted - {scenario}")
    min_val = min(float(y_test.min()), float(pd.Series(y_pred).min()))
    max_val = max(float(y_test.max()), float(pd.Series(y_pred).max()))
    plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")
    plt.tight_layout()
    fig_path = FIG_DIR / f"actual_vs_predicted_{scenario}.png"
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Đã lưu file đánh giá: {evaluation_path}")
    print(f"Đã lưu chi tiết dự đoán: {detail_path}")
    print(f"Đã lưu hình actual-vs-predicted: {fig_path}")
    print("\nMetrics:")
    for key, value in metrics.items():
        print(f"- {key}: {value:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
