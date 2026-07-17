"""
Controle de acesso aos painéis administrativos personalizados (Organizador,
Painel Central, Barra Superior, Editor do Rodapé, Área do Site, Estrutura
de Árvores, Central de Inteligência, Adicionar Arquivos).

As permissões em si são declaradas em Meta.permissions dos models
ConfiguracaoSite (conteudo), Vinculo (painel) e AlertaInteligencia
(inteligencia) — aparecem nativamente na tela de Usuário/Grupo em
"Autenticação e Autorização". Este decorator só faz a checagem, empilhado
junto ao @staff_member_required já existente em cada view (não substitui).
Superusuário sempre passa (comportamento padrão do Django).
"""
from functools import wraps

from django.core.exceptions import PermissionDenied


def exige_permissao_painel(codename):
    """Decorator: exige a permissão indicada (ex.: 'conteudo.pode_acessar_organizador')."""
    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(codename):
                raise PermissionDenied('Você não tem permissão para acessar este painel.')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador
