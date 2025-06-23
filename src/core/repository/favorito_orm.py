from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from core.config.db import Base

class FavoritoORM(Base):
    """
    Representa a relação entre clientes e produtos favoritos.
    
    Cada favorito é único por cliente e produto, garantindo que um cliente não possa favoritar 
    o mesmo produto mais de uma vez.    
    """
    __tablename__ = "favoritos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    produto_id = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('cliente_id', 'produto_id', name='uix_cliente_produto'),)
