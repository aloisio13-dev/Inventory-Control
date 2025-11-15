# Inventory Control (estoque_app)

Projeto simples de controle de estoque em Flask + SQLite.

## Requisitos
- Python 3.8+
- Virtualenv (recomendado)

## Como rodar
1. Ative o virtualenv:

```powershell
Set-Location C:\estoque_app
C:/estoque_app/venv/Scripts/Activate.ps1
```

2. Instale dependências (se necessário):

```powershell
C:/estoque_app/venv/Scripts/python.exe -m pip install -r requirements.txt
```

3. Inicie a API:

```powershell
C:/estoque_app/venv/Scripts/python.exe app.py
```

A API estará disponível em `http://127.0.0.1:5000/`.

## Endpoints principais
- `GET /` — página inicial (template)
- `GET /init` — (re)popula/ inicializa o DB
- `GET /estoque` — retorna lista de materiais
- `POST /entrada` — registra entrada: `{ "material_id": 1, "quantidade": 10 }`
- `POST /saida` — registra saída: `{ "material_id": 1, "quantidade": 2 }`
- `GET /historico` — consulta histórico, aceita `material_id`, `data_inicio`, `data_fim`

## Scripts úteis
- `alter_db_add_categoria.py` — adiciona coluna `categoria` caso não exista.
- `seed_db.py` — popula o banco com dados de teste.
- `view_db.py` — imprime dados do banco no terminal (evita abrir arquivo binário no editor).
- `cleanup_db.py` — remove registros sem categoria (executa backup antes).

## Postman
Importe `stock.postman_collection.json` no Postman. Use o environment `stock` com `baseUrl` = `http://127.0.0.1:5000`.

## Git
Este repositório contém os arquivos fonte (não inclui `estoque.db`).

