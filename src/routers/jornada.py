from fastapi import APIRouter, Depends, Query

from ..controllers import jornada_controller
from ..dependencies import get_paciente_provider
from ..providers.implementations.consultas_csv_provider import ConsultasCsvProvider
from ..providers.implementations.exame_csv_provider import ExameCsvProvider
from ..providers.implementations.internacoes_csv_provider import InternacoesCsvProvider
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..auth.auth import auth_handler

STRATEGY = "csv"

router = APIRouter(
    prefix="/api/paciente",
    tags=["Jornada"],
    dependencies=[Depends(auth_handler.decode_token)]
)

@router.get("/jornada", response_model=dict)
async def obter_jornada_paciente(
    codigo: int = Query(..., description="Código do paciente"),
    paciente_provider: PacienteProviderInterface = Depends(get_paciente_provider(STRATEGY)),
):
    consultas_provider = ConsultasCsvProvider()
    exames_provider = ExameCsvProvider()
    internacoes_provider = InternacoesCsvProvider()
    
    return await jornada_controller.JornadaController.obter_jornada_paciente(
        codigo,
        paciente_provider,
        consultas_provider,
        exames_provider,
        internacoes_provider,
    )
