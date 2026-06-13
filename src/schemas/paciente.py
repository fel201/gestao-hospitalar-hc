from pydantic import BaseModel, Field

class Pacienteschema(BaseModel):
    pac_id: int = Field(..., description="ID interno do paciente no banco")
    nome: str = Field(...,min_length=3, description="Nome do paciente")
    prontuario: str = Field(...,min_length=1, description="Número do prontuário do hc")

    # validação de dados contra JSON Schema