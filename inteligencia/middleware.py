import os
import unicodedata
from django.urls import resolve, Resolver404
from .models import PageView, DownloadEvent, SearchQuery
from .ua_parser import detectar_dispositivo, detectar_navegador

EXTENSOES_DOCUMENTO = {
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.rar', '.7z',
    '.mp4', '.avi', '.mov', '.webm', '.mkv', '.wmv',
    '.mp3', '.wav', '.ogg', '.flac',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg',
}

PREFIXOS_IGNORAR = ('/admin/', '/static/', '/__debug__/')


def _normalizar(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def _obter_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _obter_sessao_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key or ''


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method != 'GET':
            return response

        path = request.path

        if path.startswith('/media/'):
            self._rastrear_download(request, response, path)
            return response

        if any(path.startswith(p) for p in PREFIXOS_IGNORAR):
            return response

        if response.status_code != 200:
            return response

        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type:
            return response

        self._rastrear_pageview(request, path)

        return response

    def _rastrear_pageview(self, request, path):
        try:
            tipo_pagina = 'outra'
            objeto_id = None
            objeto_slug = ''

            try:
                match = resolve(path)
                view_name = match.url_name or ''
                if view_name == 'home' or path == '/':
                    tipo_pagina = 'home'
                elif view_name == 'categoria':
                    tipo_pagina = 'categoria'
                    objeto_slug = match.kwargs.get('slug', '')
                elif view_name == 'conteudo_detalhe':
                    tipo_pagina = 'conteudo'
                    objeto_slug = match.kwargs.get('slug', '')
                elif view_name == 'busca' or path == '/busca/':
                    tipo_pagina = 'busca'
            except Resolver404:
                pass

            ua = request.META.get('HTTP_USER_AGENT', '')
            referrer = request.META.get('HTTP_REFERER', '')
            if len(referrer) > 500:
                referrer = referrer[:500]

            PageView.objects.create(
                url=path[:500],
                tipo_pagina=tipo_pagina,
                objeto_id=objeto_id,
                objeto_slug=objeto_slug,
                sessao_id=_obter_sessao_id(request),
                ip=_obter_ip(request),
                user_agent=ua[:500],
                referrer=referrer,
                dispositivo=detectar_dispositivo(ua),
                navegador=detectar_navegador(ua),
            )

            if tipo_pagina == 'busca':
                termo = request.GET.get('q', '').strip()
                if termo:
                    SearchQuery.objects.create(
                        termo=termo[:300],
                        termo_normalizado=_normalizar(termo)[:300],
                        sessao_id=_obter_sessao_id(request),
                        ip=_obter_ip(request),
                    )
        except Exception:
            pass

    def _rastrear_download(self, request, response, path):
        try:
            if response.status_code not in (200, 206):
                return

            ext = os.path.splitext(path)[1].lower()
            if ext not in EXTENSOES_DOCUMENTO:
                return

            nome_arquivo = os.path.basename(path)

            DownloadEvent.objects.create(
                nome_arquivo=nome_arquivo[:300],
                extensao=ext[:10],
                url=path[:500],
                sessao_id=_obter_sessao_id(request),
                ip=_obter_ip(request),
            )
        except Exception:
            pass
