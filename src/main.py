from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from core.config.db import SessionLocal, Base, engine
from core.domain.cliente import Cliente
from core.domain.favorito import Favorito
from core.repository.cliente_repository import ClienteRepository
from core.repository.favorito_repository import FavoritoRepository
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
@app.post("/clientes/{cliente_id}/favoritos", response_model=Favorito)
def adicionar_favorito(cliente_id: int, favorito: Favorito, db: Session = Depends(get_db)):
    service = FavoritoService(FavoritoRepository(db))
    try:
        favorito.cliente_id = cliente_id
        return service.adicionar_favorito(favorito)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/clientes/{cliente_id}/favoritos", response_model=list[Favorito])
def listar_favoritos(cliente_id: int, db: Session = Depends(get_db)):
    service = FavoritoService(FavoritoRepository(db))
    return service.listar_favoritos(cliente_id)

@app.delete("/clientes/{cliente_id}/favoritos/{produto_id}")
def remover_favorito(cliente_id: int, produto_id: int, db: Session = Depends(get_db)):
    service = FavoritoService(FavoritoRepository(db))
    if not service.remover_favorito(cliente_id, produto_id):
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    return {"ok": True}
