from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from conteudo.admin_views import organizar_view

urlpatterns = [
    path('admin/organizar/', admin.site.admin_view(organizar_view), name='admin_organizar'),
    path('admin/', admin.site.urls),
    path('', include('conteudo.urls')),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
