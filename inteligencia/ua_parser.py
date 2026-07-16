import re


def detectar_dispositivo(ua):
    if not ua:
        return 'desktop'
    ua_lower = ua.lower()
    if any(k in ua_lower for k in ('ipad', 'tablet', 'kindle', 'silk')):
        return 'tablet'
    if re.search(r'android(?!.*mobile)', ua_lower):
        return 'tablet'
    if any(k in ua_lower for k in ('mobile', 'iphone', 'ipod', 'android', 'windows phone', 'opera mini', 'opera mobi')):
        return 'mobile'
    return 'desktop'


def detectar_navegador(ua):
    if not ua:
        return 'Outro'
    if 'Edg/' in ua or 'Edge/' in ua:
        return 'Edge'
    if 'OPR/' in ua or 'Opera/' in ua:
        return 'Opera'
    if 'Chrome/' in ua and 'Safari/' in ua:
        return 'Chrome'
    if 'Firefox/' in ua:
        return 'Firefox'
    if 'Safari/' in ua and 'Chrome/' not in ua:
        return 'Safari'
    return 'Outro'


def classificar_referrer(referrer):
    if not referrer:
        return 'Direto'
    r = referrer.lower()
    if 'google.' in r:
        return 'Google'
    if 'bing.' in r:
        return 'Bing'
    if 'sedu.es.gov.br' in r:
        return 'Site SEDU'
    if any(k in r for k in ('facebook.', 'instagram.', 'twitter.', 'x.com', 'linkedin.', 'youtube.', 't.co/')):
        return 'Redes sociais'
    return 'Outro'
