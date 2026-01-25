FROM python:3.12-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY server.py .

# Criar diretórios necessários
RUN mkdir -p /app/docs/memoria

# Volume para persistência
VOLUME ["/app/docs"]

CMD ["python", "server.py"]
