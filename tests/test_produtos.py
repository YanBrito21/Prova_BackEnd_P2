import pytest
from fastapi import status

# ==============================================================================
# 1. CENÁRIOS POSITIVOS (HAPPY PATH) & ISOLAMENTO
# ==============================================================================

# Teste 1: Listar produtos quando o banco está vazio (Requisito da prova)
def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []  # Deve retornar uma lista vazia

# Teste 2: Criar produto e verificar persistência (Requisito da prova)
def test_criar_produto_sucesso(client):
    payload = {"nome": "Teclado Mecânico", "preco": 299.90, "estoque": 15, "ativo": True}
    response = client.post("/produtos", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    dados = response.json()
    assert "id" in dados
    assert dados["nome"] == payload["nome"]
    assert dados["preco"] == payload["preco"]

# Teste 3: Criar produto e verificar que aparece na listagem (Requisito da prova)
def test_criar_produto_e_verificar_na_listagem(client):
    payload = {"nome": "Mouse Gamer", "preco": 150.00, "estoque": 30}
    client.post("/produtos", json=payload)
    
    response = client.get("/produtos")
    dados = response.json()
    assert len(dados) == 1
    assert dados[0]["nome"] == "Mouse Gamer"

# Teste 4: Buscar produto por ID - Caso de Sucesso (Requisito da prova usando a fixture)
def test_buscar_produto_por_id_sucesso(client, produto_existente):
    id_produto = produto_existente["id"]
    response = client.get(f"/produtos/{id_produto}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == produto_existente["nome"]

# Teste 5: Deletar produto deve retornar 204 (Requisito da prova)
def test_deletar_produto_sucesso(client, produto_existente):
    id_produto = produto_existente["id"]
    response = client.delete(f"/produtos/{id_produto}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

# Teste 6: Deletar produto e confirmar remoção com GET subsequente (Requisito da prova)
def test_deletar_e_confirmar_remocao(client, produto_existente):
    id_produto = produto_existente["id"]
    
    # Deleta
    client.delete(f"/produtos/{id_produto}")
    
    # Confirma sumiço (deve dar 404)
    response = client.get(f"/produtos/{id_produto}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Teste 7: Valida que o banco está isolado entre execuções (Requisito da prova)
def test_validar_isolamento_do_banco(client):
    # Como a fixture recria o banco a cada teste, este teste começa zerado.
    # Se o isolamento falhar, resíduos de testes anteriores apareceriam aqui.
    response = client.get("/produtos")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


# ==============================================================================
# 2. CENÁRIOS NEGATIVOS (ERROS 404)
# ==============================================================================

# Teste 8: Buscar produto com ID inexistente (Requisito da prova)
def test_buscar_produto_id_inexistente(client):
    response = client.get("/produtos/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Produto não encontrado"

# Teste 9: Deletar produto inexistente (Requisito da prova)
def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Produto não encontrado"


# ==============================================================================
# 3. VALIDAÇÕES E PAYLOADS INVÁLIDOS (ERROS 422 - PARAMETRIZADO)
# ==============================================================================

# Teste 10: Teste parametrizado cobrindo múltiplos payloads inválidos (Requisito da prova)
@pytest.mark.parametrize(
    "payload_invalido",
    [
        {"nome": "", "preco": 10.0},                  # Nome vazio (Bloqueado pela melhoria min_length)
        {"nome": "   ", "preco": 10.0},                # Apenas espaços (Bloqueado pela melhoria strip_whitespace)
        {"nome": "Produto X", "preco": 0.0},           # Preço igual a zero (Bloqueado por gt=0)
        {"nome": "Produto Y", "preco": -5.5},          # Preço negativo (Bloqueado por gt=0)
        {"nome": "Produto Z", "preco": 10.0, "estoque": -1}, # Estoque negativo (Bloqueado por ge=0)
        {"preco": 10.0},                               # Faltando campo obrigatório 'nome'
    ]
)
def test_payloads_invalidos_retornam_422(client, payload_invalido):
    response = client.post("/produtos", json=payload_invalido)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY