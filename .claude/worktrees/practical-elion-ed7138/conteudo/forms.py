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
        }


class CategoriaAdminForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'icone': IconPicker(),
            'slug': forms.TextInput(attrs={'autocomplete': 'off'}),
        }


class ConfiguracaoSiteAdminForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSite
        fields = '__all__'
        widgets = {
            'home_texto': RichTextWidget(),
        }
