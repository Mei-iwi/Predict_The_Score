from pathlib import Path
import joblib

ARTIFACT_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "model.joblib"
_model_bundle = None

def load_model_bundle():
    global _model_bundle
    if _model_bundle is None:
        if not ARTIFACT_PATH.exists():
            raise FileNotFoundError(f"Không tìm thấy model artifact: {ARTIFACT_PATH}")
        _model_bundle = joblib.load(ARTIFACT_PATH)
    return _model_bundle


