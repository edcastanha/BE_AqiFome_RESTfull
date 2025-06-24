from typing import Annotated
from pydantic import BaseModel, ConfigDict, HttpUrl, Field
from decimal import Decimal

class ProdutoExterno(BaseModel):
    """
    Modelo que representa um produto externo proveniente de APIs terceiras.
    Mantém os dados do produto de forma consistente dentro da aplicação.
    """
    id: int
    title: str
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2, description="Preço do produto (positivo, máximo 2 casas decimais)")]
    description: str
    category: str
    image: str  # Verificaria com time se validariamos a URL com válida
    model_config = ConfigDict(from_attributes=True, frozen=True)
