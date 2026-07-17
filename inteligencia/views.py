import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.safestring import mark_safe
from conteudo.permissoes import exige_permissao_painel
from . import services


def _parse_periodo(request):
    periodo = request.GET.get('periodo', '30dias')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    return services.calcular_periodo(periodo, data_inicio, data_fim)


@staff_member_required
@exige_permissao_painel('inteligencia.pode_acessar_inteligencia')
def dashboard_view(request):
    inicio, fim = _parse_periodo(request)
    periodo = request.GET.get('periodo', '30dias')

    indicadores = services.indicadores_resumo(inicio, fim)
    ranking_bot = services.ranking_botoes(inicio, fim)
    ranking_sub = services.ranking_subbotoes(inicio, fim)
    ranking_docs = services.ranking_documentos(inicio, fim)
    ranking_dl = services.ranking_downloads(inicio, fim)
    ranking_busca = services.ranking_buscas(inicio, fim)
    stats_coment = services.stats_comentarios(inicio, fim)
    rank_disp = services.ranking_dispositivos(inicio, fim)
    rank_nav = services.ranking_navegadores(inicio, fim)
    rank_ref = services.ranking_referrer(inicio, fim)
    rank_area = services.ranking_por_area_curricular(inicio, fim)
    rank_banners = services.ranking_banners(inicio, fim)
    rank_destaques = services.ranking_destaques(inicio, fim)
    docs_nunca = services.documentos_sem_acesso(dias=None)
    docs_30 = services.documentos_sem_acesso(dias=30)
    docs_90 = services.documentos_sem_acesso(dias=90)

    from .models import AlertaInteligencia
    alertas_ativos = AlertaInteligencia.objects.filter(resolvido=False).order_by('-criado_em')
    alertas_count = alertas_ativos.count()

    filtros_periodo = [
        ('hoje', 'Hoje'),
        ('ontem', 'Ontem'),
        ('7dias', '7 dias'),
        ('30dias', '30 dias'),
        ('90dias', '90 dias'),
        ('este_mes', 'Este mês'),
        ('este_ano', 'Este ano'),
        ('total', 'Total'),
    ]

    context = {
        'title': 'Central de Inteligência do Portal',
        'has_permission': True,
        'periodo_atual': periodo,
        'data_inicio': request.GET.get('data_inicio', ''),
        'data_fim': request.GET.get('data_fim', ''),
        'ind': indicadores,
        'ranking_botoes': ranking_bot,
        'ranking_subbotoes': ranking_sub,
        'ranking_documentos': ranking_docs,
        'ranking_downloads': ranking_dl,
        'ranking_buscas': ranking_busca,
        'stats_comentarios': stats_coment,
        'ranking_dispositivos': rank_disp,
        'ranking_dispositivos_json': mark_safe(json.dumps(rank_disp)),
        'ranking_navegadores': rank_nav,
        'ranking_navegadores_json': mark_safe(json.dumps(rank_nav)),
        'ranking_referrer': rank_ref,
        'ranking_areas': rank_area,
        'ranking_banners': rank_banners,
        'ranking_destaques': rank_destaques,
        'docs_nunca': docs_nunca,
        'docs_30': docs_30,
        'docs_90': docs_90,
        'alertas': alertas_ativos[:50],
        'alertas_count': alertas_count,
        'filtros_periodo': filtros_periodo,
    }
    return render(request, 'admin/inteligencia_dashboard.html', context)


@staff_member_required
@exige_permissao_painel('inteligencia.pode_acessar_inteligencia')
def dashboard_api(request):
    action = request.GET.get('action', '')
    inicio, fim = _parse_periodo(request)
    agrupamento = request.GET.get('agrupamento', 'dia')

    if action == 'grafico_acessos':
        return JsonResponse(services.serie_temporal_pageviews(inicio, fim, agrupamento))
    elif action == 'grafico_downloads':
        return JsonResponse(services.serie_temporal_downloads(inicio, fim, agrupamento))
    elif action == 'grafico_buscas':
        return JsonResponse(services.serie_temporal_buscas(inicio, fim, agrupamento))
    elif action == 'grafico_comentarios':
        return JsonResponse(services.serie_temporal_comentarios(inicio, fim, agrupamento))
    elif action == 'grafico_crescimento':
        return JsonResponse(services.crescimento_portal(inicio, fim, agrupamento))

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'resolver_alerta':
            from .models import AlertaInteligencia
            alerta_id = request.POST.get('alerta_id')
            try:
                alerta = AlertaInteligencia.objects.get(pk=alerta_id)
                alerta.resolvido = True
                alerta.save()
                return JsonResponse({'ok': True})
            except AlertaInteligencia.DoesNotExist:
                return JsonResponse({'error': 'Alerta não encontrado'}, status=404)
        elif action == 'resolver_todos':
            from .models import AlertaInteligencia
            count = AlertaInteligencia.objects.filter(resolvido=False).update(resolvido=True)
            return JsonResponse({'ok': True, 'resolvidos': count})

    return JsonResponse({'error': f'Ação desconhecida: {action}'}, status=400)


@staff_member_required
@exige_permissao_painel('inteligencia.pode_acessar_inteligencia')
def exportar_excel_view(request):
    from .exportar import gerar_excel
    inicio, fim = _parse_periodo(request)
    return gerar_excel(inicio, fim)


@staff_member_required
@exige_permissao_painel('inteligencia.pode_acessar_inteligencia')
def exportar_pdf_view(request):
    from .exportar import gerar_pdf
    inicio, fim = _parse_periodo(request)
    return gerar_pdf(inicio, fim)
