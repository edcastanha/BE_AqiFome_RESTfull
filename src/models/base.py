from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BaseEntity(BaseModel):
    """
    Classe base para todas as entidades do domínio.
    Implementa funcionalidades comuns e segue princípios de DDD.
    """
    id: Optional[int] = Field(default=None, description="Identificador único da entidade")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Data de criação")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="Data de última atualização")
    
    class Config:
        # Permite validação de tipos mais flexível
        validate_assignment = True
        # Usa alias para campos com underscore
        allow_population_by_field_name = True 