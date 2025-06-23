"""
Módulo de configuração e inicialização do banco de dados SQLAlchemy.

Responsável por criar engine, sessão e base declarativa.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config.settings import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
