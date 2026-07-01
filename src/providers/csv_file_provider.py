import asyncio
import csv
import os
from typing import Any, Callable, Dict, List, Optional

from .csv_path_resolver import resolve_csv_path


class CsvFileProvider:
    _shared_cache: Dict[tuple[str, str], tuple[int, List[Dict[str, Any]]]] = {}

    def __init__(self, csv_path: str, parser: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.csv_path = resolve_csv_path(csv_path)
        self._parser = parser
        self._cache_key = (self.csv_path, getattr(self._parser, "__name__", "parser"))

    def _get_file_mtime_ns(self) -> int:
        try:
            return os.stat(self.csv_path).st_mtime_ns
        except FileNotFoundError:
            return -1

    def _load_rows_from_disk(self) -> List[Dict[str, Any]]:
        try:
            with open(self.csv_path, mode="r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                rows = [self._parser(row) for row in reader]
                return rows
        except FileNotFoundError:
            return []
        except Exception as exc:
            print(f"Erro ao ler CSV {self.csv_path}: {exc}")
            return []

    async def get_rows(self) -> List[Dict[str, Any]]:
        current_mtime = self._get_file_mtime_ns()
        cached_entry = self._shared_cache.get(self._cache_key)
        if cached_entry is not None and cached_entry[0] == current_mtime:
            return cached_entry[1]

        rows = await asyncio.to_thread(self._load_rows_from_disk)
        self._shared_cache[self._cache_key] = (current_mtime, rows)
        return rows
