from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import ProdutoModel
from app.schemas import ProdutoCreate, ProdutoResponse

# Criando o roteador de forma organizada e modular
router = APIRouter(prefix="/produtos", tags=["Produtos"])

# 1. POST /produtos - Criar um novo produto (Status 201)
@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    # Criamos a instância do modelo com os dados validados do Pydantic
    novo_produto = ProdutoModel(**produto.model_dump())
    
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)  # Garante que o ID gerado pelo banco seja retornado
    return novo_produto

# 2. GET /produtos - Listar todos os produtos (Status 200)
@router.get("", response_model=List[ProdutoResponse], status_code=status.HTTP_200_OK)
@router.get("", response_model=List[ProdutoResponse], status_code=status.HTTP_200_OK)
def listar_produtos(
    nome: Optional[str] = Query(None, description="Filtrar produtos por parte do nome"),
    apenas_ativos: Optional[bool] = Query(None, description="Se True, filtra apenas produtos ativos"),
    db: Session = Depends(get_db)
):
    query = db.query(ProdutoModel)
    
    # Filtro dinâmico por nome (case-insensitive)
    if nome:
        query = query.filter(ProdutoModel.nome.ilike(f"%{nome}%"))
        
    # Filtro dinâmico por status ativo
    if apenas_ativos is not None:
        query = query.filter(ProdutoModel.ativo == apenas_ativos)
        
    return query.all()

# 3. GET /produtos/{id} - Buscar produto por ID (Status 200 ou 404)
@router.get("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
def buscar_produto_por_id(id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produto não encontrado"
        )
    return produto

# 4. DELETE /produtos/{id} - Remover produto (Status 204 ou 404)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produto não encontrado"
        )
        
    db.delete(produto)
    db.commit()
    return  # Retornos 204 não devem enviar corpo de resposta