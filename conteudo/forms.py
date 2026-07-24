from django import forms
from .models import Banner, Conteudo, Categoria, ConfiguracaoSite
from .widgets import CategoriaPicker, IconPicker, RichTextWidget



class BannerAdminForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'categoria': CategoriaPicker(include_home=True),
        }


class ConteudoAdminForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = '__all__'
        widgets = {
            'categoria': CategoriaPicker(include_home=False),
            'icone_manual': IconPicker(),
            'icone_imagem': forms.FileInput(attrs={
                'accept': '.ico,.png,.jpg,.jpeg,.svg,.webp,.gif',
            }),
            'arquivo': forms.FileInput(attrs={
                'accept': (
                    '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,'
                    '.mp4,.avi,.mov,.mkv,.webm,'
                    '.jpg,.jpeg,.png,.gif,.webp,'
                    '.zip,.rar,.txt,.csv,.odt,.ods,.odp'
                ),
            }),
        }


class CategoriaAdminForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'icone': IconPicker(),
            'icone_imagem': forms.FileInput(attrs={
                'accept': '.ico,.png,.jpg,.jpeg,.svg,.webp,.gif',
            }),
            'slug': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # "Categoria pai" em ÁRVORE ordenada com indentação (como o select
        # "Criar botão" do Painel Central) — antes vinha em ordem aleatória
        # no formato "Pai → Filho", difícil de localizar qualquer botão.
        campo = self.fields.get('categoria_pai')
        if campo:
            widget = campo.widget
            # desembrulha o RelatedFieldWidgetWrapper do admin (botões +/lápis)
            alvo = getattr(widget, 'widget', widget)
            alvo.choices = self._arvore_choices()
            # habilita a caixinha de pesquisa (static/js/filtro_select.js,
            # carregado pelo Media do CategoriaAdmin)
            alvo.attrs['data-pesquisavel'] = '🔍 Pesquisar botão pai...'

    def _arvore_choices(self):
        filhos = {}
        for c in Categoria.objects.order_by('ordem', 'nome'):
            filhos.setdefault(c.categoria_pai_id, []).append(c)

        proprio_pk = self.instance.pk
        itens = [('', '— Nenhuma (botão do nível principal) —')]

        def caminhar(pai_id, nivel):
            for c in filhos.get(pai_id, []):
                if c.pk == proprio_pk:
                    # pula a própria categoria (e a subárvore dela) —
                    # um botão não pode ficar dentro de si mesmo
                    continue
                recuo = ' ' * (nivel * 4)
                itens.append((c.pk, f'{recuo}{"└ " if nivel else ""}{c.nome}'))
                caminhar(c.pk, nivel + 1)

        caminhar(None, 0)
        return itens


class ConfiguracaoSiteAdminForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSite
        fields = '__all__'
        widgets = {
            'home_texto': RichTextWidget(),
            'home_intro_cor_fundo': forms.TextInput(attrs={'type': 'color', 'style': 'height:40px;width:80px;padding:2px;'}),
        }


class TituloSecoesForm(forms.ModelForm):
    """Título + ícone das 3 seções da home (Destaques / Conteúdos recentes /
    Navegue por área) — painel "Área do Site". As imagens de ícone
    (icone_*_imagem) são tratadas manualmente na view, fora deste form."""
    class Meta:
        model = ConfiguracaoSite
        fields = [
            'titulo_destaques', 'icone_destaques', 'icone_destaques_largura', 'icone_destaques_altura',
            'titulo_recentes', 'icone_recentes', 'icone_recentes_largura', 'icone_recentes_altura',
            'titulo_areas', 'icone_areas', 'icone_areas_largura', 'icone_areas_altura',
        ]
        widgets = {
            'titulo_destaques': RichTextWidget(),
            'titulo_recentes': RichTextWidget(),
            'titulo_areas': RichTextWidget(),
            'icone_destaques': IconPicker(),
            'icone_recentes': IconPicker(),
            'icone_areas': IconPicker(),
            'icone_destaques_largura': forms.NumberInput(attrs={'class': 'as-input', 'min': 10, 'max': 300, 'placeholder': 'Padrão do site', 'style': 'margin-bottom:0;'}),
            'icone_destaques_altura': forms.NumberInput(attrs={'class': 'as-input', 'min': 10, 'max': 300, 'placeholder': '= largura', 'style': 'margin-bottom:0;'}),
            'icone_recentes_largura': forms.NumberInput(attrs={'class': 'as-input', 'min': 10, 'max': 300, 'placeholder': 'Padrão do site', 'style': 'margin-bottom:0;'}),
            'icone_recentes_altura': forms.NumberInput(attrs={'class': 'as-input', 'min': 10, 'max': 300, 'placeholder': '= largura', 'style': 'margin-bottom:0;'}),
            'icone_areas_largura': forms.NumberInput(attrs={'class': 'as-input', 'min': 10, 'max': 300, 'placeholder': 'Padrão do site', 'style': 'margin-bottom:0;'}),
            'icone_areas_altura': forms.NumberInput(attrs={'class': 'as-input', 'min': 10, 'max': 300, 'placeholder': '= largura', 'style': 'margin-bottom:0;'}),
        }
