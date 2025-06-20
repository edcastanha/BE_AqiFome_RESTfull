from typing import Optional
from pydantic import BaseModel, ConfigDict

class Cliente(BaseModel):
    """
    Modelo de dados para um cliente.

    Atributos:
        id (Optional[int]): Identificador único do cliente.
        nome (str): Nome do cliente.
        email (str): E-mail do cliente.
    """
    id: Optional[int]
    nome: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao@email.com"
            }
        }
    )
