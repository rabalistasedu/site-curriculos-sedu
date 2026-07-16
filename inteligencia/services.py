from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q, Max
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth


def calcular_periodo(periodo, data_inicio=None, data_fim=None):
    agora = timezone.now()
    hoje = agora.replace(hour=0, minute=0, second=0, microsecond=0)

    if data_inicio and data_fim:
        from datetime import datetime
        try:
            inicio = timezone.make_aware(datetime.strptime(data_inicio, '%Y-%m-%d'))
            fim = timezone.make_aware(datetime.strptime(data_fim, '%Y-%m-%d')) + timedelta(days=1)
            return inicio, fim
        except (ValueError, TypeError):
            pass

    presets = {
        'hoje': (hoje, agora),
        'ontem': (hoje - timedelta(days=1), hoje),
        '7dias': (hoje - timedelta(days=7), agora),
        '30dias': (hoje - timedelta(days=30), agora),
        '90dias': (hoje - timedelta(days=90), agora),
        'este_mes': (hoje.replace(day=1), agora),
        'este_ano': (hoje.replace(month=1, day=1), agora),
        'total': (timezone.make_aware(timezone.datetime(2020, 1, 1)), agora),
    }
    return presets.get(periodo, presets['30dias'])


def indicadores_resumo(inicio, fim):
    from .models import PageView, DownloadEvent, SearchQuery
    from conteudo.models import Conteudo, Comentario

    agora = timezone.now()
    hoje = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    semana = hoje - timedelta(days=7)
    mes = hoje - timedelta(days=30)
    ano = hoje.replace(month=1, day=1)

    pvs = PageView.objects.filter(timestamp__range=(inicio, fim))

    return {
        'usuarios_online': PageView.objects.filter(
            timestamp__gte=agora - timedelta(minutes=5)
        ).values('sessao_id').distinct().count(),
        'visitantes_hoje': PageView.objects.filter(
            timestamp__gte=hoje
        ).values('sessao_id').distinct().count(),
        'visitantes_semana': PageView.objects.filter(
            timestamp__gte=semana
        ).values('sessao_id').distinct().count(),
        'visitantes_mes': PageView.objects.filter(
            timestamp__gte=mes
        ).values('sessao_id').distinct().count(),
        'visitantes_ano': PageView.objects.filter(
            timestamp__gte=ano
        ).values('sessao_id').distinct().count(),
        'visitantes_total': PageView.objects.values('sessao_id').distinct().count(),
        'visitantes_unicos': pvs.values('sessao_id').distinct().count(),
        'paginas_visitadas': pvs.count(),
        'downloads_total': DownloadEvent.objects.filter(
            timestamp__range=(inicio, fim)
        ).count(),
        'buscas_total': SearchQuery.objects.filter(
            timestamp__range=(inicio, fim)
        ).count(),
        'comentarios_total': Comentario.objects.count(),
        'conteudos_total': Conteudo.objects.filter(status='publicado').count(),
    }


def ranking_botoes(inicio, fim, limite=10):
    from .models import PageView
    from conteudo.models import Categoria

    pvs = PageView.objects.filter(
        tipo_pagina='categoria',
        timestamp__range=(inicio, fim),
        objeto_slug__gt='',
    ).values('objeto_slug').annotate(
        total=Count('id'),
        ultimo=Max('timestamp'),
    ).order_by('-total')[:limite]

    slugs = [r['objeto_slug'] for r in pvs]
    cats = {c.slug: c for c in Categoria.objects.filter(slug__in=slugs, categoria_pai__isnull=True)}

    resultado = []
    for r in pvs:
        cat = cats.get(r['objeto_slug'])
        if cat:
            resultado.append({
                'nome': cat.nome,
                'slug': r['objeto_slug'],
                'total': r['total'],
                'ultimo': r['ultimo'].strftime('%d/%m/%Y %H:%M') if r['ultimo'] else '',
            })
    return resultado


def ranking_subbotoes(inicio, fim, limite=10):
    from .models import PageView
    from conteudo.models import Categoria

    pvs = PageView.objects.filter(
        tipo_pagina='categoria',
        timestamp__range=(inicio, fim),
        objeto_slug__gt='',
    ).values('objeto_slug').annotate(
        total=Count('id'),
        ultimo=Max('timestamp'),
    ).order_by('-total')[:limite * 3]

    slugs = [r['objeto_slug'] for r in pvs]
    cats = {c.slug: c for c in Categoria.objects.filter(
        slug__in=slugs, categoria_pai__isnull=False
    ).select_related('categoria_pai')}

    resultado = []
    for r in pvs:
        cat = cats.get(r['objeto_slug'])
        if cat:
            resultado.append({
                'nome': cat.nome,
                'pai': cat.categoria_pai.nome if cat.categoria_pai else '',
                'slug': r['objeto_slug'],
                'total': r['total'],
                'ultimo': r['ultimo'].strftime('%d/%m/%Y %H:%M') if r['ultimo'] else '',
            })
            if len(resultado) >= limite:
                break
    return resultado


def ranking_documentos(inicio, fim, limite=10):
    from .models import PageView
    from conteudo.models import Conteudo

    pvs = PageView.objects.filter(
        tipo_pagina='conteudo',
        timestamp__range=(inicio, fim),
        objeto_slug__gt='',
    ).values('objeto_slug').annotate(
        total=Count('id'),
        ultimo=Max('timestamp'),
    ).order_by('-total')[:limite]

    slugs = [r['objeto_slug'] for r in pvs]
    conts = {c.slug: c for c in Conteudo.objects.filter(slug__in=slugs)}

    resultado = []
    for r in pvs:
        cont = conts.get(r['objeto_slug'])
        if cont:
            resultado.append({
                'nome': cont.titulo,
                'slug': r['objeto_slug'],
                'tipo': cont.get_tipo_display() if hasattr(cont, 'get_tipo_display') else cont.tipo,
                'total': r['total'],
                'ultimo': r['ultimo'].strftime('%d/%m/%Y %H:%M') if r['ultimo'] else '',
            })
    return resultado


def ranking_downloads(inicio, fim, limite=10):
    from .models import DownloadEvent

    return list(DownloadEvent.objects.filter(
        timestamp__range=(inicio, fim),
    ).values('nome_arquivo', 'extensao').annotate(
        total=Count('id'),
        ultimo=Max('timestamp'),
    ).order_by('-total')[:limite].values(
        'nome_arquivo', 'extensao', 'total', 'ultimo'
    ))


def ranking_buscas(inicio, fim, limite=20):
    from .models import SearchQuery

    qs = SearchQuery.objects.filter(
        timestamp__range=(inicio, fim),
    ).values('termo_normalizado').annotate(
        total=Count('id'),
        ultimo=Max('timestamp'),
    ).order_by('-total')[:limite]

    result = []
    for item in qs:
        original = SearchQuery.objects.filter(
            termo_normalizado=item['termo_normalizado']
        ).order_by('-timestamp').values_list('termo', flat=True).first()
        result.append({
            'termo': original or item['termo_normalizado'],
            'total': item['total'],
            'ultimo': item['ultimo'].strftime('%d/%m/%Y %H:%M') if item['ultimo'] else '',
        })
    return result


def stats_comentarios(inicio, fim):
    from conteudo.models import Comentario

    qs = Comentario.objects.all()
    return {
        'publicados': qs.filter(status='publicado').count(),
        'pendentes': qs.filter(status='pendente').count(),
        'recusados': qs.filter(status='recusado').count(),
        'respondidos': qs.exclude(resposta='').count(),
        'total': qs.count(),
    }


def ranking_dispositivos(inicio, fim):
    from .models import PageView

    total = PageView.objects.filter(timestamp__range=(inicio, fim)).count()
    if total == 0:
        return []
    qs = PageView.objects.filter(
        timestamp__range=(inicio, fim),
    ).values('dispositivo').annotate(
        total=Count('id'),
    ).order_by('-total')

    return [
        {
            'nome': item['dispositivo'].capitalize(),
            'total': item['total'],
            'percentual': round(item['total'] / total * 100, 1),
        }
        for item in qs
    ]


def ranking_navegadores(inicio, fim):
    from .models import PageView

    total = PageView.objects.filter(timestamp__range=(inicio, fim)).count()
    if total == 0:
        return []
    qs = PageView.objects.filter(
        timestamp__range=(inicio, fim),
    ).values('navegador').annotate(
        total=Count('id'),
    ).order_by('-total')

    return [
        {
            'nome': item['navegador'] or 'Outro',
            'total': item['total'],
            'percentual': round(item['total'] / total * 100, 1),
        }
        for item in qs
    ]


def ranking_referrer(inicio, fim):
    from .models import PageView
    from .ua_parser import classificar_referrer

    pvs = PageView.objects.filter(
        timestamp__range=(inicio, fim),
    ).values_list('referrer', flat=True)

    contagem = {}
    for ref in pvs:
        origem = classificar_referrer(ref)
        contagem[origem] = contagem.get(origem, 0) + 1

    total = sum(contagem.values()) or 1
    resultado = sorted(contagem.items(), key=lambda x: -x[1])
    return [
        {'nome': nome, 'total': t, 'percentual': round(t / total * 100, 1)}
        for nome, t in resultado
    ]


def documentos_sem_acesso(dias=None):
    from .models import PageView
    from conteudo.models import Conteudo

    publicados = Conteudo.objects.filter(status='publicado')
    slugs_acessados = set(
        PageView.objects.filter(tipo_pagina='conteudo').values_list('objeto_slug', flat=True)
    )

    if dias is not None:
        limite = timezone.now() - timedelta(days=dias)
        slugs_recentes = set(
            PageView.objects.filter(
                tipo_pagina='conteudo',
                timestamp__gte=limite,
            ).values_list('objeto_slug', flat=True)
        )
        return list(publicados.exclude(slug__in=slugs_recentes).values(
            'titulo', 'slug', 'tipo', 'data_publicacao'
        )[:50])
    else:
        return list(publicados.exclude(slug__in=slugs_acessados).values(
            'titulo', 'slug', 'tipo', 'data_publicacao'
        )[:50])


