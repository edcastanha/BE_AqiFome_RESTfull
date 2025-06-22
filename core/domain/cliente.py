from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr
from enum import IntEnum

class TipoCliente(IntEnum):
    USER = 0
    ADMIN = 1


class ClienteBase(BaseModel):
    email: EmailStr
    senha: SecretStr
    tipo: TipoCliente


class ClienteCreate(ClienteBase):
    nome: str
    


class Cliente(ClienteBase):
    id: int
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
    """
    Modelo que inclui a senha, usado para autenticação.
    """
    email: EmailStr
    senha: SecretStr


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[SecretStr] = None
    tipo: Optional[TipoCliente] = None
