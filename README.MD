# 🛒 E-Commerce Product Management API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

[cite_start]API REST completa e robusta para gerenciamento de catálogos de produtos de um pequeno e-commerce[cite: 23]. [cite_start]O projeto foi desenvolvido aplicando **Arquitetura Modular em Camadas**, validações estritas de dados com **Pydantic v2**, persistência relacional via **SQLAlchemy ORM** e uma suíte completa de testes automatizados executados contra um banco de dados real em container[cite: 9, 34].

---

## 🛠️ Arquitetura e Organização do Projeto

O projeto foi reestruturado seguindo as melhores práticas de mercado (*Clean Code* e Responsabilidade Única), dividindo as camadas lógicas para facilitar a manutenção e escalabilidade:

```text
seu_repositorio/
├── app/
│   ├── database.py    # Configuração de conexão e injeção do SQLAlchemy [cite: 35]
│   ├── models.py      # Modelagem das tabelas relacionais do banco [cite: 16]
│   ├── schemas.py     # Camada de validação de schemas de entrada/saída (Pydantic) [cite: 34]
│   └── routers.py     # Endpoints e regras de negócio da API [cite: 31]
├── tests/
│   ├── __init__.py
│   └── test_produtos.py # Suíte de testes automatizados com Pytest [cite: 46]
├── main.py            # Ponto de entrada e inicialização da aplicação [cite: 31, 65]
├── conftest.py        # Configuração de fixtures e isolamento de estado [cite: 59, 66]
├── docker-compose.yml # Orquestração dos containers de banco de dados [cite: 18, 38]
├── Dockerfile         # Instruções de empacotamento da aplicação [cite: 68]
├── pytest.ini         # Configurações globais do Pytest [cite: 69]
└── requirements.txt   # Dependências do projeto [cite: 67]
``` 

## 🚀 Como Executar a Infraestrutura (Docker)
O ambiente utiliza dois serviços PostgreSQL isolados para blindar o banco de desenvolvimento contra efeitos colaterais dos testes automatizados.  Subir os containers de banco de dados:Bashdocker-compose up -d
Confirmar se os serviços estão ativos e saudáveis (healthy):Bashdocker ps
Banco de Desenvolvimento (db_dev): Porta local 5432. Possui volume persistente para manter seus dados salvos.  Banco de Testes (db_test): Porta local 5433. Dados 100% voláteis e descartáveis.  🧪 Execução dos Testes e CoberturaA suíte conta com 15 cenários de testes executados de forma totalmente automatizada através do Pytest.  Para rodar os testes e exibir o relatório detalhado de cobertura de código, execute:  Bashpytest --cov=app -v

## 📈 Saída Esperada no Terminal

plugins: cov-7.1.0
collected 15 items

tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED          [  6%]
tests/test_produtos.py::test_criar_produto_sucesso PASSED               [ 13%]
tests/test_produtos.py::test_criar_produto_e_verificar_na_listagem PASSED [ 20%]
tests/test_produtos.py::test_buscar_produto_por_id_sucesso PASSED        [ 26%]
...
tests/test_produtos.py::test_payloads_invalidos_retornam_422[...] PASSED [100%]

---------- coverage: platform win32 ----------
Name              Stmts   Miss  Cover
-------------------------------------
app\database.py      11      0   100%
app\models.py         8      0   100%
app\routers.py       31      0   100%
app\schemas.py       13      0   100%
-------------------------------------
TOTAL                63      0   100%

================== 15 passed in 1.45s ==================

## 🛡️ Mecanismo de Isolamento entre os Testes
O isolamento impecável do estado do banco de dados entre cada execução é garantido pela fixture client estruturada no arquivo conftest.py com escopo de função (scope="function"):  
Criação Dinâmica: Antes de cada função de teste rodar individualmente, o ecossistema executa Base.metadata.create_all, gerando um esquema de tabelas limpo no container de testes (db_test).  
Injeção de Dependência: A fixture intercepta e substitui a sessão do banco original usando o recurso app.dependency_overrides do FastAPI.  
Destruição Rigorosa (Teardown): Imediatamente após a finalização de cada teste, o bloco pós-yield executa Base.metadata.drop_all, eliminando completamente as tabelas e dados gerados.  

Nota: Isso impossibilita qualquer efeito colateral ou persistência residual de dados para os testes subsequentes, permitindo que a suíte passe com sucesso independente da ordem de execução.  

## 🎯 Endpoints Principais da API
A documentação interativa e completa pode ser acessada localmente em: 👉 http://127.0.0.1:8000/docs

| Método | Rota | Status Esperado | Comportamento |
| :--- | :--- | :--- | :--- |
| **GET** | `/produtos` | `200` | Retorna a lista de todos os produtos do catálogo. |
| **POST** | `/produtos` | `201` | Valida, cria um novo produto e o retorna com o ID gerado. |
| **GET** | `/produtos/{id}` | `200 / 404` | Retorna o produto pelo ID ou lança erro se não existir. |
| **DELETE** | `/produtos/{id}` | `204 / 404` | Remove o produto do catálogo ou lança erro se não existir. |