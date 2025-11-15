#!/usr/bin/env python3
"""
Script para remover registros antigos sem categoria (IDs 1-6)
Estes dados foram criados antes da migração que adicionou a coluna categoria
"""
import sqlite3

conn = sqlite3.connect('estoque.db')
cur = conn.cursor()

print("=" * 60)
print("LIMPEZA DE DADOS - Remover IDs antigos sem categoria")
print("=" * 60)

# Verificar quais registros serão deletados
print("\nRegistros a remover (IDs 1-6, sem categoria):")
cur.execute("SELECT id, nome, categoria, quantidade FROM materiais WHERE id <= 6;")
rows = cur.fetchall()
for r in rows:
    print(f"  ID {r[0]}: {r[1]} (categoria: {r[2]})")

if not rows:
    print("  Nenhum registro para remover!")
else:
    # Confirmar antes de deletar
    confirm = input(f"\nDeseja remover {len(rows)} registro(s)? (s/n): ").lower()
    if confirm == 's':
        cur.execute("DELETE FROM materiais WHERE id <= 6;")
        conn.commit()
        print(f"✓ {cur.rowcount} registros removidos com sucesso!")
        
        # Mostrar resumo final
        print("\nResumo após limpeza:")
        cur.execute("SELECT COUNT(*) FROM materiais;")
        total = cur.fetchone()[0]
        print(f"  Total de materiais: {total}")
        
        cur.execute("SELECT id, nome, categoria, quantidade FROM materiais ORDER BY id;")
        print("\n  Materiais restantes:")
        for r in cur.fetchall():
            print(f"    ID {r[0]:2d}: {r[1]:25s} | {str(r[2]):15s} | Qtd: {r[3]}")
    else:
        print("Operação cancelada.")

conn.close()
