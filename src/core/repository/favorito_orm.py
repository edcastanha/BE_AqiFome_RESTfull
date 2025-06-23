from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from core.config.db import Base

class FavoritoORM(Base):
    __tablename__ = "favoritos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    __table_args__ = (UniqueConstraint('cliente_id', 'produto_id', name='uix_cliente_produto'),)
