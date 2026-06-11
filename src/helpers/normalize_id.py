def _normalize_id(value) -> str:
    return ''.join(ch for ch in str(value) if ch.isdigit())