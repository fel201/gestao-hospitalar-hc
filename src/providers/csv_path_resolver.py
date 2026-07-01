import os
from pathlib import Path


def resolve_csv_path(relative_path: str) -> str:
    """Resolve um caminho de CSV de forma robusta em ambientes locais e de deploy."""
    if not relative_path:
        return relative_path

    if os.path.isabs(relative_path):
        return relative_path

    candidates = []

    env_value = os.getenv("DATA_DIR")
    if env_value:
        candidates.append(Path(env_value) / relative_path)
        candidates.append(Path(env_value) / Path(relative_path).name)

    project_root = Path(__file__).resolve().parent.parent.parent
    data_dir = project_root / "data"

    candidates.extend([
        Path(relative_path),
        project_root / relative_path,
        data_dir / Path(relative_path).name,
        Path.cwd() / relative_path,
        Path.cwd() / "data" / Path(relative_path).name,
        Path.cwd() / Path(relative_path).name,
    ])

    for candidate in candidates:
        try:
            if candidate.exists():
                return str(candidate)
        except OSError:
            continue

    return str(data_dir / Path(relative_path).name)
