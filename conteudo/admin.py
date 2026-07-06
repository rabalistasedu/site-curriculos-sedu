from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count
from .models import Categoria, Conteudo, Banner, ConfiguracaoSite, Comentario, Cartaz
from .forms import BannerAdminForm, ConteudoAdminForm, CategoriaAdminForm, ConfiguracaoSiteAdminForm


# ── Customização global do Admin ──────────────────────────────────────
admin.site.site_header = 'Currículo SEDU — Painel Administrativo'
admin.site.site_title = 'Currículo SEDU Admin'
admin.site.index_title = 'Gerenciar conteúdo do site'


# ── Categoria ─────────────────────────────────────────────────────────
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaAdminForm
    list_display = ['nome', 'categoria_pai', 'ordem', 'ativa', 'total_conteudos']
    list_filter = ['ativa', 'categoria_pai']
    list_editable = ['ordem', 'ativa']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}

    fieldsets = (
        (None, {
            'fields': ('nome', 'slug', 'descricao', 'categoria_pai'),
            'description': (
                'Dica: se o campo "URL amigável" aparecer preenchido sozinho com um '
                'endereço estranho ao criar uma categoria nova, é uma sugestão de '
                'preenchimento automático do navegador (não é um erro do site) — '
                'basta apagar e digitar o texto correto, ou deixar em branco que o '
                'sistema preenche automaticamente a partir do nome.'
            ),
        }),
        ('Aparência', {
            'fields': ('icone', 'imagem', 'ordem', 'ativa'),
        }),
    )

    def total_conteudos(self, obj):
        count = obj.conteudos.filter(status='publicado').count()
        return count
    total_conteudos.short_description = 'Publicados'


# ── Conteúdo ──────────────────────────────────────────────────────────
@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    form = ConteudoAdminForm
    list_display = ['titulo', 'tipo_badge', 'area_destino', 'status_badge', 'destaque', 'recente', 'data_publicacao']
    list_filter = ['tipo', 'status', 'destaque', 'recente', 'categoria__categoria_pai', 'categoria']
    list_editable = ['destaque', 'recente']
    search_fields = ['titulo', 'resumo', 'corpo']
    date_hierarchy = 'data_publicacao'
    prepopulated_fields = {'slug': ('titulo',)}

    fieldsets = (
        ('📍 Onde publicar no site', {
            'fields': ('categoria',),
            'description': (
                'Escolha em qual área do site este conteúdo vai aparecer. '
                'As opções mostram a categoria pai → subcategoria (ex: Documentos Curriculares → Currículo Atual). '
                'Para aparecer direto em uma categoria principal, selecione apenas ela.'
            ),
        }),
        ('📝 Informações básicas', {
            'fields': ('titulo', 'slug', 'tipo', 'resumo'),
        }),
        ('📄 Conteúdo', {
            'fields': ('corpo',),
            'description': 'Use para posts e páginas com texto formatado.',
        }),
        ('📎 Arquivo / Mídia / Link', {
            'fields': ('arquivo', 'url_video', 'url_externa', 'imagem_destaque'),
            'description': (
                'Documento PDF: use "Arquivo". '
                'Vídeo YouTube/Vimeo: use "URL do vídeo". '
                'Site externo: use "Link externo".'
            ),
            'classes': ('collapse',),
        }),
        ('🎨 Ícone do card', {
            'fields': ('icone_manual',),
            'description': (
                'Aparece no card quando não há "Imagem de destaque". '
                'Escolha "Automático" para o site decidir sozinho, ou clique em um '
                'ícone específico para usar sempre esse.'
            ),
        }),
        ('⚙️ Publicação', {
            'fields': ('status', 'destaque', 'recente', 'ordem', 'autor', 'data_publicacao'),
            'description': (
                'Status "Publicado" torna o conteúdo visível no site. '
                '"Destaque" aparece na seção de destaques da home. '
                '"Aparecer em Conteúdos recentes" adiciona à lista lateral esquerda da home '
                '(marque só nos itens que você quer destacar como recentes; se desmarcar, o item '
                'continua aparecendo normalmente na categoria escolhida). '
                '📅 Agendamento: coloque uma data/hora futura em "Data de publicação" com status '
                '"Publicado" — o conteúdo fica pronto mas só aparece no site automaticamente '
                'quando a data/hora chegar.'
            ),
        }),
    )

    def area_destino(self, obj):
        """Mostra de forma clara onde o conteúdo vai aparecer no site."""
        if not obj.categoria:
            return format_html('<span style="color:#9ca3af; font-size:12px;">— sem área —</span>')
        if obj.categoria.categoria_pai:
            return format_html(
                '<span style="font-size:12px; color:#6b7280;">{}</span>'
                '<br><strong style="color:#2d5a8e;">{}</strong>',
                obj.categoria.categoria_pai.nome,
                obj.categoria.nome,
            )
        return format_html(
            '<strong style="color:#2d5a8e;">{}</strong>',
            obj.categoria.nome,
        )
    area_destino.short_description = 'Área no site'
    area_destino.admin_order_field = 'categoria__nome'

    def tipo_badge(self, obj):
        cores = {
            'documento': '#2563eb',
            'video': '#dc2626',
            'post': '#059669',
            'link': '#7c3aed',
            'pagina': '#d97706',
        }
        cor = cores.get(obj.tipo, '#6b7280')
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:600;">{}</span>',
            cor, obj.get_tipo_display()
        )
    tipo_badge.short_description = 'Tipo'
    tipo_badge.admin_order_field = 'tipo'

    def status_badge(self, obj):
        # Publicado com data futura = agendado, ainda não aparece no site.
        if obj.status == 'publicado' and obj.data_publicacao > timezone.now():
            return format_html(
                '<span style="background:#7c3aed; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:11px; font-weight:600;">'
                '⏰ Agendado — {}</span>',
                obj.data_publicacao.strftime('%d/%m/%Y %H:%M')
            )
        cores = {
            'rascunho': '#f59e0b',
            'publicado': '#10b981',
            'arquivado': '#6b7280',
        }
        cor = cores.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:600;">{}</span>',
            cor, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    actions = ['publicar_selecionados', 'arquivar_selecionados']

    @admin.action(description='✅ Publicar selecionados')
    def publicar_selecionados(self, request, queryset):
        queryset.update(status='publicado')

    @admin.action(description='📦 Arquivar selecionados')
    def arquivar_selecionados(self, request, queryset):
        queryset.update(status='arquivado')


