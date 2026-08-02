import asyncio
import csv
import os
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .csv_path_resolver import resolve_csv_path


class CsvFileProvider:
    _shared_cache: Dict[tuple, tuple[int, List[Dict[str, Any]]]] = {}

    _CAMPO_DATA = "data_hora_realizacao"  # nome já normalizado por todos os _parse_row
    _FORMATO_DATA = "%d/%m/%Y, %H:%M"

    def __init__(
        self,
        csv_path: str,
        parser: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        *,
        primary_key: Optional[str] = None,
        rename: Optional[Dict[str, str]] = None,
        integer_columns: Optional[List[str]] = None,
    ):
        self.csv_path = resolve_csv_path(csv_path)
        self._parser = parser or (lambda row: row)
        self._parser_name = getattr(self._parser, "__name__", "parser")
        self._primary_key = primary_key
        self._rename = rename or {}
        self._integer_columns = set(integer_columns or [])

    def _get_file_mtime_ns(self) -> int:
        try:
            return os.stat(self.csv_path).st_mtime_ns
        except FileNotFoundError:
            return -1

    def _parse_data(self, valor: Any) -> Optional[datetime]:
        if not valor:
            return None
        try:
            return datetime.strptime(str(valor).strip(), self._FORMATO_DATA)
        except ValueError:
            return None

    def _dentro_do_periodo(
        self,
        row: Dict[str, Any],
        data_inicio: Optional[str],
        data_fim: Optional[str],
    ) -> bool:
        if not data_inicio and not data_fim:
            return True

        data_evento = self._parse_data(row.get(self._CAMPO_DATA))
        if data_evento is None:
            # Linha sem data parseável (vazia ou formato inesperado) é mantida
            # por padrão para não sumir com dado silenciosamente.
            return True

        if data_inicio:
            inicio = self._parse_data_filtro(data_inicio)
            if inicio and data_evento < inicio:
                return False
        if data_fim:
            fim = self._parse_data_filtro(data_fim)
            if fim and data_evento > fim:
                return False
        return True

    def _parse_data_filtro(self, valor: str) -> Optional[datetime]:
        """
        data_inicio/data_fim chegam do endpoint, provavelmente como 'YYYY-MM-DD'
        (padrão de query params), então tentamos esse formato separado do formato do CSV.
        Ajuste aqui se o formato que o frontend manda for outro.
        """
        try:
            return datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            return self._parse_data(valor)  # tenta o formato do CSV como fallback

    def _normalize_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        parsed = self._parser(row)
        if not isinstance(parsed, dict):
            return {}

        normalized: Dict[str, Any] = {}
        for key, value in parsed.items():
            output_key = self._rename.get(key, key)
            normalized[output_key] = value

        for column in self._integer_columns:
            output_key = self._rename.get(column, column)
            if output_key in normalized and normalized[output_key] not in (None, ""):
                try:
                    normalized[output_key] = int(normalized[output_key])
                except (TypeError, ValueError):
                    continue

        return normalized

    def _load_rows_from_disk(
        self, data_inicio: Optional[str], data_fim: Optional[str]
    ) -> List[Dict[str, Any]]:
        rows = []
        seen_keys: set[Any] = set()
        try:
            with open(self.csv_path, mode="r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    parsed = self._normalize_row(row)
                    if self._dentro_do_periodo(parsed, data_inicio, data_fim):
                        if self._primary_key:
                            key = parsed.get(self._primary_key)
                            if key in seen_keys:
                                continue
                            seen_keys.add(key)
                        rows.append(parsed)
            return rows
        except FileNotFoundError:
            return []
        except Exception as exc:
            print(f"Erro ao ler CSV {self.csv_path}: {exc}")
            return []

    async def get_rows(
        self, data_inicio: Optional[str] = None, data_fim: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        current_mtime = self._get_file_mtime_ns()
        cache_key = (self.csv_path, self._parser_name, data_inicio, data_fim)

        cached_entry = self._shared_cache.get(cache_key)
        if cached_entry is not None and cached_entry[0] == current_mtime:
            return cached_entry[1]

        rows = await asyncio.to_thread(self._load_rows_from_disk, data_inicio, data_fim)
        self._shared_cache[cache_key] = (current_mtime, rows)
        return rows

    async def get_by_id(self, value: Any) -> Optional[Dict[str, Any]]:
        if not self._primary_key:
            return None

        rows = await self.get_rows()
        target = str(value)
        for row in rows:
            row_value = row.get(self._primary_key)
            if row_value is not None and str(row_value) == target:
                return row
        return None