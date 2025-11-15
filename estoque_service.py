import sqlite3

def registrar_entrada(material_id, quantidade):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE materiais SET quantidade = quantidade + ? WHERE id = ?", (quantidade, material_id))
    cursor.execute("INSERT INTO movimentacoes (material_id, tipo, quantidade, data) VALUES (?, 'entrada', ?, datetime('now'))", (material_id, quantidade))
    conn.commit()
    conn.close()

def registrar_saida(material_id, quantidade):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE materiais SET quantidade = quantidade - ? WHERE id = ?", (quantidade, material_id))
    cursor.execute("INSERT INTO movimentacoes (material_id, tipo, quantidade, data) VALUES (?, 'saida', ?, datetime('now'))", (material_id, quantidade))
    conn.commit()
    conn.close()

def consultar_estoque():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, categoria, quantidade FROM materiais")
    resultado = cursor.fetchall()
    conn.close()

    estoque_formatado = []
    for linha in resultado:
        estoque_formatado.append({
            'id': linha[0],
            'nome': linha[1],
            'categoria': linha[2],
            'quantidade': linha[3]
        })

    return estoque_formatado

def historico_movimentacoes(material_id=None, data_inicio=None, data_fim=None):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    query = "SELECT * FROM movimentacoes WHERE 1=1"
    params = []
    if material_id:
        query += " AND material_id = ?"
        params.append(material_id)
    if data_inicio:
        query += " AND data >= ?"
        params.append(data_inicio)
    if data_fim:
        query += " AND data <= ?"
        params.append(data_fim)
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado
