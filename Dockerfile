# Utiliza a imagem oficial do Python 3.12
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /api

# Copia os arquivos de dependências para o container
COPY ./src/requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY ./src .

COPY ./core ./core

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 