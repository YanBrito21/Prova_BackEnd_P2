import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Força a URL do Banco de Testes na porta 5433 antes de importar a aplicação
DATABASE_URL_TEST = "postgresql://postgres:postgres_password@localhost:5433/ecommerce_test"
os.environ["DATABASE_URL"] = DATABASE_URL_TEST

from main import app
from app.database import get_db
from app.database import Base

# 2. Configura o Engine e a Sessão exclusivos para o ambiente de testes
engine_test = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="function")
def db_session():
    """Garante uma sessão limpa por função de teste."""
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Cria as tabelas, substitui a injeção de dependência do FastAPI pelo banco 
    de teste, fornece o TestClient e destrói as tabelas no teardown[cite: 60].
    """
    # (a) Cria todas as tabelas limpas no banco de dados real do Docker [cite: 60]
    Base.metadata.create_all(bind=engine_test)
    
    # (b) Override da dependência get_db da API [cite: 60]
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = _get_db_override
    
    # (c) Faz o yield do TestClient para o teste rodar [cite: 60]
    with TestClient(app) as test_client:
        yield test_client
        
    # Limpa as overrides após o teste
    app.dependency_overrides.clear()
    
    # (d) Destrói todas as tabelas no teardown para isolar o próximo teste [cite: 60]
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def produto_existente(client):
    """Fixture auxiliar que cria um produto padrão no banco[cite: 61]."""
    payload = {
        "nome": "Produto Base Teste",
        "preco": 49.90,
        "estoque": 10,
        "ativo": True
    }
    response = client.post("/produtos", json=payload)
    return response.json()