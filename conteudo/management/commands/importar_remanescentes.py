# -*- coding: utf-8 -*-
"""
FASE 4 da importação do conteúdo remanescente — IMPORTAÇÃO (idempotente).

Lê o inventário do portal antigo (importacao/inventario_wordpress.json) e
cria no banco APENAS o que não existe, seguindo o plano aprovado pelo Dan
em 2026-07-11:

  - 91 Itinerários de Formação Técnica e Profissional
        -> nova subcategoria "Formação Técnica e Profissional" dentro de IFA
  - 21 Ementas do Ensino Médio -> subcategoria "Ementas Curriculares"
  - 16 visualizadores de PDF do Currículo -> sub-botões de "Currículo Atual"
        (com checagem antiduplicação pelo link do PDF dentro do visualizador)
  - Diversos (consulta pública, edital, revistas Diálogos, notícia)

Garantias de segurança (regras do documento do plano):
  - Só cria registros (get_or_create); NUNCA altera nem exclui nada
  - Idempotente: rodar duas vezes dá no mesmo resultado
  - Links continuam apontando para o portal antigo (que seguirá no ar)
  - Log completo em importacao/log_importacao_<data>.txt

Uso:
    python manage.py importar_remanescentes --dry-run   # simula, não grava
    python manage.py importar_remanescentes             # grava
"""
import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.parse import unquote

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from conteudo.models import Categoria, Conteudo
from conteudo.management.commands.comparar_portais import (
    ALIASES_WP_CATEGORIA, SLUGS_IGNORAR, normalizar_texto, normalizar_url,
)

PASTA = Path(settings.BASE_DIR) / 'importacao'
INVENTARIO = PASTA / 'inventario_wordpress.json'

# Página vazia no WP (0 bytes de conteúdo) — nada a importar
SLUGS_DESCARTAR = {'elementor-24030'}