# ── Banner ────────────────────────────────────────────────────────────
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    form = BannerAdminForm
    list_display = ['titulo', 'area_banner', 'preview_imagem', 'ordem', 'ativo']
    list_editable = ['ordem', 'ativo']

    fieldsets = (
        ('📍 Onde este banner vai aparecer', {
            'fields': ('categoria',),
            'description': (
                'Clique em um botão abaixo para escolher onde o banner será exibido. '
                'Escolha "Página inicial" para aparecer no topo do site, '
                'ou selecione uma área específica para aparecer dentro daquela seção.'
            ),
        }),
        ('📝 Conteúdo do banner', {
            'fields': ('titulo', 'subtitulo', 'link'),
        }),
        ('🖼️ Imagem', {
            'fields': ('imagem', 'tamanho'),
            'description': (
                'Qualquer formato de imagem funciona (horizontal ou vertical) — '
                'ela nunca será cortada ou distorcida. Use "Tamanho" para controlar '
                'a altura do banner na página.'
            ),
        }),
        ('⚙️ Exibição', {
            'fields': ('ordem', 'ativo'),
        }),
    )

    def area_banner(self, obj):
        if not obj.categoria:
            return format_html(
                '<span style="background:#0369a1;color:white;padding:3px 10px;'
                'border-radius:12px;font-size:11px;font-weight:600;">🏠 Home</span>'
            )
        if obj.categoria.categoria_pai:
            return format_html(
                '<span style="font-size:11px;color:#6b7280;">{}</span> → '
                '<strong style="color:#2d5a8e;">{}</strong>',
                obj.categoria.categoria_pai.nome,
                obj.categoria.nome,
            )
        return format_html('<strong style="color:#2d5a8e;">{}</strong>', obj.categoria.nome)
    area_banner.short_description = 'Aparece em'

    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="height:40px; border-radius:4px;" />',
                obj.imagem.url
            )
        return '—'
    preview_imagem.short_description = 'Preview'


