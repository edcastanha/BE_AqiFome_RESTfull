from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
import os
import logging

# Configurando logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_pass: str = os.getenv("DB_PASS", "postgres")
    db_name: str = os.getenv("DB_NAME", "postgres")
    
    # Mantendo model_config apenas para compatibilidade com o Pydantic
    model_config = {
        "extra": "ignore"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(f"Configurações finais - Host: {self.db_host}, Port: {self.db_port}, DB: {self.db_name}")
        # Verificar se o host é alcançável
        import socket
        try:
            socket.gethostbyname(self.db_host)
            logger.info(f"Host {self.db_host} é alcançável via DNS")
        except socket.gaierror:
            logger.warning(f"Não foi possível resolver o host {self.db_host}. Verifique a configuração e a rede.")
        logger.info(f"DB_HOST na instância Settings: '{self.db_host}'")

    @property
    def database_url(self) -> str:
        if not self.db_host or not self.db_port or not self.db_user or not self.db_pass or not self.db_name:
            logger.error("Configuração do banco de dados incompleta")
            raise ValueError("Configuração do banco de dados incompleta")
        logger.info(f"Construindo URL do banco de dados com host: {self.db_host}, porta: {self.db_port}, usuário: {self.db_user}")
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

def get_settings() -> Settings:
    return Settings()
