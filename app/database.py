import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# URL lida da variável de ambiente com fallback para dev [cite: 36]
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres_password@localhost:5432/ecommerce_dev")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency Injection para a Sessão do Banco [cite: 35]
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()