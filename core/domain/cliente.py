from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from enum import IntEnum

class TipoCliente(IntEnum):
    USER = 0
    ADMIN = 1


class ClienteBase(BaseModel):
    email: EmailStr
    senha: str
    tipo: TipoCliente


class ClienteCreate(ClienteBase):
    nome: str
    


class Cliente(ClienteBase):
    id: Optional[int]
    nome: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Edson Bezerra",
                "email": "edson@aiqfome.com",
                "tipo": 0,
            }
        },
    )


class ClienteInDB(Cliente):
    senha: str
