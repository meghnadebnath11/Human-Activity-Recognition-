from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "artifacts"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"

DATASET_URL = "https://archive.ics.uci.edu/static/public/344/heterogeneity%2Bactivity%2Brecognition.zip"
ARCHIVE_NAME = "hhar_activity_recognition.zip"
EXTRACTED_DIR_NAME = "Activity recognition exp"

