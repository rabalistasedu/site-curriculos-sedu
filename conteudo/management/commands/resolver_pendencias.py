"""
Resolve as 3 pendências da migração do WordPress (decisão do Dan, 2026-07-10):

- pk 58 "GEEPEI — Espaços Potencialmente Educativos e Inovadores":
  a URL antiga hoje mostra outro conteúdo e o original não foi encontrado
  em lugar nenhum do site antigo → ARQUIVADO (some do site, continua no
  admin e pode ser restaurado se o conteúdo original reaparecer).

- pk 20 "Orientações Curriculares 2024" e pk 21 "Orientações Curriculares 2023":
  as URLs antigas só exibem a versão 2026 — as versões 2023/2024 não
  existem mais → ARQUIVADOS (a versão vigente já está migrada na
  categoria "Orientações Curriculares").

Idempotente: rodar de novo não muda nada. Confere o título antes de agir
para nunca arquivar o item errado se os pks forem outros em outro banco.
"""
from django.core.management.base import BaseCommand
from conteudo.models import Conteudo

PENDENCIAS = [
    (58, 'GEEPEI'),
    (20, 'Orientações Curriculares 2024'),
    (21, 'Orientações Curriculares 2023'),
]


class Command(BaseCommand):
    help = 'Arquiva os 3 conteúdos pendentes da migração do WordPress (GEEPEI e Orientações 2023/2024).'

    def handle(self, *args, **options):
        for pk, trecho_titulo in PENDENCIAS:
            try:
                c = Conteudo.objects.get(pk=pk)
            except Conteudo.DoesNotExist:
                # Banco diferente: procura pelo título
                c = Conteudo.objects.filter(titulo__icontains=trecho_titulo).first()
                if not c:
                    self.stdout.write(self.style.WARNING(
                        f'  [AVISO] "{trecho_titulo}" não encontrado — nada a fazer.'))
                    continue
            if trecho_titulo.lower() not in c.titulo.lower():
                self.stdout.write(self.style.WARNING(
                    f'  [AVISO] pk {pk} tem outro título ("{c.titulo[:50]}") — pulado por segurança.'))
                continue
            if c.status == 'arquivado':
                self.stdout.write(f'  [OK] "{c.titulo[:60]}" já estava arquivado.')
                continue
            c.status = 'arquivado'
            c.save(update_fields=['status'])
            self.stdout.write(self.style.SUCCESS(f'  [OK] "{c.titulo[:60]}" arquivado.'))

        self.stdout.write(self.style.SUCCESS('Pendências resolvidas.'))
