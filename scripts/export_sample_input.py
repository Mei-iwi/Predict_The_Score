from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SAMPLES_DIR = PROJECT_ROOT / "data" / "samples"
ARTIFACT_DIR = PROJECT_ROOT / "ml-service" / "artifacts"

SAMPLES_DIR.mkdir(parents=True, exist_ok=True)


def get_active_features(default_scenario: str = "web_minimal") -> tuple[list[str], str]:
    model_path = ARTIFACT_DIR / "model.joblib"
    if model_path.exists():
        bundle = joblib.load(model_path)
        return bundle["feature_names"], bundle.get("scenario", default_scenario)

    feature_config_path = PROCESSED_DIR / "feature_config.json"
    if not feature_config_path.exists():
        raise FileNotFoundError("Không tìm thấy feature_config.json để sinh sample_input.csv")

    feature_config = json.loads(feature_config_path.read_text(encoding="utf-8"))
    scenarios = feature_config.get("scenarios", {})
    if default_scenario not in scenarios:
        raise ValueError(f"Không tìm thấy scenario mặc định '{default_scenario}'")
    return scenarios[default_scenario], default_scenario


def main() -> int:
    parser = argparse.ArgumentParser(description="Xuất dữ liệu mẫu để test frontend/backend.")
    parser.add_argument("--n", type=int, default=5, help="Số dòng mẫu muốn xuất.")
    parser.add_argument(
        "--scenario",
        choices=["reference", "early_warning", "web_minimal"],
        default=None,
        help="Chọn scenario cụ thể. Nếu bỏ trống, script sẽ ưu tiên model đang active.",
    )
    args = parser.parse_args()

    processed_path = PROCESSED_DIR / "student_performance_clean.csv"
    feature_config_path = PROCESSED_DIR / "feature_config.json"
    if not processed_path.exists():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu sạch: {processed_path}")

    df = pd.read_csv(processed_path)

    if args.scenario:
        if not feature_config_path.exists():
            raise FileNotFoundError(f"Không tìm thấy cấu hình biến: {feature_config_path}")
        feature_config = json.loads(feature_config_path.read_text(encoding="utf-8"))
        feature_names = feature_config["scenarios"][args.scenario]
        scenario = args.scenario
    else:
        feature_names, scenario = get_active_features()

    sample_df = df[feature_names].head(args.n).copy()
    csv_path = SAMPLES_DIR / "sample_input.csv"
    json_path = SAMPLES_DIR / "sample_input.json"

    sample_df.to_csv(csv_path, index=False)
    json_path.write_text(sample_df.to_json(orient="records", force_ascii=False, indent=2), encoding="utf-8")

    print(f"Đã xuất sample_input theo scenario '{scenario}': {csv_path}")
    print(f"Đã xuất JSON mẫu: {json_path}")
    print("\nCác cột đã xuất:")
    for col in feature_names:
        print(f"- {col}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
