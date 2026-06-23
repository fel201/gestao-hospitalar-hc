from datetime import datetime
import csv
from typing import List, Dict, Any
from fastapi import HTTPException, status

from ..interfaces.paciente_provider_interface import PacienteProviderInterface

class PacienteCsvProvider(PacienteProviderInterface):
    def __init__(self, csv_path: str = 'data/pacientes.csv'):
        self.csv_path = csv_path
        self._check_file_exists()

    def _check_file_exists(self):
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                pass
        except FileNotFoundError:
            raise RuntimeError(f"Arquivo CSV de pacientes não encontrado em: {self.csv_path}")

    async def listar_pacientes(
        self,
        page: int = 1,
        limit: int = 50,
        especialidade: str | None = None,
        unidade: str | None = None,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        ordenar_por: str = "nome"
    ) -> List[Dict[str, Any]]:
        pacientes = []

        # filtro de datas
        dt_inicio = datetime.strptime(data_inicio, "%d/%m/%Y") if data_inicio else None
        dt_fim = datetime.strptime(data_fim, "%d/%m/%Y") if data_fim else None

        # CRUZAMENTO (JOIN) COM O CSV DE CONSULTAS
        codigos_validos_por_consulta = set()
        filtrar_por_consulta = False

        if especialidade or unidade:
            filtrar_por_consulta = True
            try:
                # Abre o outro arquivo para descobrir quais pacientes atendem ao critério
                with open('data/consultas.csv', mode='r', encoding='utf-8') as f_consultas:
                    reader_consultas = csv.DictReader(f_consultas)
                    for row_c in reader_consultas:
                        
                        # Verifica se a linha da consulta bate com os filtros fornecidos
                        if especialidade and row_c.get('especialidade') != especialidade:
                            continue
                        if unidade and row_c.get('Unidade Funcional') != unidade:
                            continue
                        
                        # Se passou pelos filtros, extrai o código do paciente dessa consulta
                        pront_str = row_c.get('Prontuario', '').replace('.', '')
                        if pront_str.isdigit():
                            codigos_validos_por_consulta.add(int(pront_str))
            except Exception as e:
                print(f"Erro ao ler CSV de consultas: {e}")

        # LEITURA E FILTRAGEM DO ARQUIVO DE PACIENTES
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    
                    try:
                        codigo_str = row.get('pac_codigo', '').replace('.', '')
                        codigo = int(codigo_str) if codigo_str else 0
                    except ValueError:
                        codigo = 0

                    prontuario_str = row.get('prontuario', '').replace('.', '')
                    prontuario_int = int(prontuario_str) if prontuario_str.isdigit() else 0

                    if filtrar_por_consulta and prontuario_int   not in codigos_validos_por_consulta:
                        continue

                    # FILTRO DE DATA DE CADASTRO
                    if dt_inicio or dt_fim:
                        data_str = row.get('data_cadastro', '')
                        if data_str:
                            try:
                                dt_cadastro = datetime.strptime(data_str, "%d/%m/%Y")
                                if dt_inicio and dt_cadastro < dt_inicio:
                                    continue
                                if dt_fim and dt_cadastro > dt_fim:
                                    continue
                            except ValueError:
                                pass 

                    # Mapear os campos para o formato padronizado (não-sensível)
                    paciente = {
                        'codigo': codigo,
                        'prontuario': row.get('prontuario', ''),
                        'nome': row.get('nome_iniciais', ''),
                        'data_cadastro': row.get('data_cadastro', ''),
                        'idade': row.get('idade', ''),
                        'sexo': row.get('sexo', ''),
                        'estado_civil': row.get('estado_civil', ''),
                        'cidade': row.get('cidade', ''),
                        'uf': row.get('uf', ''),
                    }
                    pacientes.append(paciente)
        
            # 4. ORDENAÇÃO
            if ordenar_por == 'data_cadastro':
                pacientes.sort(key=lambda x: datetime.strptime(x['data_cadastro'], "%d/%m/%Y") if x['data_cadastro'] else datetime.min)
            else:
                pacientes.sort(key=lambda x: x['nome'])

            # 5. PAGINAÇÃO
            inicio = (page - 1) * limit
            fim = inicio + limit
            return pacientes[inicio:fim]

        except Exception as e:
            print(f"Erro ao ler CSV de pacientes: {e}")
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
    


    # código abaixo é totalmente provisório
    async def obter_paciente_por_prontuario(self, prontuario: str) -> Dict[str, Any]:
        """Implementação exigida pela interface para buscar por prontuário."""
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('prontuario') == prontuario:
                        return row
        except Exception as e:
            print(f"Erro ao ler CSV: {e}")
        return {}

    async def salvar_paciente(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Implementação exigida pela interface para salvar paciente."""
        # Como o CSV é apenas para leitura neste cenário atual, 
        # levantamos um erro amigável se alguém tentar salvar por aqui.
        raise NotImplementedError("A inserção de pacientes ainda não foi implementada para o provedor CSV.")

