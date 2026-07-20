from __future__ import annotations

import logging
import shutil
import zipfile
from http.client import IncompleteRead
from pathlib import Path
from urllib.error import URLError
from urllib.request import ProxyHandler, Request, build_opener

from .config import ARCHIVE_NAME, DATASET_URL, EXTRACTED_DIR_NAME, RAW_DATA_DIR

LOGGER = logging.getLogger(__name__)
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
MAX_DOWNLOAD_RETRIES = 8


def download_dataset(force_download: bool = False) -> Path:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = RAW_DATA_DIR / ARCHIVE_NAME

    if archive_path.exists() and not force_download:
        try:
            with zipfile.ZipFile(archive_path, "r") as zip_file:
                zip_file.namelist()
            LOGGER.info("Using cached dataset archive at %s", archive_path)
            return archive_path
        except zipfile.BadZipFile:
            LOGGER.warning("Cached dataset archive is invalid. Re-downloading %s", archive_path)
            archive_path.unlink()

    LOGGER.info("Downloading HHAR dataset archive from %s", DATASET_URL)
    opener = build_opener(ProxyHandler({}))

    for attempt in range(1, MAX_DOWNLOAD_RETRIES + 1):
        downloaded_bytes = archive_path.stat().st_size if archive_path.exists() else 0
        request = Request(DATASET_URL)
        if downloaded_bytes > 0:
            request.add_header("Range", f"bytes={downloaded_bytes}-")
            LOGGER.info("Resuming dataset download from byte %s (attempt %s)", downloaded_bytes, attempt)
        else:
            LOGGER.info("Starting dataset download attempt %s", attempt)

        try:
            with archive_path.open("ab" if downloaded_bytes > 0 else "wb") as file_handle:
                with opener.open(request, timeout=180) as response:
                    while True:
                        chunk = response.read(DOWNLOAD_CHUNK_SIZE)
                        if not chunk:
                            break
                        file_handle.write(chunk)

            with zipfile.ZipFile(archive_path, "r") as zip_file:
                zip_file.testzip()
            break
        except (IncompleteRead, URLError, OSError, zipfile.BadZipFile) as exc:
            LOGGER.warning("Dataset download attempt %s failed: %s", attempt, exc)
            if attempt == MAX_DOWNLOAD_RETRIES:
                raise
    else:
        raise RuntimeError("Dataset download failed after maximum retries.")

    with zipfile.ZipFile(archive_path, "r") as zip_file:
        zip_file.namelist()

    LOGGER.info("Dataset archive saved to %s", archive_path)
    return archive_path


def extract_dataset(archive_path: Path, force_extract: bool = False) -> Path:
    extract_dir = RAW_DATA_DIR / EXTRACTED_DIR_NAME

    if extract_dir.exists() and not force_extract:
        LOGGER.info("Using cached extracted dataset at %s", extract_dir)
        return extract_dir

    if extract_dir.exists() and force_extract:
        shutil.rmtree(extract_dir)

    LOGGER.info("Extracting dataset archive to %s", RAW_DATA_DIR)
    with zipfile.ZipFile(archive_path, "r") as zip_file:
        zip_file.extractall(RAW_DATA_DIR)

    return extract_dir
