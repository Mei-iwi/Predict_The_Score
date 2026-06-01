from pathlib import Path

import joblib

ARTIFACT_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "model.joblib"
_model_bundle = None


def load_model_bundle():
    """Lazy load model để API không đọc file joblib lặp lại ở mỗi request."""
    global _model_bundle
    if _model_bundle is None:
        if not ARTIFACT_PATH.exists():
            raise FileNotFoundError(f"Model artifact was not found: {ARTIFACT_PATH}")
        _model_bundle = joblib.load(ARTIFACT_PATH)
    return _model_bundle


def get_model_info() -> dict:
    """Chuẩn hóa metadata model cho endpoint /model-info."""
    bundle = load_model_bundle()
    scenario = bundle.get("scenario", "unknown")
    model_name = bundle.get("model_name", "LinearRegression")

    return {
        "model_name": f"{model_name}-{scenario}",
        "scenario": scenario,
        "feature_names": bundle.get("feature_names", []),
        "target": bundle.get("target", "G3"),
        "metrics": bundle.get("metrics"),
    }
