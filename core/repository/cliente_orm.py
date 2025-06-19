from sqlalchemy import Column, Integer, String
from src.core.config.db import Base

class ClienteORM(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
