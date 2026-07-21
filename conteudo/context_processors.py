from .models import Categoria, ConfiguracaoSite, RodapeImagem


def site_config(request):
    """Disponibiliza dados globais em todos os templates"""
    imagens_rodape = list(RodapeImagem.objects.all())
    return {
        'config': ConfiguracaoSite.get_config(),
        'menu_categorias': Categoria.objects.filter(
            ativa=True, categoria_pai__isnull=True, mostrar_menu_superior=True
        ),
        'imagens_rodape_esq': [i for i in imagens_rodape if i.alinhamento == 'esquerda'],
        'imagens_rodape_centro': [i for i in imagens_rodape if i.alinhamento == 'centro'],
        'imagens_rodape_dir': [i for i in imagens_rodape if i.alinhamento == 'direita'],
    }
