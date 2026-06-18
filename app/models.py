from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # 
    nome = Column(String, nullable=False) # 
    preco = Column(Float, nullable=False) # 
    estoque = Column(Integer, default=0, nullable=False) # 
    ativo = Column(Boolean, default=True, nullable=False) #