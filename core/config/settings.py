from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    db_host: str = os.getenv("DB_HOST", "db")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_pass: str = os.getenv("DB_PASS", "postgres")
    db_name: str = os.getenv("DB_NAME", "postgres")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
