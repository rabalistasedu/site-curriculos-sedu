"""
Cria a categoria principal "Projetos Integradores" (Navegue por área)
com o texto introdutório e os documentos de:
https://curriculo.sedu.es.gov.br/curriculo/projetointegrador/

Os 4 documentos "Projeto Integrador" específicos por área/série já
tinham sido migrados (via migrar_orientacoes.py) para dentro de
"Orientações Curriculares" — este comando os MOVE para cá, que é o
lugar mais correto (têm botão próprio, como no site original).

Os 3 documentos gerais dos IFAs (IFA Quatro Áreas, IFA LingCHSA,
IFA CNTMAT) aparecem em AMBAS as páginas do WordPress (/documentos/ e
/projetointegrador/) — como já têm um lar natural em "Itinerários
Formativos de Aprofundamento (IFA)", este comando não os duplica aqui;
apenas cria o 1 documento realmente novo (a orientação específica do
Projeto Integrador) e move os 4 projetos por área.

Idempotente e autossuficiente (move docs existentes por URL, cria os
que faltam, slugs fixos).
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from conteudo.models import Categoria, Conteudo

B = 'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/'

DESCRICAO = (
    '<p>Os <strong>Projetos Integradores</strong> constituem o coração pedagógico dos '
    'Itinerários Formativos de Aprofundamento – IFAs, desenhados para transcender as '
    'fronteiras disciplinares e materializar a aprendizagem, eles desafiam os(as) '
    'estudantes a se mobilizarem, de forma sinérgica e crítica, os saberes de todas as '
    'áreas do conhecimento na investigação e na proposição de soluções para problemas '
    'complexos e situações reais da atualidade.</p>'
    '<p>Cada projeto parte de um tema gerador ou um problema contemporâneo que exige '
    'uma abordagem multidimensional, com cada área contribuindo dentro de sua '
    'perspectiva, para a construção do conhecimento.</p>'
    '<p>Assim, Linguagens e suas Tecnologias fornecem as ferramentas de comunicação, a '
    'Matemática e suas Tecnologias oferecem a lógica quantitativa e modelagem, as '
    'Ciências da Natureza e suas Tecnologias apresentam o método investigativo e a '
    'compreensão dos fenômenos naturais, enquanto as Ciências Humanas e Sociais '
    'Aplicadas, contextualizam o projeto no tecido social, histórico, geográfico, '
    'econômico e filosófico.</p>'
    '<p>Mais do que um produto, o processo é formativo. Os(As) estudantes desenvolvem '
    'autonomia, trabalho colaborativo, pensamento crítico e criatividade, construindo '
    'um repertório sólido para transformar os desafios cotidianos em oportunidades.</p>'
    '<p>Os Projetos Integradores foram concebidos para o primeiro trimestre. O Projeto '
    'de Linguagens está voltado para a 1ª série Noturno, Humanas para a 2ª série '
    'Noturno e os projetos de Linguagens e Humanas, Natureza e Matemática, para a 2ª '
    'série Diurno.</p>'
)

# (slug_fixo, nome, icone, ordem, [(titulo, url), ...])
SUBCATEGORIAS = [
    ('pi-documentos-gerais', 'Documentos Gerais', 'fas fa-file-alt', 1, [
        ('Orientações para Elaboração do Projeto Integrador IFA (Sequência Didática)',
         B + '2026/05/ORIENTACOES-PARA-ELABORACAO-PROJETO-INTEGRADOR-IFA.-FINAL-SEQ-DIDATICA.pdf'),
    ]),
    ('pi-linguagens-humanas-2diurno', 'Linguagens e Ciências Humanas (2ª Série Diurno)', 'fas fa-sun', 2, [
        ('Projeto Integrador — Linguagens e Ciências Humanas e Sociais Aplicadas (2ª Série Diurno)',
         B + '2025/12/PROJETO-INTEGRADOR-LINGUAGENS-E-HUMANAS-2a-SERIE-DIURNO-FINALIZADO.pdf'),
    ]),
    ('pi-natureza-matematica-2diurno', 'Ciências da Natureza e Matemática (2ª Série Diurno)', 'fas fa-sun', 3, [
        ('Projeto Integrador — Ciências da Natureza e Matemática e suas Tecnologias (2ª Série Diurno)',
         B + '2025/12/PROJETO-INTEGRADOR-CNT-E-MAT-2a-SERIE-DIURNO-FINALIZADO.pdf'),
    ]),
    ('pi-linguagens-1noturno', 'Linguagens (1ª Série Noturno)', 'fas fa-moon', 4, [
        ('Projeto Integrador — Linguagens e suas Tecnologias (1ª Série Noturno)',
         B + '2025/12/PROJETO-INTEGRADOR-LIINGUAGENS-1a-SERIE-NOTURNO-FINALIZADO-1.pdf'),
    ]),
    ('pi-chsa-2noturno', 'Ciências Humanas e Sociais Aplicadas (2ª Série Noturno)', 'fas fa-moon', 5, [
        ('Projeto Integrador — Ciências Humanas e Sociais Aplicadas (2ª Série Noturno)',
         B + '2025/12/PROJETO-INTEGRADOR-CHSA-2a-SERIE-NOTURNO-FINALIZADO.pdf'),
    ]),
]


class Command(BaseCommand):
    help = 'Migra a categoria "Projetos Integradores" do WordPress'

    def handle(self, *args, **options):
        cat_principal, criada = Categoria.objects.get_or_create(
            slug='projetos-integradores',
            defaults={
                'nome': 'Projetos Integradores',
                'descricao': DESCRICAO,
                'icone': 'fas fa-diagram-project',
                'ordem': 4,
                'ativa': True,
            }
        )
        if not criada and not cat_principal.descricao:
            cat_principal.descricao = DESCRICAO
            cat_principal.save()
        self.stdout.write(('  ✔ categoria criada' if criada else '  — categoria já existe')
                          + f': {cat_principal.nome}')

        movidos = 0
        criados = 0

        for slug_sub, nome_sub, icone_sub, ordem_sub, docs in SUBCATEGORIAS:
            sub, criada_sub = Categoria.objects.get_or_create(
                slug=slug_sub,
                defaults={
                    'nome': nome_sub,
                    'icone': icone_sub,
                    'categoria_pai': cat_principal,
                    'ordem': ordem_sub,
                    'ativa': True,
                }
            )
            if criada_sub:
                self.stdout.write(f'    ✔ subcategoria criada: {nome_sub}')

            for titulo, url in docs:
                doc = Conteudo.objects.filter(url_externa=url).first()
                if doc:
                    mudou = False
                    if doc.categoria_id != sub.id:
                        doc.categoria = sub
                        mudou = True
                    if mudou:
                        doc.save()
                        movidos += 1
                        self.stdout.write(f'      → movido: {titulo[:60]}')
                else:
                    slug_doc = ('pi-' + titulo.lower())[:50]
                    slug_doc = ''.join(c if c.isalnum() or c == '-' else '-' for c in
                                       slug_doc.replace('ç', 'c').replace('ã', 'a').replace('á', 'a')
                                       .replace('é', 'e').replace('ê', 'e').replace('í', 'i')
                                       .replace('ó', 'o').replace('ô', 'o').replace('ú', 'u')
                                       .replace('â', 'a').replace('õ', 'o').replace(' ', '-'))
                    base_slug = slug_doc
                    i = 2
                    while Conteudo.objects.filter(slug=slug_doc).exists():
                        slug_doc = f'{base_slug[:46]}-{i}'
                        i += 1
                    Conteudo.objects.create(
                        titulo=titulo,
                        slug=slug_doc,
                        tipo='link',
                        status='publicado',
                        url_externa=url,
                        categoria=sub,
                        data_publicacao=timezone.now(),
                    )
                    criados += 1
                    self.stdout.write(f'      + criado: {titulo[:60]}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: {len(SUBCATEGORIAS)} subcategorias, '
            f'{movidos} documentos movidos, {criados} documentos criados.'
        ))
        self.stdout.write(
            '\nℹ Os 3 documentos gerais dos IFAs (Quatro Áreas, LingCHSA, CNTMAT) '
            'aparecem também na página de origem, mas permanecem em "Itinerários '
            'Formativos de Aprofundamento (IFA) → Documentos Gerais dos IFAs", pois já '
            'têm lugar próprio lá e não foram duplicados.'
        )

        # Reordena o menu "Navegue por área" para caber logo após o IFA,
        # empurrando as categorias seguintes uma posição adiante.
        Categoria.objects.filter(slug='modalidades-e-diversidade').update(ordem=5)
        Categoria.objects.filter(slug='olimpiadas-e-competicoes').update(ordem=6)
        Categoria.objects.filter(slug='institucional').update(ordem=7)
        cat_principal.ordem = 4
        cat_principal.save()
