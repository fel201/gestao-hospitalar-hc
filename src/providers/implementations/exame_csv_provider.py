from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..csv_file_provider import CsvFileProvider


class ExameCsvProvider:
    def __init__(self, csv_path: str = 'data/exames.csv'):
        self.csv_path = csv_path
        self._csv_data = CsvFileProvider(csv_path, parser=self._parse_row)

    def _parse_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'exame_id': row.get('exame_id', ''),
            'paciente_id': row.get('paciente_id', ''),
            'paciente_prontuario': row.get('paciente_prontuario', ''),
            'nome_exame': row.get('nome_exame', ''),
            'tipo_exame': row.get('tipo_exame', ''),
            'data_hora_solicitacao': row.get('data_hora_solicitacao', ''),
            'data_hora_realizacao': row.get('data_hora_realizacao', ''),
            'data_hora_liberacao': row.get('data_hora_liberacao', ''),
            'situacao_codigo': row.get('situacao_codigo', ''),
            'situacao': row.get('situacao', ''),
            'especialidade_solicitante_nome': row.get('especialidade_solicitante_nome', ''),
            'retorno': row.get('retorno', ''),
            'condicao': row.get('condicao_exame', ''),
        }

    async def listar_exames(self) -> List[Dict[str, Any]]:
        return await self._csv_data.get_rows()

    async def obter_exame_por_id(self, exame_id: str) -> Dict[str, Any]:
        exames = await self._csv_data.get_rows()
        for exame in exames:
            if exame.get('exame_id', '') == exame_id:
                return exame

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exame não encontrado no CSV")
