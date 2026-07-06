"""
Comando para popular o banco de dados com as categorias do site Currículo SEDU.
Uso: python manage.py popular_categorias
"""
from django.core.management.base import BaseCommand
from conteudo.models import Categoria, ConfiguracaoSite


class Command(BaseCommand):
    help = 'Popula as categorias e subcategorias do site'

    def handle(self, *args, **options):
        # Configuração do site
        ConfiguracaoSite.get_config()
        self.stdout.write('Configuração do site criada.')

        categorias = [
            {
                'nome': 'Documentos Curriculares',
                'icone': 'fas fa-book',
                'descricao': 'Documentos curriculares oficiais da Educação Básica do Espírito Santo',
                'ordem': 1,
                'subs': [
                    'Currículo Atual',
                    'Currículo de Computação',
                    'Orientações Curriculares',
                    'Guias de Habilidades',
                    'Cadernos Metodológicos',
                    'Mapas de Progressão',
                    'Ementas Curriculares',
                    'Aprofundamento em Leitura e Escrita',
                    'Sequências Didáticas',
                    'Rotinas de Recomposição',
                    'Nivelamento e AMA',
                    'Práticas Experimentais EF',
                    'Projeto de Vida EF',
                    'Projeto de Vida EM',
                    'Itinerários Formativos e Projetos Integradores',
                    'Materiais de Apoio EM',
                    'Guia de Oportunidades EF',
                    'Guia de Oportunidades EM',
                    'Currículo 2018',
                    'Currículo 2009',
                ]
            },
            {
                'nome': 'Programas',
                'icone': 'fas fa-rocket',
                'descricao': 'Programas educacionais da SEDU',
                'ordem': 2,
                'subs': [
                    'Matemática na Rede',
                    'Educar para a Paz',
                    'Música na Rede',
                    'Mais Leitores',
                    'Educação Ambiental',
                    'Sucesso Escolar',
                    'GEEPEI',
                    'PROETI',
                    'PIPAT',
                ]
            },
            {
                'nome': 'Livro Didático e Materiais',
                'icone': 'fas fa-book-open',
                'descricao': 'PNLD, catálogos e materiais de apoio pedagógico',
                'ordem': 3,
                'subs': [
                    'PNLD',
                    'Catálogo de Livros',
                    'Práticas Experimentais',
                    'Espaços Potencialmente Educativos',
                ]
            },
            {
                'nome': 'Modalidades e Diversidade',
                'icone': 'fas fa-users',
                'descricao': 'EJA, Educação do Campo, Indígena, Quilombola e outras modalidades',
                'ordem': 4,
                'subs': [
                    'EJA — Documentos',
                    'EJA — Orientações Curriculares',
                    'EJA — Cadernos de Práticas',
                    'EJA — Planos de Curso',
                    'Educação do Campo',
                    'Educação Escolar Indígena',
                    'Educação Escolar Quilombola',
                    'Relações Étnico-Raciais',
                    'Socioeducação',
                    'Educação Integral em Tempo Integral',
                    'Estudos Especiais e Recuperação',
                    'Busca Ativa Escolar',
                ]
            },
            {
                'nome': 'Olimpíadas e Competições',
                'icone': 'fas fa-trophy',
                'descricao': 'Olimpíadas de conhecimento e competições acadêmicas',
                'ordem': 5,
                'subs': [
                    'Olimpíadas de Física',
                    'Olimpíadas de Matemática',
                    'Olimpíadas de Biologia',
                    'Educação Financeira',
                    'Empreendedorismo',
                    'Outras Competições',
                ]
            },
            {
                'nome': 'Institucional',
                'icone': 'fas fa-landmark',
                'descricao': 'Informações sobre a GECEB, notícias e publicações',
                'ordem': 6,
                'subs': [
                    'Sobre a GECEB',
                    'Revista Diálogos',
                    'Currículo Interativo',
                    'Notícias e Informes',
                ]
            },
        ]

        for cat_data in categorias:
            cat, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={
                    'icone': cat_data['icone'],
                    'descricao': cat_data['descricao'],
                    'ordem': cat_data['ordem'],
                }
            )
            status = 'criada' if created else 'já existe'
            self.stdout.write(f'  Categoria "{cat.nome}" — {status}')

            for i, sub_nome in enumerate(cat_data.get('subs', []), 1):
                sub, sub_created = Categoria.objects.get_or_create(
                    nome=sub_nome,
                    categoria_pai=cat,
                    defaults={'ordem': i}
                )
                if sub_created:
                    self.stdout.write(f'    └─ Subcategoria "{sub_nome}" criada')

        self.stdout.write(self.style.SUCCESS('\nCategorias populadas com sucesso!'))
