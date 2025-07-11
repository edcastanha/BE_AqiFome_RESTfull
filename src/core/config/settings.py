from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
import os
import logging

# Configurando logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente.

    Atributos:
        db_host (str): Host do banco de dados.
        db_port (str): Porta do banco de dados.
        db_user (str): Usuário do banco de dados.
        db_pass (str): Senha do banco de dados.
        db_name (str): Nome do banco de dados.
        secret_key (str): Chave secreta para assinar tokens JWT.
        algorithm (str): Algoritmo de assinatura JWT.
        access_token_expire_minutes (int): Tempo de expiração do token de acesso.
    """

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_pass: str = os.getenv("DB_PASS", "postgres")
    db_name: str = os.getenv("DB_NAME", "postgres")
    secret_key: str = os.getenv("SECRET_KEY", "22fe53ced2c099e3f81f42cbb1ef7e2daeb120cf858184c25072d9cce611e2bb")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Mantendo model_config apenas para compatibilidade com o Pydantic
    model_config = {
        "extra": "ignore"
    }

    def __init__(self, **kwargs):
        """
        Inicializa as configurações e valida o host do banco de dados.
        """
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
        """
        Monta a URL de conexão com o banco de dados PostgreSQL.

        Returns:
            str: URL de conexão.
        Raises:
            ValueError: Se alguma configuração estiver ausente.
        """
        if not self.db_host or not self.db_port or not self.db_user or not self.db_pass or not self.db_name:
            logger.error("Configuração do banco de dados incompleta")
            raise ValueError("Configuração do banco de dados incompleta")
        logger.info(f"Construindo URL do banco de dados com host: {self.db_host}, porta: {self.db_port}, usuário: {self.db_user}")
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

def get_settings() -> Settings:
    """
    Retorna uma instância das configurações da aplicação.

    Returns:
        Settings: Instância de Settings.
    """
    return Settings()
