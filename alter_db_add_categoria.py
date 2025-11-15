import sqlite3
import shutil
import os
import sys

DB_PATH = 'estoque.db'
BACKUP_PATH = 'estoque.db.bak'

print('Projeto CWD:', os.getcwd())

# 1) backup
if os.path.exists(DB_PATH):
    print(f'Criando backup: {BACKUP_PATH}')
    shutil.copy2(DB_PATH, BACKUP_PATH)
else:
    print(f'Banco {DB_PATH} não encontrado — nada a fazer.')
    sys.exit(1)

# 2) conectar e checar colunas
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
try:
    cur.execute("PRAGMA table_info(materiais);")
    cols_info = cur.fetchall()
    cols = [row[1] for row in cols_info]
    print('Colunas atuais na tabela materiais:', cols)

    if 'categoria' in cols:
        print("A coluna 'categoria' já existe. Nenhuma alteração necessária.")
    else:
        print("Adicionando coluna 'categoria' (TEXT) na tabela materiais...")
        cur.execute("ALTER TABLE materiais ADD COLUMN categoria TEXT")
        conn.commit()
        cur.execute("PRAGMA table_info(materiais);")
        cols_info = cur.fetchall()
        cols = [row[1] for row in cols_info]
        print('Colunas após alteração:', cols)
        print('Migração concluída com sucesso.')

except Exception as e:
    print('Erro ao executar migração:', e)
    raise
finally:
    conn.close()
    print('Conexão com DB fechada.')
