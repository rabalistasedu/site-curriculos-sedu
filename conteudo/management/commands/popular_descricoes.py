"""
Comando para popular os textos introdutórios das subcategorias.
Uso: python manage.py popular_descricoes
"""
from django.core.management.base import BaseCommand
from conteudo.models import Categoria


DESCRICOES = {
    'Currículo Atual': (
        '<p><strong>Caro(a) Professor(a)</strong></p>'
        '<p>O Currículo do Espírito Santo é uma conquista na busca de políticas públicas que '
        'promovam melhorias na qualidade da Educação Básica do nosso território.</p>'
        '<p>Elaborado em regime de colaboração entre Estado e municípios, representados, '
        'respectivamente, pela Secretaria de Estado da Educação e União Nacional dos '
        'Dirigentes Municipais de Educação, torna-se um referencial que alinha as '
        'necessidades educacionais próprias do Espírito Santo à Base Nacional Comum Curricular.</p>'
        '<p>Esse referencial deve nortear as ações de ensino-aprendizagem nas escolas, suas '
        'propostas pedagógicas, a seleção de material didático, bem como pautar as avaliações '
        'e os processos formativos para gestores e professores.</p>'
        '<p>Assim, disponibilizamos, neste site, o documento curricular da Educação Infantil e do '
        'Ensino Fundamental já finalizado, o documento de transição curricular de 2020, recursos '
        'produzidos e selecionados por professores especialistas da Secretaria de Educação do '
        'Estado e dos Municípios, bem como os materiais referentes à etapa do Ensino Médio.</p>'
    ),

    'Orientações Curriculares': (
        '<p><strong>Caro(a) Professor(a)!</strong></p>'
        '<p>A Gerência de Currículo da Educação Básica (GECEB), da Secretaria de Estado da '
        'Educação do Espírito Santo (SEDU), convida vocês a conhecerem as Orientações '
        'Curriculares, elaboradas por Etapas de Ensino e Componentes Curriculares a partir '
        'do Currículo do nosso estado.</p>'
    ),

    'Cadernos Metodológicos': (
        '<p><strong>Caro(a) Professor(a)!</strong></p>'
        '<p>O Governo do Estado do Espírito Santo, por meio da Secretaria de Estado da Educação, '
        'da Subsecretaria de Educação Básica e Profissional — Gerência de Currículo da Educação '
        'Básica (GECEB) em conjunto com outras instituições (Secretaria de Direitos Humanos, '
        'Secretaria da Fazenda, Universidade Federal do Espírito Santo e o Instituto Federal do '
        'Espírito Santo), a fim de fomentar a implementação dos Temas Integradores em sala de '
        'aula, firmaram parceria para elaborar os Cadernos Metodológicos.</p>'
        '<p>Os Cadernos estão em consonância com as novas Diretrizes da Educação propostas pela '
        'Base Nacional Comum Curricular (BNCC), com o Currículo do Espírito Santo e com as '
        'diretrizes das parcerias estabelecidas.</p>'
        '<p>É oportuno destacar que os Cadernos Metodológicos delineiam ferramentas estratégicas '
        'de natureza socioemocionais e cognitivas para que os estudantes possam tomar decisões '
        'claras, objetivas e salutares para o bem-estar de cada um.</p>'
    ),

    'Mapas de Progressão': (
        '<p>A Gerência de Currículo da Educação Básica (GECEB), da Secretaria de Estado da '
        'Educação do Espírito Santo (SEDU), convida vocês a conhecerem os nossos Mapas de '
        'Progressão das Habilidades, elaborados por Componentes Curriculares a partir do '
        'Currículo do nosso estado.</p>'
        '<p>Os Mapas de Progressão das Habilidades têm como intuito orientar, sistematizar, '
        'organizar e fomentar o seu trabalho, de modo a flexibilizar o Currículo, buscando, '
        'assim, melhorar a aprendizagem dos estudantes capixabas.</p>'
        '<p>Dessa forma, você já deve ter notado que, ao longo de todo o documento curricular '
        'do Espírito Santo, podemos diferenciar as Habilidades, uma vez que algumas delas são '
        'consideradas mais simples e outras mais complexas.</p>'
        '<p>Acreditamos que você, professor(a), poderá, por meio de nosso Mapa, aperfeiçoar o '
        'processo de construção de seu plano de ensino, contribuindo, assim, que as aprendizagens '
        'essenciais exigidas pela Base Nacional Comum Curricular (BNCC) sejam asseguradas a todos '
        'os estudantes nos diferentes contextos escolares — tudo isso visando a construção do '
        'conhecimento.</p>'
    ),

    'Ementas Curriculares': (
        '<p><strong>Caro(a) Professor(a)!</strong></p>'
        '<p>A Gerência de Currículo da Educação Básica (GECEB), da Secretaria de Estado da '
        'Educação do Espírito Santo (SEDU), convida vocês a conhecerem as Ementas Curriculares, '
        'elaboradas por Modalidades de Ensino, Componentes e Ano a partir do Currículo do nosso '
        'estado.</p>'
    ),

    'Rotinas de Recomposição': (
        '<p><strong>Recomposição das Aprendizagens</strong></p>'
        '<p>A recomposição das aprendizagens refere-se a um conjunto de ações sistematicamente '
        'organizadas que envolve: a busca ativa para reintegrar os estudantes ao ambiente escolar; '
        'a prevenção da evasão escolar; a redução da reprovação; a priorização curricular dos '
        'componentes curriculares de Língua Portuguesa e Matemática; a utilização de material '
        'didático próprio; a aplicação de avaliações diagnósticas e formativas; a adoção de '
        'práticas pedagógicas adequadas e a formação dos educadores para fortalecer aprendizagens '
        'que não foram plenamente desenvolvidas.</p>'
    ),

    'Espaços Potencialmente Educativos': (
        '<p>Quando nós, professores, profissionais da educação formal, optamos por levar os '
        'alunos para fora da escola, fica implícito nesta escolha uma concepção de educação '
        'para além da educação formal. Certamente, é uma escolha que possibilita outros tipos '
        'de educação, como a educação não formal e a informal.</p>'
        '<p>Sair da escola, com profissionais da escola, permite ao aluno vivenciar a integração '
        'desses três tipos de educação (formal, não formal e informal). Esse ganho é único, '
        'é algo diferente de conhecer um museu ou qualquer espaço de educação não formal com '
        'a família, por exemplo.</p>'
        '<p>Nesta página optamos caracterizar todos os espaços fora da escola com possibilidades '
        'educativas utilizando o termo "Espaço Potencialmente Educativo". Com certeza, qualquer '
        'espaço tem potencial educativo, mas trabalhar os espaços fora da escola articulado com '
        'a educação formal é um grande desafio e é um olhar diferenciado.</p>'
    ),

    # ── Programas ──
    'Educar para a Paz': (
        '<p>Procurando beneficiar as comunidades escolares da rede pública estadual do Espírito '
        'Santo, a Secretaria de Estado da Educação lança o Programa Educar para a Paz, que busca '
        'implementar medidas de conscientização, prevenção e combate aos diversos tipos de '
        'violência nas escolas da rede por meio da promoção da cultura de paz.</p>'
    ),

    'Mais Leitores': (
        '<p>O Governo do Estado do Espírito Santo, através da Secretaria de Estado da Educação, '
        'apresenta um conjunto de ações que possibilitam o desenvolvimento de experiências '
        'concretas de acesso e uso do livro e do incentivo da formação leitora junto à comunidade '
        'escolar da rede pública Estadual de ensino, através do Programa Mais Leitores, com o '
        'propósito de restabelecer as iniciativas de incentivo à leitura implementadas ao longo '
        'das últimas décadas pelo Governo Federal, bem como aquelas desenvolvidas no âmbito '
        'estadual.</p>'
    ),

    'Educação Ambiental': (
        '<p>A educação ambiental é fundamental para formar cidadãos conscientes e responsáveis. '
        'Nas escolas, ela vai além de ensinar sobre a preservação do meio ambiente e ecologia; '
        'trata-se de promover uma visão crítica sobre o mundo ao nosso redor, incentivando os '
        'estudantes a refletirem sobre o impacto de suas ações e a buscarem soluções sustentáveis '
        'para os desafios do presente.</p>'
        '<p>Integrar a educação ambiental ao cotidiano escolar ajuda a desenvolver atitudes que '
        'respeitam a natureza e promovem o bem-estar coletivo, preparando as futuras gerações '
        'para um mundo mais equilibrado e sustentável.</p>'
        '<p>Convidamos você a conhecer e participar das diversas ações de Educação Ambiental '
        'promovidas pela Secretaria Estadual de Educação do Espírito Santo!</p>'
    ),

    'Sucesso Escolar': (
        '<p>A Secretaria da Educação (SEDU) instituiu, por meio da Portaria nº 348-R/2022, '
        'o funcionamento do Programa Sucesso Escolar, destinado aos estudantes em situação de '
        'distorção idade-série, matriculados nos 6º e 7º anos do Ensino Fundamental das '
        'unidades escolares da Rede Estadual.</p>'
        '<p>O Programa é uma proposta construída de forma coletiva, coordenada pela Gerência de '
        'Educação Infantil e Ensino Fundamental (GEIEF) da SEDU, e tem como objetivo geral '
        'assegurar aos estudantes a progressão da aprendizagem e a continuidade dos estudos '
        'com sucesso escolar, a fim de garantir a equidade na Rede Estadual de Ensino.</p>'
    ),

    # ── Modalidades ──
    'EJA — Documentos': (
        '<p>Os presentes documentos apresentam as Diretrizes Curriculares da Educação de Jovens '
        'e Adultos da Rede Pública Estadual do Estado do Espírito Santo (DCEJA/ES). Reúne '
        'princípios, funções e concepções da modalidade com base no que pensam estudantes, '
        'equipes pedagógicas e gestoras de nossas escolas, bem como técnicos educacionais das '
        'Superintendências Regionais de Educação (SREs) e da Gerência de Educação de Jovens e '
        'Adultos (GEEJA), da Subsecretaria de Educação Básica e Profissional (SEEB) da '
        'Secretaria de Estado da Educação (SEDU), além de pesquisadores e estudiosos da área.</p>'
        '<p>Estas diretrizes curriculares foram atualizadas conforme as orientações do Conselho '
        'Estadual de Educação (CEE), por meio da Resolução 3.724, de 31 de março de 2014. Estão '
        'alinhadas às legislações nacionais e estaduais, como a Constituição Federal, a Lei de '
        'Diretrizes e Bases da Educação Nacional (LDB), o Plano Estadual de Educação do Espírito '
        'Santo (PEE/ES), entre outros documentos legais pertinentes.</p>'
    ),

    # ── Categorias Principais ──
    'Documentos Curriculares': (
        '<p>Documentos curriculares oficiais da Educação Básica do Espírito Santo, incluindo '
        'o Currículo ES para Educação Infantil, Ensino Fundamental e Ensino Médio, orientações '
        'curriculares, cadernos metodológicos, guias de habilidades e materiais de apoio.</p>'
    ),

    'Programas': (
        '<p>Programas educacionais da Secretaria de Estado da Educação do Espírito Santo, '
        'voltados para o fortalecimento do currículo, incentivo à leitura, educação ambiental, '
        'cultura de paz e sucesso escolar.</p>'
    ),

    'Modalidades e Diversidade': (
        '<p>Documentos e orientações para as diversas modalidades de ensino e públicos '
        'específicos: Educação de Jovens e Adultos (EJA), Educação do Campo, Educação Escolar '
        'Indígena, Quilombola, Relações Étnico-Raciais, Socioeducação e Educação Integral.</p>'
    ),

    'Olimpíadas e Competições': (
        '<p>As Olimpíadas do Conhecimento são essenciais para o desenvolvimento educacional e '
        'pessoal dos estudantes. Elas incentivam o aprofundamento do conhecimento além do '
        'currículo tradicional, promovendo o interesse e a paixão por áreas específicas, e '
        'desenvolvem habilidades críticas como pensamento analítico e resolução de problemas.</p>'
        '<p>Além disso, essas competições fomentam disciplina, dedicação e resiliência, essenciais '
        'para o crescimento pessoal. Ao promover um espírito de competição saudável e colaboração, '
        'as Olimpíadas enriquecem o aprendizado e criam um ambiente educacional dinâmico e '
        'inspirador, além de revelarem verdadeiros talentos para o desenvolvimento do nosso '
        'Estado e da nossa Nação.</p>'
    ),
}


class Command(BaseCommand):
    help = 'Popula os textos introdutórios das categorias e subcategorias'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n═══ Populando textos introdutórios ═══\n'))

        atualizados = 0
        for nome, descricao in DESCRICOES.items():
            try:
                cats = Categoria.objects.filter(nome=nome)
                if cats.exists():
                    for cat in cats:
                        cat.descricao = descricao
                        cat.save()
                        self.stdout.write(f'  ✓ {cat} — texto atualizado')
                        atualizados += 1
                else:
                    self.stderr.write(f'  ⚠ Categoria "{nome}" não encontrada')
            except Exception as e:
                self.stderr.write(f'  ✗ Erro em "{nome}": {e}')

        self.stdout.write(self.style.SUCCESS(f'\n═══ {atualizados} categorias atualizadas ═══\n'))