# ── Comentários ───────────────────────────────────────────────────────
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'conteudo_link', 'texto_resumido', 'aprovado', 'data_criacao']
    list_filter = ['aprovado', 'data_criacao']
    list_editable = ['aprovado']
    search_fields = ['nome', 'email', 'texto', 'conteudo__titulo']
    readonly_fields = ['nome', 'email', 'texto', 'conteudo', 'data_criacao']
    ordering = ['-data_criacao']

    fieldsets = (
        ('💬 Comentário recebido', {
            'fields': ('conteudo', 'nome', 'email', 'texto', 'data_criacao'),
        }),
        ('✅ Moderação', {
            'fields': ('aprovado',),
            'description': 'Marque "Aprovado" para publicar o comentário no site. Desmarque para ocultar.',
        }),
    )

    def conteudo_link(self, obj):
        return format_html(
            '<a href="/admin/conteudo/conteudo/{}/change/" style="color:#2d5a8e;">{}</a>',
            obj.conteudo.pk,
            obj.conteudo.titulo[:50]
        )
    conteudo_link.short_description = 'Conteúdo'

    def texto_resumido(self, obj):
        return obj.texto[:80] + '…' if len(obj.texto) > 80 else obj.texto
    texto_resumido.short_description = 'Texto'

    def aprovado_badge(self, obj):
        if obj.aprovado:
            return format_html('<span style="color:#10b981; font-weight:700;">✓ Aprovado</span>')
        return format_html('<span style="color:#f59e0b; font-weight:700;">⏳ Aguardando</span>')
    aprovado_badge.short_description = 'Status'

    actions = ['aprovar_selecionados', 'reprovar_selecionados', 'excluir_selecionados']

    @admin.action(description='✅ Aprovar comentários selecionados')
    def aprovar_selecionados(self, request, queryset):
        queryset.update(aprovado=True)
        self.message_user(request, f'{queryset.count()} comentário(s) aprovado(s).')

    @admin.action(description='❌ Reprovar / ocultar comentários selecionados')
    def reprovar_selecionados(self, request, queryset):
        queryset.update(aprovado=False)
        self.message_user(request, f'{queryset.count()} comentário(s) ocultado(s).')

    @admin.action(description='🗑️ Excluir comentários selecionados')
    def excluir_selecionados(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} comentário(s) excluído(s) permanentemente.')


# ── Cartazes ─────────────────────────────────────────────────────────
@admin.register(Cartaz)
class CartazAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'lado_badge', 'preview_imagem', 'ordem', 'ativo']
    list_filter = ['lado', 'ativo']
    list_editable = ['ordem', 'ativo']

    fieldsets = (
        ('🖼️ Cartaz do evento', {
            'fields': ('titulo', 'imagem', 'link'),
            'description': (
                'Suba a imagem do cartaz e cole o link do evento. '
                'O cartaz aparece discretamente nas laterais da página principal.'
            ),
        }),
        ('⚙️ Posição e exibição', {
            'fields': ('lado', 'tamanho', 'ordem', 'ativo'),
            'description': 'Escolha em qual lado da página o cartaz vai aparecer e o tamanho desejado.',
        }),
    )

    def lado_badge(self, obj):
        cor = '#2d5a8e' if obj.lado == 'esquerdo' else '#7c3aed'
        emoji = '⬅️' if obj.lado == 'esquerdo' else '➡️'
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;'
            'border-radius:12px;font-size:11px;font-weight:600;">'
            '{} {}</span>',
            cor, emoji, obj.get_lado_display()
        )
    lado_badge.short_description = 'Lado'

    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:4px;" />',
                obj.imagem.url
            )
        return '—'
    preview_imagem.short_description = 'Preview'


# ── Configuração do site ──────────────────────────────────────────────
@admin.register(ConfiguracaoSite)
class ConfiguracaoSiteAdmin(admin.ModelAdmin):
    form = ConfiguracaoSiteAdminForm
    list_display = ['nome_site', 'email_contato', 'telefone']

    fieldsets = (
        ('📝 Texto da página inicial', {
            'fields': ('home_titulo', 'home_texto'),
            'description': (
                'Este é o título e o texto que aparecem na home, logo abaixo do banner. '
                'Use a barra de ferramentas para negrito, itálico, sublinhado e alinhamento.'
            ),
        }),
        ('🏢 Dados institucionais', {
            'fields': ('nome_site', 'descricao', 'email_contato', 'telefone', 'endereco'),
        }),
        ('🖼️ Identidade visual', {
            'fields': ('logo', 'favicon'),
        }),
    )

    def has_add_permission(self, request):
        return not ConfiguracaoSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
