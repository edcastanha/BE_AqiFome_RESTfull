import os
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from pydantic import SecretStr

# Adiciona o diretório raiz ao path para encontrar os módulos da aplicação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config.db import SessionLocal
from core.domain.cliente import ClienteCreate
from core.service.cliente_service import ClienteService
from core.repository.cliente_repository import ClienteRepository

# Carrega variáveis do arquivo .env
load_dotenv()

def seed_database():
    """
    Popula o banco de dados com um usuário administrador inicial
    lido a partir de variáveis de ambiente.
    """
    db: Session = SessionLocal()
    try:
        admin_email = os.getenv("SEED_ADMIN_EMAIL")
        admin_password = os.getenv("SEED_ADMIN_PASSWORD")
        admin_nome = os.getenv("SEED_ADMIN_NAME")
        admin_tipo = os.getenv("SEED_ADMIN_TIPO")

        tipo_map = {"ADMIN": 1, "USER": 0}
        admin_tipo = tipo_map.get(admin_tipo.upper(), 1)

        if not admin_email or not admin_password:
            print("ERRO: As variáveis de ambiente SEED_ADMIN_EMAIL e SEED_ADMIN_PASSWORD devem ser definidas no arquivo .env")
            return

        print(f"Verificando se o usuário '{admin_email}' já existe...")
        
        cliente_repo = ClienteRepository(db)
        cliente_service = ClienteService(cliente_repo)

        if cliente_repo.get_by_email(admin_email):
            print(f"O usuário '{admin_email}' já existe. Nenhuma ação necessária.")
            return

        print(f"Criando usuário administrador: {admin_nome} ({admin_email})")        
        
        admin_user_data = ClienteCreate(
            nome=admin_nome,
            email=admin_email,
            senha=SecretStr(admin_password),
            tipo=admin_tipo
        )
        cliente_service.criar_cliente(admin_user_data)

        print("Usuário administrador criado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao criar o usuário administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()