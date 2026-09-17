from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = APP_DIR / "generated" / "audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
