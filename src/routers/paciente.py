from fastapi import APIRouter, Depends
from typing import List

from ..controllers import paciente_controller
# Alteração: Importamos apenas a FÁBRICA
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


from fastapi import Query

@router.get("")
async def listar_pacientes(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    provider: PacienteProviderInterface = Depends(get_paciente_provider(STRATEGY))
):
    paciente_provider = PacienteCsvProvider()
    exames_provider = ExameCsvProvider()
    consultas_provider = ConsultasCsvProvider()
    internacoes_provider = InternacoesCsvProvider()

    return await jornada_controller.listar_pacientes_com_jornada(
        paciente_provider,
        consultas_provider,
        exames_provider,
        internacoes_provider,
        page=page,
        page_size=page_size,
    )
    
@router.get("/{codigo}", response_model=dict)
async def obter_paciente(
    codigo: int,
    provider: PacienteProviderInterface = Depends(get_paciente_provider(STRATEGY))
):
    """Obtém um paciente pelo código a partir da fonte de dados configurada no roteador."""
    return await paciente_controller.obter_paciente_por_codigo(codigo, provider)
