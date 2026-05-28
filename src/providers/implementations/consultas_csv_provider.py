import csv
from typing import List, Dict, Any
from fastapi import HTTPException, status

class ConsultasCsvProvider:
    def __init__(self, csv_path: str = 'data/consultas.csv'):
        self.csv_path = csv_path
        self._check_file_exists()

    def _check_file_exists(self):
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                pass
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo CSV de consultas não encontrado em: {self.csv_path}")

    async def listar_consultas(self) -> List[Dict[str, Any]]:
        consultas = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if len(consultas) >= 50:
                        break

                    try:
                        consulta_id = int(row.get('id', '') or 0)
                    except ValueError:
                        consulta_id = 0

                    consultas.append({
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
                    })
        except Exception as e:
            print(f"Erro ao ler CSV de consultas: {e}")
        return consultas

    async def obter_consulta_por_id(self, consulta_id: int) -> Dict[str, Any]:
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        current_id = int(row.get('id', '') or -1)
                    except ValueError:
                        continue

                    if current_id == consulta_id:
                        return {
                            'id': current_id,
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
                        }
        except Exception as e:
            print(f"Erro ao ler CSV de consultas: {e}")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada no CSV")
