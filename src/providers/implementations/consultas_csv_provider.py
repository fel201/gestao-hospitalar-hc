from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..csv_file_provider import CsvFileProvider


class ConsultasCsvProvider:
    def __init__(self, csv_path: str = 'data/consultas.csv'):
        self.csv_path = csv_path
        self._csv_data = CsvFileProvider(csv_path, parser=self._parse_row)

    def _parse_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        try:
            consulta_id = int(str(row.get('id', '') or 0))
        except ValueError:
            consulta_id = 0

        return {
            'id': consulta_id,
            'num_consulta': row.get('num_consulta', ''),
            'procedimento': row.get('procedimento', ''),
            'profissional_atendeu': row.get('profissional_atendeu', ''),
            'prontuario': row.get('Prontuario', ''),
            'especialidade': row.get('especialidade', ''),
            'cid': row.get('CID', ''),
            'data_hora_consulta': row.get('Data/Hora da Consulta', ''),
            'data_hora_fim': row.get('Data/Hora de Fim', ''),
            'justificativa': row.get('Justificativa', ''),
            'justificativa_falta': row.get('Justificativa da Falta', ''),
            'tipo': row.get('tipo', ''),
            'data_procedimento': row.get('data_procedimento', ''),
            'retorno': row.get('Retorno', ''),
            'paciente_id': row.get('ID do Paciente', ''),
            'condicao': row.get('Condição do Atendimento', ''),
        }

    async def listar_consultas(self) -> List[Dict[str, Any]]:
        return await self._csv_data.get_rows()

    async def obter_consulta_por_id(self, consulta_id: int) -> Dict[str, Any]:
        consultas = await self._csv_data.get_rows()
        for consulta in consultas:
            if consulta.get('id') == consulta_id:
                return consulta

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada no CSV")
