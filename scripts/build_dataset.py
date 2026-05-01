from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

import matplotlib.pyplot as plt
import pandas as pd

# scripts/build_dataset.py -> parents[1] là thư mục gốc project Predict_the_score/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"
FIG_DIR = REPORT_DIR / "figures"
TABLE_DIR = REPORT_DIR / "tables"

DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)

USE_COLS = [
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "schoolsup",
    "famsup",
    "internet",
    "higher",
    "traveltime",
    "G3",
]

NUMERIC_COLS = ["studytime", "failures", "absences", "G1", "G2", "traveltime", "G3"]
BINARY_COLS = ["schoolsup", "famsup", "internet", "higher"]

VALID_RANGES: dict[str, tuple[int, int]] = {
    "studytime": (1, 4),
    "failures": (0, 4),
    "absences": (0, 93),
    "G1": (0, 20),
    "G2": (0, 20),
    "traveltime": (1, 4),
    "G3": (0, 20),
}


def basename_in_zip(member_name: str) -> str:
    return PurePosixPath(member_name).name


def find_file_bytes_in_zip_bytes(zip_bytes: bytes, expected_name: str) -> bytes:
    """
    Tìm expected_name trong zip, kể cả zip lồng zip.
    Ví dụ:
    - student-mat.csv
    - student/student-mat.csv
    - outer.zip -> student.zip -> student-mat.csv
    """
    with ZipFile(BytesIO(zip_bytes), "r") as archive:
        names = archive.namelist()

        # 1. Tìm trực tiếp theo basename
        for name in names:
            if name.endswith("/"):
                continue

            if basename_in_zip(name) == expected_name:
                return archive.read(name)

        # 2. Tìm trong zip con
        for name in names:
            if name.endswith("/"):
                continue

            data = archive.read(name)

            if not data.startswith(b"PK"):
                continue

            try:
                return find_file_bytes_in_zip_bytes(data, expected_name)
            except (BadZipFile, KeyError):
                continue

    raise KeyError(f"Không tìm thấy '{expected_name}' trong zip.")


def load_csv_from_zip(zip_path: Path, member_name: str) -> pd.DataFrame:
    file_bytes = find_file_bytes_in_zip_bytes(zip_path.read_bytes(), member_name)
    return pd.read_csv(BytesIO(file_bytes), sep=";")


def find_raw_sources() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """Tìm student-mat.csv và student-por.csv theo cấu trúc project hiện tại.

    Ưu tiên:
    1) data/raw/student-mat.csv và data/raw/student-por.csv
    2) student_performance/student-mat.csv và student_performance/student-por.csv
    3) đọc trực tiếp từ student.zip trong project root hoặc data/raw
    """
    candidates = [
        (DATA_RAW_DIR / "student-mat.csv", DATA_RAW_DIR / "student-por.csv", "data/raw"),
        (PROJECT_ROOT / "student_performance" / "student-mat.csv", PROJECT_ROOT / "student_performance" / "student-por.csv", "student_performance/"),
        (PROJECT_ROOT / "student-mat.csv", PROJECT_ROOT / "student-por.csv", "project root"),
    ]

    for mat_path, por_path, label in candidates:
        if mat_path.exists() and por_path.exists():
            mat = pd.read_csv(mat_path, sep=";")
            por = pd.read_csv(por_path, sep=";")
            return mat, por, label

    zip_candidates = [
        DATA_RAW_DIR / "student.zip",
        PROJECT_ROOT / "student.zip",
        PROJECT_ROOT / "student_performance.zip",
    ]
    for zip_path in zip_candidates:
        if zip_path.exists():
            mat = load_csv_from_zip(zip_path, "student-mat.csv")
            por = load_csv_from_zip(zip_path, "student-por.csv")
            return mat, por, f"zip: {zip_path.name}"

    raise FileNotFoundError(
        "Không tìm thấy dữ liệu gốc. Hãy chạy scripts/download_data.py "
        "hoặc đặt student-mat.csv và student-por.csv vào data/raw/."
    )


