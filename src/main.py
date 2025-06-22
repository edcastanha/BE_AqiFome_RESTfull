from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from core.externos.fake_store_client import FakeStoreClient
from core.config.db import SessionLocal, Base, engine
from core.domain.cliente import Cliente, ClienteCreate
from core.domain.favorito import (
    FavoritoCreate,
    FavoritoCreateRequest,
    FavoritoResponse,
)
from core.repository.cliente_repository import ClienteRepository
from core.repository.favorito_repository import FavoritoRepository
from core.repository.produto_repository import ProdutoRepository
from core.service.cliente_service import ClienteService
from core.service.favorito_service import FavoritoService
from core.security.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

logger = logging.getLogger("uvicorn.error")
# Configuração do logger
logging.basicConfig(
    level=logging.WARN,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)   

app = FastAPI(title="AqiFome RESTful API")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_produto_repository(db: Session = Depends(get_db)) -> ProdutoRepository:
    return ProdutoRepository(db)

def get_fake_store_client() -> FakeStoreClient:
    return FakeStoreClient()

def get_favorito_service(
    db: Session = Depends(get_db),
    produto_repository: ProdutoRepository = Depends(get_produto_repository),
    fake_store_client: FakeStoreClient = Depends(get_fake_store_client)
) -> FavoritoService:
    return FavoritoService(
        repository=FavoritoRepository(db),
        produto_repository=produto_repository,
        fake_store_client=fake_store_client
    )

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    cliente_repo = ClienteRepository(db)
    user = cliente_repo.get_by_email(email=form_data.username)
    if not user or not verify_password(form_data.password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def root():
    return {"message": "API Online"}

# --- Clientes ---
@app.post("/clientes", response_model=Cliente)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    service = ClienteService(ClienteRepository(db))
    try:
        hashed_password = get_password_hash(cliente.senha)
        cliente_com_senha_hash = cliente.model_copy(
            update={"senha": hashed_password}
        )
        return service.criar_cliente(cliente_com_senha_hash)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/clientes", response_model=list[Cliente])
def listar_clientes(
    db: Session = Depends(get_db), current_user: Cliente = Depends(get_current_user)
):
    service = ClienteService(ClienteRepository(db))
    return service.listar_clientes()

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_user),
):
    service = ClienteService(ClienteRepository(db))
    cliente = service.buscar_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def atualizar_cliente(
    cliente_id: int,
    cliente: Cliente,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_user),
):
    service = ClienteService(ClienteRepository(db))
    atualizado = service.atualizar_cliente(cliente_id, cliente)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return atualizado

@app.delete("/clientes/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_user),
):
    service = ClienteService(ClienteRepository(db))
    if not service.deletar_cliente(cliente_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"ok": True}

# --- Favoritos ---
@app.post(
    "/clientes/{cliente_id}/favoritos",
    response_model=list[FavoritoResponse],  # Correção aqui
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar um produto aos favoritos de um cliente",
    tags=["Favoritos"],
)
async def adicionar_favoritos(
    cliente_id: int,
    request_data: FavoritoCreateRequest,
    service: FavoritoService = Depends(get_favorito_service),
    current_user: Cliente = Depends(get_current_user),
):
    """
    Adiciona um ou mais produtos à lista de favoritos de um cliente.
    """
    if cliente_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted",
        )
    try:
        favoritos_criados = await service.adicionar_favoritos(
            cliente_id=cliente_id, produto_ids=request_data.produto_ids
        )
        return favoritos_criados
    except ValueError as e:
        logger.error(f"Erro ao adicionar favoritos: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao adicionar favoritos: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {e}")

@app.get("/clientes/{cliente_id}/favoritos", response_model=list[FavoritoResponse])
def listar_favoritos(
    cliente_id: int,
    service: FavoritoService = Depends(get_favorito_service),
    current_user: Cliente = Depends(get_current_user),
):
    if cliente_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted",
        )
    return service.listar_favoritos(cliente_id)


@app.delete("/clientes/{cliente_id}/favoritos/{produto_id}")
def remover_favorito(
    cliente_id: int,
    produto_id: int,
    service: FavoritoService = Depends(get_favorito_service),
    current_user: Cliente = Depends(get_current_user),
):
    if cliente_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted",
        )
    if not service.remover_favorito(cliente_id, produto_id):
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    return {"ok": True}
