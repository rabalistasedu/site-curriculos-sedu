"""
Migra TODO o conteúdo da página "Orientações Curriculares" do site WordPress
(https://curriculo.sedu.es.gov.br/curriculo/orientacoescurriculares/) para
dentro do site Django.

Cria uma categoria principal "Orientações Curriculares" (aparece em
"Navegue por área" da home) com subcategorias por etapa de ensino e área,
e um item de conteúdo para cada documento (PDF), apontando direto para o
arquivo. Idempotente: usa get_or_create, pode rodar quantas vezes quiser.

Uso: python manage.py migrar_orientacoes
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from conteudo.models import Categoria, Conteudo


B = 'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/'

# Estrutura: cada subcategoria com sua lista de (título, url do PDF).
# Os títulos são únicos e descritivos para não colidirem entre seções.
ESTRUTURA = [
    ('Ensino Fundamental — Anos Iniciais', 'fas fa-child', [
        ('Arte — Anos Iniciais', B + '2025/12/EFAI_Arte_26_09_12_25.pdf'),
        ('Ciências — Anos Iniciais', B + '2025/12/EFAI_CI_26_09_12_25.pdf'),
        ('Educação Física — Anos Iniciais', B + '2025/12/EFAI_EF_26_09_12_25.pdf'),
        ('Ensino Religioso — Anos Iniciais', B + '2025/12/EFAI_ER_26_09_12_25.pdf'),
        ('Geografia — Anos Iniciais', B + '2025/12/EFAI_GE_26_09_12_25.pdf'),
        ('História — Anos Iniciais', B + '2025/12/EFAI_HI_26_01_07_25.pdf'),
        ('Língua Portuguesa — Anos Iniciais', B + '2026/04/EFAI_LP_26_09_12_25.pdf'),
        ('Matemática — Anos Iniciais', B + '2026/05/EFAI_MAT_26_21_05_26.pdf'),
    ]),
    ('Ensino Fundamental — Anos Finais', 'fas fa-user-graduate', [
        ('Arte — Anos Finais', B + '2025/12/EFAF_AR_26_08_12_25.pdf'),
        ('Ciências — Anos Finais', B + '2025/12/EFAF_CI_26_09_12_25.pdf'),
        ('Educação Física — Anos Finais', B + '2025/12/EFAF_EF_26_09_12_25.pdf'),
        ('Ensino Religioso — Anos Finais', B + '2025/12/EFAF_ER_26_09_12_25.pdf'),
        ('Geografia — Anos Finais', B + '2026/03/EFAF_GE_26_12_03_26.pdf'),
        ('História — Anos Finais', B + '2025/12/EFAF_HI_26_09_12_25.pdf'),
        ('Língua Inglesa — Anos Finais', B + '2025/12/EFAF_LI_26_11_12_2025.pdf'),
        ('Língua Portuguesa — Anos Finais', B + '2026/04/EFAF_LP_26_16_12_25.pdf'),
        ('Matemática — Anos Finais', B + '2026/01/EFAF_MAT_26_20_01_26.pdf'),
    ]),
    ('Ensino Médio — Formação Geral Básica', 'fas fa-graduation-cap', [
        ('Arte — EM Regular', B + '2025/12/EM_D_ART_26_17_12_25.pdf'),
        ('Arte — EM Noturno', B + '2025/12/EM_N_ART_26_17_12_25.pdf'),
        ('Arte — EM Educação Técnica Profissional', B + '2025/12/EM_ETP_ART_26_17_12_25.pdf'),
        ('Biologia — EM Regular', B + '2026/02/EM_D_26_03_02_26.pdf'),
        ('Biologia — EM Noturno', B + '2025/12/EM_N_26_18_12_25.pdf'),
        ('Biologia — EM Educação Técnica Profissional', B + '2025/12/EM_ETP_26_18_12_25.pdf'),
        ('Educação Física — EM Regular', B + '2025/12/EM_D_EF_25_17_12_25.pdf'),
        ('Educação Física — EM Noturno', B + '2025/12/EM_N_EF_25_17_12_25.pdf'),
        ('Educação Física — EM Educação Técnica Profissional', B + '2025/12/EM_ETP_EF_25_17_12_25.pdf'),
        ('Filosofia — EM Regular', B + '2026/01/EM_D_FIL_26_23_01_26.pdf'),
        ('Filosofia — EM Noturno', B + '2026/01/EM_N_FIL_26_27_01_26.pdf'),
        ('Filosofia — EM Educação Técnica Profissional', B + '2026/01/EM_ETP_FIL_26_28_01_26.pdf'),
        ('Física — EM Regular', B + '2026/02/EM_D_FIS_26_26_02_26.pdf'),
        ('Física — EM Noturno', B + '2025/12/EM_N_FIS_26_29_09_25.pdf'),
        ('Física — EM Educação Técnica Profissional', B + '2025/12/EM_ETP_FIS_26_23_12_25.pdf'),
        ('Geografia — EM Regular', B + '2026/03/EM_D_GEO_26_16_03_26.pdf'),
        ('Geografia — EM Noturno', B + '2026/03/EM_N_GEO_26_16_03_26.pdf'),
        ('Geografia — EM Educação Técnica Profissional', B + '2026/03/EM_ETP_GEO_26_16_03_26.pdf'),
        ('História — EM Regular', B + '2026/03/EM_D_HIS_26_10_03_26.pdf'),
        ('História — EM Noturno', B + '2025/12/EM_N_HIS_26_18_12_25.pdf'),
        ('História — EM Educação Técnica Profissional', B + '2026/03/EM_ETP_HIS_26_10_03_26.pdf'),
        ('Língua Inglesa — EM Regular', B + '2026/01/EM_D_LI_26_26_01_26.pdf'),
        ('Língua Inglesa — EM Noturno', B + '2026/01/EM_N_LI_26_26_01_26.pdf'),
        ('Língua Inglesa — EM Educação Técnica Profissional', B + '2026/01/EM_ETP_LI_26_26_01_26.pdf'),
        ('Língua Espanhola — EM Regular', B + '2026/03/EM_ESP_26_22_12_25.pdf'),
        ('Língua Portuguesa — EM (1º Trimestre)', B + '2026/04/EM_D_LP_26_14_04_26.pdf'),
        ('Língua Portuguesa — EM (2º Trimestre)', B + '2026/06/OCs-2026-EM-2o-tri.pdf'),
        ('Matemática — EM (1º Trimestre)', B + '2026/04/EM_D_MAT_26_14_04_26.pdf'),
        ('Matemática — EM (2º Trimestre)', B + '2026/06/MAT-OCs-EM-2o-trim-2026-12-06-26.pdf'),
        ('Química — EM Regular', B + '2026/02/EM_D_QUI_26_26_02_26.pdf'),
        ('Química — EM Noturno', B + '2025/12/EM_N_QUI_26_16_12_25.pdf'),
        ('Química — EM Educação Técnica Profissional', B + '2025/12/EM_ETP_QUI_26_16_12_25.pdf'),
        ('Sociologia — EM Regular', B + '2026/01/EM_D_SOC_26_29_01_26.pdf'),
        ('Sociologia — EM Noturno', B + '2026/01/EM_N_SOC_26_29_01_26.pdf'),
        ('Sociologia — EM Educação Técnica Profissional', B + '2026/01/EM_ETP_SOC_26_29_01_26.pdf'),
    ]),
    ('Itinerários de Aprofundamento (IFA) — Linguagens e Ciências Humanas', 'fas fa-route', [
        ('Resolução CEE-ES nº 9.178/2025 (IFA)', B + '2025/12/RESOLUCAO-CEE-ES-No-9.1782025.pdf'),
        ('IFA — Aprofundamento de Arte (2ª Série Diurno)', B + '2025/12/ARTE-DIURNO-2a-SERIE.pdf'),
        ('IFA — Aprofundamento de Língua Espanhola (2ª Série Diurno)', B + '2025/12/LINGUA-ESPANHOLA-DIURNO-2a-SERIE.pdf'),
        ('IFA — Aprofundamento de Sociologia (2ª Série Diurno)', B + '2026/02/4OC-SOC-D-2-120226.pdf'),
        ('IFA — Aprofundamento de Geografia (2ª Série Diurno)', B + '2026/02/2OC-GEO-D-2-120226.pdf'),
        ('IFA — Aprofundamento de Língua Portuguesa (2ª Série Diurno)', B + '2025/12/LING.-PORTUGUESA-DIURNO-2a-SERIE.pdf'),
        ('IFA — Projeto Integrador Linguagens e Humanas (2ª Série Diurno)', B + '2025/12/PROJETO-INTEGRADOR-LINGUAGENS-E-HUMANAS-2a-SERIE-DIURNO-FINALIZADO.pdf'),
    ]),
    ('Itinerários de Aprofundamento (IFA) — Matemática e Ciências da Natureza', 'fas fa-route', [
        ('IFA — Aprofundamento de Matemática (2ª Série Diurno)', B + '2025/12/MATEMATICA-DIURNO-2a-SERIE-1.pdf'),
        ('IFA — Aprofundamento de Física (2ª Série Diurno)', B + '2025/12/FISICA-DIURNO-2a-SERIE1.pdf'),
        ('IFA — Aprofundamento de Biologia (2ª Série Diurno)', B + '2025/12/BIOLOGIA-DIURNO-2a-SERIE.pdf'),
        ('IFA — Aprofundamento de Química (2ª Série Diurno)', B + '2025/12/QUIMICA-DIURNO-2a-SERIE.pdf'),
        ('IFA — Projeto Integrador Matemática e Natureza (2ª Série Diurno)', B + '2025/12/PROJETO-INTEGRADOR-CNT-E-MAT-2a-SERIE-DIURNO-FINALIZADO.pdf'),
    ]),
    ('Itinerários de Aprofundamento (IFA) — Quatro Áreas (Noturno)', 'fas fa-route', [
        ('IFA — Aprofundamento de Língua Portuguesa (1ª Série Noturno)', B + '2025/12/LINGUA-PORTUGUESA-NOTURNO-1a-SERIE.pdf'),
        ('IFA — Aprofundamento de Língua Inglesa (1ª Série Noturno)', B + '2025/12/LINGUA-INGLESA-NOTURNO-1a-SERIE.pdf'),
        ('IFA — Aprofundamento de Arte (1ª Série Noturno)', B + '2025/12/ARTE-NOTURNO-1a-SERIE.pdf'),
        ('IFA — Aprofundamento de Educação Física (1ª Série Noturno)', B + '2025/12/EDUCACAO-FISICA-NOTURNO-1a-SERIE.pdf'),
        ('IFA — Aprofundamento de História (Noturno)', B + '2026/02/3OC-HIS-N-2.pdf'),
        ('IFA — Aprofundamento de Geografia (Noturno)', B + '2026/02/2OC-GEO-N-2.pdf'),
        ('IFA — Aprofundamento de Sociologia (Noturno)', B + '2026/02/4OC-SOC-N-2.pdf'),
        ('IFA — Aprofundamento de Filosofia (Noturno)', B + '2026/02/1OC-FIL-N-2.pdf'),
        ('IFA — Projeto Integrador Linguagens (1ª Série Noturno)', B + '2025/12/PROJETO-INTEGRADOR-LIINGUAGENS-1a-SERIE-NOTURNO-FINALIZADO-1.pdf'),
        ('IFA — Projeto Integrador CHSA (2ª Série Noturno)', B + '2025/12/PROJETO-INTEGRADOR-CHSA-2a-SERIE-NOTURNO-FINALIZADO.pdf'),
    ]),
    ('Itinerário — Educação Financeira e Fiscal', 'fas fa-coins', [
        ('Matemática Financeira (3ª Série)', B + '2025/12/Matematica-Financeira-3a-serie-2026.pdf'),
        ('Estatística (3ª Série)', B + '2025/12/Estatistica-3a-serie-2026.pdf'),
        ('Consumo Responsável e Educação Tributária (3ª Série)', B + '2025/12/Consumo-Responsavel-e-Educacao-Tributaria-3a-serie-2026.pdf'),
        ('Educação Financeira (3ª Série)', B + '2025/12/Educacao-Financeira-3a-serie-2026.pdf'),
        ('Projetos em Educação Financeira e Fiscal (3ª Série)', B + '2025/12/Projetos-em-Educacao-Financeira-e-Fiscal-3a-serie-2026.pdf'),
    ]),
    ('Itinerário — Terra, Vida e Cosmo', 'fas fa-globe', [
        ('Ciência, Tecnologia e Saúde (Diurno)', B + '2025/12/Ciencia-tecnologia-e-saude-Diurno.pdf'),
        ('Ciência, Tecnologia e Saúde (Noturno)', B + '2025/12/Ciencia-tecnologia-e-saude-Noturno.pdf'),
        ('Que Haja Luz', B + '2025/12/QUE_HAJA-LUZ-2026.pdf'),
        ('Do Micro ao Macro: A Química Está em Tudo?', B + '2025/12/AP7_MMQT_25_02_09_26.pdf'),
    ]),
    ('Itinerário — Modernização, Transformação Social e Meio Ambiente', 'fas fa-leaf', [
        ('Bioética e Natureza (Diurno)', B + '2025/12/AP-FILOSOFIA-BIOETICA-E-NATUREZA-DIURNO.pdf'),
        ('Bioética e Natureza (Noturno)', B + '2025/12/AP-FILOSOFIA-BIOETICA-E-NATUREZA-NOTURNO.pdf'),
        ('Perspectivas Geográficas: Sociedade, Espaço e Recursos Naturais', B + '2025/12/3a-SERIE-GEOGRAFIA-PGSERN.pdf'),
        ('Sociologia e Sociedade', B + '2025/12/3a-SERIE-SOCIOLOGIA-E-SOCIEDADE-2026.pdf'),
        ('Transformações Socioambientais, Políticas e Cidadania', B + '2025/12/Transformacoes_Socioambientais_Politicas_e_Cidadania_26_02_10_2025.pdf'),
    ]),
    ('Itinerário — Energias Renováveis e Eficiência Energética', 'fas fa-bolt', [
        ('A Física e as Matrizes Energéticas', B + '2025/12/A-FISICA-DAS-MATIZES-ENERGETICAS-2026.pdf'),
        ('Matemática e Sociedade (3ª Série)', B + '2025/12/Matematica-e-Sociedade-3a-serie-2026.pdf'),
        ('Fontes de Obtenção de Energia (Diurno)', B + '2026/02/Fontes-e-obtencao-de-energia-Diurno.pdf'),
        ('Fontes de Obtenção de Energia (Noturno)', B + '2026/02/Fontes-e-obtencao-de-energia-Noturno.pdf'),
        ('Matéria e Energia', B + '2025/12/AP5_ME_25_02_09_25.pdf'),
        ('Português Instrumental', B + '2025/12/PORTUGUES-INSTRUMENTAL-2026.pdf'),
        ('Desenho Técnico (3ª Série)', B + '2025/12/3a-serie-Desenho-Tecnico.pdf'),
    ]),
    ('Itinerário — Narrativas Socioliterárias', 'fas fa-book-open', [
        ('Arte, Poder e (I)Materialidade (3ª Série)', B + '2025/12/3a-serie-Arte-poder-e-imaterialidade.pdf'),
        ('Análise Crítica Metodológica (Diurno)', B + '2025/12/AP-FILOSOFIA-ANALISE-CRITICA-METODOLOGICA-DIURNO.pdf'),
        ('Análise Crítica Metodológica (Noturno)', B + '2025/12/AP-FILOSOFIA-ANALISE-CRITICA-METODOLOGICA-NOTURNO.pdf'),
        ('Narrativas de Clio: A História por meio da Literatura', B + '2025/12/Narrativas_de_Clio_a_Historia_por_meio_da_Literatura_26_02_10_2025.pdf'),
        ('Literatura e Sociedade: Conexões Contemporâneas', B + '2025/12/LITERATURA-E-SOCIEDADE-2026.pdf'),
        ('Narrativas Sociais (3ª Série)', B + '2025/12/3a-SERIE-NARRATIVAS-SOCIAIS-2026.pdf'),
    ]),
    ('Itinerário — Humanidades e Relações Socioambientais', 'fas fa-hands-holding-circle', [
        ('A Espécie Humana e a Relação com os Recursos Naturais (Diurno)', B + '2025/12/A-especie-humana-e-as-relacoes-Diurno.pdf'),
        ('A Espécie Humana e a Relação com os Recursos Naturais (Noturno)', B + '2025/12/A-especie-humana-e-as-relacoes-Noturno.pdf'),
        ('Percurso Filosófico sobre a Evolução Humana (Diurno)', B + '2025/12/AP-FILOSOFIA-PERCURSO-FILOSOFICO-SOBRE-A-EVOLUCAO-HUMANA-DIURNO.pdf'),
        ('Percurso Filosófico sobre a Evolução Humana (Noturno)', B + '2025/12/AP-FILOSOFIA-PERCURSO-FILOSOFICO-SOBRE-A-EVOLUCAO-HUMANA-NOTURNO.pdf'),
        ('Trajetórias Humanas na História', B + '2025/12/Trajetorias_Humanas_na_Historia_26_02_10_2025-VF.pdf'),
        ('Perspectiva Geográfica: Desenvolvimento e Espaço', B + '2025/12/3a-SERIE-GEOGRAFIA-PGDE.pdf'),
        ('Indivíduos, Natureza e Sociedade', B + '2026/03/AP3_INS_26_16_03_26.pdf'),
    ]),
    ('Itinerário — Aspirações Docentes', 'fas fa-chalkboard-user', [
        ('Vivência Pedagógica', B + '2025/12/VIVENCIA_PEDAGOGICA_2026.pdf'),
        ('Educação Conectada', B + '2025/12/EDUCACAO_CONECTADA-2026.pdf'),
        ('Ciência por Investigação', B + '2025/12/AP9_CI_25_02_09_25.pdf'),
        ('Humanidades 4.0 (Diurno)', B + '2025/12/AP-FILOSOFIA-HUMANIDADES-4.0-DIURNO.pdf'),
        ('Humanidades 4.0 (Noturno)', B + '2025/12/AP-FILOSOFIA-HUMANIDADES-4.0-NOTURNO.pdf'),
        ('Matemática (3ª Série) — Aspirações Docentes', B + '2025/12/Matematica-3a-serie-2026.pdf'),
        ('Linguagens: interações com o Mundo (Diurno)', B + '2025/12/Linguagens-interacoes-com-o-mundo-2026-diurno.pdf'),
        ('Linguagens: interações com o Mundo (Noturno)', B + '2025/12/Linguagens-interacoes-com-o-mundo-2026-noturno.pdf'),
    ]),
    ('Itinerário — Mídias Digitais, Linguagens em Ação', 'fas fa-photo-film', [
        ('A Língua Espanhola na América Latina', B + '2025/12/A-LINGUA-ESPANHOLA-NA-AMERICA-LATINA.pdf'),
        ('Arte e Patrimônio Cultural (3ª Série)', B + '2025/12/3a-serie-Arte-e-Patrimonio-Cultural.pdf'),
        ('Língua Inglesa e as Mídias Digitais', B + '2025/12/AP-LINGUA-INGLESA-E-AS-MIDIAS-DIGITAIS-1.pdf'),
        ('Linguagem, Comunicação e Mídia', B + '2025/12/LINGUAGEM-COMUNICACAO-E-MIDIA-2026.pdf'),
        ('Mídias Digitais e Práticas Corporais', B + '2025/12/MIDIAS_DIGITAIS_E_PRATICAS_CORPORAIS_2026.pdf'),
    ]),
    ('Itinerário — O Esporte, a Ciência e suas Linguagens', 'fas fa-medal', [
        ('Da Mecânica à Biomecânica', B + '2025/12/DA_MECANICA_A_BIOMECANICA-2026.pdf'),
        ('Enhanced Much: Inglês como Ferramenta de Integração', B + '2025/12/Aprofundamento-Enhanced-Much-2026.pdf'),
        ('Morfologia Humana e Atividades Físicas (Diurno)', B + '2025/12/Morfologia-Humana-e-a-Atividade-Fisica-Diurno.pdf'),
        ('Morfologia Humana e Atividades Físicas (Noturno)', B + '2025/12/Morfologia-Humana-e-a-atividade-Fisica-Noturno.pdf'),
        ('Química e Esporte', B + '2025/12/AP6_QE_25_02_09_25.pdf'),
        ('Rompendo os Limites do Esporte', B + '2025/12/ROMPENDO_OS_LIMITES_DO_ESPORTE_2026.pdf'),
    ]),
    ('Anos anteriores', 'fas fa-clock-rotate-left', [
        ('Orientações Curriculares 2025', 'https://curriculo.sedu.es.gov.br/curriculo/orientacoescurriculares2025'),
        ('Orientações Curriculares 2024', 'https://curriculo.sedu.es.gov.br/curriculo/orientacoescurriculares2024/'),
    ]),
]

DESCRICAO_PRINCIPAL = (
    '<p>A Gerência de Currículo da Educação Básica (GECEB), da Secretaria de '
    'Estado da Educação do Espírito Santo (SEDU), convida você a conhecer as '
    '<strong>Orientações Curriculares</strong>, elaboradas por Etapas de Ensino '
    'e Componentes Curriculares a partir do Currículo do nosso estado.</p>'
    '<p>Escolha abaixo a etapa de ensino ou o itinerário formativo para acessar '
    'os documentos.</p>'
)


class Command(BaseCommand):
    help = 'Migra a página Orientações Curriculares (todos os documentos) do WordPress'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n═══ Migração das Orientações Curriculares ═══\n'))

        # 1) Categoria principal (aparece em "Navegue por área")
        principal, criada = Categoria.objects.get_or_create(
            slug='orientacoes-curriculares-2026',
            defaults={
                'nome': 'Orientações Curriculares',
                'descricao': DESCRICAO_PRINCIPAL,
                'icone': 'fas fa-compass',
                'ordem': 2,
                'ativa': True,
                'categoria_pai': None,
            },
        )
        # Garante que os campos estejam atualizados mesmo se já existia
        principal.nome = 'Orientações Curriculares'
        principal.descricao = DESCRICAO_PRINCIPAL
        principal.icone = 'fas fa-compass'
        principal.ordem = 2
        principal.ativa = True
        principal.categoria_pai = None
        principal.save()
        self.stdout.write(
            ('  ✓ Categoria principal criada' if criada
             else '  — Categoria principal atualizada') + ': Orientações Curriculares')

        total_docs = 0
        for ordem_sub, (nome_sub, icone_sub, docs) in enumerate(ESTRUTURA, start=1):
            sub, criada_sub = Categoria.objects.get_or_create(
                slug=slugify('oc-' + nome_sub)[:50],
                defaults={
                    'nome': nome_sub,
                    'icone': icone_sub,
                    'ordem': ordem_sub,
                    'ativa': True,
                    'categoria_pai': principal,
                },
            )
            sub.nome = nome_sub
            sub.icone = icone_sub
            sub.ordem = ordem_sub
            sub.ativa = True
            sub.categoria_pai = principal
            sub.save()
            self.stdout.write(self.style.HTTP_INFO(f'\n  {nome_sub}'))

            for ordem_doc, (titulo, url) in enumerate(docs, start=1):
                obj, criado = Conteudo.objects.get_or_create(
                    titulo=titulo,
                    defaults={
                        'tipo': 'link',
                        'categoria': sub,
                        'url_externa': url,
                        'status': 'publicado',
                        'ordem': ordem_doc,
                        'data_publicacao': timezone.now(),
                        'autor': 'GECEB/SEDU',
                    },
                )
                if not criado:
                    # Atualiza categoria/url caso já existisse com outro valor
                    obj.tipo = 'link'
                    obj.categoria = sub
                    obj.url_externa = url
                    obj.status = 'publicado'
                    obj.save()
                total_docs += 1
                self.stdout.write(f'    {"✓" if criado else "—"} {titulo}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: 1 categoria principal, {len(ESTRUTURA)} subcategorias, '
            f'{total_docs} documentos.\n'))
