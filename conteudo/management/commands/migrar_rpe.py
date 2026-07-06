"""
Cria a categoria principal "Rotinas Pedagógicas Escolares (RPE)"
(Navegue por área) com o texto introdutório e os 42 materiais
(apostilas de estudante e professor, por ano/série e trimestre) de:
https://curriculo.sedu.es.gov.br/curriculo/rpe/

A página do WordPress tem 4 níveis (Matéria > Público > Etapa > Ano >
Trimestre), mas o site novo só suporta 2 níveis de categoria. Por isso
o 3º/4º nível vira o TÍTULO do documento dentro da subcategoria:
subcategoria = "Matéria — Público (Etapa)", título = "Ano/Série —
Trimestre".

Existia um item antigo "Rotina Pedagógica Escolar — RPE" que era só um
link para a página do WordPress (sem os arquivos reais) — este comando
o remove, pois agora o conteúdo real está migrado.

Idempotente e autossuficiente.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from conteudo.models import Categoria, Conteudo

B = 'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/'

DESCRICAO = (
    '<p>A recomposição das aprendizagens refere-se a um conjunto de ações '
    'sistematicamente organizadas que envolve: a busca ativa para reintegrar os '
    'estudantes ao ambiente escolar; a prevenção da evasão escolar; a redução da '
    'reprovação; a priorização curricular dos componentes curriculares de Língua '
    'Portuguesa e Matemática; a utilização de material didático próprio; a aplicação '
    'de avaliações diagnósticas e formativas; a adoção de práticas pedagógicas '
    'adequadas e a formação dos educadores para fortalecer aprendizagens que não '
    'foram plenamente desenvolvidas.</p>'
)

# (slug_fixo, nome, icone, ordem, [(titulo_doc, url), ...])
SUBCATEGORIAS = [
    ('rpe-lp-ef-estudante', 'Língua Portuguesa — Ensino Fundamental (Estudante)', 'fas fa-book-open', 1, [
        ('5º Ano — 1º Trimestre', B + '2025/12/5o-ano-1o-TRIMESTRE-2026-LP.pdf'),
        ('5º Ano — 2º Trimestre', B + '2026/05/Apostila-5o-ano-EF-2o-TRI-2026.pdf'),
        ('6º Ano — 1º Trimestre', B + '2026/02/6o-ano-1o-TRIMESTRE-2026-LP.pdf'),
        ('6º Ano — 2º Trimestre', B + '2026/05/Apostila-6o-ano-EF-2o-TRI-2026_13_05.pdf'),
        ('7º Ano — 1º Trimestre', B + '2026/02/7o-ano-1o-TRIMESTRE-2026-LP.pdf'),
        ('7º Ano — 2º Trimestre', B + '2026/05/Apostila-7o-ano-EF-2o-TRI-2026.pdf'),
        ('8º Ano — 1º Trimestre', B + '2026/04/8o-ano-1o-TRIMESTRE-2026-LP.pdf'),
        ('8º Ano — 2º Trimestre', B + '2026/05/Apostila-8o-ano-2o-TRI-2026-LP-26-05-2026.pdf'),
        ('9º Ano — 1º Trimestre', B + '2026/02/9o-ano-1o-TRIMESTRE-2026-LP.pdf'),
        ('9º Ano — 2º Trimestre', B + '2026/05/Apostila-9o-ano-EF-2o-TRI-2026_15_05.pdf'),
    ]),
    ('rpe-lp-em-estudante', 'Língua Portuguesa — Ensino Médio (Estudante)', 'fas fa-book-open', 2, [
        ('1ª Série — 1º Trimestre', B + '2025/12/1a-EM-1o-TRIMESTRE-2026-LP.pdf'),
        ('2ª Série — 1º Trimestre', B + '2025/12/2a-EM-1o-TRIMESTRE-2026-LP.pdf'),
        ('3ª Série — 1º Trimestre', B + '2025/12/3a-EM-1o-TRIMESTRE-2026-LP.pdf'),
    ]),
    ('rpe-lp-ef-professor', 'Língua Portuguesa — Ensino Fundamental (Professor)', 'fas fa-chalkboard-teacher', 3, [
        ('5º Ano — 2º Trimestre', B + '2026/05/Material-do-prof.-5o-ano-EF-2o-tri_compressed.pdf'),
        ('6º Ano — 2º Trimestre', B + '2026/05/Material-do-prof.-6o-ano-EF-2o-tri-20-05-2026.pdf'),
        ('7º Ano — 2º Trimestre', B + '2026/05/Material-do-Prof.-7o-ano-EF-2o-tri-20-05-2026.pdf'),
        ('8º Ano — 1º Trimestre', B + '2026/04/Material-do-Prof.-8o-ano-EF.pdf'),
        ('8º Ano — 2º Trimestre', B + '2026/05/Material-do-Prof.-8o-ano-EF-2o-tri-20-05-2026.pdf'),
        ('9º Ano — 2º Trimestre', B + '2026/05/Material-do-Prof.-9o-ano-EF-2o-tri-20-05-2026.pdf'),
    ]),
    ('rpe-lp-em-professor', 'Língua Portuguesa — Ensino Médio (Professor)', 'fas fa-chalkboard-teacher', 4, [
        ('1ª Série — 2º Trimestre', B + '2026/05/1a-Serie-2o-tri-RPE-2026-LP-EM-20-05-2026.pdf'),
        ('2ª Série — 2º Trimestre', B + '2026/05/2a-Serie-2o-tri-RPE-2026-LP-EM-25_05_2026.pdf'),
        ('3ª Série — 2º Trimestre', B + '2026/05/3a-Serie-2o-tri-RPE-2026-LP-EM.pdf'),
    ]),
    ('rpe-mat-ef-estudante', 'Matemática — Ensino Fundamental (Estudante)', 'fas fa-square-root-alt', 5, [
        ('5º Ano — 1º Trimestre', B + '2026/03/5°-ano-RPE-2026-1°-Trimestre-02_03_MAT.pdf'),
        ('5º Ano — 2º Trimestre', B + '2026/05/Apostila-do-Estudante-5o-ano-EF-MAT-2o-TRI-2026.pdf'),
        ('6º Ano — 1º Trimestre', B + '2026/01/6°-ano-RPE-2026-1°-Trimestre-29_01_MAT.pdf'),
        ('7º Ano — 1º Trimestre', B + '2026/01/7o-ano-RPE-2026-1°-Trimestre-29_01_MAT.pdf'),
        ('7º Ano — 2º Trimestre', B + '2026/05/Apostila-do-Estudante-7o-ano-EF-MAT-2o-TRI-2026.pdf'),
        ('8º Ano — 1º Trimestre', B + '2026/01/8o-ano-RPE-2026-1°-Trimestre-29_01_MAT.pdf'),
        ('9º Ano — 1º Trimestre', B + '2026/01/9o-ano-RPE-2026-1°-Trimestre-29_01_MAT.pdf'),
        ('9º Ano — 2º Trimestre', B + '2026/05/Apostila-do-Estudante-9o-ano-EF-MAT-2o-TRI-2026.pdf'),
    ]),
    ('rpe-mat-em-estudante', 'Matemática — Ensino Médio (Estudante)', 'fas fa-square-root-alt', 6, [
        ('1ª Série — 1º Trimestre', B + '2025/12/1a-serie-RPE-2026-1°-Trimestre-23_12_MAT.pdf'),
        ('2ª Série — 1º Trimestre', B + '2026/01/2a-serie-RPE-2026-1°-Trimestre-29_01_MAT.pdf'),
        ('3ª Série — 1º Trimestre', B + '2026/03/3a-serie-RPE-2026-1°-Trimestre-27_03_MAT.pdf'),
    ]),
    ('rpe-mat-ef-professor', 'Matemática — Ensino Fundamental (Professor)', 'fas fa-chalkboard-teacher', 7, [
        ('5º Ano — 2º Trimestre', B + '2026/05/Material-do-prof.-5o-ano-EF-MAT-2o-tri-2026.pdf'),
        ('6º Ano — 2º Trimestre', B + '2026/05/Material-do-prof.-6o-ano-EF-MAT-2o-tri-2026.pdf'),
        ('7º Ano — 2º Trimestre', B + '2026/05/Material-do-prof.-7o-ano-EF-MAT-2o-tri-2026.pdf'),
        ('8º Ano — 2º Trimestre', B + '2026/05/Material-do-prof.-8o-ano-EF-MAT-2o-tri-2026.pdf'),
        ('9º Ano — 2º Trimestre', B + '2026/05/Material-do-prof.-9o-ano-EF-MAT-2o-tri-2026.pdf'),
    ]),
    ('rpe-mat-em-professor', 'Matemática — Ensino Médio (Professor)', 'fas fa-chalkboard-teacher', 8, [
        ('1ª Série — 2º Trimestre', B + '2026/06/1a-Serie-EM-MAT-2o-tri-RPE-2026-30_06_26.pdf'),
        ('2ª Série — 2º Trimestre', B + '2026/06/2a-Serie-EM-MAT-2o-tri-RPE-2026-30_06_26.pdf'),
        ('3ª Série — 1º Trimestre', B + '2026/03/3a-serie-RPE-2026-1°-Trimestre-25_03_-MAT-_-PROF.pdf'),
        ('3ª Série — 2º Trimestre', B + '2026/06/3a-Serie-EM-MAT-2o-tri-RPE-2026-30_06_26.pdf'),
    ]),
]


class Command(BaseCommand):
    help = 'Migra a categoria "Rotinas Pedagógicas Escolares (RPE)" do WordPress'

    def handle(self, *args, **options):
        cat_principal, criada = Categoria.objects.get_or_create(
            slug='rotinas-pedagogicas-escolares',
            defaults={
                'nome': 'Rotinas Pedagógicas Escolares (RPE)',
                'descricao': DESCRICAO,
                'icone': 'fas fa-calendar-check',
                'ordem': 5,
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
                    if doc.titulo != titulo:
                        doc.titulo = titulo
                        mudou = True
                    if mudou:
                        doc.save()
                        movidos += 1
                        self.stdout.write(f'      → movido/atualizado: {titulo}')
                else:
                    slug_doc = (slug_sub + '-' + slugify(titulo))[:50]
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
                    self.stdout.write(f'      + criado: {titulo}')

        # Remove o item antigo que só apontava para a página do WordPress
        # (não são as apostilas reais — o conteúdo verdadeiro já está migrado acima)
        antigo = Conteudo.objects.filter(
            titulo='Rotina Pedagógica Escolar — RPE',
            url_externa='https://curriculo.sedu.es.gov.br/curriculo/rpe/'
        ).first()
        removido = False
        if antigo:
            antigo.delete()
            removido = True
            self.stdout.write('  × removido item antigo (link genérico para a página do WordPress)')

        # Reordena o menu para caber logo após "Projetos Integradores"
        Categoria.objects.filter(slug='modalidades-e-diversidade').update(ordem=6)
        Categoria.objects.filter(slug='olimpiadas-e-competicoes').update(ordem=7)
        Categoria.objects.filter(slug='institucional').update(ordem=8)
        cat_principal.ordem = 5
        cat_principal.save()

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: {len(SUBCATEGORIAS)} subcategorias, '
            f'{movidos} documentos movidos/atualizados, {criados} documentos criados'
            f'{", 1 item antigo removido" if removido else ""}.'
        ))
