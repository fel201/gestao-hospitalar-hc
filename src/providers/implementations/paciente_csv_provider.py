from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..csv_file_provider import CsvFileProvider


class PacienteCsvProvider:
    def __init__(self, csv_path: str = 'data/pacientes.csv'):
        self.csv_path = csv_path
        self._csv_data = CsvFileProvider(csv_path, parser=self._parse_row)

    def _parse_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        try:
            codigo_str = str(row.get('pac_codigo', '')).replace('.', '')
            codigo = int(codigo_str) if codigo_str else 0
        except ValueError:
            codigo = 0

        return {
            'codigo': codigo,
            'prontuario': row.get('prontuario', ''),
            'nome': row.get('nome_iniciais', ''),
            'nome_social': row.get('nome_social_iniciais', ''),
            'nome_mae': row.get('nome_mae_iniciais', ''),
            'nome_pai': row.get('nome_pai_iniciais', ''),
            'idade': row.get('idade', ''),
            'sexo': row.get('sexo', ''),
            'estado_civil': row.get('estado_civil', ''),
            'cor': row.get('cor', ''),
            'nacionalidade': row.get('nacionalidade', ''),
            'naturalidade': row.get('naturalidade', ''),
            'cidade': row.get('cidade', ''),
            'uf': row.get('uf', ''),
        }

    async def listar_pacientes(self) -> List[Dict[str, Any]]:
        return await self._csv_data.get_rows()

    async def obter_paciente_por_codigo(self, codigo: int) -> Dict[str, Any]:
        pacientes = await self._csv_data.get_rows()
        for paciente in pacientes:
            if paciente.get('codigo') == codigo:
                return paciente

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado no CSV")

