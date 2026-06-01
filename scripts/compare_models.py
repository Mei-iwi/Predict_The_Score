from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLE_DIR = PROJECT_ROOT / "reports" / "tables"

TABLE_DIR.mkdir(parents=True, exist_ok=True)

TEST_SIZE = 0.2
RANDOM_STATE = 42


def load_data() -> tuple[pd.DataFrame, dict]:
    """Đọc dữ liệu sạch và danh sách scenario để so sánh."""
    data_path = PROCESSED_DIR / "student_performance_clean.csv"
    config_path = PROCESSED_DIR / "feature_config.json"

    if not data_path.exists():
        raise FileNotFoundError(f"Missing clean data file: {data_path}")
    if not config_path.exists():
        raise FileNotFoundError(f"Missing feature config file: {config_path}")

    return pd.read_csv(data_path), json.loads(config_path.read_text(encoding="utf-8"))


def compute_metrics(y_true: pd.Series, y_pred) -> dict[str, float]:
    """Tính MAE, MSE, RMSE và R2 cho từng scenario."""
    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": mse,
        "rmse": float(mse**0.5),
        "r2": float(r2_score(y_true, y_pred)),
    }


def train_linear_regression(df: pd.DataFrame, target: str, scenario: str, feature_names: list[str]) -> tuple[dict, list[dict]]:
    """Train LinearRegression cho một scenario và trả metrics cùng coefficients."""
    X = df[feature_names]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    metrics = compute_metrics(y_test, model.predict(X_test))
    row = {
        "scenario": scenario,
        "model_name": "LinearRegression",
        "feature_count": len(feature_names),
        "features": ", ".join(feature_names),
        **metrics,
    }

    coefficient_rows = [
        {
            "scenario": scenario,
            "model_name": "LinearRegression",
            "feature": name,
            "coefficient": float(coef),
        }
        for name, coef in zip(feature_names, model.coef_)
    ]
    coefficient_rows.append(
        {
            "scenario": scenario,
            "model_name": "LinearRegression",
            "feature": "intercept",
            "coefficient": float(model.intercept_),
        }
    )

    return row, coefficient_rows


def main() -> int:
    df, config = load_data()
    target = config.get("target", "G3")
    scenarios = config.get("scenarios", {})
    scenario_names = ["web_minimal", "early_warning", "reference"]

    comparison_rows = []
    coefficient_rows = []

    # So sánh từ form web tối giản đến bộ feature tham chiếu nhiều thông tin hơn.
    for scenario in scenario_names:
        if scenario not in scenarios:
            continue
        row, rows = train_linear_regression(df, target, scenario, scenarios[scenario])
        comparison_rows.append(row)
        coefficient_rows.extend(rows)

    if len(comparison_rows) < 2:
        raise ValueError("At least two scenarios are required for model comparison.")

    comparison_df = pd.DataFrame(comparison_rows).sort_values(["rmse", "mae"])
    best = comparison_df.iloc[0].to_dict()

    comparison_csv = TABLE_DIR / "model_comparison.csv"
    comparison_json = TABLE_DIR / "model_comparison.json"
    coefficients_csv = TABLE_DIR / "model_coefficients.csv"

    comparison_df.to_csv(comparison_csv, index=False)
    pd.DataFrame(coefficient_rows).to_csv(coefficients_csv, index=False)
    comparison_json.write_text(
        json.dumps(
            {
                "target": target,
                "test_size": TEST_SIZE,
                "random_state": RANDOM_STATE,
                "best_scenario": best["scenario"],
                "explanation": "Lower MAE/RMSE means smaller prediction error. Higher R2 means the model explains more score variation.",
                "results": comparison_df.to_dict(orient="records"),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved model comparison CSV: {comparison_csv}")
    print(f"Saved model comparison JSON: {comparison_json}")
    print(f"Saved LinearRegression coefficients: {coefficients_csv}")
    print(f"Best scenario by RMSE: {best['scenario']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
