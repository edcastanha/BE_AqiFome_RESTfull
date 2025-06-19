from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config.settings import get_settings

settings = get_settings()
engine = create_engine(settings.resolved_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
