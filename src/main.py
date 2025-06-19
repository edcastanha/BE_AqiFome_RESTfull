import uvicorn
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "API RESTful está funcionando!"}


@app.get("/itens")
def read_all():
    """
    Endpoint de leitura de todos os itens da API Public Fake Store.
    Retorna uma lista de itens disponíveis na loja.
    """
    print("Acessando a API externa...")
    # Fazendo uma requisição GET para a API externa
    try:
        response = requests.get('https://fakestoreapi.com:443/products', timeout=10)
        response.raise_for_status()
        return {"mensagem": "Endpoint de leitura de todos os itens", "itens": response.json()}
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API externa: {e}")
        return {"mensagem": "Erro ao acessar a API externa. Por favor, tente novamente mais tarde.", "itens": []}

