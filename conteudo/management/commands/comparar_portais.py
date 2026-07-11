# -*- coding: utf-8 -*-
"""
FASE 2 da importação do conteúdo remanescente — COMPARAÇÃO (somente leitura).

Cruza o inventário do portal antigo (importacao/inventario_wordpress.json,
gerado pela Fase 1) com o banco atual do Django e gera o relatório
importacao/relatorio_comparacao.md com três listas:

  - JÁ EXISTE  : página antiga com correspondente no portal novo
  - FALTA      : página antiga sem correspondente (candidata a importar)
  - AMBÍGUO    : parecido mas não idêntico — decisão manual

NÃO grava nada no banco. Uso:
    python manage.py comparar_portais
"""
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from conteudo.models import Anexo, Categoria, Conteudo

PASTA = Path(settings.BASE_DIR) / 'importacao'
INVENTARIO = PASTA / 'inventario_wordpress.json'
RELATORIO = PASTA / 'relatorio_comparacao.md'

# Páginas do WP que são infraestrutura do site antigo, não conteúdo
SLUGS_IGNORAR = {
    'home', 'inicio', 'pagina-inicial', 'sample-page', 'pagina-exemplo',
    'contato', 'fale-conosco', 'mapa-do-site', 'busca', 'search',
    'politica-de-cookies',
}

# Páginas "hub" do WP cujo equivalente no site novo é um BOTÃO (categoria)
# com slug/título diferentes — o casamento automático não os encontra.
# WP slug -> slug da categoria no Django. Se o slug não existir no banco
# (bancos diferem entre máquinas), o item cai em FALTA normalmente (seguro).
ALIASES_WP_CATEGORIA = {
    'olimpiadas': 'olimpiadas-e-competicoes',
    'rpe': 'rotinas-pedagogicas-escolares',
    'rpe2025': 'rotinas-pedagogicas-escolares',
    'livrodidatico': 'livro-didatico-e-materiais',
    'documentoscurriculares': 'documentos-curriculares',
    'orientacoescurriculares': 'orientacoes-curriculares-2026',
    'projetointegrador': 'projetos-integradores',
}


def normalizar_url(url):
    """Remove protocolo, www, barra final e caixa — para comparar URLs."""
    u = (url or '').strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    return u.rstrip('/')


