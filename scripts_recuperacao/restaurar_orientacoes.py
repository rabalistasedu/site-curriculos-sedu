"""
Script de recuperação ÚNICA: recria as 20 categorias da árvore "Orientações
Curriculares" (excluídas localmente em 2026-07-23) a partir dos dados
extraídos do backup Postgres de hoje 15:05 (dados_recuperados.json),
recria o anexo de link, e reconecta os 127 conteúdos órfãos de volta às
categorias originais (só ajusta o campo categoria_id, não toca em mais
nada desses conteúdos — preserva qualquer edição feita neles depois).

Rodar com: python manage.py shell < scripts_recuperacao/restaurar_orientacoes.py
"""
import json
from django.utils.dateparse import parse_datetime
from conteudo.models import Categoria, Conteudo, Anexo

with open(r'scripts_recuperacao/dados_recuperados.json', encoding='utf-8') as f:
    data = json.load(f)


def to_bool(v):
    return v == 't'


def to_int_or_none(v):
    return int(v) if v not in (None, '') else None


print('=== 1) Recriando categorias (ordem: raiz primeiro) ===')
criadas = 0
for row in data['categorias']:
    pk = int(row['id'])
    if Categoria.objects.filter(pk=pk).exists():
        print(f'  id={pk} ja existe, pulando (nao sobrescreve)')
        continue
    pai_id = to_int_or_none(row['categoria_pai_id'])
    Categoria.objects.create(
        pk=pk,
        nome=row['nome'],
        slug=row['slug'],
        descricao=row['descricao'] or '',
        icone=row['icone'] or '',
        imagem=row['imagem'] or '',
        ordem=int(row['ordem']),
        ativa=to_bool(row['ativa']),
        categoria_pai_id=pai_id,
        mostrar_menu_superior=to_bool(row['mostrar_menu_superior']),
        mostrar_navegue_area=to_bool(row['mostrar_navegue_area']),
        icone_imagem=row['icone_imagem'] or '',
        mostrar_conteudos_recentes=to_bool(row['mostrar_conteudos_recentes']),
        url_externa=row['url_externa'] or '',
        mostrar_area_central=to_bool(row['mostrar_area_central']),
        mostrar_como_card=to_bool(row['mostrar_como_card']),
        icone_altura=to_int_or_none(row['icone_altura']),
        icone_largura=to_int_or_none(row['icone_largura']),
    )
    criadas += 1
    print(f'  id={pk} nome={row["nome"]!r} pai={pai_id} -> criada')
print(f'Total categorias criadas: {criadas}')

print()
print('=== 2) Recriando anexo (link) ===')
for row in data['anexos']:
    pk = int(row['id'])
    if Anexo.objects.filter(pk=pk).exists():
        print(f'  anexo id={pk} ja existe, pulando')
        continue
    Anexo.objects.create(
        pk=pk,
        arquivo=row['arquivo'] or '',
        nome=row['nome'] or '',
        ordem=int(row['ordem']),
        conteudo_id=to_int_or_none(row['conteudo_id']),
        categoria_id=to_int_or_none(row['categoria_id']),
        url=row['url'] or '',
    )
    print(f'  anexo id={pk} recriado (categoria_id={row["categoria_id"]})')

print()
print('=== 3) Reconectando conteudos orfaos (so ajusta categoria_id) ===')
reconectados = 0
nao_encontrados = []
for row in data['conteudos']:
    pk = int(row['id'])
    cat_id = to_int_or_none(row['categoria_id'])
    updated = Conteudo.objects.filter(pk=pk, categoria__isnull=True).update(categoria_id=cat_id)
    if updated:
        reconectados += 1
    else:
        nao_encontrados.append(pk)
print(f'Conteudos reconectados: {reconectados}')
if nao_encontrados:
    print(f'NAO reconectados (ja tinham categoria ou nao existem mais): {nao_encontrados}')

print()
print('=== Verificacao final ===')
raiz = Categoria.objects.filter(pk=64).first()
print('Categoria raiz restaurada:', raiz)
print('Total de subcategorias (recursivo esperado 19):', Categoria.objects.filter(pk__in=[int(c["id"]) for c in data["categorias"]]).count())
print('Total de conteudos hoje ligados a essa arvore:', Conteudo.objects.filter(categoria_id__in=[int(c["id"]) for c in data["categorias"]]).count())
