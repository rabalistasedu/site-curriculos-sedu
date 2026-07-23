from django import template

from conteudo.models import Comentario

register = template.Library()


@register.simple_tag
def comentarios_pendentes_count():
    return Comentario.objects.filter(status='pendente').count()
