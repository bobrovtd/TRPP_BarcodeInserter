from pathlib import Path

# Определяем корневую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent  # Путь к папке `BarcodeInserter`

# Пути к важным папкам
DATA_DIR = BASE_DIR / "data"

OUTPUT_DIR = DATA_DIR / "output"

ACTIVE_DIR = DATA_DIR / "active"
BARCODES_DIR = ACTIVE_DIR / "barcodes"
EXCELS_DIR = ACTIVE_DIR / "excels"
PDFS_DIR = ACTIVE_DIR / "pdfs"

USED_DIR = DATA_DIR / "used"
USED_BARCODES_DIR = USED_DIR / "barcodes"
USED_PDFS_DIR = USED_DIR / "pdfs"

# Убедитесь, что директории существуют
BARCODES_DIR.mkdir(parents=True, exist_ok=True)
EXCELS_DIR.mkdir(parents=True, exist_ok=True)
PDFS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)