from django.contrib import admin
from .models import Vinculo, EstiloBotao


@admin.register(Vinculo)
class VinculoAdmin(admin.ModelAdmin):
    list_display = ['conteudo', 'categoria', 'ordem', 'pulsante', 'criado_em']
    list_filter = ['categoria', 'pulsante']
    list_editable = ['ordem', 'pulsante']
    search_fields = ['conteudo__titulo', 'categoria__nome']
    autocomplete_fields = []


@admin.register(EstiloBotao)
class EstiloBotaoAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'cor_fundo', 'cor_texto', 'tamanho_fonte', 'alinhamento', 'pulsante']
    list_filter = ['pulsante']
    list_editable = ['pulsante']
    search_fields = ['categoria__nome']
