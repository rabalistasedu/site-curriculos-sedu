"""
Comando para migrar todo o conteúdo do site WordPress para o Django.
Uso: python manage.py migrar_conteudo

Cria conteúdos do tipo 'link' apontando para os PDFs e páginas originais,
e do tipo 'post' para textos completos (como o FAQ do PNLD).
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from conteudo.models import Categoria, Conteudo


class Command(BaseCommand):
    help = 'Migra todo o conteúdo do site WordPress curriculo.sedu.es.gov.br'

    def get_or_create_sub(self, nome, pai_nome):
        """Busca subcategoria pelo nome e pai"""
        try:
            pai = Categoria.objects.get(nome=pai_nome, categoria_pai__isnull=True)
            sub, created = Categoria.objects.get_or_create(
                nome=nome,
                categoria_pai=pai,
                defaults={'ordem': 0}
            )
            return sub
        except Categoria.DoesNotExist:
            self.stderr.write(f'  ⚠ Categoria pai "{pai_nome}" não encontrada')
            return None

    def get_cat(self, nome):
        """Busca categoria principal"""
        try:
            return Categoria.objects.get(nome=nome, categoria_pai__isnull=True)
        except Categoria.DoesNotExist:
            self.stderr.write(f'  ⚠ Categoria "{nome}" não encontrada')
            return None

    def criar(self, titulo, tipo, categoria, url='', resumo='', corpo='', ordem=0, destaque=False):
        """Cria conteúdo se não existir"""
        obj, created = Conteudo.objects.get_or_create(
            titulo=titulo,
            defaults={
                'tipo': tipo,
                'categoria': categoria,
                'url_externa': url,
                'resumo': resumo,
                'corpo': corpo,
                'status': 'publicado',
                'ordem': ordem,
                'destaque': destaque,
                'data_publicacao': timezone.now(),
                'autor': 'GECEB/SEDU',
            }
        )
        status = 'criado' if created else 'já existe'
        self.stdout.write(f'  {"✓" if created else "—"} {titulo} ({status})')
        return obj

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n═══ Migração de conteúdo do site original ═══\n'))

        # ──────────────────────────────────────────────
        # 1. DOCUMENTOS CURRICULARES
        # ──────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO('\n── Documentos Curriculares ──'))

        # --- Currículo Atual ---
        cat = self.get_or_create_sub('Currículo Atual', 'Documentos Curriculares')
        if cat:
            self.stdout.write('  Resoluções:')
            self.criar('Resolução CEE-ES Nº 5.190/2018 — Educação Infantil e Ensino Fundamental',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/09/RESOLUCAO-CEE-ES-No-5.190-2018-EI-e-EF.pdf',
                       'Resolução do Conselho Estadual de Educação que institui o Currículo ES para EI e EF.')
            self.criar('Resolução CEE-ES Nº 5.777/2020 — Ensino Médio',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/09/RESOLUCAO-CEE-ES-No.-5.777-2020-Ensino-Medio.pdf',
                       'Resolução do Conselho Estadual de Educação que institui o Currículo ES para o Ensino Médio.')

            self.stdout.write('  Educação Infantil:')
            self.criar('Currículo ES — Vol. 01 — Educação Infantil (Revisão 2026)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2026/05/Curriculo-ES-2020-Vol-01-Educacao-Infantil-REV2026.pdf',
                       'Volume 1 do Currículo do Espírito Santo — Educação Infantil, revisão 2026.', ordem=1)
            self.criar('Tema Integrador',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2024/10/Tema-Integrador-final-24-10.pdf',
                       'Documento de Temas Integradores do Currículo ES.', ordem=2)

            self.stdout.write('  Ensino Fundamental — Anos Iniciais:')
            self.criar('Currículo ES — Vol. 02 — EF Anos Iniciais — Ciências da Natureza e Matemática',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/02/Curr%C3%ADculo-ES-2019-Vol-02-Ensino-Fundamental-Anos-Iniciais-%C3%81rea-de-Ci%C3%AAncias-da-Natureza-e-Matem%C3%A1tica-Miolo.pdf',
                       'Volume 2 — Área de Ciências da Natureza e Matemática.', ordem=3)
            self.criar('Currículo ES — Vol. 03 — EF Anos Iniciais — Ciências Humanas e Ensino Religioso',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/02/Curr%C3%ADculo-ES-2019-Vol-03-Ensino-Fundamental-Anos-Iniciais-%C3%81rea-de-Ci%C3%AAncias-Humanas-e-Ensino-Religioso-Miolo.pdf',
                       'Volume 3 — Área de Ciências Humanas e Ensino Religioso.', ordem=4)
            self.criar('Currículo ES — Vol. 04 — EF Anos Iniciais — Linguagens, Arte e Educação Física',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/02/Curr%C3%ADculo-ES-2019-Vol-04-Ensino-Fundamental-Anos-Iniciais-%C3%81rea-de-Linguagens-Arte-e-Educa%C3%A7%C3%A3o-F%C3%ADsica-Miolo.pdf',
                       'Volume 4 — Área de Linguagens, Arte e Educação Física.', ordem=5)
            self.criar('Currículo ES — Vol. 05 — EF Anos Iniciais — Língua Portuguesa',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/02/Curr%C3%ADculo-ES-2019-Vol-05-Ensino-Fundamental-Anos-Iniciais-%C3%81rea-de-Linguagens-L%C3%ADngua-Portuguesa-Miolo.pdf',
                       'Volume 5 — Área de Linguagens, Língua Portuguesa.', ordem=6)

            self.stdout.write('  Ensino Fundamental — Anos Finais:')
            self.criar('Currículo ES — Vol. 06 — EF Anos Finais — Ciências da Natureza e Matemática',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/04/Curr%C3%ADculo-ES-2020-Vol-06-Ensino-Fundamental-Anos-Finais-%C3%81rea-de-Ci%C3%AAncias-da-Natureza-e-Matem%C3%A1tica-Miolo.pdf',
                       'Volume 6 — Área de Ciências da Natureza e Matemática.', ordem=7)
            self.criar('Currículo ES — Vol. 07 — EF Anos Finais — Ciências Humanas e Ensino Religioso',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/04/Curr%C3%ADculo-ES-2020-Vol-07-Ensino-Fundamental-Anos-Finais-%C3%81rea-de-Ci%C3%AAncias-Humanas-e-Ensino-Religioso-Miolo.pdf',
                       'Volume 7 — Área de Ciências Humanas e Ensino Religioso.', ordem=8)
            self.criar('Currículo ES — Vol. 08 — EF Anos Finais — Linguagens, Arte, Ed. Física e Língua Inglesa',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/04/Curr%C3%ADculo-ES-2020-Vol-08-Ensino-Fundamental-Anos-Finais-%C3%81rea-de-Linguagens-Arte-Educa%C3%A7%C3%A3o-F%C3%ADsica-e-L%C3%ADngua-Inglesa-Miolo.pdf',
                       'Volume 8 — Área de Linguagens, Arte, Educação Física e Língua Inglesa.', ordem=9)
            self.criar('Currículo ES — Vol. 09 — EF Anos Finais — Língua Portuguesa',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2020/05/Curr%C3%ADculo-ES-2020-Vol-09-Ensino-Fundamental-Anos-Finais-%C3%81rea-de-Linguagens-L%C3%ADngua-Portuguesa-Miolo.pdf',
                       'Volume 9 — Área de Linguagens, Língua Portuguesa.', ordem=10)

            self.stdout.write('  Ensino Médio — Formação Geral Básica (Google Drive):')
            self.criar('Currículo EM — Texto Introdutório',
                       'link', cat,
                       'https://drive.google.com/file/d/1B41xYpgWgvZGd8dccl6lDtOkjHL4jjC5/view',
                       'Texto introdutório do Currículo do Ensino Médio.', ordem=11)
            self.criar('Currículo EM — Linguagens e suas Tecnologias',
                       'link', cat,
                       'https://drive.google.com/file/d/17J9vNQxxXHtsSIvOfwZpU7BjtsTxJ1tm/view',
                       'Área de Linguagens e suas Tecnologias — Ensino Médio.', ordem=12)
            self.criar('Currículo EM — Língua Portuguesa',
                       'link', cat,
                       'https://drive.google.com/file/d/1WXt8O7971HKbbf_NH0hFYGaf59qYo5Z0/view',
                       'Língua Portuguesa — Ensino Médio.', ordem=13)
            self.criar('Currículo EM — Ciências da Natureza e suas Tecnologias',
                       'link', cat,
                       'https://drive.google.com/file/d/1lkF-KXuPbUThYXKA6Ur_WxcdlXvWPJvM/view',
                       'Área de Ciências da Natureza e suas Tecnologias — Ensino Médio.', ordem=14)
            self.criar('Currículo EM — Ciências Humanas e Sociais Aplicadas',
                       'link', cat,
                       'https://drive.google.com/file/d/1U908DVKACU5vsaUWNPciI-xKLc40RHa8/view',
                       'Área de Ciências Humanas e Sociais Aplicadas — Ensino Médio.', ordem=15)
            self.criar('Currículo EM — Matemática e suas Tecnologias',
                       'link', cat,
                       'https://drive.google.com/file/d/1HUz1PZbSCDAA_QIZHxqa1PTyQJFW1exA/view',
                       'Área de Matemática e suas Tecnologias — Ensino Médio.', ordem=16)

        # --- Currículo de Computação ---
        cat = self.get_or_create_sub('Currículo de Computação', 'Documentos Curriculares')
        if cat:
            # Subpage exists but we don't have PDF links yet
            self.criar('Currículo de Computação do Espírito Santo',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/curriculocomputacao/',
                       'Documento curricular de Computação para a Educação Básica do ES.')

        # --- Orientações Curriculares ---
        cat = self.get_or_create_sub('Orientações Curriculares', 'Documentos Curriculares')
        if cat:
            self.criar('Orientações Curriculares 2024',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/orientacoescurriculares',
                       'Orientações curriculares por trimestre — 2024.', ordem=1)
            self.criar('Orientações Curriculares 2023',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/orientacoescurriculares',
                       'Orientações curriculares por trimestre — 2023.', ordem=2)

        # --- Guias de Habilidades ---
        cat = self.get_or_create_sub('Guias de Habilidades', 'Documentos Curriculares')
        if cat:
            self.criar('Guias de Habilidades',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/guiasdehabilidades/',
                       'Guias de habilidades por componente curricular.')

        # --- Cadernos Metodológicos ---
        cat = self.get_or_create_sub('Cadernos Metodológicos', 'Documentos Curriculares')
        if cat:
            self.criar('Cadernos Metodológicos',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/cadernosmetodologicos/',
                       'Cadernos com orientações metodológicas para professores.')

        # --- Mapas de Progressão ---
        cat = self.get_or_create_sub('Mapas de Progressão', 'Documentos Curriculares')
        if cat:
            self.criar('Mapa de Progressão da Aprendizagem',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/progressao/',
                       'Mapas de progressão da aprendizagem por componente curricular.')

        # --- Ementas Curriculares ---
        cat = self.get_or_create_sub('Ementas Curriculares', 'Documentos Curriculares')
        if cat:
            self.criar('Ementas Curriculares',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/ementas/',
                       'Ementas dos componentes curriculares.')

        # --- Aprofundamento em Leitura e Escrita ---
        cat = self.get_or_create_sub('Aprofundamento em Leitura e Escrita', 'Documentos Curriculares')
        if cat:
            self.criar('Aprofundamento em Leitura e Escrita',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/aprofundamento-em-leitura-e-escrita/',
                       'Material de aprofundamento em leitura e escrita.')

        # --- Sequências Didáticas ---
        cat = self.get_or_create_sub('Sequências Didáticas', 'Documentos Curriculares')
        if cat:
            self.criar('Sequências Didáticas do Projeto Aventuras Literárias',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/sequencias-didaticas-do-projeto-aventuras-literarias/',
                       'Sequências didáticas do Projeto Aventuras Literárias.')

        # --- Rotinas de Recomposição ---
        cat = self.get_or_create_sub('Rotinas de Recomposição', 'Documentos Curriculares')
        if cat:
            self.criar('Rotina Pedagógica Escolar — RPE',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/rpe/',
                       'Roteiros pedagógicos para recomposição da aprendizagem.')

        # --- Nivelamento e AMA ---
        cat = self.get_or_create_sub('Nivelamento e AMA', 'Documentos Curriculares')
        if cat:
            self.criar('Material de Apoio para Nivelamento e AMA',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/nivelamentoeama/',
                       'Materiais de apoio para nivelamento e Avaliação Mensal de Aprendizagem.')

        # --- Práticas Experimentais EF ---
        cat = self.get_or_create_sub('Práticas Experimentais EF', 'Documentos Curriculares')
        if cat:
            self.criar('Práticas Experimentais — Ensino Fundamental',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/praticasexperimentaisef/',
                       'Roteiros de práticas experimentais para o Ensino Fundamental.')

        # --- Projeto de Vida EF ---
        cat = self.get_or_create_sub('Projeto de Vida EF', 'Documentos Curriculares')
        if cat:
            self.criar('Projeto de Vida — Ensino Fundamental',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/projetodevidaef/',
                       'Material de Projeto de Vida para o Ensino Fundamental.')

        # --- Projeto de Vida EM ---
        cat = self.get_or_create_sub('Projeto de Vida EM', 'Documentos Curriculares')
        if cat:
            self.criar('Projeto de Vida — Ensino Médio',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/projetodevidaem',
                       'Material de Projeto de Vida para o Ensino Médio.')

        # --- Itinerários Formativos e Projetos Integradores ---
        cat = self.get_or_create_sub('Itinerários Formativos e Projetos Integradores', 'Documentos Curriculares')
        if cat:
            self.stdout.write('  Novos IFAs:')
            self.criar('Orientações para Elaboração dos Projetos Integradores dos IFAs',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/12/ORIENTACOES-PARA-ELABORACAO-DOS-PROJETOS-INTEGRADORES-3.pdf',
                       'Documento orientador para elaboração dos projetos integradores.', ordem=1)
            self.criar('IFA das Quatro Áreas do Conhecimento',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/12/IFA-DAS-QUATRO-AREAS-DO-CONHECIMENTO-FINALIZADO.pdf',
                       'Itinerário Formativo de Aprofundamento: Linguagens, CHSA, CN e Matemática.', ordem=2)
            self.criar('IFA Linguagens e Ciências Humanas',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/12/IFA-LINGCHSA-6-1.pdf',
                       'Itinerário Formativo: Linguagens e CHSA.', ordem=3)
            self.criar('IFA Matemática e Ciências da Natureza',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/12/IFA-CNTMAT.pdf',
                       'Itinerário Formativo: Matemática e CN.', ordem=4)

            self.stdout.write('  Antigos IFAs — Aprofundamentos por Área:')
            self.criar('Aprofundamento — Matemática (Educação Financeira e Fiscal)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf',
                       'Itinerário Formativo anterior — Área de Matemática.', ordem=5)
            self.criar('Referenciais Curriculares para Elaboração de Itinerários Formativos',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/01/Referenciais-Curriculares-para-Elaboracao-de-Itinerarios-Formativos-1-1.pdf',
                       'Documento referencial para elaboração de IFs.', ordem=6)
            self.criar('Aprofundamento — Ciências da Natureza (Terra, Vida e Cosmo)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/Curriculo-EM_Aprofundamento-da-area_-CN_-Alterado_-20_04_22.pdf',
                       'Itinerário Formativo anterior — Área de CN.', ordem=7)
            self.criar('Aprofundamento — Linguagens (Mídias Digitais: Linguagens em Ação)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/Curriculo-EM_Aprofundamento-da-area_-Linguagens_Alterado_19-04.pdf',
                       'Itinerário Formativo anterior — Área de Linguagens.', ordem=8)
            self.criar('Aprofundamento — Ciências Humanas (Modernização, Transformação Social e Meio Ambiente)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/CurriculoEM_Aprofundamento-da-area-de-CHSA.pdf',
                       'Itinerário Formativo anterior — Área de CHSA.', ordem=9)

            self.stdout.write('  Antigos IFAs — Aprofundamentos entre Áreas:')
            self.criar('O Esporte, a Ciência e suas Linguagens (CN e Linguagens)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/Curriculo-EM_Aprofundamento-entreareas_-CN.e-Linguagens_Alterado_20_04_22.pdf',
                       'Aprofundamento entre áreas: CN e Linguagens.', ordem=10)
            self.criar('Energias Renováveis e Eficiência Energética (CN, CHSA, Mat e Linguagens)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/Curriculo-EM_Aprofundamento-entreareas_CN-CHSA-Mat-e-Linguagens_Alterado_20_04_22.pdf',
                       'Aprofundamento entre áreas: CN, CHSA, Mat e Linguagens.', ordem=11)
            self.criar('Narrativas Socioliterárias (Linguagens e CHSA)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/Curriculo-EM_Aprofundamento-entreareas_CHSA-e-Linguagens_Alterado-20_04_22.pdf',
                       'Aprofundamento entre áreas: Linguagens e CHSA.', ordem=12)
            self.criar('Humanidades e Relações Socioambientais (CN e CHSA)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/Curriculo-EM_Aprofundamento-entreareas_-CHSA-e-CN_alterado_20-04-22.pdf',
                       'Aprofundamento entre áreas: CN e CHSA.', ordem=13)
            self.criar('Aspirações Docentes (Linguagens, Matemática, CN e CHSA)',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/04/Aspiracoes-Docentes-versao-revisada.pdf',
                       'Aprofundamento entre áreas: todas as áreas.', ordem=14)

        # --- Materiais de Apoio EM ---
        cat = self.get_or_create_sub('Materiais de Apoio EM', 'Documentos Curriculares')
        if cat:
            self.criar('Materiais de Apoio para Aprofundamentos do Ensino Médio',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/itinerarios/',
                       'Materiais de apoio para os aprofundamentos dos Itinerários Formativos do EM.')

        # --- Guia de Oportunidades EF ---
        cat = self.get_or_create_sub('Guia de Oportunidades EF', 'Documentos Curriculares')
        if cat:
            self.criar('Guia de Oportunidades para o Estudante do Ensino Fundamental',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/guiaoportunidadesef/',
                       'Guia de oportunidades para estudantes do EF.')

        # --- Guia de Oportunidades EM ---
        cat = self.get_or_create_sub('Guia de Oportunidades EM', 'Documentos Curriculares')
        if cat:
            self.criar('Guia de Oportunidades para o Estudante do Ensino Médio Capixaba',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/guiadeoportunidades',
                       'Guia de oportunidades para estudantes do EM.')

        # --- Currículo 2018 ---
        cat = self.get_or_create_sub('Currículo 2018', 'Documentos Curriculares')
        if cat:
            self.criar('Currículo do Espírito Santo — 2018',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/curriculo-2018/',
                       'Versão 2018 do Currículo ES.')

        # --- Currículo 2009 ---
        cat = self.get_or_create_sub('Currículo 2009', 'Documentos Curriculares')
        if cat:
            self.criar('Currículo do Espírito Santo — 2009',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/curriculo-2009/',
                       'Versão 2009 do Currículo ES — CBC.')

        # ──────────────────────────────────────────────
        # 2. PROGRAMAS
        # ──────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO('\n── Programas ──'))

        cat = self.get_or_create_sub('Matemática na Rede', 'Programas')
        if cat:
            self.criar('Programa Matemática na Rede',
                       'link', cat,
                       'https://matematicanarede.sedu.es.gov.br/',
                       'Programa de fortalecimento do ensino de Matemática na rede estadual.')

        cat = self.get_or_create_sub('Educar para a Paz', 'Programas')
        if cat:
            self.criar('Programa Educar para a Paz',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/educarparaapaz/',
                       'Programa de cultura de paz e prevenção à violência escolar.')

        cat = self.get_or_create_sub('Música na Rede', 'Programas')
        if cat:
            self.criar('Programa Música na Rede',
                       'link', cat,
                       'https://musicanarede.fames.es.gov.br/',
                       'Programa de ensino de música em parceria com a FAMES.')

        cat = self.get_or_create_sub('Mais Leitores', 'Programas')
        if cat:
            self.criar('Programa Mais Leitores',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/maisleitores/',
                       'Programa de incentivo à leitura.')

        cat = self.get_or_create_sub('Educação Ambiental', 'Programas')
        if cat:
            self.criar('Programa Educação Ambiental',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/educacaoambiental/',
                       'Programa de educação ambiental da SEDU.')

        cat = self.get_or_create_sub('Sucesso Escolar', 'Programas')
        if cat:
            self.criar('Programa Sucesso Escolar',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/sucessoescolar/',
                       'Programa para redução de reprovação e abandono escolar.')

        cat = self.get_or_create_sub('GEEPEI', 'Programas')
        if cat:
            self.criar('GEEPEI — Espaços Potencialmente Educativos e Inovadores',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/geepei/',
                       'Grupo de Estudos de Espaços Potencialmente Educativos e Inovadores.')

        cat = self.get_or_create_sub('PROETI', 'Programas')
        if cat:
            self.criar('PROETI — Fomento às Escolas Municipais em Tempo Integral',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/proeti/',
                       'Programa Capixaba de Fomento à Implementação das Escolas Municipais em Tempo Integral.')

        cat = self.get_or_create_sub('PIPAT', 'Programas')
        if cat:
            self.criar('PIPAT — Projeto Integrador de Pesquisa e Articulação com o Território',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/pipat/',
                       'Projeto Integrador de Pesquisa e Articulação com o Território.')

        # ──────────────────────────────────────────────
        # 3. LIVRO DIDÁTICO E MATERIAIS
        # ──────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO('\n── Livro Didático e Materiais ──'))

        cat = self.get_or_create_sub('PNLD', 'Livro Didático e Materiais')
        if cat:
            self.criar('PNLD no Espírito Santo — Informações e FAQ',
                       'pagina', cat,
                       resumo='O Programa Nacional do Livro e do Material Didático (PNLD) compreende um conjunto de ações voltadas para a distribuição de obras didáticas, pedagógicas e literárias.',
                       corpo='<p>O <strong>Programa Nacional do Livro e do Material Didático</strong> (PNLD) compreende um conjunto de ações voltadas para a distribuição de obras didáticas, pedagógicas e literárias, entre outros materiais de apoio à prática educativa, destinados aos alunos e professores das escolas públicas de educação básica do País.</p><p>A Coordenação Estadual do Livro Didático encontra-se na Assessoria de Apoio Curricular e Educação Ambiental — telefone (27) 3636-7868/7822 ou geceb@sedu.es.gov.br.</p>',
                       ordem=1)

            # PDFs das SREs - PNLD 2026
            sres = [
                ('SRE Afonso Cláudio', 'SRE-Afonso-Claudio'),
                ('SRE Barra de São Francisco', 'SRE-Barra-de-Sao-Francisco'),
                ('SRE Cachoeiro de Itapemirim', 'SRE-Cachoeiro-de-Itapemirim'),
                ('SRE Carapina "Nilza Pereira Leite"', 'SRE-Carapina-Nilza-Pereira-Leite'),
                ('SRE Cariacica', 'SRE-Cariacica'),
                ('SRE Colatina "Professora Eucy Rossi Pagani"', 'SRE-Colatina-Professora-Eucy-Rossi-Pagani'),
                ('SRE Guaçuí "Comendadora Jurema Moretz Sohn"', 'SRE-Guacui-Comendadora-Jurema-Moretz-Sohn'),
                ('SRE Linhares', 'SRE-Linhares'),
                ('SRE Nova Venécia', 'SRE-Nova-Venecia'),
                ('SRE São Mateus', 'SRE-Sao-Mateus'),
                ('SRE Vila Velha', 'SRE-Vila-Velha'),
            ]
            for i, (nome, arquivo) in enumerate(sres, 2):
                self.criar(f'PNLD 2026 EM — {nome}',
                           'link', cat,
                           f'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/09/{arquivo}.pdf',
                           f'Resultado da unificação da escolha PNLD 2026 — {nome}.', ordem=i)

            self.criar('PNLD 2026 EM — Resumo por Coleção-Editora',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/09/Resumo-do-quantitativo-de-SREs-por-Colecao-Editora-1.pdf',
                       'Resumo do quantitativo de SREs por Coleção-Editora.', ordem=14)

        cat = self.get_or_create_sub('Catálogo de Livros', 'Livro Didático e Materiais')
        if cat:
            self.criar('Catálogo de Livros Físicos — Bibliotecas SEDU',
                       'link', cat,
                       'https://bibliotecas.sedu.es.gov.br/',
                       'Catálogo online de livros físicos das bibliotecas da rede estadual.')

        cat = self.get_or_create_sub('Práticas Experimentais', 'Livro Didático e Materiais')
        if cat:
            self.criar('Práticas Experimentais',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/praticasexperimentais/',
                       'Roteiros de práticas experimentais para Ciências da Natureza.')

        cat = self.get_or_create_sub('Espaços Potencialmente Educativos', 'Livro Didático e Materiais')
        if cat:
            self.criar('Espaços Potencialmente Educativos do Espírito Santo',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/espacoseducativos/',
                       'Mapeamento de espaços educativos não formais no ES.')

        # ──────────────────────────────────────────────
        # 4. MODALIDADES E DIVERSIDADE
        # ──────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO('\n── Modalidades e Diversidade ──'))

        cat = self.get_or_create_sub('EJA — Documentos', 'Modalidades e Diversidade')
        if cat:
            self.criar('Documento Curricular da EJA — DCEJA',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/dceja/',
                       'Documento Curricular da Educação de Jovens e Adultos do ES.')

        cat = self.get_or_create_sub('EJA — Orientações Curriculares', 'Modalidades e Diversidade')
        if cat:
            self.criar('Orientações Curriculares da EJA',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/orientacoescurriculareseja/',
                       'Orientações curriculares específicas para a EJA.')

        cat = self.get_or_create_sub('EJA — Cadernos de Práticas', 'Modalidades e Diversidade')
        if cat:
            self.criar('Cadernos de Práticas da EJA',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/cadernospraticaseja/',
                       'Cadernos de práticas pedagógicas para a EJA.')

        cat = self.get_or_create_sub('EJA — Planos de Curso', 'Modalidades e Diversidade')
        if cat:
            self.criar('Planos de Curso dos Cursos de Qualificação Profissional — EJA',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/eja/',
                       'Planos de curso dos cursos de qualificação profissional integrados ao EM na modalidade EJA.')

        cat = self.get_or_create_sub('Educação do Campo', 'Modalidades e Diversidade')
        if cat:
            self.criar('Educação do Campo',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/educacaodocampo/',
                       'Orientações e materiais para a Educação do Campo.')

        cat = self.get_or_create_sub('Educação Escolar Indígena', 'Modalidades e Diversidade')
        if cat:
            self.criar('Educação Escolar Indígena',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/educacaoescolarindigena/',
                       'Orientações e materiais para a Educação Escolar Indígena.')

        cat = self.get_or_create_sub('Educação Escolar Quilombola', 'Modalidades e Diversidade')
        if cat:
            self.criar('Educação Escolar Quilombola',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/educacaoescolarquilombola',
                       'Orientações e materiais para a Educação Escolar Quilombola.')

        cat = self.get_or_create_sub('Relações Étnico-Raciais', 'Modalidades e Diversidade')
        if cat:
            self.criar('Educação das Relações Étnico-Raciais',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/relacoesetnicoraciais/',
                       'Educação das Relações Étnico-Raciais e Estratégias para a Educação Racial.')

        cat = self.get_or_create_sub('Socioeducação', 'Modalidades e Diversidade')
        if cat:
            self.criar('Socioeducação',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/socioeducacao/',
                       'Orientações para atendimento socioeducativo.')

        cat = self.get_or_create_sub('Educação Integral em Tempo Integral', 'Modalidades e Diversidade')
        if cat:
            self.criar('Educação Integral em Tempo Integral',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/tempo-integral/',
                       'Orientações para a Educação Integral em Tempo Integral.')

        cat = self.get_or_create_sub('Estudos Especiais e Recuperação', 'Modalidades e Diversidade')
        if cat:
            self.criar('Estudos Especiais de Recuperação',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/eer/',
                       'Orientações para estudos especiais e recuperação.')

        cat = self.get_or_create_sub('Busca Ativa Escolar', 'Modalidades e Diversidade')
        if cat:
            self.criar('Busca Ativa Escolar',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/buscaativaescolar/',
                       'Programa de Busca Ativa Escolar.')
            self.criar('Caderno de Ações de Acolhimento, Permanência e Aprendizagem — Busca Ativa',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2025/09/Caderno-de-Acoes-de-Acolhimento-Permanencia-e-Aprendizagem-para-o-Publico-da-Busca-Ativa-Escolar.pdf',
                       'Caderno de ações para o público da Busca Ativa Escolar.', ordem=2)

        # ──────────────────────────────────────────────
        # 5. OLIMPÍADAS E COMPETIÇÕES
        # ──────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO('\n── Olimpíadas e Competições ──'))

        cat = self.get_or_create_sub('Olimpíadas de Física', 'Olimpíadas e Competições')
        if cat:
            self.criar('Olimpíada Brasileira de Física — OBF',
                       'link', cat,
                       'https://www.sbfisica.org.br/v1/olimpiada/2024/',
                       'Site oficial da Olimpíada Brasileira de Física.')
            self.criar('Olimpíada Brasileira de Física das Escolas Públicas — OBFEP',
                       'link', cat,
                       'https://www1.fisica.org.br/~obfep/inscricoes-2025/',
                       'Site oficial da OBFEP — inscrições 2025.')

        cat = self.get_or_create_sub('Olimpíadas de Matemática', 'Olimpíadas e Competições')
        if cat:
            self.criar('Movimento Meninas Olímpicas',
                       'link', cat,
                       'https://olimpiadas.ufsm.br/',
                       'Programa de incentivo à participação feminina em olimpíadas científicas.')

        cat = self.get_or_create_sub('Olimpíadas de Biologia', 'Olimpíadas e Competições')
        if cat:
            self.criar('Olimpíada Brasileira de Biologia Sintética',
                       'link', cat,
                       'https://olimpiadadebiologiasintetica.org/',
                       'Site oficial da Olimpíada de Biologia Sintética.')

        cat = self.get_or_create_sub('Educação Financeira', 'Olimpíadas e Competições')
        if cat:
            self.criar('Olimpíada do Tesouro Direto de Educação Financeira — OLITEF',
                       'link', cat,
                       'https://olitef.com.br/',
                       'Olimpíada de Educação Financeira do Tesouro Direto.')

        cat = self.get_or_create_sub('Empreendedorismo', 'Olimpíadas e Competições')
        if cat:
            self.criar('Olimpíada do Empreendedorismo',
                       'link', cat,
                       'https://olimpiadaempreendedorismo.com.br/',
                       'Olimpíada voltada ao empreendedorismo estudantil.')

        cat = self.get_or_create_sub('Outras Competições', 'Olimpíadas e Competições')
        if cat:
            self.criar('Prêmio Jovem Cientista',
                       'link', cat,
                       'https://jovemcientista.cnpq.br/projeto/premio-jovem-cientista',
                       'Prêmio Jovem Cientista do CNPq.')
            self.criar('Olimpíada do Bem Público — FGV',
                       'link', cat,
                       'https://eppg.fgv.br/iv-olimpiada-do-bem-publico-2024',
                       'Olimpíada do Bem Público — FGV.')
            self.criar('Programa Jovem Senador',
                       'link', cat,
                       'https://www12.senado.leg.br/jovemsenador',
                       'Programa Jovem Senador do Senado Federal.')

        # ──────────────────────────────────────────────
        # 6. INSTITUCIONAL
        # ──────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO('\n── Institucional ──'))

        cat = self.get_or_create_sub('Sobre a GECEB', 'Institucional')
        if cat:
            self.criar('Sobre a Gerência de Currículo da Educação Básica',
                       'pagina', cat,
                       resumo='A GECEB é responsável pela elaboração, implementação e acompanhamento do Currículo do Espírito Santo.',
                       corpo='<p>A <strong>Gerência de Currículo da Educação Básica (GECEB)</strong> é responsável pela elaboração, implementação e acompanhamento do Currículo do Espírito Santo para toda a Educação Básica.</p><p><strong>Contato:</strong><br>E-mail: gerenciadecurriculo@sedu.es.gov.br<br>Telefone: (27) 3636-7838 / 7842</p><p><strong>Endereço:</strong><br>Secretaria de Estado da Educação (SEDU)<br>Av. César Hilal, 1111 – Santa Lúcia<br>CEP: 29056-085 – Vitória / ES</p>')

        cat = self.get_or_create_sub('Revista Diálogos', 'Institucional')
        if cat:
            self.criar('Revista Diálogos',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/revistadialogos/',
                       'Revista Diálogos — publicação da GECEB/SEDU.')

        cat = self.get_or_create_sub('Currículo Interativo', 'Institucional')
        if cat:
            self.criar('Currículo Interativo',
                       'link', cat,
                       'https://curriculointerativo.sedu.es.gov.br/',
                       'Plataforma do Currículo Interativo do Espírito Santo.')

        cat = self.get_or_create_sub('Notícias e Informes', 'Institucional')
        if cat:
            self.criar('Mitigação de Desigualdades na Educação Básica pela Educação Especial Inclusiva',
                       'link', cat,
                       'https://curriculo.sedu.es.gov.br/curriculo/documentoscurriculares/',
                       'A Mitigação de Desigualdades na Educação Básica do ES pela via da Educação Especial na Perspectiva Inclusiva.')

        # ── RESUMO ──
        total = Conteudo.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n═══ Migração concluída! {total} conteúdos no banco. ═══\n'))
