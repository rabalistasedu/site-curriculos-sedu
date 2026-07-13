# -*- coding: utf-8 -*-
"""
View para servir arquivos de media (video, audio) com suporte a Range Requests.
Necessário para streaming de video funcionar via ngrok e outros proxies.
"""
import os
import re
import mimetypes
from wsgiref.util import FileWrapper
from django.http import (
    HttpResponse, HttpResponseNotFound,
    HttpResponseNotModified, StreamingHttpResponse,
)
from django.utils.http import http_date
from django.conf import settings


RANGE_RE = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.IGNORECASE)


def _file_iterator(path, offset, length, chunk_size=8192):
    with open(path, 'rb') as f:
        f.seek(offset)
        remaining = length
        while remaining > 0:
            data = f.read(min(chunk_size, remaining))
            if not data:
                break
            remaining -= len(data)
            yield data


def serve_media(request, path):
    """Serve arquivos de media com suporte a Range Requests."""
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    full_path = os.path.normpath(full_path)

    if not full_path.startswith(os.path.normpath(settings.MEDIA_ROOT)):
        return HttpResponseNotFound()

    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return HttpResponseNotFound()

    file_size = os.path.getsize(full_path)
    content_type, _ = mimetypes.guess_type(full_path)
    if content_type is None:
        content_type = 'application/octet-stream'

    range_header = request.META.get('HTTP_RANGE', '').strip()
    if range_header:
        match = RANGE_RE.match(range_header)
        if match:
            start = int(match.group(1))
            end_str = match.group(2)
            end = int(end_str) if end_str else file_size - 1
            end = min(end, file_size - 1)
            length = end - start + 1

            response = StreamingHttpResponse(
                _file_iterator(full_path, start, length),
                status=206,
                content_type=content_type,
            )
            response['Content-Length'] = str(length)
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response['Accept-Ranges'] = 'bytes'
            response['Last-Modified'] = http_date(os.path.getmtime(full_path))
            response['ngrok-skip-browser-warning'] = 'true'
            return response

    response = StreamingHttpResponse(
        _file_iterator(full_path, 0, file_size),
        content_type=content_type,
    )
    response['Content-Length'] = str(file_size)
    response['Accept-Ranges'] = 'bytes'
    response['Last-Modified'] = http_date(os.path.getmtime(full_path))
    response['ngrok-skip-browser-warning'] = 'true'
    return response
