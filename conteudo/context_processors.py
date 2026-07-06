from .models import Categoria, ConfiguracaoSite


def site_config(request):
    """Disponibiliza dados globais em todos os templates"""
    return {
        'config': ConfiguracaoSite.get_config(),
        'menu_categorias': Categoria.objects.filter(ativa=True, categoria_pai__isnull=True),
    }
