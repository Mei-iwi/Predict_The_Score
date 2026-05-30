from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

import matplotlib.pyplot as plt
import pandas as pd

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

VALID_RANGES = {
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
    """Find a file in a zip archive, including nested zip archives."""
    with ZipFile(BytesIO(zip_bytes), "r") as archive:
        for name in archive.namelist():
            if not name.endswith("/") and basename_in_zip(name) == expected_name:
                return archive.read(name)

        for name in archive.namelist():
            if name.endswith("/"):
                continue

            data = archive.read(name)
            if not data.startswith(b"PK"):
                continue

            try:
                return find_file_bytes_in_zip_bytes(data, expected_name)
            except (BadZipFile, KeyError):
                continue

    raise KeyError(f"Could not find {expected_name} in zip archive.")


def load_csv_from_zip(zip_path: Path, member_name: str) -> pd.DataFrame:
    file_bytes = find_file_bytes_in_zip_bytes(zip_path.read_bytes(), member_name)
    return pd.read_csv(BytesIO(file_bytes), sep=";")


def find_raw_sources() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """Find student-mat.csv and student-por.csv in common project locations."""
    csv_candidates = [
        (DATA_RAW_DIR / "student-mat.csv", DATA_RAW_DIR / "student-por.csv", "data/raw"),
        (
            PROJECT_ROOT / "student_performance" / "student-mat.csv",
            PROJECT_ROOT / "student_performance" / "student-por.csv",
            "student_performance",
        ),
        (PROJECT_ROOT / "student-mat.csv", PROJECT_ROOT / "student-por.csv", "project root"),
    ]

    for mat_path, por_path, label in csv_candidates:
        if mat_path.exists() and por_path.exists():
            return pd.read_csv(mat_path, sep=";"), pd.read_csv(por_path, sep=";"), label

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
        "Raw data was not found. Run scripts/download_data.py or put "
        "student-mat.csv and student-por.csv in data/raw/."
    )


def preprocess_student_performance() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    mat, por, source_label = find_raw_sources()

    mat = mat.copy()
    por = por.copy()
    mat["subject"] = "mat"
    por["subject"] = "por"

    raw_df = pd.concat([mat, por], ignore_index=True)
    original_rows = len(raw_df)

    selected_columns = USE_COLS + ["subject"]
    df = raw_df[selected_columns].copy()
    rows_after_selection = len(df)

    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)
    rows_after_dropping_duplicates = len(df)

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    binary_map = {"yes": 1, "no": 0}
    invalid_binary_counts = {}
    for col in BINARY_COLS:
        invalid_binary_counts[col] = int((~df[col].isin(binary_map.keys())).sum())
        df[col] = df[col].map(binary_map)

    df["subject"] = df["subject"].map({"mat": 0, "por": 1})

    missing_rows = int(df.isna().any(axis=1).sum()) # type: ignore
    missing_rows_path = REPORT_DIR / "invalid_rows_after_cast.csv"
    if missing_rows:
        df[df.isna().any(axis=1)].to_csv(missing_rows_path, index=False) # type: ignore
    elif missing_rows_path.exists():
        missing_rows_path.unlink()

    df = df.dropna().reset_index(drop=True)

    valid_range_mask = pd.Series(True, index=df.index)
    for col, (min_value, max_value) in VALID_RANGES.items():
        valid_range_mask &= df[col].between(min_value, max_value)

    invalid_range_rows = int((~valid_range_mask).sum())
    invalid_range_path = REPORT_DIR / "invalid_rows_out_of_range.csv"
    if invalid_range_rows:
        df.loc[~valid_range_mask].to_csv(invalid_range_path, index=False)
    elif invalid_range_path.exists():
        invalid_range_path.unlink()

    df_clean = df.loc[valid_range_mask].reset_index(drop=True)

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
        "dataset_source_name": f"UCI Student Performance ({source_label})",
        "selected_columns": selected_columns,
        "original_rows": original_rows,
        "rows_after_selecting_columns": rows_after_selection,
        "duplicate_rows": duplicate_rows,
        "rows_after_dropping_duplicates": rows_after_dropping_duplicates,
        "missing_or_invalid_rows": missing_rows + invalid_range_rows,
        "rows_after_cleaning": int(len(df_clean)),
        "yes_no_encoding": "yes/no values are encoded as 1/0.",
        "rows_with_missing_values_after_type_cast": missing_rows,
        "rows_out_of_valid_ranges": invalid_range_rows,
        "invalid_binary_counts_before_mapping": invalid_binary_counts,
        "valid_ranges": {name: {"min": values[0], "max": values[1]} for name, values in VALID_RANGES.items()},
    }

    return df_clean, pearson_corr, audit


def save_feature_config() -> None:
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
            "reference: includes G1 and G2 for accuracy comparison.",
            "early_warning: removes G1 and G2 for earlier prediction.",
            "web_minimal: uses only fields available in the current web form.",
        ],
    }
    (DATA_PROCESSED_DIR / "feature_config.json").write_text(
        json.dumps(feature_config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_figures(df_clean: pd.DataFrame, pearson_corr: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 8))
    image = plt.imshow(pearson_corr, interpolation="nearest", cmap="viridis")
    plt.colorbar(image)
    plt.xticks(range(len(pearson_corr.columns)), pearson_corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(pearson_corr.index)), pearson_corr.index)
    plt.title("Pearson correlation heatmap")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pearson_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.hist(df_clean["absences"], bins=20)
    plt.title("Distribution of absences")
    plt.xlabel("absences")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "hist_absences.png", dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.scatter(df_clean["G2"], df_clean["G3"], alpha=0.6)
    plt.title("Relationship between G2 and G3")
    plt.xlabel("G2")
    plt.ylabel("G3")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "scatter_g2_g3.png", dpi=300, bbox_inches="tight")
    plt.close()


def save_outputs(df_clean: pd.DataFrame, pearson_corr: pd.DataFrame, audit: dict) -> None:
    clean_path = DATA_PROCESSED_DIR / "student_performance_clean.csv"
    pearson_path = TABLE_DIR / "pearson_correlation.csv"
    audit_path = REPORT_DIR / "processing_audit.json"

    df_clean.to_csv(clean_path, index=False)
    pearson_corr.to_csv(pearson_path)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    save_feature_config()
    save_figures(df_clean, pearson_corr)

    print(f"Saved clean data: {clean_path}")
    print(f"Saved processing audit: {audit_path}")
    print(f"Saved Pearson correlation table: {pearson_path}")
    print(f"Saved report figures in: {FIG_DIR}")


if __name__ == "__main__":
    clean_df, corr_df, audit_info = preprocess_student_performance()
    save_outputs(clean_df, corr_df, audit_info)