def preprocess_student_performance() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    mat, por, source_label = find_raw_sources()

    mat = mat.copy()
    por = por.copy()
    mat["subject"] = "mat"
    por["subject"] = "por"

    raw_df = pd.concat([mat, por], ignore_index=True)
    raw_rows = len(raw_df)

    df = raw_df[USE_COLS + ["subject"]].copy()

    duplicate_rows_before = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    binary_map = {"yes": 1, "no": 0}
    invalid_binary_counts: dict[str, int] = {}
    for col in BINARY_COLS:
        invalid_binary_counts[col] = int((~df[col].isin(binary_map.keys())).sum())
        df[col] = df[col].map(binary_map)

    df["subject"] = df["subject"].map({"mat": 0, "por": 1})

    na_rows_after_cast = int(df.isna().any(axis=1).sum())
    invalid_na_rows = df[df.isna().any(axis=1)].copy()
    if not invalid_na_rows.empty:
        invalid_na_rows.to_csv(REPORT_DIR / "invalid_rows_after_cast.csv", index=False)

    df = df.dropna().reset_index(drop=True)

    range_mask = pd.Series(True, index=df.index)
    for col, (min_value, max_value) in VALID_RANGES.items():
        range_mask &= df[col].between(min_value, max_value)

    invalid_range_rows = df.loc[~range_mask].copy()
    invalid_range_count = int((~range_mask).sum())
    if invalid_range_count:
        invalid_range_rows.to_csv(REPORT_DIR / "invalid_rows_out_of_range.csv", index=False)

    df_clean = df.loc[range_mask].reset_index(drop=True)

    corr_cols = [
        "subject",
        "studytime",
        "failures",
        "absences",
        "G1",
        "G2",
        "schoolsup",
        "famsup",
        "internet",
        "higher",
        "traveltime",
        "G3",
    ]
    pearson_corr = df_clean[corr_cols].corr(method="pearson", numeric_only=True)

    audit = {
        "data_source": source_label,
        "raw_rows_combined": raw_rows,
        "rows_after_column_selection": len(raw_df[USE_COLS + ["subject"]]),
        "duplicate_rows_before_drop": duplicate_rows_before,
        "rows_after_drop_duplicates": int(len(raw_df[USE_COLS + ["subject"]].drop_duplicates())),
        "rows_with_na_after_type_cast": na_rows_after_cast,
        "rows_out_of_valid_ranges": invalid_range_count,
        "rows_after_cleaning": int(len(df_clean)),
        "columns_used": USE_COLS + ["subject"],
        "invalid_binary_counts_before_mapping": invalid_binary_counts,
        "valid_ranges": {k: {"min": v[0], "max": v[1]} for k, v in VALID_RANGES.items()},
    }

    return df_clean, pearson_corr, audit


def save_outputs(df_clean: pd.DataFrame, pearson_corr: pd.DataFrame, audit: dict) -> None:
    clean_path = DATA_PROCESSED_DIR / "student_performance_clean.csv"
    pearson_path = TABLE_DIR / "pearson_correlation.csv"
    audit_path = REPORT_DIR / "processing_audit.json"
    feature_config_path = DATA_PROCESSED_DIR / "feature_config.json"

    df_clean.to_csv(clean_path, index=False)
    pearson_corr.to_csv(pearson_path)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    feature_config = {
        "target": "G3",
        "scenarios": {
            "reference": [
                "subject",
                "studytime",
                "failures",
                "absences",
                "G1",
                "G2",
                "schoolsup",
                "famsup",
                "internet",
                "higher",
                "traveltime",
            ],
            "early_warning": [
                "subject",
                "studytime",
                "failures",
                "absences",
                "schoolsup",
                "famsup",
                "internet",
                "higher",
                "traveltime",
            ],
            "web_minimal": [
                "studytime",
                "failures",
                "absences",
                "schoolsup",
                "famsup",
                "internet",
            ],
        },
        "notes": [
            "reference: giữ G1 và G2 để so sánh độ chính xác.",
            "early_warning: bỏ G1 và G2 để phù hợp cảnh báo sớm.",
            "web_minimal: rút gọn cho form nhập liệu đơn giản trên giao diện hiện tại.",
        ],
    }
    feature_config_path.write_text(json.dumps(feature_config, ensure_ascii=False, indent=2), encoding="utf-8")

    plt.figure(figsize=(10, 8))
    image = plt.imshow(pearson_corr, interpolation="nearest")
    plt.colorbar(image)
    plt.xticks(range(len(pearson_corr.columns)), pearson_corr.columns, rotation=45, ha="right") # type: ignore
    plt.yticks(range(len(pearson_corr.index)), pearson_corr.index) # type: ignore
    plt.title("Heatmap tương quan Pearson")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pearson_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.hist(df_clean["absences"], bins=20)
    plt.title("Phân phối số buổi vắng học")
    plt.xlabel("absences")
    plt.ylabel("Tần suất")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "hist_absences.png", dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.scatter(df_clean["G2"], df_clean["G3"], alpha=0.6)
    plt.title("Quan hệ giữa G2 và G3")
    plt.xlabel("G2")
    plt.ylabel("G3")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "scatter_g2_g3.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Đã lưu dữ liệu sạch: {clean_path}")
    print(f"Đã lưu ma trận Pearson: {pearson_path}")
    print(f"Đã lưu audit xử lý: {audit_path}")
    print(f"Đã lưu cấu hình biến: {feature_config_path}")
    print(f"Đã lưu hình minh họa vào: {FIG_DIR}")


if __name__ == "__main__":
    clean_df, corr_df, audit_info = preprocess_student_performance()
    save_outputs(clean_df, corr_df, audit_info)
