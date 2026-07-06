"""
Migração completa e final da página
https://curriculo.sedu.es.gov.br/curriculo/documentos/

Essa página do WordPress é a fonte de "Currículo Atual". A maior parte do
seu conteúdo (volumes por etapa, resoluções, Tema Integrador, documentos
dos Itinerários Formativos de Aprofundamento) já tinha sido migrada por
comandos anteriores (migrar_conteudo, organizar_curriculo_atual,
migrar_material_apoio, migrar_ifa). Este comando adiciona o que ainda
faltava para não deixar nada de fora:

1. Dezenas de links de apoio (vídeos, artigos, PDFs do Google Drive) da
   seção "MATERIAL DE APOIO" da página antiga — agrupados por assunto no
   próprio título do card, já que o site só permite 2 níveis de categoria
   e "Material de Apoio" já é o 2º nível dentro de "Currículo Atual".

2. O material de apoio de cada área dos "Itinerários Formativos de
   Aprofundamento" (apresentação em slide, vídeo, PDF e link do Canva do
   caderno de itinerários) — adicionado dentro da subcategoria de cada
   área já existente em "Itinerários Formativos de Aprofundamento (IFA)".

3. Os 2 vídeos/apresentações introdutórios gerais dos Itinerários
   Formativos — adicionados em "Documentos Gerais dos IFAs".

4. A nova subcategoria "Educação Profissional" (EPT Integrado), dentro de
   "Itinerários Formativos de Aprofundamento (IFA)".

Idempotente: usa a URL como chave (get_or_create) — pode ser rodado
quantas vezes for preciso sem duplicar nada.

NÃO migrado (link quebrado na própria página de origem, sem destino
válido): "Socioemocional: educação para a vida" (http://socioemocional-
educacao-para-a-vida/ não é uma URL real).
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from conteudo.models import Categoria, Conteudo


def is_video(url):
    return 'youtube.com/watch' in url or 'youtu.be/' in url


# ── 1. Material de Apoio (dentro de "Currículo Atual") ──────────────────
# (titulo, url) — o prefixo do título indica o assunto/agrupamento original
DOCS_MATERIAL_APOIO = [
    # Competências e Habilidades
    ('Competências e Habilidades — As competências gerais da BNCC',
     'https://drive.google.com/file/d/1-goo2aixj7g3hWrQXl92OR4_iTjTIypj/view'),
    ('Competências e Habilidades — Dimensões e Desenvolvimento das Competências Gerais',
     'https://drive.google.com/open?id=1gUbuGnS26ohdHDTpF563N0qSKmkeWrMM'),
    ('Competências e Habilidades — BNCC na prática: aprenda tudo sobre competências gerais',
     'https://drive.google.com/file/d/1bLEKxVmGZbbr3hNICW8WiIpCwbl_zqzU/view'),
    ('Competências e Habilidades — Habilidades e competências na prática docente (leitura complementar)',
     'https://drive.google.com/file/d/1XqXDOlY6jwEb6X2mw8Z3AI0vcchBaciR/view'),
    ('Competências e Habilidades — Bases teóricas e conceituais da pedagogia das competências (leitura complementar)',
     'https://drive.google.com/file/d/18yBeQIJf8q-eMg8of2Ke35OfVCXanB9e/view'),

    # Competências Socioemocionais
    ('Competências Socioemocionais — O que os Educadores pensam sobre o Socioemocional na escola?',
     'https://drive.google.com/file/d/1tzESBagP1ZYyiwuCxNOIUw_fhyK89bsB/view'),
    ('Competências Socioemocionais — Gráfico de competências',
     'https://drive.google.com/file/d/12SH1l1kRDG3Nct4zJBuF_iRIbsi7xcZ5/view'),
    ('Competências Socioemocionais — Gráfico de competências 2',
     'https://drive.google.com/file/d/12RCDGPtmyn6KRtWyaHircXD8w9txeOht/view'),
    ('Competências Socioemocionais — Os 4 pilares para a educação no século XXI',
     'https://drive.google.com/file/d/1dhMUzLhQs48kr0-UWSVVWfJ5VfHzJ3OD/view'),
    ('Competências Socioemocionais — Desenvolvimento das competências socioemocionais dentro das 10 competências BNCC',
     'https://drive.google.com/file/d/1FYSeGhjxkknzo-2CXOCVokHSibWBVM35/view'),
    ('Competências Socioemocionais — Marcos legais que fundamentam competências socioemocionais',
     'https://drive.google.com/file/d/1YvnohTlkvmpAc3Ym4buMwwXFSMSTeXyB/view'),
    ('Competências Socioemocionais — Quando as emoções entram no currículo (leitura complementar)',
     'https://drive.google.com/file/d/1FVtZOFmoNEbrHpQXnG7Zf6bUhooQMlBJ/view'),
    ('Competências Socioemocionais — Que competências socioemocionais precisam ser desenvolvidas? (leitura complementar)',
     'https://drive.google.com/file/d/1GHq7oHL_szKW0iKBFUAWr4T3C0BFVegb/view'),
    ('Competências Socioemocionais — Competências socioemocionais na BNCC (leitura complementar)',
     'https://drive.google.com/file/d/1M3dOUzEx27cGh_5pkgGSjWgkhmOAc8fL/view'),
    ('Competências Socioemocionais — O trabalho com socioemocionais não precisa ser oneroso ao professor (leitura complementar)',
     'https://drive.google.com/file/d/1Z7cuiZySqa9jsV435inSg0adeoP-xc9V/view'),

    # Educação Integral
    ('Educação Integral — Marcos legais da educação integral',
     'https://drive.google.com/file/d/1eoUywGpjLH68TyfySWKlJfyxGxb5hNy8/view'),
    ('Educação Integral — Princípios da política de educação integral',
     'https://www.youtube.com/watch?v=69SzDmbhtao'),
    ('Educação Integral — Educação integral conceitos: marcos legais',
     'https://educacaointegral.org.br/marcos-legais'),
    ('Educação Integral — Política de educação integral na prática',
     'https://educacaointegral.org.br/na-pratica/'),
    ('Educação Integral — Currículo na educação integral',
     'https://www.youtube.com/watch?v=6RHZzvO7BlM'),
    ('Educação Integral — Práticas Pedagógicas: articulando saberes e estratégias',
     'https://educacaointegral.org.br/especiais/praticas-pedagogicas/mandala/'),
    ('Educação Integral — Educação integral: componente curricular geografia',
     'https://drive.google.com/file/d/1ObuKBVZG99inxdNtDiUgdFyW4GsF91S5/view'),

    # Educação Básica (Etapas) — Educação Infantil
    ('Educação Infantil (Etapa) — Formação 2019: educação infantil, características da etapa',
     'https://drive.google.com/file/d/19WllcYFqwanIsVe6PFSi64rikq6EtTV_/view'),
    ('Educação Infantil (Etapa) — Criança, sujeito de direitos: prioridade absoluta',
     'https://www.youtube.com/watch?v=0Y4s4m8kJBM'),
    ('Educação Infantil (Etapa) — Características básicas: educação infantil',
     'https://www.youtube.com/watch?v=ygGScINSpHU'),
    ('Educação Infantil (Etapa) — Relação família escola',
     'https://drive.google.com/file/d/1zj1VLMPQ1qgLfNYL1KLsCn-dof4wxXhZ/view'),
    ('Educação Infantil (Etapa) — Currículo do ES: educação infantil: formação 2019',
     'https://drive.google.com/file/d/1jUNQHYVGyfV6THlsfKjXqp3gThowG00U/view'),
    ('Educação Infantil (Etapa) — Educação infantil: escola e família',
     'https://www.youtube.com/watch?v=5Zlo3VVwCz4'),
    ('Educação Infantil (Etapa) — Concepção de sujeito (criança)',
     'https://drive.google.com/file/d/1n8LboAzJ2lyk8Ko71bYVWLbLD3cQOZRQ/view'),
    ('Educação Infantil (Etapa) — Transição da educação infantil para anos iniciais do EF',
     'https://www.youtube.com/watch?v=fwPGwFDgdqk'),
    ('Educação Infantil (Etapa) — Transição creche-pré-escola-ensino fundamental',
     'https://drive.google.com/file/d/1HDkBhyVjIDsl2xf2Q1B0b-iduvvA3mc0/view'),
    ('Educação Infantil (Etapa) — Como nosso olhar sobre a pequena infância mudou',
     'https://drive.google.com/file/d/1DBOljbfUOKhEIjORtbtLdQyCG8n9K3eU/view'),
    ('Educação Infantil (Etapa) — Oferta e demanda de educação infantil no campo',
     'http://portal.mec.gov.br/index.php?option=com_docman&view=download&alias=12465-oferta-demanda-educacao-ampo-pdf&category_slug=fevereiro-2013-pdf&Itemid=30192'),
    ('Educação Infantil (Etapa) — Concepções de criança e creche',
     'https://www.youtube.com/watch?v=Q5jMNs5Xz2w'),

    # Educação Básica (Etapas) — Ensino Fundamental
    ('Ensino Fundamental (Etapa) — O ensino fundamental',
     'https://drive.google.com/file/d/1cK0xHWECyvngxGrqzY85sdi__8R9Bdyu/view'),
    ('Ensino Fundamental (Etapa) — Festa nas nuvens: reflexão sobre diferença',
     'https://www.youtube.com/watch?v=pktG7AJRL8k'),
    ('Ensino Fundamental (Etapa) — Tirinhas da Mafalda: reflexões sobre escola, ensino e alfabetização',
     'https://www.espacoeducar.net/2012/07/tirinhas-da-mafalda-reflexoes-sobre.html'),
    ('Ensino Fundamental (Etapa) — Relação família escola',
     'https://www.youtube.com/watch?v=SKqNPq-rcvo'),
    ('Ensino Fundamental (Etapa) — Escola e família: como cuidar dessa relação',
     'https://novaescola.org.br/conteudo/1577/escola-e-familia-como-cuidar-dessa-relacao'),
    ('Ensino Fundamental (Etapa) — Infográfico de transição e acolhimento (Anos Iniciais)',
     'https://drive.google.com/file/d/18b21DUaDTvKCldAcK5D3JEFdx1FqivjS/view'),
    ('Ensino Fundamental (Etapa) — Anos iniciais do EF na BNCC',
     'https://www.youtube.com/watch?v=5hd_WpAQsXI'),
    ('Ensino Fundamental (Etapa) — Alfabetização no ciclo inicial do ensino fundamental de nove anos',
     'https://drive.google.com/file/d/1PvLjzzum0o_RXrBE1lHtsiBUMTkZyROv/view'),
    ('Ensino Fundamental (Etapa) — Educação pública numa democracia moribunda',
     'https://www.inesc.org.br/educacao-publica-numa-democracia-moribunda/'),
    ('Ensino Fundamental (Etapa) — As crianças e a infância: definindo conceitos, delimitando o campo (leitura complementar)',
     'https://drive.google.com/file/d/1TFz_rooqCJZgEZZUf2E4LrpYs6jAgtHI/view'),
    ('Ensino Fundamental (Etapa) — Ensino fundamental: anos finais: desafios, sujeitos e transição',
     'https://drive.google.com/file/d/1tY-ZVuTYmRzPH0TVRpeDvqWLMrwg-Yqw/view'),
    ('Ensino Fundamental (Etapa) — Transição do EF: anos iniciais para anos finais',
     'https://drive.google.com/file/d/18PD5pTphiSNW7bU9_HJmVHgxU9HlBc8G/view'),
    ('Ensino Fundamental (Etapa) — Transição EF para EM',
     'https://www.youtube.com/watch?v=B8PRHPAnwE0'),
    ('Ensino Fundamental (Etapa) — Infográfico: estudantes do ensino fundamental (Anos Finais)',
     'https://drive.google.com/file/d/1vj31pepGJz3Cr0b3QUuqr1R9v-itxD80/view'),
    ('Ensino Fundamental (Etapa) — Adolescência de Maria',
     'https://www.youtube.com/watch?v=0bKI0iZwijE'),

    # Educação Básica (Etapas) — Ensino Médio
    ('Ensino Médio (Etapa) — A etapa do ensino médio na BNCC',
     'https://www.youtube.com/watch?v=-t_QkKzC1L4'),
    ('Ensino Médio (Etapa) — Novo ensino médio: série de infográficos explica as mudanças',
     'https://porvir.org/novo-ensino-medio-serie-de-infograficos-explica-as-mudancas/'),
    ('Ensino Médio (Etapa) — As principais mudanças no ensino médio',
     'https://www.youtube.com/watch?v=KaiAD8TVSkQ'),
    ('Ensino Médio (Etapa) — A arquitetura curricular no novo ensino médio (Itinerários Formativos)',
     'https://www.youtube.com/watch?v=5I8D3HC0KDM'),
    ('Ensino Médio (Etapa) — Novo ensino médio: entenda os itinerários formativos',
     'https://porvir.org/novo-ensino-medio-entenda-os-itinerarios-formativos/'),
    ('Ensino Médio (Etapa) — Infográfico 1 — Itinerários Formativos',
     'https://drive.google.com/file/d/1auoWQaJnkDwDi1ofdL3X2FjvTZxaRb43/view'),
    ('Ensino Médio (Etapa) — Infográfico 2 — Itinerários Formativos',
     'https://drive.google.com/file/d/1EF6Qut_Bv3q6XlN9SnikefZcEBTT8zLE/view'),
    ('Ensino Médio (Etapa) — Infográfico 3 — Itinerários Formativos',
     'https://drive.google.com/file/d/18FDiMRIRUONTnhOEUaYvRZpJBHiWn13J/view'),

    # Participação dos Estudantes
    ('Participação dos Estudantes — Participação dos estudantes na escola',
     'https://participacao.porvir.org/'),
    ('Participação dos Estudantes — Universo (relatos de experiências)',
     'https://participacao.porvir.org/#container_universo'),
    ('Participação dos Estudantes — Consultar os estudantes sobre o seu próprio processo educativo',
     'https://participacao.porvir.org/#bloco-escuta'),
    ('Participação dos Estudantes — O que o diretor pode fazer para se aproximar de seus alunos no dia a dia?',
     'https://participacao.porvir.org/#dicas'),
    ('Participação dos Estudantes — Permitir que os estudantes façam escolhas em relação ao seu processo educativo',
     'https://participacao.porvir.org/#bloco-escolha'),
    ('Participação dos Estudantes — Fomentar a participação dos estudantes em processos autorais',
     'https://participacao.porvir.org/#bloco-coautoria'),
]

# ── 2. Material de apoio por área do IFA (slug da subcategoria → itens) ──
DOCS_IFA_POR_AREA = {
    'ifa-educacao-financeira-e-fiscal': [
        ('Apresentação — Educação Financeira e Fiscal', 'https://drive.google.com/file/d/1C4_ozyy8Y4dhp1j8CkSsprLfTxx6x5TI/view'),
        ('Vídeo — Educação Financeira e Fiscal', 'https://drive.google.com/file/d/1JS45CauFcWCXFV96JsQ-hCzQgWT3ZN-d/view'),
        ('Itinerários Volume I (PDF)', 'https://drive.google.com/file/d/1y-Fa_hbt0VIlPhohA7yZzsc_RwUbPZRl/view'),
        ('Itinerários Volume I (Canva)', 'https://www.canva.com/design/DAE3y4bvsps/Njh0sNGd8ezYSP-9TtHscA/edit'),
    ],
    'ifa-terra-vida-e-cosmo': [
        ('Apresentação — Terra, Vida e Cosmo', 'https://drive.google.com/file/d/1elQQU8FizGafAUTqdvn4FvIrYvqNLtqB/view'),
        ('Vídeo — Terra, Vida e Cosmo', 'https://drive.google.com/file/d/1YfMPrlraKgNr3aR3DsnkAKOLd3gueOS9/view'),
        ('Itinerários Volume II (PDF)', 'https://drive.google.com/file/d/1QejlvIEb4oh_bVPnWUgwXz4rMUIdmrm7/view'),
        ('Itinerários Volume II (Canva)', 'https://www.canva.com/design/DAE2XSEixQc/C6BoNLvE11kBuYC1cBWm4g/edit'),
    ],
    'ifa-midias-digitais-linguagens-em-acao': [
        ('Apresentação — Mídias Digitais: Linguagens em Ação', 'https://drive.google.com/file/d/14xWn94RKN1Uc9QqvDEq2Uqlv1mWwzGTR/view'),
        ('Vídeo — Mídias Digitais: Linguagens em Ação', 'https://drive.google.com/file/d/18BNRvBM1GlOazF41Pl-xjyiK7WRcHENX/view'),
        ('Itinerários Volume III (PDF)', 'https://drive.google.com/file/d/1bNL4k7ZNIVG_Vk_fP48a9SBAd1LFBRvT/view'),
        ('Itinerários Volume III (Canva)', 'https://www.canva.com/design/DAE6rlUZ2QQ/x6GhJ8IAttUrAXuN1XuxDA/edit'),
    ],
    'ifa-modernizacao-transformacao-social-e-meio': [
        ('Apresentação — Modernização, Transformação Social e Meio Ambiente', 'https://drive.google.com/file/d/1V_sE9Zaj6hm4ZhA6C7-EjjiuIxGTKPqV/view'),
        ('Vídeo — Modernização, Transformação Social e Meio Ambiente', 'https://drive.google.com/file/d/1ebBwVjYuCLTTsBptTBbYuu62oY6pBd6e/view'),
        ('Itinerários Volume IV (PDF)', 'https://drive.google.com/file/d/1wpsHywWnx0xFE08UcGfgBaiDkVBC_6Ph/view'),
        ('Itinerários Volume IV (Canva)', 'https://www.canva.com/design/DAE6gjOtxWQ/ExuQAF4XhdmAXi-CU1ezYw/edit'),
    ],
    'ifa-o-esporte-a-ciencia-e-suas-linguagens': [
        ('Apresentação — O Esporte, a Ciência e suas Linguagens', 'https://drive.google.com/file/d/1CzQUor_PkHO1Zh-d4wz9-vSeyX50Qi0s/view'),
        ('Vídeo — O Esporte, a Ciência e suas Linguagens', 'https://drive.google.com/file/d/1hWbIAe1Wvg3cieiL8Upyo_VxJBdt1d3y/view'),
        ('Itinerários Volume V (PDF)', 'https://drive.google.com/file/d/1N5M4uoVGqbmWzb-BYrHf-I8MGJ-VH5bh/view'),
        ('Itinerários Volume V (Canva)', 'https://www.canva.com/design/DAE-PhnfVI4/0Fx2cshkrQcFFW1mXkq1RQ/edit'),
    ],
    'ifa-energias-renovaveis-e-eficiencia-energet': [
        ('Apresentação — Energias Renováveis e Eficiência Energética', 'https://drive.google.com/file/d/1xh4FME6Jp1BpZTGR4P8mEMmSTwykjXw5/view'),
        ('Vídeo — Energias Renováveis e Eficiência Energética', 'https://drive.google.com/file/d/1wwQtpk2uCqzLsqO0HSwFLkObcwVWzEmt/view'),
        ('Itinerários Volume VI (PDF)', 'https://drive.google.com/file/d/1svi5AsFNcrPdwdxeqsKOojY68oejiu8g/view'),
        ('Itinerários Volume VI (Canva)', 'https://www.canva.com/design/DAE3-OJOAdA/v8DXrNHAAzd51lJd5gKbRw/edit'),
    ],
    'ifa-narrativas-socioliterarias': [
        ('Apresentação — Narrativas Socioliterárias', 'https://drive.google.com/file/d/1AuEqFHE6RKkTMGZX_I5y0pBOUd5VPpbO/view'),
        ('Vídeo — Narrativas Socioliterárias', 'https://drive.google.com/file/d/1O30MJbj7tiH0A91II14C4g84WnYKWoT6/view'),
        ('Itinerários Volume VII (PDF)', 'https://drive.google.com/file/d/1u72P5NJlXOcn1Cl93ytrDfrsfd-aSx12/view'),
        ('Itinerários Volume VII (Canva)', 'https://www.canva.com/design/DAE8c1M6NB8/IYdDYhHUM6-H8DupAxzzLA/edit'),
    ],
    'ifa-humanidades-e-relacoes-socioambientais': [
        ('Apresentação — Humanidades e Relações Socioambientais', 'https://drive.google.com/file/d/1Fwq80IC55xmiOSvmjNIqLEI84lRlCupo/view'),
        ('Vídeo — Humanidades e Relações Socioambientais', 'https://drive.google.com/file/d/1YohtLpjiLHEgOTv3qrapxdlraUjuKwB5/view'),
        ('Itinerários Volume VIII (PDF)', 'https://drive.google.com/file/d/1p7wz4yy4Zr62RugojcWNSwz3NWAEOAgx/view'),
        ('Itinerários Volume VIII (Canva)', 'https://www.canva.com/design/DAE4bJ2vxiQ/Lvym3y9Gp0sGynz0daOKmA/edit'),
    ],
    'ifa-aspiracoes-docentes': [
        ('Apresentação — Aspirações Docentes', 'https://drive.google.com/file/d/1XhT2G4vlIpGG8kJzPTgrxQywIj36fmro/view'),
        ('Vídeo — Aspirações Docentes', 'https://drive.google.com/file/d/1rsI4OIH9u46drkWCNrDGNMFE1cm8FM2f/view'),
        ('Itinerários Volume IX (PDF)', 'https://drive.google.com/file/d/1sT_s6pvUBAi9Wy-bLc5yX0cU2WJyTFkD/view'),
        ('Itinerários Volume IX (Canva)', 'https://www.canva.com/design/DAE_pHjuqV8/8no88iUYw-tRw_-kRP_VWw/edit'),
    ],
}

# ── 3. Itens introdutórios gerais dos IFAs ───────────────────────────────
DOCS_IFA_INTRO = [
    ('Apresentação — Itinerário Formativo', 'https://drive.google.com/file/d/1AGJoEUvfW39__yE5UhcZNxDgfUxBbQVp/view'),
    ('Vídeo — Itinerários Formativos', 'https://drive.google.com/file/d/1OU3ttGb40zonX-eequkQuUF8MoEVz3Tz/view'),
]

# ── 4. Nova subcategoria "Educação Profissional" (dentro do IFA) ────────
DOCS_EDU_PROFISSIONAL = [
    ('EPT Integrado (Documento)', 'https://drive.google.com/file/d/14kpZ-TpgJpq8FpBN9h9dtqrdhUoK2PqK/view'),
    ('Apresentação — EPT Integrado', 'https://drive.google.com/file/d/16zg8SPEx67_FmLmTwEaxFi_uWZgo_OzM/view'),
    ('Vídeo — EPT Integrado', 'https://drive.google.com/file/d/1AJqnrnlpNA47LJdpyDfIV4vUVytAmrPc/view'),


]


class Command(BaseCommand):
    help = 'Migração final e completa da página "documentos" (Currículo Atual) do WordPress'

    def _slug_unico(self, base):
        slug = base[:50]
        original = slug
        i = 2
        while Conteudo.objects.filter(slug=slug).exists():
            slug = f'{original[:46]}-{i}'
            i += 1
        return slug

    def _criar_ou_mover(self, titulo, url, categoria, prefixo_slug):
        """Cria o conteúdo se a URL ainda não existir em nenhuma categoria;
        se já existir, apenas garante que está na categoria certa."""
        doc = Conteudo.objects.filter(url_externa=url).first() or Conteudo.objects.filter(url_video=url).first()
        if doc:
            if doc.categoria_id != categoria.id:
                doc.categoria = categoria
                doc.save()
                self.stdout.write(f'      -> movido: {titulo[:60]}')
            return 'existia'

        campos = dict(
            titulo=titulo,
            slug=self._slug_unico(f'{prefixo_slug}-{slugify(titulo)}'),
            status='publicado',
            categoria=categoria,
            data_publicacao=timezone.now(),
        )
        if is_video(url):
            campos['tipo'] = 'video'
            campos['url_video'] = url
        else:
            campos['tipo'] = 'link'
            campos['url_externa'] = url

        Conteudo.objects.create(**campos)
        self.stdout.write(f'      + criado: {titulo[:60]}')
        return 'criado'

    def handle(self, *args, **options):
        criados = 0
        existiam = 0

        # 1) Material de Apoio (Currículo Atual)
        try:
            ca_material = Categoria.objects.get(slug='ca-material-de-apoio')
        except Categoria.DoesNotExist:
            self.stderr.write('Categoria "ca-material-de-apoio" nao encontrada. '
                               'Rode "python manage.py migrar_material_apoio" primeiro.')
            return

        self.stdout.write(self.style.MIGRATE_HEADING('Material de Apoio (Currículo Atual)'))
        for titulo, url in DOCS_MATERIAL_APOIO:
            resultado = self._criar_ou_mover(titulo, url, ca_material, 'ca-apoio')
            criados += resultado == 'criado'
            existiam += resultado == 'existia'

        # 2) IFA — material de apoio por área
        self.stdout.write(self.style.MIGRATE_HEADING('Material de apoio por área (IFA)'))
        for slug_sub, itens in DOCS_IFA_POR_AREA.items():
            sub = Categoria.objects.filter(slug=slug_sub).first()
            if not sub:
                self.stderr.write(f'  Subcategoria IFA "{slug_sub}" nao encontrada, pulando.')
                continue
            self.stdout.write(f'  {sub.nome}')
            for titulo, url in itens:
                resultado = self._criar_ou_mover(titulo, url, sub, 'ifa-apoio')
                criados += resultado == 'criado'
                existiam += resultado == 'existia'

        # 3) IFA — itens introdutórios gerais
        ifa_geral = Categoria.objects.filter(slug='ifa-documentos-gerais-dos-ifas').first()
        if ifa_geral:
            self.stdout.write(self.style.MIGRATE_HEADING('Itens introdutórios gerais (IFA)'))
            for titulo, url in DOCS_IFA_INTRO:
                resultado = self._criar_ou_mover(titulo, url, ifa_geral, 'ifa-intro')
                criados += resultado == 'criado'
                existiam += resultado == 'existia'
        else:
            self.stderr.write('Subcategoria "ifa-documentos-gerais-dos-ifas" nao encontrada, pulando itens introdutórios.')

        # 4) Nova subcategoria "Educação Profissional" (dentro do IFA)
        ifa_top = Categoria.objects.filter(categoria_pai=None, slug='itinerarios-formativos-ifa').first()
        if ifa_top:
            edu_prof, criada_cat = Categoria.objects.get_or_create(
                slug='ifa-educacao-profissional',
                defaults={
                    'nome': 'Educação Profissional',
                    'icone': 'fas fa-user-graduate',
                    'categoria_pai': ifa_top,
                    'ordem': 99,
                    'ativa': True,
                }
            )
            self.stdout.write(self.style.MIGRATE_HEADING('Educação Profissional (nova subcategoria do IFA)'))
            self.stdout.write(('  criada' if criada_cat else '  ja existia') + f': {edu_prof.nome}')
            for titulo, url in DOCS_EDU_PROFISSIONAL:
                resultado = self._criar_ou_mover(titulo, url, edu_prof, 'ifa-eduprof')
                criados += resultado == 'criado'
                existiam += resultado == 'existia'
        else:
            self.stderr.write('Categoria principal do IFA nao encontrada, pulando "Educação Profissional".')

        self.stdout.write(self.style.SUCCESS(
            f'\nConcluído: {criados} itens criados, {existiam} já existiam (verificados/realocados).\n'
            f'Não migrado (link quebrado na origem): "Socioemocional: educação para a vida".'
        ))
