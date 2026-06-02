from pathlib import Path
import sys

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app


def main() -> None:
    output_path = Path("docs/openapi.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(app.openapi(), file, sort_keys=False, allow_unicode=True)

    print(f"OpenAPI spec exported to {output_path}")


if __name__ == "__main__":
    main()
