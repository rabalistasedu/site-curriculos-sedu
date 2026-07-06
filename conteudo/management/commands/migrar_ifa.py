"""
Cria a categoria principal "Itinerários Formativos de Aprofundamento (IFA)"
com subcategorias e documentos migrados de:
https://curriculo.sedu.es.gov.br/curriculo/documentos/

O comando é IDEMPOTENTE e AUTOSSUFICIENTE: para cada documento, se já
existir um Conteudo com a mesma URL (por exemplo, criado por outra
migração anterior), ele é MOVIDO para a subcategoria correta do IFA;
se não existir, é CRIADO. Rodar várias vezes não duplica nada.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from conteudo.models import Categoria, Conteudo

B = 'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/'
REF = B + '2023/01/Referenciais-Curriculares-para-Elaboracao-de-Itinerarios-Formativos-1-1.pdf'

# (slug_subcategoria, nome_subcategoria, icone, [(titulo_doc, url_pdf), ...])
# Os slugs são FIXOS (não gerados) para nunca criar duplicatas ao rodar de novo.
SUBCATEGORIAS = [
    ('ifa-documentos-gerais-dos-ifas', 'Documentos Gerais dos IFAs', 'fas fa-file-alt', [
        ('Referenciais Curriculares para a Elaboração de Itinerários Formativos', REF),
        ('Orientações para Elaboração dos Projetos Integradores dos IFAs',
         B + '2025/12/ORIENTACOES-PARA-ELABORACAO-DOS-PROJETOS-INTEGRADORES-3.pdf'),
        ('IFA — Quatro Áreas do Conhecimento',
         B + '2025/12/IFA-DAS-QUATRO-AREAS-DO-CONHECIMENTO-FINALIZADO.pdf'),
        ('IFA — Linguagens e Ciências Humanas e Sociais Aplicadas',
         B + '2025/12/IFA-LINGCHSA-6-1.pdf'),
        ('IFA — Matemática e Ciências da Natureza e suas Tecnologias',
         B + '2025/12/IFA-CNTMAT.pdf'),
    ]),
    ('ifa-educacao-financeira-e-fiscal', 'Educação Financeira e Fiscal', 'fas fa-coins', [
        ('Documento Curricular — Educação Financeira e Fiscal (Matemática)',
         B + '2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf'),
    ]),
    ('ifa-terra-vida-e-cosmo', 'Terra, Vida e Cosmo', 'fas fa-globe', [
        ('Documento Curricular — Terra, Vida e Cosmo (Ciências da Natureza)',
         B + '2022/04/Curriculo-EM_Aprofundamento-da-area_-CN_-Alterado_-20_04_22.pdf'),
    ]),
    ('ifa-midias-digitais-linguagens-em-acao', 'Mídias Digitais: Linguagens em Ação', 'fas fa-film', [
        ('Documento Curricular — Mídias Digitais: Linguagens em Ação (Linguagens)',
         B + '2022/04/Curriculo-EM_Aprofundamento-da-area_-Linguagens_Alterado_19-04.pdf'),
    ]),
    ('ifa-modernizacao-transformacao-social-e-meio', 'Modernização, Transformação Social e Meio Ambiente', 'fas fa-leaf', [
        ('Documento Curricular — Modernização, Transformação Social e Meio Ambiente (Ciências Humanas)',
         B + '2022/04/CurriculoEM_Aprofundamento-da-area-de-CHSA.pdf'),
    ]),
    ('ifa-o-esporte-a-ciencia-e-suas-linguagens', 'O Esporte, a Ciência e suas Linguagens', 'fas fa-running', [
        ('Documento Curricular — O Esporte, a Ciência e suas Linguagens (CN e Linguagens)',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_-CN.e-Linguagens_Alterado_20_04_22.pdf'),
    ]),
    ('ifa-energias-renovaveis-e-eficiencia-energet', 'Energias Renováveis e Eficiência Energética', 'fas fa-solar-panel', [
        ('Documento Curricular — Energias Renováveis e Eficiência Energética (CN, CHSA, Mat e Linguagens)',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_CN-CHSA-Mat-e-Linguagens_Alterado_20_04_22.pdf'),
    ]),
    ('ifa-narrativas-socioliterarias', 'Narrativas Socioliterárias', 'fas fa-book-open', [
        ('Documento Curricular — Narrativas Socioliterárias: Literatura, Arte e Ciências Humanas',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_CHSA-e-Linguagens_Alterado-20_04_22.pdf'),
    ]),
    ('ifa-humanidades-e-relacoes-socioambientais', 'Humanidades e Relações Socioambientais', 'fas fa-users', [
        ('Documento Curricular — Humanidades e Relações Socioambientais (CN e Ciências Humanas)',
         B + '2022/04/Curriculo-EM_Aprofundamento-entreareas_-CHSA-e-CN_alterado_20-04-22.pdf'),
    ]),
    ('ifa-aspiracoes-docentes', 'Aspirações Docentes', 'fas fa-chalkboard-teacher', [
        ('Documento Curricular — Aspirações Docentes (Linguagens, Matemática, CN e Ciências Humanas)',
         B + '2022/04/Aspiracoes-Docentes-versao-revisada.pdf'),
    ]),
]


class Command(BaseCommand):
    help = 'Migra Itinerários Formativos de Aprofundamento (IFA) do WordPress'

    def handle(self, *args, **options):
        cat_principal, criada = Categoria.objects.get_or_create(
            slug='itinerarios-formativos-ifa',
            defaults={
                'nome': 'Itinerários Formativos de Aprofundamento (IFA)',
                'descricao': '<p>Documentos curriculares dos <strong>Itinerários Formativos de Aprofundamento (IFA)</strong> do Ensino Médio do Espírito Santo, organizados por área de conhecimento.</p>',
                'icone': 'fas fa-route',
                'ordem': 3,
                'ativa': True,
            }
        )
        self.stdout.write(('  ✔ Categoria principal criada' if criada
                           else '  — Categoria principal já existe') + f': {cat_principal.nome}')

        total_subs = 0
        movidos = 0
        criados = 0

        for ordem_sub, (slug_sub, nome_sub, icone_sub, docs) in enumerate(SUBCATEGORIAS, start=1):
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
                total_subs += 1

            for titulo, url in docs:
                doc = Conteudo.objects.filter(url_externa=url).first()
                if doc:
                    # Já existe (talvez em outra categoria): move para o IFA
                    mudou = False
                    if doc.categoria_id != sub.id:
                        doc.categoria = sub
                        mudou = True
                    if doc.titulo != titulo:
                        doc.titulo = titulo
                        mudou = True
                    if doc.status != 'publicado':
                        doc.status = 'publicado'
                        mudou = True
                    if mudou:
                        doc.save()
                        movidos += 1
                        self.stdout.write(f'      → movido/atualizado: {titulo[:55]}')
                else:
                    # Não existe: cria
                    slug_doc = ('ifa-' + slugify(titulo))[:50]
                    # garante slug único
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
                    self.stdout.write(f'      + criado: {titulo[:55]}')

        # Limpeza: remove subcategorias do IFA que ficaram vazias
        # (duplicatas antigas com slug diferente, sem nenhum documento)
        slugs_validos = {s[0] for s in SUBCATEGORIAS}
        vazias = Categoria.objects.filter(categoria_pai=cat_principal).exclude(slug__in=slugs_validos)
        removidas = 0
        for v in vazias:
            if not Conteudo.objects.filter(categoria=v).exists():
                self.stdout.write(f'      × removendo subcategoria vazia duplicada: {v.slug}')
                v.delete()
                removidas += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: {total_subs} subcategorias novas, '
            f'{movidos} documentos movidos/atualizados, {criados} documentos criados, '
            f'{removidas} subcategorias vazias removidas.'
        ))
