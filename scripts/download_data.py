from __future__ import annotations

import argparse
import ssl
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile

# scripts/download_data.py -> parents[1] là thư mục gốc project Predict_the_score/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZIP_PATH = PROJECT_ROOT / "data" / "raw" / "student.zip"
DEFAULT_EXTRACT_DIR = PROJECT_ROOT / "data" / "raw"

UCI_DATASET_URLS = [
    "https://archive.ics.uci.edu/static/public/320/student.zip",
    "https://archive.ics.uci.edu/static/public/320/student%2Bperformance.zip",
    "https://archive.ics.uci.edu/static/public/320/student+performance.zip",
]

HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUIRED_FILES = {"student-mat.csv", "student-por.csv", "student.txt"}


def fetch_bytes(url: str, timeout: int = 60) -> bytes:
    request = Request(url, headers=HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read()
    except ssl.SSLCertVerificationError:
        # Fallback cho môi trường lỗi CA bundle
        context = ssl._create_unverified_context()
        with urlopen(request, context=context, timeout=timeout) as response:
            return response.read()


def download_zip(urls: list[str], output_path: Path, retries: int = 3, delay_seconds: int = 3) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None

    for url in urls:
        for attempt in range(1, retries + 1):
            try:
                print(f"Đang tải từ: {url} (lần {attempt}/{retries})")
                data = fetch_bytes(url)
                output_path.write_bytes(data)
                print(f"Đã lưu file zip: {output_path}")
                return output_path
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                last_error = exc
                print(f"Tải thất bại: {exc}")
                if attempt < retries:
                    time.sleep(delay_seconds)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                print(f"Lỗi không mong đợi: {exc}")
                break

    raise RuntimeError(f"Không thể tải dataset sau nhiều lần thử. Lỗi cuối: {last_error}")


def validate_zip(zip_path: Path) -> None:
    try:
        with ZipFile(zip_path, "r") as archive:
            names = set(archive.namelist())
    except BadZipFile as exc:
        raise RuntimeError(f"File zip không hợp lệ: {zip_path}") from exc

    missing = REQUIRED_FILES - names
    if missing:
        raise RuntimeError(
            "Dataset tải về không đúng cấu trúc mong đợi. "
            f"Thiếu file: {sorted(missing)}"
        )


def extract_zip(zip_path: Path, extract_dir: Path) -> None:
    extract_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "r") as archive:
        archive.extractall(extract_dir)
    print(f"Đã giải nén vào: {extract_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tải bộ dữ liệu Student Performance từ UCI và giải nén theo cấu trúc dự án hiện tại."
    )
    parser.add_argument(
        "--zip-path",
        type=Path,
        default=DEFAULT_ZIP_PATH,
        help="Đường dẫn lưu file zip tải về. Mặc định: data/raw/student.zip",
    )
    parser.add_argument(
        "--extract-dir",
        type=Path,
        default=DEFAULT_EXTRACT_DIR,
        help="Thư mục giải nén dữ liệu. Mặc định: data/raw/",
    )
    parser.add_argument(
        "--skip-download-if-exists",
        action="store_true",
        help="Nếu zip đã tồn tại thì bỏ qua bước tải lại.",
    )
    args = parser.parse_args()

    try:
        if args.skip_download_if_exists and args.zip_path.exists():
            print(f"Đã có file zip sẵn: {args.zip_path}")
        else:
            download_zip(UCI_DATASET_URLS, args.zip_path)

        validate_zip(args.zip_path)
        extract_zip(args.zip_path, args.extract_dir)

        print("\nCác file chính sau khi giải nén:")
        for name in sorted(REQUIRED_FILES):
            print(f"- {args.extract_dir / name}")

        print("\nXong. Tiếp theo có thể chạy scripts/build_dataset.py để tiền xử lý dữ liệu.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
