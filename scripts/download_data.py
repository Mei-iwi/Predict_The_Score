from __future__ import annotations

import argparse
import ssl
import sys
import time
from io import BytesIO
from pathlib import Path, PurePosixPath
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

def basename_in_zip(member_name: str) -> str:
    return PurePosixPath(member_name).name


def read_required_files_from_zip_bytes(zip_bytes: bytes, level: int = 0) -> dict[str, bytes]:
    """
    Đọc các file cần thiết trong zip, kể cả trường hợp zip lồng zip.
    Trả về dict: {filename: file_content_bytes}
    """
    found: dict[str, bytes] = {}

    try:
        with ZipFile(BytesIO(zip_bytes), "r") as archive:
            names = archive.namelist()

            # 1. Tìm trực tiếp theo basename, ví dụ student/student-mat.csv vẫn nhận student-mat.csv
            for name in names:
                if name.endswith("/"):
                    continue

                base_name = basename_in_zip(name)

                if base_name in REQUIRED_FILES and base_name not in found:
                    found[base_name] = archive.read(name)

            # 2. Nếu còn thiếu, tìm tiếp trong các file zip con
            missing = REQUIRED_FILES - set(found.keys())

            if missing:
                for name in names:
                    if name.endswith("/"):
                        continue

                    data = archive.read(name)

                    # File zip thường bắt đầu bằng PK
                    if not data.startswith(b"PK"):
                        continue

                    try:
                        nested_found = read_required_files_from_zip_bytes(data, level + 1)

                        for required_name in missing:
                            if required_name in nested_found and required_name not in found:
                                found[required_name] = nested_found[required_name]

                        missing = REQUIRED_FILES - set(found.keys())

                        if not missing:
                            break

                    except BadZipFile:
                        continue

    except BadZipFile:
        return found

    return found


def read_required_files_from_zip_path(zip_path: Path) -> dict[str, bytes]:
    return read_required_files_from_zip_bytes(zip_path.read_bytes())


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
        found = read_required_files_from_zip_path(zip_path)
    except BadZipFile as exc:
        raise RuntimeError(f"File zip không hợp lệ: {zip_path}") from exc

    missing = REQUIRED_FILES - set(found.keys())

    if missing:
        with ZipFile(zip_path, "r") as archive:
            sample_names = archive.namelist()[:30]

        raise RuntimeError(
            "Dataset tải về không đúng cấu trúc mong đợi. "
            f"Thiếu file: {sorted(missing)}. "
            f"Một số file cấp ngoài trong zip: {sample_names}"
        )


def extract_zip(zip_path: Path, extract_dir: Path) -> None:
    """
    Giải nén đúng 3 file cần thiết ra data/raw/,
    kể cả khi chúng nằm trong zip con.
    """
    extract_dir.mkdir(parents=True, exist_ok=True)

    found = read_required_files_from_zip_path(zip_path)
    missing = REQUIRED_FILES - set(found.keys())

    if missing:
        raise RuntimeError(f"Không thể giải nén vì thiếu file: {sorted(missing)}")

    for filename, content in found.items():
        output_path = extract_dir / filename
        output_path.write_bytes(content)
        print(f"Đã ghi: {output_path}")

    print(f"Đã giải nén dữ liệu cần thiết vào: {extract_dir}")


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
