from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..csv_file_provider import CsvFileProvider


class InternacoesCsvProvider:
    def __init__(self, csv_path: str = 'data/internacoes.csv'):
        self.csv_path = csv_path
        self._csv_data = CsvFileProvider(csv_path, parser=self._parse_row)

    def _parse_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        try:
            internacao_id = int(str(row.get('id_internacao', '') or 0))
        except ValueError:
            internacao_id = 0

        return {
            'id_internacao': internacao_id,
            'atendimento': row.get('atendimento', ''),
            'prontuario': row.get('prontuario', ''),
            'codigo_paciente': row.get('codigo_paciente', ''),
            'dthr_inicio': row.get('dthr_inicio', ''),
            'dthr_fim': row.get('dthr_fim', ''),
            'tempo_permanencia_dias': row.get('tempo_permanencia_dias', ''),
            'situacao_sumario_alta': row.get('Indica situação do sumário de alta', ''),
            'descricao_origem_evento': row.get('descricao_origem_evento', ''),
            'descricao_tipo_alta_medica': row.get('descricao_tipo_alta_medica', ''),
            'unf_descricao': row.get('unf_descricao', ''),
            'unf_sigla': row.get('unf_sigla', ''),
            'especialidade': row.get('esp_nome_especialidade', ''),
            'ind_saida_pac': row.get('ind_saida_pac', ''),
        }

    async def listar_internacoes(self) -> List[Dict[str, Any]]:
        return await self._csv_data.get_rows()

    async def obter_internacao_por_id(self, internacao_id: int) -> Dict[str, Any]:
        internacoes = await self._csv_data.get_rows()
        for internacao in internacoes:
            if internacao.get('id_internacao') == internacao_id:
                return internacao

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Internação não encontrada no CSV")
