from pydantic import EmailStr, Field, validator
from .base import BaseEntity
from typing import Optional

class Cliente(BaseEntity):
    """
    Modelo que representa um cliente no sistema.
    Segue os princípios de DDD e Clean Code.
    """
    nome: str = Field(..., min_length=1, max_length=100, description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email único do cliente")
    
    @validator('nome')
    def validar_nome(cls, v):
        """Valida se o nome não está vazio e tem pelo menos 2 caracteres."""
        if not v or len(v.strip()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')
        return v.strip()
    
    class Config:
        # Exemplo de como o modelo seria representado
        schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao.silva@email.com"
            }
        } 