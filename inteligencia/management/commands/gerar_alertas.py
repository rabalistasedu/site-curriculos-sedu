from django.core.management.base import BaseCommand
from inteligencia.alertas import (
    verificar_documentos_sem_acesso,
    verificar_links_quebrados,
    verificar_arquivos_ausentes,
    verificar_picos_acesso,
)


class Command(BaseCommand):
    help = 'Gera alertas de inteligencia (documentos sem acesso, links quebrados, arquivos ausentes, picos)'

    def add_arguments(self, parser):
        parser.add_argument('--skip-links', action='store_true',
                            help='Pular verificacao de links (demora mais)')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Verificando documentos sem acesso...'))
        n = verificar_documentos_sem_acesso(dias=90)
        self.stdout.write(f'  {n} alertas criados')

        if not options['skip_links']:
            self.stdout.write(self.style.NOTICE('Verificando links quebrados...'))
            n = verificar_links_quebrados()
            self.stdout.write(f'  {n} alertas criados')
        else:
            self.stdout.write('  Links pulados (--skip-links)')

        self.stdout.write(self.style.NOTICE('Verificando arquivos ausentes...'))
        n = verificar_arquivos_ausentes()
        self.stdout.write(f'  {n} alertas criados')

        self.stdout.write(self.style.NOTICE('Verificando picos de acesso...'))
        n = verificar_picos_acesso()
        self.stdout.write(f'  {n} alertas criados')

        from inteligencia.models import AlertaInteligencia
        total = AlertaInteligencia.objects.filter(resolvido=False).count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal de alertas ativos: {total}'))
