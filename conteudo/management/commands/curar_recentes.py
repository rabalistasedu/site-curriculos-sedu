"""
Marca a curadoria oficial de "Conteúdos recentes" (seção da home, lista
lateral esquerda) — para que essa seleção seja idêntica em qualquer
ambiente (local, PythonAnywhere, outro computador), sem precisar clicar
manualmente no admin em cada lugar.

O campo Conteudo.recente controla o que aparece nessa lista (ver
conteudo/views.py: home()). Como o banco de dados (db.sqlite3) não é
versionado no Git — cada ambiente tem o seu — este comando é a forma
automatizada de reproduzir a mesma curadoria em qualquer lugar: basta
rodar `python manage.py curar_recentes` depois de popular o banco.

Para trocar a seleção no futuro, edite a lista URLS_RECENTES abaixo
(usa a URL do documento como chave, igual aos comandos de migração) e
rode o comando de novo — ele ATUALIZA a seleção inteira (marca os da
lista, desmarca quem não estiver mais nela).

Idempotente: rodar várias vezes sempre produz o mesmo resultado.
"""
from django.core.management.base import BaseCommand
from conteudo.models import Conteudo

# URLs dos documentos que devem aparecer em "Conteúdos recentes".
# Escolhidos para representar as principais novidades do site.
URLS_RECENTES = [
    'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2026/05/ORIENTACOES-PARA-ELABORACAO-PROJETO-INTEGRADOR-IFA.-FINAL-SEQ-DIDATICA.pdf',
    'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2026/02/9o-ano-1o-TRIMESTRE-2026-LP.pdf',
    'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2022/06/HIST_GEO-PAEBES-MATRIZ-CH-9EF.pdf',
    'https://www.sbfisica.org.br/v1/olimpiada/2024/',
    'https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2026/05/Curriculo-ES-2020-Vol-01-Educacao-Infantil-REV2026.pdf',
]


class Command(BaseCommand):
    help = 'Marca a curadoria oficial de "Conteúdos recentes" da home (idempotente)'

    def handle(self, *args, **options):
        marcados = 0
        nao_encontrados = 0

        for url in URLS_RECENTES:
            doc = Conteudo.objects.filter(url_externa=url).first()
            if not doc:
                nao_encontrados += 1
                self.stdout.write(self.style.WARNING(f'  ⚠ não encontrado: {url}'))
                continue
            if not doc.recente:
                doc.recente = True
                doc.save()
                marcados += 1
                self.stdout.write(f'  ✔ marcado: {doc.titulo}')
            else:
                self.stdout.write(f'  — já estava marcado: {doc.titulo}')

        # Desmarca qualquer item que esteja marcado mas não faça mais
        # parte da lista atual (mantém a seleção sempre em sincronia)
        desmarcados = 0
        for doc in Conteudo.objects.filter(recente=True):
            if doc.url_externa not in URLS_RECENTES:
                doc.recente = False
                doc.save()
                desmarcados += 1
                self.stdout.write(f'  × desmarcado (fora da curadoria atual): {doc.titulo}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: {marcados} marcados, {desmarcados} desmarcados, '
            f'{nao_encontrados} não encontrados no banco.'
        ))
