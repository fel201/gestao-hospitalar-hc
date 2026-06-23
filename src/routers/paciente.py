from fastapi import APIRouter, Depends
from typing import List, Optional

from ..controllers import paciente_controller
# Alteração: Importamos apenas a FÁBRICA
# import provavelmente nao mais necessários
from ..dependencies import get_paciente_provider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..controllers.jornada_controller import JornadaController as jornada_controller
from ..providers.implementations.paciente_csv_provider import PacienteCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..auth.auth import auth_handler

# --- PONTO ÚNICO DE CONFIGURAÇÃO PARA ESTE ROTEADOR ---
# Para usar o banco de dados em produção, altere esta linha para "postgres"
STRATEGY = "csv"
# ----------------------------------------------------

router = APIRouter(
    prefix="/api/pacientes",
    tags=["Pacientes"],
    dependencies=[Depends(auth_handler.decode_token)]
)

@router.get("", response_model=List[dict])
async def listar_pacientes(

    page: int = 1,
    limit: int = 50,
    especialidade: Optional[str] = None,
    unidade: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    ordenar_por: str = "nome",
    provider: PacienteProviderInterface = Depends(get_paciente_provider(STRATEGY))
):
    """Lista todos os pacientes com suporte a paginação e filtros."""
    return await paciente_controller.listar_pacientes(
        provider=provider,
        page=page,
        limit=limit,
        especialidade=especialidade,
        unidade=unidade,
        data_inicio=data_inicio,
        data_fim=data_fim,
        ordenar_por=ordenar_por
    )
    
@router.get("/{codigo}", response_model=dict)
async def obter_paciente(
    codigo: int,
    provider: PacienteProviderInterface = Depends(get_paciente_provider(STRATEGY))
):
    """Obtém um paciente pelo código a partir da fonte de dados configurada no roteador."""
    return await paciente_controller.obter_paciente_por_codigo(codigo, provider)
