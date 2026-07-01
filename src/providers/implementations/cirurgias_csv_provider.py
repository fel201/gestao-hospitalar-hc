from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..csv_file_provider import CsvFileProvider


class CirurgiasCsvProvider:
    def __init__(self, csv_path: str = "data/cirurgias.csv"):
        self.csv_path = csv_path
        self._csv_data = CsvFileProvider(csv_path, parser=self._parse_row)

    def _parse_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        try:
            cirurgia_id = int(str(row.get("cirurgia_id", "") or 0))
        except ValueError:
            cirurgia_id = 0

        return {
            "cid": row.get("CID", ""),
            "id": cirurgia_id,
            "paciente_id": row.get("Codigo do Paciente", ""),
            "especialidade": row.get("Especialidade", ""),
            "duracao_cirurgia": row.get("duracao_cirurgia", ""),
            "data_inicio_cirurgia": row.get("data_inicio_cirurgia", ""),
            "data_fim_cirurgia": row.get("data_fim_cirurgia", ""),
            "cancelada": row.get("cancelada", ""),
            "situacao": row.get("situacao", ""),
        }

    async def listar_cirurgias(self) -> List[Dict[str, Any]]:
        return await self._csv_data.get_rows()

    async def obter_cirurgia_por_id(
        self, cirurgia_id: int
    ) -> Dict[str, Any]:
        cirurgias = await self._csv_data.get_rows()
        for cirurgia in cirurgias:
            if cirurgia.get("id") == cirurgia_id:
                return cirurgia

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cirurgia não encontrada no CSV",
        )