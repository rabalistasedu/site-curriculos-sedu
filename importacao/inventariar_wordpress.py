# -*- coding: utf-8 -*-
"""
FASE 1 da importação do conteúdo remanescente — INVENTÁRIO (somente leitura).

Baixa, via API REST do WordPress, tudo que existe no portal antigo
(https://curriculo.sedu.es.gov.br/curriculo/) e salva em
importacao/inventario_wordpress.json. NÃO toca no banco do Django.

Uso:  python importacao/inventariar_wordpress.py
      (com o venv ativado, ou venv\\Scripts\\python.exe importacao\\inventariar_wordpress.py)

Usa apenas a biblioteca padrão do Python — não precisa instalar nada.
"""
import json
import re
import sys
import time
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

BASE = 'https://curriculo.sedu.es.gov.br/curriculo'
API = BASE + '/wp-json/wp/v2'
PASTA = Path(__file__).resolve().parent
SAIDA = PASTA / 'inventario_wordpress.json'
HEADERS = {'User-Agent': 'Mozilla/5.0 (inventario-migracao-sedu)'}


def baixar(url, tentativas=3):
    """GET com retry simples; devolve bytes."""
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            if i == tentativas - 1:
                raise
            print(f'  ! erro em {url} ({e}), tentando de novo...')
            time.sleep(3)


def baixar_json(url):
    return json.loads(baixar(url).decode('utf-8'))


def baixar_colecao(endpoint, fields):
    """Percorre todas as páginas de um endpoint da API (per_page=100)."""
    itens = []
    pagina = 1
    while True:
        url = f'{API}/{endpoint}?per_page=100&page={pagina}&_fields={fields}'
        try:
            lote = baixar_json(url)
        except urllib.error.HTTPError as e:
            if e.code == 400:  # passou da última página
                break
            raise
        if not lote:
            break
        itens.extend(lote)
        print(f'  {endpoint}: página {pagina} -> {len(lote)} itens (total {len(itens)})')
        if len(lote) < 100:
            break
        pagina += 1
    return itens


# ── Extração de links do conteúdo HTML de cada página ─────────────────
RE_LINK = re.compile(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
                     re.IGNORECASE | re.DOTALL)
RE_TAGS = re.compile(r'<[^>]+>')


def classificar_url(url):
    u = url.lower()
    if '/wp-content/uploads/' in u:
        return 'arquivo_wp'
    if 'drive.google' in u or 'docs.google' in u:
        return 'google_drive'
    if 'youtube.com' in u or 'youtu.be' in u:
        return 'youtube'
    if 'curriculo.sedu.es.gov.br/curriculo' in u:
        return 'pagina_interna'
    if u.startswith('#') or u.startswith('mailto:') or u.startswith('tel:'):
        return 'ancora'
    return 'externo'


def extrair_links(html):
    links = []
    for href, texto in RE_LINK.findall(html or ''):
        texto_limpo = RE_TAGS.sub('', texto).strip()
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo)
        tipo = classificar_url(href)
        if tipo == 'ancora':
            continue
        links.append({'url': href, 'texto': texto_limpo[:200], 'tipo': tipo})
    return links


