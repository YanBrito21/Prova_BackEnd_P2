from pydantic import BaseModel, Field

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, strip_whitespace=True, description="Nome do produto")
    preco: float = Field(..., gt=0, description="Preço deve ser maior que zero")
    estoque: int = Field(default=0, ge=0, description="Estoque não pode ser negativo")
    ativo: bool = Field(default=True)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nome": "Controle Sem Fio PS5 DualSense",
                "preco": 429.90,
                "estoque": 15,
                "ativo": True
            }
        }