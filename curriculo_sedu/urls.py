from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from conteudo.admin_views import (
    organizar_view, adicionar_arquivos_view, api_subcategorias_itens,
    barra_superior_view, editor_rodape_view, area_do_site_view, lixeira_view,
    paginas_livres_view,
)
from conteudo.arvore_views import estrutura_arvores_view, arvore_api
from conteudo.media_views import serve_media

urlpatterns = [
    path('admin/painel-central/', include('painel.urls')),
    path('admin/adicionar-arquivos/', admin.site.admin_view(adicionar_arquivos_view), name='admin_adicionar_arquivos'),
    path('admin/api/subcategorias/', admin.site.admin_view(api_subcategorias_itens), name='api_subcategorias_itens'),
    path('admin/organizar/', admin.site.admin_view(organizar_view), name='admin_organizar'),
    path('admin/barra-superior/', admin.site.admin_view(barra_superior_view), name='admin_barra_superior'),
    path('admin/editor-rodape/', admin.site.admin_view(editor_rodape_view), name='admin_editor_rodape'),
    path('admin/area-do-site/', admin.site.admin_view(area_do_site_view), name='admin_area_do_site'),
    path('admin/estrutura-arvores/', admin.site.admin_view(estrutura_arvores_view), name='admin_estrutura_arvores'),
    path('admin/estrutura-arvores/api/', admin.site.admin_view(arvore_api), name='admin_arvore_api'),
    path('admin/lixeira/', admin.site.admin_view(lixeira_view), name='admin_lixeira'),
    path('admin/paginas-livres/', admin.site.admin_view(paginas_livres_view), name='admin_paginas_livres'),
    path('admin/inteligencia/', include('inteligencia.urls')),
    path('admin/', admin.site.urls),
    path('', include('conteudo.urls')),
]

# Servir arquivos de mídia com suporte a Range Requests (necessário para vídeo via ngrok)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve_media),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
