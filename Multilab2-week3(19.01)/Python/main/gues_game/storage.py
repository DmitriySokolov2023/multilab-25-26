import json
from pathlib import Path


SAVE_PATH = Path("save.json")


def load_data() -> dict:
    if not SAVE_PATH.exists():
        return {}

    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # файл повреждён или пустой
        return {}


def save_data(data: dict) -> None:
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
