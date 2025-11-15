#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de teste.
Insere produtos (materiais) na tabela 'materiais'.
"""

import sqlite3

def seed_materiais():
    conn = sqlite3.connect('estoque.db')
    cur = conn.cursor()

    # Dados de teste: (nome, categoria, quantidade)
    materiais = [
        ('Parafuso', 'Ferragens', 500),
        ('Martelo', 'Ferramentas', 15),
        ('Caneta Azul', 'Escritório', 200),
        ('Papel A4', 'Escritório', 50),
        ('Cimento 50kg', 'Construção', 30),
        ('Areia', 'Construção', 100),
        ('Prego 3"', 'Ferragens', 1000),
        ('Chave de Fenda', 'Ferramentas', 8),
        ('Chave Inglesa', 'Ferramentas', 5),
        ('Lâmpada LED', 'Elétrico', 40),
    ]

    print('Inserindo materiais no banco de dados...')
    for nome, categoria, quantidade in materiais:
        try:
            cur.execute(
                "INSERT INTO materiais (nome, categoria, quantidade) VALUES (?, ?, ?)",
                (nome, categoria, quantidade)
            )
            print(f'  ✓ Inserido: {nome} (categoria: {categoria}, qtd: {quantidade})')
        except sqlite3.IntegrityError as e:
            print(f'  ! {nome} já existe ou erro: {e}')

    conn.commit()
    
    # Mostra dados inseridos
    print('\nDados na tabela materiais:')
    cur.execute("SELECT id, nome, categoria, quantidade FROM materiais ORDER BY id")
    for row in cur.fetchall():
        print(f'  ID {row[0]}: {row[1]} ({row[2]}) - Qtd: {row[3]}')

    conn.close()
    print('\n✓ População do banco concluída.')

if __name__ == '__main__':
    seed_materiais()
