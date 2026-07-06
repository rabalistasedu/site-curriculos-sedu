"""
Migra a seção "MATERIAL DE APOIO" de
https://curriculo.sedu.es.gov.br/curriculo/documentos/

Cria a subcategoria "Material de Apoio" dentro de "Currículo Atual" com
os documentos que ainda não tinham sido migrados (Tema Integrador e
Referenciais Curriculares já existiam em outras categorias e não são
duplicados aqui).

Idempotente: usa a URL como chave — se o documento já existe em
qualquer categoria, apenas atualiza; senão, cria.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from conteudo.models import Categoria, Conteudo

DOCS = [
    ('Critérios para um Atendimento em Creches que Respeite os Direitos Fundamentais das Crianças',
     'http://portal.mec.gov.br/dmdocuments/direitosfundamentais.pdf'),
    ('Deixa Eu Falar! — Rede Nacional Primeira Infância (OMEP)',
     'http://agendaprimeirainfancia.org.br/arquivos/deixa_eu_falar_novembro2011.pdf'),
    ('Participação dos Estudantes na Escola (Guia Porvir)',
     'http://s3.amazonaws.com/porvir/wp-content/uploads/2017/10/30160146/Resumo_GuiaParticipacaoEstudantesPorvir.pdf'),
    ('Matriz de Referência PAEBES — História e Geografia (9º ano EF)',
     'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/06/HIST_GEO-PAEBES-MATRIZ-CH-9EF.pdf'),
    ('Matriz de Referência PAEBES — História e Geografia (3ª série EM)',
     'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/06/HIST_GEO-PAEBES-MATRIZ-CH-3EM.pdf'),
]


class Command(BaseCommand):
    help = 'Migra a seção "Material de Apoio" do WordPress'

    def handle(self, *args, **options):
        try:
            pai = Categoria.objects.get(slug='curriculo-atual')
        except Categoria.DoesNotExist:
            self.stderr.write('❌ Subcategoria "curriculo-atual" não encontrada. '
                              'Rode "python manage.py migrar_conteudo" primeiro.')
            return

        sub, criada = Categoria.objects.get_or_create(
            slug='ca-material-de-apoio',
            defaults={
                'nome': 'Material de Apoio',
                'icone': 'fas fa-toolbox',
                'categoria_pai': pai,
                'ordem': 5,
                'ativa': True,
            }
        )
        self.stdout.write(('  ✔ criada' if criada else '  — já existe') + f': {sub.nome}')

        movidos = 0
        criados = 0
        for titulo, url in DOCS:
            doc = Conteudo.objects.filter(url_externa=url).first()
            if doc:
                mudou = False
                if doc.categoria_id != sub.id:
                    doc.categoria = sub
                    mudou = True
                if mudou:
                    doc.save()
                    movidos += 1
                    self.stdout.write(f'      → movido: {titulo[:55]}')
            else:
                slug_doc = ('ca-apoio-' + slugify(titulo))[:50]
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

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: {movidos} documentos movidos, {criados} documentos criados.'
        ))
