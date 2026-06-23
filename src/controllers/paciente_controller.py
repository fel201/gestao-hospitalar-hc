from typing import List, Dict, Any
from fastapi import HTTPException
from ..providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from ..schemas.paciente import PacienteSchema 

async def listar_pacientes(
    provider: PacienteProviderInterface,
    page: int = 1,
    limit: int = 50,
    especialidade: str | None = None,
    unidade: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    ordenar_por: str = "nome"
) -> List[Dict[str, Any]]:
    "implementando"

    page = max(page, 1)

    return await provider.listar_pacientes(
        page=page,
        limit=limit,
        especialidade=especialidade,
        unidade=unidade,
        data_inicio=data_inicio,
        data_fim=data_fim,
        ordenar_por=ordenar_por
    )
    
async def obter_paciente_por_codigo(
    codigo: int,
    provider: PacienteProviderInterface
) -> Dict[str, Any]:
    return await provider.obter_paciente_por_codigo(codigo)

async def criar_paciente(
    paciente_data: PacienteSchema,
    provider: PacienteProviderInterface,
) -> Dict[str, Any]:
    
    # checa se o prontuário já existe
    paciente_existe = await provider.obter_paciente_por_prontuario(paciente_data.prontuario)

    if paciente_existe:
        raise HTTPException(
            status_code=409, 
            detail=f"Prontuário {paciente_data.prontuario} já existe"
        )
    
    # se não existir, cria o paciente
    return await provider.salvar_paciente(paciente_data.model_dump()) # <- Corrigido com a letra L