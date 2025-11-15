#!/usr/bin/env python3
"""
Script para visualizar dados do banco estoque.db
Sem abrir no VSCode (evita CPU alta com arquivo binário)
"""

import sqlite3
import sys

def view_all():
    """Exibe todos os dados principais do banco"""
    conn = sqlite3.connect('estoque.db')
    cur = conn.cursor()

    print('\n' + '='*80)
    print('BANCO DE DADOS: estoque.db')
    print('='*80)

    # Tabelas
    print('\n[TABELAS]')
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for t in cur.fetchall():
        print(f'  - {t[0]}')

    # Categorias
    print('\n[CATEGORIAS]')
    cur.execute("SELECT id, nome FROM categorias ORDER BY id;")
    categories = cur.fetchall()
    if categories:
        for r in categories:
            print(f'  ID {r[0]}: {r[1]}')
    else:
        print('  (nenhuma)')

    # Materiais
    print('\n[MATERIAIS]')
    cur.execute("SELECT COUNT(*) FROM materiais;")
    total = cur.fetchone()[0]
    print(f'  Total: {total} produtos\n')
    
    cur.execute("SELECT id, nome, categoria, quantidade FROM materiais ORDER BY id;")
    for r in cur.fetchall():
        print(f'  ID {r[0]:2d}: {r[1]:25s} | Categoria: {str(r[2]):15s} | Qtd: {r[3]:5d}')

    # Movimentações (últimas)
    print('\n[ÚLTIMAS MOVIMENTAÇÕES]')
    cur.execute("SELECT COUNT(*) FROM movimentacoes;")
    total_mov = cur.fetchone()[0]
    print(f'  Total: {total_mov} registros\n')
    
    cur.execute("""
        SELECT m.id, m.material_id, mat.nome, m.tipo, m.quantidade, m.data 
        FROM movimentacoes m 
        JOIN materiais mat ON m.material_id = mat.id 
        ORDER BY m.data DESC LIMIT 15
    """)
    for r in cur.fetchall():
        print(f'  {r[0]:3d} | Material ID {r[1]:2d} ({r[2]:20s}) | {r[3]:7s} x {r[4]:4d} | {r[5]}')

    conn.close()
    print('\n' + '='*80 + '\n')

if __name__ == '__main__':
    try:
        view_all()
    except Exception as e:
        print(f'Erro ao ler banco: {e}', file=sys.stderr)
        sys.exit(1)
