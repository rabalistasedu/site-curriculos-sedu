from django.core.management.base import BaseCommand

from conteudo.admin_views import _purgar_lixeira_expirada, LIXEIRA_PRAZO_DIAS


class Command(BaseCommand):
    help = (
        f'Exclui definitivamente (hard delete) botões e conteúdos que estão na '
        f'lixeira há mais de {LIXEIRA_PRAZO_DIAS} dias. A mesma limpeza já roda '
        f'automaticamente toda vez que a tela "Lixeira" do admin é aberta — este '
        f'comando é opcional, para quem preferir agendar no Windows (mesmo padrão '
        f'do sincronizar_teams). Idempotente — seguro rodar quantas vezes quiser.'
    )

    def handle(self, *args, **options):
        n_categorias, n_conteudos = _purgar_lixeira_expirada()
        self.stdout.write(self.style.SUCCESS(
            f'Limpeza concluída: {n_categorias} botão(ões) e {n_conteudos} '
            f'conteúdo(s) excluído(s) definitivamente (estavam há mais de '
            f'{LIXEIRA_PRAZO_DIAS} dias na lixeira).'
        ))
