"""
Busca tolerante para todo o site: ignora acentos, maiúsculas/minúsculas
e cedilha. "matematica", "MATEMÁTICA" e "Matemática" encontram o mesmo
resultado. O SQLite não tem 'unaccent', então a comparação é feita em
Python — o volume de conteúdos (centenas) torna isso instantâneo.
"""
import unicodedata


def normalizar(texto):
    """Remove acentos e converte para minúsculas: 'Educação' → 'educacao'."""
    texto = unicodedata.normalize('NFKD', str(texto or ''))
    return texto.encode('ascii', 'ignore').decode('ascii').lower()


def filtrar_por_texto(itens, query, campos):
    """Filtra uma lista de objetos: mantém os que contêm a busca
    (normalizada) em qualquer um dos campos indicados."""
    alvo = normalizar(query)
    if not alvo:
        return list(itens)
    resultado = []
    for item in itens:
        texto = ' '.join(normalizar(getattr(item, campo, '') or '') for campo in campos)
        if alvo in texto:
            resultado.append(item)
    return resultado


class BuscaSemAcentoMixin:
    """Mixin para ModelAdmin: torna a caixa de pesquisa do admin
    insensível a acentos. Defina `busca_normalizada_campos` com os
    campos de texto do próprio modelo a considerar."""
    busca_normalizada_campos = ()

    def get_search_results(self, request, queryset, search_term):
        qs, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        term = (search_term or '').strip()
        if term and self.busca_normalizada_campos:
            alvo = normalizar(term)
            extras = [
                obj.pk for obj in queryset
                if alvo in ' '.join(
                    normalizar(getattr(obj, campo, '') or '')
                    for campo in self.busca_normalizada_campos
                )
            ]
            if extras:
                pks = set(qs.values_list('pk', flat=True)) | set(extras)
                qs = queryset.model.objects.filter(pk__in=pks)
        return qs, may_have_duplicates
