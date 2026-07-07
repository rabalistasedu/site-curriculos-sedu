"""
Cria a subcategoria "Antigos Itinerários Formativos: Aprofundamentos"
dentro de "Currículo Atual" com os 11 documentos do site antigo:
https://curriculo.sedu.es.gov.br/curriculo/documentos/

Idempotente: usa get_or_create e verifica URL antes de criar.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from conteudo.models import Categoria, Conteudo

WP = 'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/'
GD = 'https://drive.google.com/file/d/'

DOCS = [
    ('Apresentação Itinerário Formativo',
     GD + '1AGJoEUvfW39__yE5UhcZNxDgfUxBbQVp/view?usp=sharing', 'link'),
    ('Vídeo Itinerários Formativo',
     GD + '1OU3ttGb40zonX-eequkQuUF8MoEVz3Tz/view?usp=sharing', 'video'),
    ('Educação Financeira e Fiscal (Matemática)',
     WP + '2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf', 'documento'),
    ('Terra, Vida e Cosmo (Ciências da Natureza)',
     WP + '2022/04/Curriculo-EM_Aprofundamento-da-area_-CN_-Alterado_-20_04_22.pdf', 'documento'),
    ('Mídias Digitais: Linguagens em Ação (Linguagens)',
     WP + '2022/04/Curriculo-EM_Aprofundamento-da-area_-Linguagens_Alterado_19-04.pdf', 'documento'),
    ('Modernização, Transformação Social e Meio Ambiente (Ciências Humanas)',
     WP + '2022/04/CurriculoEM_Aprofundamento-da-area-de-CHSA.pdf', 'documento'),
    ('O Esporte, a Ciência e Suas Linguagens',
     WP + '2022/04/Curriculo-EM_Aprofundamento-entreareas_-CN.e-Linguagens_Alterado_20_04_22.pdf', 'documento'),
    ('Energias Renováveis e Eficiência Energética',
     WP + '2022/04/Curriculo-EM_Aprofundamento-entreareas_CN-CHSA-Mat-e-Linguagens_Alterado_20_04_22.pdf', 'documento'),
    ('Narrativas Socioliterárias',
     WP + '2022/04/Curriculo-EM_Aprofundamento-entreareas_CHSA-e-Linguagens_Alterado-20_04_22.pdf', 'documento'),
    ('Humanidades e Relações Socioambientais',
     WP + '2022/04/Curriculo-EM_Aprofundamento-entreareas_-CHSA-e-CN_alterado_20-04-22.pdf', 'documento'),
    ('Aspirações Docentes',
     WP + '2022/04/Aspiracoes-Docentes-versao-revisada.pdf', 'documento'),
]


class Command(BaseCommand):
    help = 'Migra "Antigos Itinerários Formativos: Aprofundamentos" para Currículo Atual'

    def handle(self, *args, **options):
        ca = Categoria.objects.filter(slug='curriculo-atual').first()
        if not ca:
            self.stderr.write(self.style.ERROR('Categoria "Currículo Atual" não encontrada.'))
            return

        sub, criada = Categoria.objects.get_or_create(
            slug='ca-antigos-ifa',
            defaults={
                'nome': 'Antigos Itinerários Formativos: Aprofundamentos',
                'icone': 'fas fa-archive',
                'categoria_pai': ca,
                'ordem': 7,
                'ativa': True,
            }
        )
        self.stdout.write(
            ('  + Subcategoria criada' if criada else '  - Subcategoria ja existe')
            + f': {sub.nome}'
        )

        criados = 0
        existentes = 0
        for ordem, (titulo, url, tipo) in enumerate(DOCS, start=1):
            doc = Conteudo.objects.filter(url_externa=url).first()
            if doc:
                mudou = False
                if doc.categoria_id != sub.id:
                    doc.categoria = sub
                    mudou = True
                if not doc.ordem or doc.ordem != ordem:
                    doc.ordem = ordem
                    mudou = True
                if mudou:
                    doc.save()
                    self.stdout.write(f'    > movido: {titulo[:60]}')
                else:
                    self.stdout.write(f'    - ja existe: {titulo[:60]}')
                existentes += 1
            else:
                slug_doc = ('aifa-' + slugify(titulo))[:50]
                base_slug = slug_doc
                i = 2
                while Conteudo.objects.filter(slug=slug_doc).exists():
                    slug_doc = f'{base_slug[:46]}-{i}'
                    i += 1
                Conteudo.objects.create(
                    titulo=titulo,
                    slug=slug_doc,
                    tipo=tipo,
                    status='publicado',
                    url_externa=url,
                    categoria=sub,
                    ordem=ordem,
                    data_publicacao=timezone.now(),
                )
                criados += 1
                self.stdout.write(f'    + criado: {titulo[:60]}')

        self.stdout.write(self.style.SUCCESS(
            f'\nConcluido: {criados} criados, {existentes} ja existentes.'
        ))