RE_IFRAME = re.compile(r'<iframe[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)

# Títulos bonitos para os visualizadores de PDF "-2" (títulos originais
# do WP são nomes de arquivo, ex.: "01_Guia_de_Implementacao")
TITULOS_VIEWERS = {
    '01_guia_de_implementacao-2': 'Guia de Implementação do Currículo',
    '02_ef_anos_iniciais-2': 'Currículo — Ensino Fundamental Anos Iniciais',
    '03_ef_anos_finais_vol_01_linguagens_e_codigos-2':
        'Currículo — EF Anos Finais Vol. 1: Linguagens e Códigos',
    '04_ef_anos_finais_vol_02_ciencias_da_natureza-2':
        'Currículo — EF Anos Finais Vol. 2: Ciências da Natureza',
    '05_ef_anos_finais_vol_03_ciencias_humanas-2':
        'Currículo — EF Anos Finais Vol. 3: Ciências Humanas',
    '06_em_vol_01_linguagens_e_codigos-2':
        'Currículo — Ensino Médio Vol. 1: Linguagens e Códigos',
    '07_em_vol_02_ciencias_da_natureza-2':
        'Currículo — Ensino Médio Vol. 2: Ciências da Natureza',
    '08_em_vol_03_ciencias_humanas-2':
        'Currículo — Ensino Médio Vol. 3: Ciências Humanas',
}


def limpar_titulo(t):
    t = unescape(t or '')
    return re.sub(r'\s+', ' ', t).strip()


def extrair_pdf_iframe(html):
    """Devolve a URL do documento embutido num visualizador (iframe)."""
    for src in RE_IFRAME.findall(html or ''):
        # visualizadores tipo pdf.js: viewer.html?file=<url codificada>
        m = re.search(r'[?&]file=([^&]+)', src)
        if m:
            return unquote(m.group(1))
        if '/wp-content/uploads/' in src:
            return src.split('#')[0]
    return ''


class Command(BaseCommand):
    help = 'Importa do portal antigo apenas o conteúdo que falta (idempotente)'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Simula a importação sem gravar nada')

    # ── categorias de destino (busca robusta + criação só se faltar) ──
    def cat_por_slug(self, *slugs):
        for s in slugs:
            c = Categoria.objects.filter(slug=s).first()
            if c:
                return c
        return None

    def cat_por_nome(self, trecho, pai=None):
        qs = Categoria.objects.all()
        if pai is not None:
            qs = qs.filter(categoria_pai=pai)
        alvo = normalizar_texto(trecho)
        for c in qs:
            if alvo in normalizar_texto(c.nome):
                return c
        return None

    def garantir_sub(self, nome, slug, pai):
        """Subcategoria: usa a existente ou cria (só quando realmente falta)."""
        c = self.cat_por_slug(slug) or self.cat_por_nome(nome, pai=pai)
        if c:
            return c, False
        if self.dry:
            self.log(f'  [dry-run] criaria botão "{nome}" dentro de "{pai}"')
            return None, True
        c = Categoria.objects.create(nome=nome, slug=slug, categoria_pai=pai,
                                     ativa=True, ordem=0)
        self.log(f'  + botão criado: "{nome}" (dentro de "{pai}")')
        self.criadas_categorias += 1
        return c, True

    def log(self, msg):
        self.stdout.write(msg)
        self.linhas_log.append(msg)

    # ── comando ────────────────────────────────────────────────────────
    def handle(self, *args, **options):
        self.dry = options['dry_run']
        self.linhas_log = []
        self.criadas_categorias = 0
        agora = datetime.now().strftime('%Y%m%d-%H%M')
        modo = 'SIMULAÇÃO (--dry-run, nada será gravado)' if self.dry else 'IMPORTAÇÃO REAL'
        self.log(f'=== Importação do conteúdo remanescente — {modo} ===\n')

        if not INVENTARIO.exists():
            self.stderr.write('Inventário não encontrado. Rode antes: '
                              'python importacao/inventariar_wordpress.py')
            return

        inv = json.loads(INVENTARIO.read_text(encoding='utf-8'))
        itens = [p for p in inv['paginas'] + inv['posts']
                 if p['status'] == 'publish'
                 and p['slug'] not in SLUGS_IGNORAR
                 and p['slug'] not in SLUGS_DESCARTAR]

        # ── o que já existe (mesma lógica da comparação) ──────────────
        conteudos = list(Conteudo.objects.all().values(
            'pk', 'titulo', 'slug', 'url_externa'))
        categorias = list(Categoria.objects.all().values('pk', 'nome', 'slug'))
        urls_db = {normalizar_url(c['url_externa'])
                   for c in conteudos if c['url_externa']}
        slugs_cont = {c['slug'] for c in conteudos}
        slugs_cat = {c['slug'] for c in categorias}
        titulos_db = ({normalizar_texto(c['titulo']) for c in conteudos}
                      | {normalizar_texto(c['nome']) for c in categorias})
        blob = ' '.join(Conteudo.objects.exclude(corpo='')
                        .values_list('corpo', flat=True))
        blob += ' '.join(Categoria.objects.exclude(descricao='')
                         .values_list('descricao', flat=True))
        blob_norm = normalizar_url(blob)

        def ja_existe(p):
            if ALIASES_WP_CATEGORIA.get(p['slug']) in slugs_cat:
                return True
            return (normalizar_url(p['url']) in urls_db
                    or p['slug'] in slugs_cont
                    or p['slug'] in slugs_cat
                    or normalizar_texto(p['titulo']) in titulos_db)

        faltantes = [p for p in itens if not ja_existe(p)]
        self.log(f'Itens do portal antigo analisados: {len(itens)} | '
                 f'já existiam: {len(itens) - len(faltantes)} | '
                 f'a importar: {len(faltantes)}\n')

        # ── categorias de destino ─────────────────────────────────────
        cat_ifa = (self.cat_por_slug('itinerarios-formativos-ifa')
                   or self.cat_por_nome('itinerarios formativos'))
        cat_ementas = (self.cat_por_slug('ementas-curriculares')
                       or self.cat_por_nome('ementas'))
        cat_rpe = (self.cat_por_slug('rotinas-pedagogicas-escolares')
                   or self.cat_por_nome('rotinas pedagogicas'))
        cat_institucional = (self.cat_por_slug('institucional')
                             or self.cat_por_nome('institucional'))
        cat_programas = (self.cat_por_slug('programas')
                         or self.cat_por_nome('programas'))
        cat_ca_ei = self.cat_por_slug('ca-educacao-infantil')
        cat_ca_efi = self.cat_por_slug('ca-ef-anos-iniciais')
        cat_ca_eff = self.cat_por_slug('ca-ef-anos-finais')
        cat_ca_em = self.cat_por_slug('ca-ensino-medio')
        cat_ca_apoio = self.cat_por_slug('ca-material-de-apoio')
        cat_curriculo = self.cat_por_slug('curriculo-atual')

        # Subcategoria nova aprovada pelo Dan: Formação Técnica dentro de IFA
        cat_ftp = None
        if cat_ifa:
            cat_ftp, _ = self.garantir_sub(
                'Formação Técnica e Profissional',
                'formacao-tecnica-e-profissional', cat_ifa)

        # Reserva (só é criada se algum item não tiver destino conhecido);
        # nasce OCULTA da home/menu para não mexer no visual do site
        self._cat_reserva = None

        def cat_reserva():
            if self._cat_reserva is None:
                c = self.cat_por_slug('portal-antigo-a-classificar')
                if not c and not self.dry:
                    c = Categoria.objects.create(
                        nome='Portal Antigo — a classificar',
                        slug='portal-antigo-a-classificar', ativa=True,
                        mostrar_menu_superior=False, mostrar_navegue_area=False)
                    self.criadas_categorias += 1
                    self.log('  + botão reserva criado (oculto da home): '
                             '"Portal Antigo — a classificar"')
                self._cat_reserva = c
            return self._cat_reserva

        # ── regras de destino por item ────────────────────────────────
        def resolver(p):
            """Devolve (categoria, titulo, url_externa, resumo) ou None p/ pular."""
            slug, titulo = p['slug'], limpar_titulo(p['titulo'])
            url_pagina = p['url']

            if 'itinerario-de-formacao-tecnica' in slug:
                return (cat_ftp or cat_ifa or cat_reserva(), titulo,
                        url_pagina, 'Itinerário de Formação Técnica e '
                        'Profissional — documento do portal do Currículo ES.')

            if slug.startswith('ementa-'):
                return (cat_ementas or cat_reserva(), titulo, url_pagina,
                        'Ementa curricular do Ensino Médio.')

            if slug in TITULOS_VIEWERS:
                pdf = extrair_pdf_iframe(p['html'])
                if pdf and (normalizar_url(pdf) in urls_db
                            or normalizar_url(pdf) in blob_norm):
                    self.log(f'  - pulado (PDF já existe no portal novo): {titulo}')
                    return None
                destino = cat_ca_apoio
                if '_ef_anos_iniciais' in slug:
                    destino = cat_ca_efi
                elif '_ef_anos_finais' in slug:
                    destino = cat_ca_eff
                elif '_em_' in slug:
                    destino = cat_ca_em
                return (destino or cat_curriculo or cat_reserva(),
                        TITULOS_VIEWERS[slug], pdf or url_pagina,
                        'Documento do Currículo do Espírito Santo.')

            if slug == 'educacao-infantil':
                return (cat_ca_ei or cat_curriculo or cat_reserva(),
                        'Currículo — Volume 1: Educação Infantil',
                        url_pagina, 'Documento do Currículo do Espírito Santo.')

            if slug.startswith(('volume-', 'v-9')):
                destino = cat_ca_efi if 'anos-iniciais' in slug else cat_ca_eff
                return (destino or cat_curriculo or cat_reserva(), titulo,
                        url_pagina, 'Documento do Currículo do Espírito Santo.')

            if slug == 'consultacurriculosifas':
                return (cat_ifa or cat_reserva(),
                        'Consulta Pública — Currículos dos Novos Itinerários '
                        'Formativos', url_pagina,
                        'Documentos da consulta pública dos currículos dos '
                        'novos Itinerários Formativos de Aprofundamento.')

            if slug == 'edital-rotinas-2025':
                return (cat_rpe or cat_reserva(), 'Edital Rotinas 2025',
                        url_pagina, 'Edital das Rotinas Pedagógicas 2025.')

            if slug.startswith('dialogos-'):
                n = slug.split('-')[-1]
                return (cat_institucional or cat_reserva(),
                        f'Revista Diálogos — {n}ª Edição', url_pagina,
                        'Revista Diálogos da SEDU.')

            if 'egidio-bordoni' in slug:
                destino = (self.cat_por_nome('mais leitores')
                           or cat_programas or cat_reserva())
                return (destino, titulo, url_pagina,
                        'Ações da Escola Egídio Bordoni com a Árvore de Livros.')

            # sem regra específica -> botão reserva (oculto), decisão do Dan
            return (cat_reserva(), titulo, url_pagina,
                    'Importado do portal antigo — aguardando classificação.')

        # ── importação ────────────────────────────────────────────────
        criados, pulados, erros = 0, 0, 0
        por_categoria = {}
        for p in sorted(faltantes, key=lambda x: x['slug']):
            try:
                r = resolver(p)
                if r is None:
                    pulados += 1
                    continue
                categoria, titulo, url, resumo = r
                if self.dry:
                    nome_cat = categoria.nome if categoria else '(botão reserva)'
                    self.log(f'  [dry-run] criaria: "{titulo[:70]}" -> {nome_cat}')
                    criados += 1
                    por_categoria[nome_cat] = por_categoria.get(nome_cat, 0) + 1
                    continue
                obj, created = Conteudo.objects.get_or_create(
                    slug=p['slug'],
                    defaults={
                        'titulo': titulo[:300],
                        'tipo': 'link',
                        'categoria': categoria,
                        'url_externa': url,
                        'resumo': resumo,
                        'status': 'publicado',
                        'ordem': 0,
                        'autor': 'GECEB/SEDU',
                        'data_publicacao': timezone.now(),
                    })
                if created:
                    criados += 1
                    por_categoria[categoria.nome] = \
                        por_categoria.get(categoria.nome, 0) + 1
                    self.log(f'  + "{titulo[:70]}" -> {categoria.nome}')
                else:
                    pulados += 1
                    self.log(f'  - já existia (slug): {p["slug"]}')
            except Exception as e:  # nunca deixar um item derrubar o lote
                erros += 1
                self.log(f'  ! ERRO em {p["slug"]}: {e}')

        # ── resumo e log ──────────────────────────────────────────────
        self.log('\n=== RESUMO ===')
        self.log(f'Conteúdos criados: {criados} | pulados: {pulados} | '
                 f'erros: {erros} | botões criados: {self.criadas_categorias}')
        for nome, n in sorted(por_categoria.items(), key=lambda x: -x[1]):
            self.log(f'  {n:4} -> {nome}')

        arq_log = PASTA / f'log_importacao_{agora}{"_dryrun" if self.dry else ""}.txt'
        arq_log.write_text('\n'.join(self.linhas_log), encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f'\nLog salvo em {arq_log}'))
