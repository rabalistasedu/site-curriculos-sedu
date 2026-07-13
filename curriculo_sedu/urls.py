from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from conteudo.admin_views import (
    organizar_view, adicionar_arquivos_view, api_subcategorias_itens,
    barra_superior_view,
)
from conteudo.media_views import serve_media

urlpatterns = [
    path('admin/painel-central/', include('painel.urls')),
    path('admin/adicionar-arquivos/', admin.site.admin_view(adicionar_arquivos_view), name='admin_adicionar_arquivos'),
    path('admin/api/subcategorias/', admin.site.admin_view(api_subcategorias_itens), name='api_subcategorias_itens'),
    path('admin/organizar/', admin.site.admin_view(organizar_view), name='admin_organizar'),
    path('admin/barra-superior/', admin.site.admin_view(barra_superior_view), name='admin_barra_superior'),
    path('admin/', admin.site.urls),
    path('', include('conteudo.urls')),
]

# Servir arquivos de mídia com suporte a Range Requests (necessário para vídeo via ngrok)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve_media),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
