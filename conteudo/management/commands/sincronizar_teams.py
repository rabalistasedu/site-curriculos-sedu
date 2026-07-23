from django.core.management.base import BaseCommand
from django.conf import settings

from conteudo.teams_integration import vincular_mensagens_pendentes, verificar_respostas


class Command(BaseCommand):
    help = (
        'Sincroniza a integração de comentários com o Microsoft Teams (grupo GECEB): '
        'vincula mensagens já postadas no canal aos comentários correspondentes e '
        'verifica se chegaram respostas novas da equipe. Idempotente — seguro rodar '
        'quantas vezes quiser, inclusive em intervalos curtos (ex.: a cada 3-5 min).'
    )

    def handle(self, *args, **options):
        if not getattr(settings, 'TEAMS_CLIENT_ID', ''):
            self.stdout.write(self.style.WARNING(
                'Integração com Teams ainda não configurada (TEAMS_CLIENT_ID vazio). '
                'Nada para fazer — configure as variáveis TEAMS_* quando a TI da SEDU '
                'liberar o cadastro no Azure AD. Veja o guia de configuração do Teams.'
            ))
            return

        vinculados = vincular_mensagens_pendentes()
        respondidos = verificar_respostas()

        self.stdout.write(self.style.SUCCESS(
            f'Sincronização concluída: {vinculados} comentário(s) vinculado(s) à '
            f'mensagem do Teams, {respondidos} resposta(s) nova(s) importada(s).'
        ))
