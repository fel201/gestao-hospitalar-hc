import os
from pathlib import Path


def resolve_csv_path(relative_path: str) -> str:
    """Resolve um caminho de CSV de forma robusta em ambientes locais e de deploy."""
    candidates = []

    if os.path.isabs(relative_path):
        return relative_path

    env_value = os.getenv("DATA_DIR")
    if env_value:
        candidates.append(Path(env_value) / relative_path)

    candidates.extend([
        Path(relative_path),
        Path(__file__).resolve().parent.parent.parent / relative_path,
        Path(__file__).resolve().parent.parent.parent / "data" / Path(relative_path).name,
        Path.cwd() / relative_path,
        Path.cwd() / "data" / Path(relative_path).name,
    ])

    for candidate in candidates:
        try:
            if candidate.exists():
                return str(candidate)
        except OSError:
            continue

    return relative_path
