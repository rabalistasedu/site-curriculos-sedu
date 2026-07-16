from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Remove registros de analytics mais antigos que N meses (default: 12)'

    def add_arguments(self, parser):
        parser.add_argument('--meses', type=int, default=12,
                            help='Meses de retencao (default: 12)')
        parser.add_argument('--dry-run', action='store_true',
                            help='Apenas mostra o que seria excluido')

    def handle(self, *args, **options):
        from inteligencia.models import PageView, DownloadEvent, SearchQuery

        meses = options['meses']
        limite = timezone.now() - timedelta(days=meses * 30)
        dry = options['dry_run']

        for modelo, nome in [(PageView, 'PageViews'), (DownloadEvent, 'Downloads'), (SearchQuery, 'Pesquisas')]:
            qs = modelo.objects.filter(timestamp__lt=limite)
            count = qs.count()
            if dry:
                self.stdout.write(f'  {nome}: {count} registros seriam excluidos')
            else:
                qs.delete()
                self.stdout.write(f'  {nome}: {count} registros excluidos')

        modo = ' (DRY RUN)' if dry else ''
        self.stdout.write(self.style.SUCCESS(f'Limpeza concluida{modo} (retencao: {meses} meses)'))