def normalizar_texto(texto):
    """minúsculas + sem acento + espaços únicos — para comparar títulos."""
    t = unicodedata.normalize('NFKD', texto or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', t.lower()).strip()


class Command(BaseCommand):
    help = 'Compara o inventário do portal antigo com o banco atual (somente leitura)'

    def handle(self, *args, **options):
        if not INVENTARIO.exists():
            self.stderr.write(
                'Inventário não encontrado. Rode antes: '
                'python importacao/inventariar_wordpress.py')
            return

        inv = json.loads(INVENTARIO.read_text(encoding='utf-8'))
        paginas = [p for p in inv['paginas'] if p['status'] == 'publish']
        posts = [p for p in inv['posts'] if p['status'] == 'publish']
        itens_wp = paginas + posts

        # ── Índices do banco novo ─────────────────────────────────────
        conteudos = list(Conteudo.objects.all().values(
            'pk', 'titulo', 'slug', 'url_externa', 'tipo', 'status'))
        categorias = list(Categoria.objects.all().values(
            'pk', 'nome', 'slug', 'ativa'))

        por_url = {}
        for c in conteudos:
            if c['url_externa']:
                por_url[normalizar_url(c['url_externa'])] = ('conteudo', c)

        cont_por_slug = {c['slug']: c for c in conteudos}
        cat_por_slug = {c['slug']: c for c in categorias}
        cont_por_titulo = {normalizar_texto(c['titulo']): c for c in conteudos}
        cat_por_nome = {normalizar_texto(c['nome']): c for c in categorias}

        # Blob com todos os corpos + descrições: acha URLs de documentos
        # que já estão citadas dentro de páginas/textos do site novo
        blob = ' '.join(Conteudo.objects.exclude(corpo='')
                        .values_list('corpo', flat=True))
        blob += ' '.join(Categoria.objects.exclude(descricao='')
                         .values_list('descricao', flat=True))
        blob_norm = normalizar_url(blob)  # normaliza igual às URLs

        urls_anexos = set()
        for a in Anexo.objects.all():
            if a.arquivo:
                urls_anexos.add(normalizar_url(str(a.arquivo)))

        # ── Comparação item a item ────────────────────────────────────
        ja_existe, falta, ambiguo, ignorados = [], [], [], []
        titulos_novos = list(cont_por_titulo) + list(cat_por_nome)

        for p in itens_wp:
            if p['slug'] in SLUGS_IGNORAR:
                ignorados.append(p)
                continue

            url_n = normalizar_url(p['url'])
            titulo_n = normalizar_texto(p['titulo'])
            docs = [l for l in p['links']
                    if l['tipo'] in ('arquivo_wp', 'google_drive', 'youtube')]
            docs_cobertos = sum(
                1 for l in docs
                if normalizar_url(l['url']) in por_url
                or normalizar_url(l['url']) in blob_norm)
            cobertura = f'{docs_cobertos}/{len(docs)}' if docs else '—'

            info = {
                'wp': p, 'cobertura_docs': cobertura,
                'docs_total': len(docs), 'docs_cobertos': docs_cobertos,
            }

            # 0) apelido manual: página-hub do WP -> botão do site novo
            alias = ALIASES_WP_CATEGORIA.get(p['slug'])
            if alias and alias in cat_por_slug:
                c = cat_por_slug[alias]
                info['match'] = (f'hub (apelido manual) → botão/categoria '
                                 f'"{c["nome"]}" (pk {c["pk"]})')
                ja_existe.append(info)
                continue
            # 1) URL exata
            if url_n in por_url:
                c = por_url[url_n][1]
                info['match'] = f'URL → conteúdo "{c["titulo"]}" (pk {c["pk"]})'
                ja_existe.append(info)
                continue
            # 2) slug de conteúdo / categoria
            if p['slug'] in cont_por_slug:
                c = cont_por_slug[p['slug']]
                info['match'] = f'slug → conteúdo "{c["titulo"]}" (pk {c["pk"]})'
                ja_existe.append(info)
                continue
            if p['slug'] in cat_por_slug:
                c = cat_por_slug[p['slug']]
                info['match'] = f'slug → botão/categoria "{c["nome"]}" (pk {c["pk"]})'
                ja_existe.append(info)
                continue
            # 3) título normalizado
            if titulo_n in cont_por_titulo:
                c = cont_por_titulo[titulo_n]
                info['match'] = f'título → conteúdo "{c["titulo"]}" (pk {c["pk"]})'
                ja_existe.append(info)
                continue
            if titulo_n in cat_por_nome:
                c = cat_por_nome[titulo_n]
                info['match'] = f'título → botão/categoria "{c["nome"]}" (pk {c["pk"]})'
                ja_existe.append(info)
                continue
            # 4) fuzzy — parecido mas não idêntico = ambíguo
            melhor, melhor_r = None, 0.0
            for t in titulos_novos:
                r = SequenceMatcher(None, titulo_n, t).ratio()
                if r > melhor_r:
                    melhor, melhor_r = t, r
            if melhor_r >= 0.85:
                info['match'] = f'parecido ({melhor_r:.0%}) com "{melhor}"'
                ambiguo.append(info)
                continue

            info['match'] = ''
            falta.append(info)

        # ── Relatório ─────────────────────────────────────────────────
        linhas = [
            '# Relatório de comparação — portal antigo × portal novo',
            '',
            f'- Gerado em: {inv["gerado_em"][:19]} (inventário) / agora (comparação)',
            f'- Itens analisados do portal antigo: **{len(itens_wp)}** '
            f'({len(paginas)} páginas + {len(posts)} posts publicados)',
            f'- Banco novo no momento da comparação: {len(conteudos)} conteúdos, '
            f'{len(categorias)} botões/categorias',
            '',
            '| Situação | Quantidade |',
            '|---|---|',
            f'| ✅ Já existe no portal novo | {len(ja_existe)} |',
            f'| ❌ FALTA (candidato a importar) | {len(falta)} |',
            f'| ⚠️ Ambíguo (decisão manual) | {len(ambiguo)} |',
            f'| ⏭️ Ignorado (página de infraestrutura) | {len(ignorados)} |',
            '',
            '"Cobertura de docs" = quantos dos arquivos/links citados na página',
            'antiga já existem no portal novo (como conteúdo ou dentro de textos).',
            '',
        ]

        def tabela(titulo, itens, com_match=True):
            linhas.append(f'## {titulo} ({len(itens)})')
            linhas.append('')
            if not itens:
                linhas.append('*Nenhum item.*')
                linhas.append('')
                return
            cab = '| Título (portal antigo) | URL antiga | Cobertura de docs |'
            sep = '|---|---|---|'
            if com_match:
                cab += ' Correspondência |'
                sep += '---|'
            linhas.append(cab)
            linhas.append(sep)
            for i in sorted(itens, key=lambda x: normalizar_texto(x['wp']['titulo'])):
                p = i['wp']
                caminho = p['url'].replace(
                    'https://curriculo.sedu.es.gov.br/curriculo/', '/')
                linha = (f'| {p["titulo"][:70]} | `{caminho}` '
                         f'| {i["cobertura_docs"]} |')
                if com_match:
                    linha += f' {i["match"]} |'
                linhas.append(linha)
            linhas.append('')

        tabela('❌ FALTA — candidatos a importar', falta, com_match=False)
        tabela('⚠️ AMBÍGUO — revisar manualmente', ambiguo)
        tabela('✅ JÁ EXISTE — nada a fazer', ja_existe)

        if ignorados:
            linhas.append(f'## ⏭️ Ignorados ({len(ignorados)})')
            linhas.append('')
            for p in ignorados:
                linhas.append(f'- {p["titulo"]} (`{p["slug"]}`)')
            linhas.append('')

        RELATORIO.write_text('\n'.join(linhas), encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(
            f'\nRelatório salvo em {RELATORIO}\n'
            f'  Já existe: {len(ja_existe)} | FALTA: {len(falta)} | '
            f'Ambíguo: {len(ambiguo)} | Ignorado: {len(ignorados)}'))
