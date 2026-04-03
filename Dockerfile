FROM python:3.9-slim

WORKDIR /app

# Instala as dependências
RUN pip install fastapi uvicorn boto3 python-multipart

# Copia o código para o container
COPY main.py .

# Comando para rodar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]