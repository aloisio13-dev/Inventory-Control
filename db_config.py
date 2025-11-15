import sqlite3

def popular_db():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            quantidade INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            tipo TEXT CHECK(tipo IN ('entrada', 'saida')),
            quantidade INTEGER,
            data TEXT,
            FOREIGN KEY(material_id) REFERENCES materiais(id)
        )
    ''')

    conn.commit()
    conn.close()
