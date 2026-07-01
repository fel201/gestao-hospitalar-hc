import csv
from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..csv_path_resolver import resolve_csv_path


class CirurgiasCsvProvider:
    def __init__(self, csv_path: str = "data/cirurgias.csv"):
        self.csv_path = resolve_csv_path(csv_path)
        self._check_file_exists()

    def _check_file_exists(self):
        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as f:
                pass
        except FileNotFoundError:
            raise RuntimeError(
                f"Arquivo CSV de cirurgias não encontrado em: {self.csv_path}"
            )

    async def listar_cirurgias(self) -> List[Dict[str, Any]]:
        cirurgias = []

        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:

                    try:
                        cirurgia_id = int(row.get("cirurgia_id", "") or 0)
                    except ValueError:
                        cirurgia_id = 0

                    cirurgias.append({
                        "cid": row.get("CID", ""),
                        "id": cirurgia_id,
                        "paciente_id": row.get("Codigo do Paciente", ""),
                        "especialidade": row.get("Especialidade", ""),
                        "duracao_cirurgia": row.get("duracao_cirurgia", ""),
                        "data_inicio_cirurgia": row.get("data_inicio_cirurgia", ""),
                        "data_fim_cirurgia": row.get("data_fim_cirurgia", ""),
                        "cancelada": row.get("cancelada", ""),
                        "situacao": row.get("situacao", ""),
                    })

        except Exception as e:
            print(f"Erro ao ler CSV de cirurgias: {e}")

        return cirurgias

    async def obter_cirurgia_por_id(
        self, cirurgia_id: int
    ) -> Dict[str, Any]:

        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:

                    try:
                        current_id = int(row.get("cirurgia_id", "") or -1)
                    except ValueError:
                        continue

                    if current_id == cirurgia_id:
                        return {
                            "id": current_id,
                            "paciente_id": row.get("Codigo do Paciente", ""),
                            "especialidade": row.get("Especialidade", ""),
                            "duracao_cirurgia": row.get("duracao_cirurgia", ""),
                            "data_inicio_cirurgia": row.get("data_inicio_cirurgia", ""),
                            "data_fim_cirurgia": row.get("data_fim_cirurgia", ""),
                            "cancelada": row.get("cancelada", ""),
                            "situacao": row.get("situacao", ""),
                        }

        except Exception as e:
            print(f"Erro ao ler CSV de cirurgias: {e}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cirurgia não encontrada no CSV",
        )