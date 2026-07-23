"""
Script de recuperação ÚNICA (não faz parte do projeto permanente): extrai a
árvore completa da categoria "Orientações Curriculares" (raiz id=64 no dump
Postgres de 2026-07-23 15:05) + todos os conteúdos e anexos ligados a ela,
a partir do backup docker_backups/backup_20260723_150450/banco_postgres.sql,
e gera um arquivo JSON pronto para importar via Django (loaddata-like custom).
"""
import re
import csv
import io
import json

DUMP = r"C:\ridan\Claude\Projects\Site Curriculos SEDU\docker_backups\backup_20260723_150450\banco_postgres.sql"

def parse_copy_block(text, table_name):
    pattern = rf"^COPY public\.{re.escape(table_name)} \(([^)]+)\) FROM stdin;\n(.*?)\n\\\.\n"
    m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if not m:
        raise ValueError(f"Bloco COPY nao encontrado para {table_name}")
    cols = [c.strip() for c in m.group(1).split(',')]
    body = m.group(2)
    rows = []
    for line in body.split('\n'):
        if not line:
            continue
        # Postgres COPY usa TAB como separador e \N para NULL
        parts = line.split('\t')
        row = {}
        for col, val in zip(cols, parts):
            if val == r'\N':
                row[col] = None
            else:
                # unescape sequencias do formato COPY (\\t, \\n, \\\\)
                val = val.replace('\\t', '\t').replace('\\n', '\n').replace('\\r', '\r').replace('\\\\', '\\')
                row[col] = val
        rows.append(row)
    return cols, rows

with open(DUMP, 'r', encoding='utf-8') as f:
    text = f.read()

cat_cols, cat_rows = parse_copy_block(text, 'conteudo_categoria')
cont_cols, cont_rows = parse_copy_block(text, 'conteudo_conteudo')
anexo_cols, anexo_rows = parse_copy_block(text, 'conteudo_anexo')

cat_by_id = {int(r['id']): r for r in cat_rows}

RAIZ_ID = 64  # "Orientações Curriculares", confirmado via grep manual

# BFS para achar todos os descendentes de RAIZ_ID
alvo_ids = {RAIZ_ID}
mudou = True
while mudou:
    mudou = False
    for r in cat_rows:
        pai = r['categoria_pai_id']
        if pai is not None and int(pai) in alvo_ids and int(r['id']) not in alvo_ids:
            alvo_ids.add(int(r['id']))
            mudou = True

categorias_recuperar = [cat_by_id[i] for i in alvo_ids]
# ordena por profundidade (raiz primeiro) para inserir respeitando FK categoria_pai_id
def profundidade(cat_id, cache={}):
    if cat_id in cache:
        return cache[cat_id]
    cat = cat_by_id[cat_id]
    pai = cat['categoria_pai_id']
    if pai is None or int(pai) not in cat_by_id:
        d = 0
    else:
        d = 1 + profundidade(int(pai))
    cache[cat_id] = d
    return d

categorias_recuperar.sort(key=lambda r: profundidade(int(r['id'])))

conteudos_recuperar = [r for r in cont_rows if r['categoria_id'] is not None and int(r['categoria_id']) in alvo_ids]
conteudo_ids = {int(r['id']) for r in conteudos_recuperar}

anexos_recuperar = [
    r for r in anexo_rows
    if (r['categoria_id'] is not None and int(r['categoria_id']) in alvo_ids)
    or (r['conteudo_id'] is not None and int(r['conteudo_id']) in conteudo_ids)
]

print(f"Categorias a recuperar: {len(categorias_recuperar)}")
for r in categorias_recuperar:
    print(f"  id={r['id']} nome={r['nome']!r} pai={r['categoria_pai_id']}")
print(f"Conteudos a recuperar: {len(conteudos_recuperar)}")
print(f"Anexos a recuperar: {len(anexos_recuperar)}")

out = {
    'categoria_cols': cat_cols,
    'categorias': categorias_recuperar,
    'conteudo_cols': cont_cols,
    'conteudos': conteudos_recuperar,
    'anexo_cols': anexo_cols,
    'anexos': anexos_recuperar,
}
OUT_PATH = r"C:\ridan\Claude\Projects\Site Curriculos SEDU\scripts_recuperacao\dados_recuperados.json"
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"Salvo em {OUT_PATH}")