# ── Parse do menu de navegação da home antiga ──────────────────────────
class MenuParser(HTMLParser):
    """Extrai a hierarquia de itens de menu (li.menu-item) do HTML da home."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = []
        self.pilha = []        # pilha de listas-filho (níveis do menu)
        self.item_atual = None
        self.em_a = False
        self.dentro_menu = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = a.get('class', '')
        if tag == 'ul' and ('menu' in classes or self.dentro_menu):
            self.dentro_menu += 1
            if self.dentro_menu == 1:
                self.pilha = [self.raiz]
            else:
                filhos = self.item_atual.setdefault('filhos', []) if self.item_atual else self.raiz
                self.pilha.append(filhos)
        elif tag == 'li' and self.dentro_menu and 'menu-item' in classes:
            item = {'nome': '', 'url': '', 'filhos': []}
            self.pilha[-1].append(item)
            self.item_atual = item
        elif tag == 'a' and self.dentro_menu and self.item_atual is not None:
            self.em_a = True
            if not self.item_atual['url']:
                self.item_atual['url'] = a.get('href', '')

    def handle_endtag(self, tag):
        if tag == 'ul' and self.dentro_menu:
            self.dentro_menu -= 1
            if len(self.pilha) > 1:
                self.pilha.pop()
        elif tag == 'a':
            self.em_a = False

    def handle_data(self, data):
        if self.em_a and self.item_atual is not None:
            self.item_atual['nome'] = (self.item_atual['nome'] + ' ' + data.strip()).strip()


def limpar_menu(itens):
    """Remove itens vazios e a chave 'filhos' quando vazia."""
    limpos = []
    for it in itens:
        if not it['nome']:
            continue
        novo = {'nome': re.sub(r'\s+', ' ', it['nome']), 'url': it['url']}
        filhos = limpar_menu(it.get('filhos', []))
        if filhos:
            novo['filhos'] = filhos
        limpos.append(novo)
    return limpos


def main():
    print('=== FASE 1: Inventário do portal antigo (somente leitura) ===\n')

    print('[1/4] Baixando páginas via API...')
    paginas = baixar_colecao(
        'pages', 'id,slug,link,status,parent,menu_order,title,content')

    print('[2/4] Baixando posts via API...')
    posts = baixar_colecao('posts', 'id,slug,link,status,title,content')

    print('[3/4] Baixando HTML da home para extrair o menu...')
    home_html = baixar(BASE + '/').decode('utf-8', errors='replace')
    parser = MenuParser()
    parser.feed(home_html)
    menu = limpar_menu(parser.raiz)
    print(f'  menu: {len(menu)} itens de primeiro nível')

    print('[4/4] Processando páginas (limpando HTML e extraindo links)...')
    inventario_paginas = []
    for p in paginas:
        html = (p.get('content') or {}).get('rendered', '')
        inventario_paginas.append({
            'id': p['id'],
            'slug': p['slug'],
            'url': p['link'],
            'status': p['status'],
            'pai_id': p.get('parent', 0),
            'ordem_menu': p.get('menu_order', 0),
            'titulo': re.sub(r'\s+', ' ', RE_TAGS.sub('', (p.get('title') or {}).get('rendered', ''))).strip(),
            'tamanho_html': len(html),
            'links': extrair_links(html),
            'html': html,
        })

    inventario_posts = []
    for p in posts:
        html = (p.get('content') or {}).get('rendered', '')
        inventario_posts.append({
            'id': p['id'],
            'slug': p['slug'],
            'url': p['link'],
            'status': p['status'],
            'titulo': re.sub(r'\s+', ' ', RE_TAGS.sub('', (p.get('title') or {}).get('rendered', ''))).strip(),
            'tamanho_html': len(html),
            'links': extrair_links(html),
            'html': html,
        })

    total_links = sum(len(p['links']) for p in inventario_paginas)
    inventario = {
        'gerado_em': datetime.now().isoformat(),
        'origem': BASE,
        'totais': {
            'paginas': len(inventario_paginas),
            'posts': len(inventario_posts),
            'itens_menu_nivel1': len(menu),
            'links_encontrados': total_links,
        },
        'menu': menu,
        'paginas': inventario_paginas,
        'posts': inventario_posts,
    }

    SAIDA.write_text(json.dumps(inventario, ensure_ascii=False, indent=1),
                     encoding='utf-8')
    print(f'\nOK! Inventário salvo em {SAIDA}')
    print(f'  Páginas: {len(inventario_paginas)} | Posts: {len(inventario_posts)}'
          f' | Links dentro das páginas: {total_links}')


if __name__ == '__main__':
    sys.exit(main())
