from django.contrib import admin
from .models import PageView, DownloadEvent, SearchQuery, AlertaInteligencia


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('url', 'tipo_pagina', 'dispositivo', 'navegador', 'timestamp')
    list_filter = ('tipo_pagina', 'dispositivo', 'navegador')
    search_fields = ('url', 'objeto_slug')
    date_hierarchy = 'timestamp'
    readonly_fields = ('url', 'tipo_pagina', 'objeto_id', 'objeto_slug', 'timestamp',
                       'sessao_id', 'ip', 'user_agent', 'referrer', 'dispositivo', 'navegador')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DownloadEvent)
class DownloadEventAdmin(admin.ModelAdmin):
    list_display = ('nome_arquivo', 'extensao', 'timestamp')
    list_filter = ('extensao',)
    search_fields = ('nome_arquivo',)
    date_hierarchy = 'timestamp'
    readonly_fields = ('anexo_id', 'conteudo_id', 'nome_arquivo', 'extensao',
                       'url', 'timestamp', 'sessao_id', 'ip')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('termo', 'n_resultados', 'timestamp')
    search_fields = ('termo',)
    date_hierarchy = 'timestamp'
    readonly_fields = ('termo', 'termo_normalizado', 'n_resultados', 'timestamp',
                       'sessao_id', 'ip')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AlertaInteligencia)
class AlertaInteligenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'resolvido', 'criado_em')
    list_filter = ('tipo', 'resolvido')
    search_fields = ('titulo', 'descricao')
    list_editable = ('resolvido',)
