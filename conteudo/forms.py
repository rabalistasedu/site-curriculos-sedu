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
            'slug': forms.TextInput(attrs={'autocomplete': 'off'}),
        }


class ConfiguracaoSiteAdminForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSite
        fields = '__all__'
        widgets = {
            'home_texto': RichTextWidget(),
        }
