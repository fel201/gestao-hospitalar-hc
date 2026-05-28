import csv
from typing import List, Dict, Any
from fastapi import HTTPException, status

class ExameCsvProvider:
    def __init__(self, csv_path: str = 'data/exames.csv'):
        self.csv_path = csv_path
        self._check_file_exists()

    def _check_file_exists(self):
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                pass
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo CSV de exames não encontrado em: {self.csv_path}")

    async def listar_exames(self) -> List[Dict[str, Any]]:
        exames = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if len(exames) >= 50:
                        break

                    exames.append({
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
                    })
        except Exception as e:
            print(f"Erro ao ler CSV de exames: {e}")
        return exames

    async def obter_exame_por_id(self, exame_id: str) -> Dict[str, Any]:
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('exame_id', '') == exame_id:
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
                        }
        except Exception as e:
            print(f"Erro ao ler CSV de exames: {e}")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exame não encontrado no CSV")
