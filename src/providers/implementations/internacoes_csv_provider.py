import csv
from typing import List, Dict, Any
from fastapi import HTTPException, status

class InternacoesCsvProvider:
    def __init__(self, csv_path: str = 'data/internacoes.csv'):
        self.csv_path = csv_path
        self._check_file_exists()

    def _check_file_exists(self):
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                pass
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo CSV de internações não encontrado em: {self.csv_path}")

    async def listar_internacoes(self) -> List[Dict[str, Any]]:
        internacoes = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if len(internacoes) >= 50:
                        break

                    try:
                        internacao_id = int(row.get('id_internacao', '') or 0)
                    except ValueError:
                        internacao_id = 0

                    internacoes.append({
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
                    })
        except Exception as e:
            print(f"Erro ao ler CSV de internações: {e}")
        return internacoes

    async def obter_internacao_por_id(self, internacao_id: int) -> Dict[str, Any]:
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        current_id = int(row.get('id_internacao', '') or -1)
                    except ValueError:
                        continue

                    if current_id == internacao_id:
                        return {
                            'id_internacao': current_id,
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
                        }
        except Exception as e:
            print(f"Erro ao ler CSV de internações: {e}")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Internação não encontrada no CSV")
