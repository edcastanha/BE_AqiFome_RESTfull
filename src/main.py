from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from core.externos.fake_store_client import FakeStoreClient
from core.config.db import SessionLocal, Base, engine
from core.domain.cliente import Cliente
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

@app.get("/")
def root():
    return {"message": "API Online"}

# --- Clientes ---
@app.post("/clientes", response_model=Cliente)
def criar_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    service = ClienteService(ClienteRepository(db))
    try:
        return service.criar_cliente(cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/clientes", response_model=list[Cliente])
def listar_clientes(db: Session = Depends(get_db)):
    service = ClienteService(ClienteRepository(db))
    return service.listar_clientes()

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(ClienteRepository(db))
    cliente = service.buscar_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: int, cliente: Cliente, db: Session = Depends(get_db)):
    service = ClienteService(ClienteRepository(db))
    atualizado = service.atualizar_cliente(cliente_id, cliente)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return atualizado

@app.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(ClienteRepository(db))
    if not service.deletar_cliente(cliente_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"ok": True}

# --- Favoritos ---
@app.post(
    "/clientes/{cliente_id}/favoritos",
    response_model=FavoritoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar um produto aos favoritos de um cliente",
    tags=["Favoritos"],
)
async def adicionar_favorito(
    cliente_id: int,
    request_data: FavoritoCreateRequest,
    
    service: FavoritoService = Depends(get_favorito_service),
):
    """
    Adiciona um produto à lista de favoritos de um cliente específico.
    """
    try:
        # O papel do endpoint é apenas preparar os dados para o serviço.
        favorito_para_criar = FavoritoCreate(
            cliente_id=cliente_id, produto_id=request_data.produto_id
        )

        favorito_criado = await service.adicionar_favorito(favorito_para_criar)
        return favorito_criado
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {e}")

@app.get("/clientes/{cliente_id}/favoritos", response_model=list[FavoritoResponse])
def listar_favoritos(cliente_id: int, service: FavoritoService = Depends(get_favorito_service)):
    return service.listar_favoritos(cliente_id)

@app.delete("/clientes/{cliente_id}/favoritos/{produto_id}")
def remover_favorito(cliente_id: int, produto_id: int, service: FavoritoService = Depends(get_favorito_service)):
    if not service.remover_favorito(cliente_id, produto_id):
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    return {"ok": True}
