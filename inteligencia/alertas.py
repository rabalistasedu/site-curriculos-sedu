import os
import urllib.request
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import AlertaInteligencia


def verificar_documentos_sem_acesso(dias=90):
    from .models import PageView
    from conteudo.models import Conteudo

    limite = timezone.now() - timedelta(days=dias)
    slugs_recentes = set(
        PageView.objects.filter(
            tipo_pagina='conteudo',
            timestamp__gte=limite,
        ).values_list('objeto_slug', flat=True)
    )

    sem_acesso = Conteudo.objects.filter(
        status='publicado',
    ).exclude(slug__in=slugs_recentes).exclude(slug='')

    criados = 0
    for conteudo in sem_acesso[:100]:
        _, created = AlertaInteligencia.objects.get_or_create(
            tipo='sem_acesso',
            objeto_tipo='conteudo',
            objeto_id=conteudo.pk,
            resolvido=False,
            defaults={
                'titulo': f'Sem acesso em {dias} dias: {conteudo.titulo[:200]}',
                'descricao': f'O conteudo "{conteudo.titulo}" (tipo: {conteudo.tipo}) nao foi acessado nos ultimos {dias} dias.',
            }
        )
        if created:
            criados += 1
    return criados


def verificar_links_quebrados(timeout=10):
    from conteudo.models import Conteudo

    links = Conteudo.objects.filter(
        status='publicado',
        tipo='link',
    ).exclude(url_externa='').values('pk', 'titulo', 'url_externa')

    criados = 0
    for item in links[:50]:
        url = item['url_externa']
        try:
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0 (Central de Inteligencia)')
            resp = urllib.request.urlopen(req, timeout=timeout)
            if resp.status >= 400:
                raise urllib.error.HTTPError(url, resp.status, '', {}, None)
        except Exception as e:
            erro = str(e)[:200]
            _, created = AlertaInteligencia.objects.get_or_create(
                tipo='link_quebrado',
                objeto_tipo='conteudo',
                objeto_id=item['pk'],
                resolvido=False,
                defaults={
                    'titulo': f'Link quebrado: {item["titulo"][:200]}',
                    'descricao': f'URL: {url}\nErro: {erro}',
                }
            )
            if created:
                criados += 1
    return criados


def verificar_arquivos_ausentes():
    from conteudo.models import Conteudo, Anexo

    criados = 0

    for anexo in Anexo.objects.exclude(arquivo=''):
        caminho = os.path.join(settings.MEDIA_ROOT, str(anexo.arquivo))
        if not os.path.exists(caminho):
            _, created = AlertaInteligencia.objects.get_or_create(
                tipo='arquivo_ausente',
                objeto_tipo='anexo',
                objeto_id=anexo.pk,
                resolvido=False,
                defaults={
                    'titulo': f'Arquivo ausente: {anexo.nome_exibicao}',
                    'descricao': f'O arquivo {anexo.arquivo} nao foi encontrado no disco.',
                }
            )
            if created:
                criados += 1

    for conteudo in Conteudo.objects.exclude(arquivo=''):
        caminho = os.path.join(settings.MEDIA_ROOT, str(conteudo.arquivo))
        if not os.path.exists(caminho):
            _, created = AlertaInteligencia.objects.get_or_create(
                tipo='arquivo_ausente',
                objeto_tipo='conteudo',
                objeto_id=conteudo.pk,
                resolvido=False,
                defaults={
                    'titulo': f'Arquivo ausente: {conteudo.titulo[:200]}',
                    'descricao': f'O arquivo {conteudo.arquivo} nao foi encontrado no disco.',
                }
            )
            if created:
                criados += 1

    return criados


def verificar_picos_acesso():
    from .models import PageView

    agora = timezone.now()
    hoje_inicio = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    acessos_hoje = PageView.objects.filter(timestamp__gte=hoje_inicio).count()

    dias_anteriores = []
    for i in range(1, 8):
        dia_inicio = hoje_inicio - timedelta(days=i)
        dia_fim = dia_inicio + timedelta(days=1)
        dias_anteriores.append(
            PageView.objects.filter(timestamp__range=(dia_inicio, dia_fim)).count()
        )

    media = sum(dias_anteriores) / len(dias_anteriores) if dias_anteriores else 0

    if media > 0 and acessos_hoje > media * 3:
        _, created = AlertaInteligencia.objects.get_or_create(
            tipo='pico_acesso',
            resolvido=False,
            criado_em__date=agora.date(),
            defaults={
                'titulo': f'Pico de acesso detectado: {acessos_hoje} acessos hoje (media: {int(media)})',
                'descricao': f'Os acessos de hoje ({acessos_hoje}) sao {acessos_hoje/media:.1f}x maiores que a media dos ultimos 7 dias ({int(media)}).',
            }
        )
        return 1 if created else 0
    return 0
