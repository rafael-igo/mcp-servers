FROM python:3.11-slim

WORKDIR /app

# Instalar Docker CLI para gerenciar host
RUN apt-get update && apt-get install -y \
    docker.io \
    docker-compose \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar server
COPY server.py .

# Criar diretório de docs
RUN mkdir -p /app/docs

CMD ["python", "server.py"]
