from typing import Optional
from pydantic import BaseModel

class Cliente(BaseModel):
    id: Optional[int]
    nome: str
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao@email.com"
            }
        }
