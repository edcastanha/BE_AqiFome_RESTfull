from typing import Optional
from pydantic import BaseModel, ConfigDict

class ClienteBase(BaseModel):
    email: str


class ClienteCreate(ClienteBase):
    nome: str
    senha: str


class Cliente(ClienteBase):
    id: Optional[int]
    nome: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Edson Bezerra",
                "email": "edson@email.com",
            }
        },
    )


class ClienteInDB(Cliente):
    senha: str
