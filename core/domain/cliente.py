from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import IntEnum

class TipoCliente(IntEnum):
    NORMAL = 0
    ADMIN = 1


class ClienteBase(BaseModel):
    email: str
    senha: str
    tipo: TipoCliente = TipoCliente.NORMAL  # 1 = Admin


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
                "tipo": "NORMAL",
            }
        },
    )


class ClienteInDB(Cliente):
    senha: str
