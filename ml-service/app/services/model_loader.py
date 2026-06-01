from pathlib import Path

import joblib

ARTIFACT_DIR = Path(__file__).resolve().parents[2] / "artifacts"
DEFAULT_SCENARIO = "web_minimal"
SCENARIO_MODEL_PATHS = {
    "web_minimal": ARTIFACT_DIR / "model_web_minimal.joblib",
    "early_warning": ARTIFACT_DIR / "model_early_warning.joblib",
    "reference": ARTIFACT_DIR / "model_reference.joblib",
}
FALLBACK_MODEL_PATH = ARTIFACT_DIR / "model.joblib"
_model_cache = {}


def get_model_path(scenario: str) -> Path:
    """Chọn file model theo scenario, giữ model.joblib làm fallback cho web_minimal."""
    if scenario not in SCENARIO_MODEL_PATHS:
        raise ValueError(f"Scenario không hợp lệ: {scenario}")
    path = SCENARIO_MODEL_PATHS[scenario]
    if scenario == DEFAULT_SCENARIO and not path.exists():
        return FALLBACK_MODEL_PATH
    return path


def load_model_bundle(scenario: str = DEFAULT_SCENARIO):
    """Lazy load model theo scenario để API không đọc file joblib lặp lại ở mỗi request."""
    path = get_model_path(scenario)
    cache_key = str(path)
    if cache_key not in _model_cache:
        if not path.exists():
            raise FileNotFoundError(
                f"Model artifact for scenario '{scenario}' was not found: {path}. "
                f"Run scripts/train_model.py --scenario {scenario}."
            )
        _model_cache[cache_key] = joblib.load(path)
    return _model_cache[cache_key]


def get_available_scenarios() -> list[str]:
    """Liệt kê scenario đã có file model artifact trong thư mục artifacts."""
    available = []
    for scenario, path in SCENARIO_MODEL_PATHS.items():
        if path.exists() or (scenario == DEFAULT_SCENARIO and FALLBACK_MODEL_PATH.exists()):
            available.append(scenario)
    return available


def get_model_info() -> dict:
    """Chuẩn hóa metadata model cho endpoint /model-info."""
    bundle = load_model_bundle(DEFAULT_SCENARIO)
    scenario = bundle.get("scenario", "unknown")
    model_name = bundle.get("model_name", "LinearRegression")
    available = get_available_scenarios()

    return {
        "model_name": f"{model_name}-{scenario}",
        "scenario": scenario,
        "feature_names": bundle.get("feature_names", []),
        "target": bundle.get("target", "G3"),
        "metrics": bundle.get("metrics"),
        "available_scenarios": available,
        "missing_scenarios": [name for name in SCENARIO_MODEL_PATHS if name not in available],
    }