def serie_temporal_pageviews(inicio, fim, agrupamento='dia'):
    from .models import PageView
    return _serie_temporal(PageView, 'timestamp', inicio, fim, agrupamento)


def serie_temporal_downloads(inicio, fim, agrupamento='dia'):
    from .models import DownloadEvent
    return _serie_temporal(DownloadEvent, 'timestamp', inicio, fim, agrupamento)


def serie_temporal_buscas(inicio, fim, agrupamento='dia'):
    from .models import SearchQuery
    return _serie_temporal(SearchQuery, 'timestamp', inicio, fim, agrupamento)


def serie_temporal_comentarios(inicio, fim, agrupamento='dia'):
    from conteudo.models import Comentario
    return _serie_temporal(Comentario, 'data_criacao', inicio, fim, agrupamento)


def crescimento_portal(inicio, fim, agrupamento='dia'):
    from conteudo.models import Conteudo
    return _serie_temporal(Conteudo, 'data_criacao', inicio, fim, agrupamento, cumulativo=True)


def _serie_temporal(modelo, campo_data, inicio, fim, agrupamento='dia', cumulativo=False):
    trunc_map = {'dia': TruncDay, 'semana': TruncWeek, 'mes': TruncMonth}
    trunc_fn = trunc_map.get(agrupamento, TruncDay)

    qs = modelo.objects.filter(
        **{f'{campo_data}__range': (inicio, fim)}
    ).annotate(
        periodo=trunc_fn(campo_data)
    ).values('periodo').annotate(
        total=Count('id')
    ).order_by('periodo')

    labels = []
    dados = []
    acum = 0

    fmt = {'dia': '%d/%m', 'semana': '%d/%m', 'mes': '%m/%Y'}.get(agrupamento, '%d/%m')

    for item in qs:
        if item['periodo']:
            labels.append(item['periodo'].strftime(fmt))
            if cumulativo:
                acum += item['total']
                dados.append(acum)
            else:
                dados.append(item['total'])

    return {'labels': labels, 'dados': dados}


def ranking_banners(inicio, fim, limite=10):
    from .models import PageView
    from conteudo.models import Banner

    pvs_home = PageView.objects.filter(
        tipo_pagina='home',
        timestamp__range=(inicio, fim),
    ).count()

    banners = Banner.objects.filter(ativo=True).order_by('ordem')
    resultado = []
    for b in banners:
        resultado.append({
            'titulo': b.titulo or f'Banner #{b.pk}',
            'link': b.link or '',
            'impressoes': pvs_home,
            'ultimo_acesso': '',
        })
    return resultado


def ranking_destaques(inicio, fim, limite=10):
    from .models import PageView
    from conteudo.models import Conteudo

    destaques = Conteudo.objects.filter(destaque=True, status='publicado')

    pvs = PageView.objects.filter(
        tipo_pagina='conteudo',
        timestamp__range=(inicio, fim),
        objeto_slug__gt='',
    ).values('objeto_slug').annotate(
        total=Count('id'),
        ultimo=Max('timestamp'),
    )
    pvs_map = {r['objeto_slug']: r for r in pvs}

    pvs_home = PageView.objects.filter(
        tipo_pagina='home',
        timestamp__range=(inicio, fim),
    ).count()

    resultado = []
    for d in destaques[:limite]:
        stats = pvs_map.get(d.slug, {})
        cliques = stats.get('total', 0)
        ultimo = stats.get('ultimo')
        ctr = round(cliques / pvs_home * 100, 1) if pvs_home > 0 else 0
        resultado.append({
            'titulo': d.titulo or f'#{d.pk}',
            'slug': d.slug,
            'tipo': d.get_tipo_display(),
            'impressoes': pvs_home,
            'cliques': cliques,
            'ctr': ctr,
            'ultimo': ultimo.strftime('%d/%m/%Y %H:%M') if ultimo else '',
        })
    resultado.sort(key=lambda x: -x['cliques'])
    return resultado


def ranking_por_area_curricular(inicio, fim, limite=20):
    from .models import PageView
    from conteudo.models import Categoria

    pvs = PageView.objects.filter(
        tipo_pagina='categoria',
        timestamp__range=(inicio, fim),
        objeto_slug__gt='',
    ).values('objeto_slug').annotate(total=Count('id')).order_by('-total')

    slugs = [r['objeto_slug'] for r in pvs]
    cats = {c.slug: c for c in Categoria.objects.filter(slug__in=slugs).select_related('categoria_pai')}

    areas = {}
    for r in pvs:
        cat = cats.get(r['objeto_slug'])
        if not cat:
            continue
        raiz = cat
        while raiz.categoria_pai:
            raiz = raiz.categoria_pai
        nome = raiz.nome
        areas[nome] = areas.get(nome, 0) + r['total']

    resultado = sorted(areas.items(), key=lambda x: -x[1])[:limite]
    total = sum(v for _, v in resultado) or 1
    return [
        {'nome': nome, 'total': t, 'percentual': round(t / total * 100, 1)}
        for nome, t in resultado
    ]
