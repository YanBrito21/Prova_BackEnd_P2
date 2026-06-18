# 1. Usa uma imagem oficial leve do Python
FROM python:3.12-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Evita que o Python escreva arquivos .pyc no disco e ativa o buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o restante do código do projeto para dentro do container
COPY . .

# 6. Expõe a porta que a API vai rodar
EXPOSE 8000

# 7. Comando padrão para iniciar a API usando o Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]