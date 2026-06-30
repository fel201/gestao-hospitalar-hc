import csv
from typing import List, Dict, Any
from fastapi import HTTPException, status


class PacienteCsvProvider:
    def __init__(self, csv_path: str = 'data/pacientes.csv'):
        self.csv_path = csv_path
        self._check_file_exists()

    def _check_file_exists(self):
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                pass
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo CSV de pacientes não encontrado em: {self.csv_path}")

    async def listar_pacientes(self) -> List[Dict[str, Any]]:
        pacientes = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    
                    try:
                        # Remover pontos do formato brasileiro (17.774 -> 17774)
                        codigo_str = row.get('pac_codigo', '').replace('.', '')
                        codigo = int(codigo_str) if codigo_str else 0
                    except ValueError:
                        codigo = 0
                    
                    # Mapear os campos do CSV para um formato padronizado
                    paciente = {
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
                    pacientes.append(paciente)
        except Exception as e:
            print(f"Erro ao ler CSV: {e}")
        return pacientes

    async def obter_paciente_por_codigo(self, codigo: int) -> Dict[str, Any]:
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Remover pontos do formato brasileiro (17.774 -> 17774)
                        codigo_str = row.get('pac_codigo', '').replace('.', '')
                        current_codigo = int(codigo_str) if codigo_str else -1
                        
                        if current_codigo == codigo:
                            # Mapear os campos do CSV para um formato padronizado
                            paciente = {
                                'codigo': current_codigo,
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
                            return paciente
                    except ValueError:
                        continue
        except Exception as e:
            print(f"Erro ao ler CSV: {e}")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado no CSV")

