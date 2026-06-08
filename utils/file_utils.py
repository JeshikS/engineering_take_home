import json
from pathlib import Path


def save_json(data, filename):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved to {file_path}")


def load_json(filename):
    file_path = Path("output") / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)