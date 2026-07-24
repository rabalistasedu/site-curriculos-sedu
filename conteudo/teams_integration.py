"""
Integração de Comentários com o Microsoft Teams (grupo GECEB).

Fluxo:
  1) enviar_comentario_para_teams() — chamado logo após um Comentario ser
     criado no site. Envia um POST simples (JSON) para o webhook do Power
     Automate (modelo "Publicar em um canal quando um webhook for
     recebido"). Best-effort: nunca lança exceção para quem chamou.
  2) vincular_mensagens_pendentes() + verificar_respostas() — chamados
     periodicamente pelo management command `sincronizar_teams`. Usam a
     Microsoft Graph API (aplicação, client-credentials) para descobrir o
     ID da mensagem criada no Teams e depois checar se já chegou resposta.

Tudo aqui é opcional: sem as variáveis de ambiente TEAMS_* configuradas,
todas as funções são no-ops seguros (não erram, só avisam via logging).
Nenhuma função altera o fluxo de moderação existente (status/aprovado) —
só os campos novos teams_* e, quando uma resposta chega, os MESMOS campos
`resposta`/`data_resposta` que o admin já usa manualmente.
"""
import logging

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger('conteudo.teams_integration')

GRAPH_BASE = 'https://graph.microsoft.com/v1.0'


def _requests():
    """Import tardio — evita erro de import se 'requests' não estiver instalado
    em algum ambiente que ainda não rodou pip install (a integração vira no-op)."""
    try:
        import requests
        return requests
    except ImportError:
        logger.warning('Biblioteca "requests" não instalada — integração com Teams desativada.')
        return None


def _titulo_e_link(comentario):
    """Devolve (título da página, caminho relativo) de onde veio o comentário."""
    origem = comentario.origem
    if origem is None:
        return ('(origem removida)', '')
    if comentario.conteudo_id:
        titulo = comentario.conteudo.titulo
        caminho = reverse('conteudo:conteudo_detalhe', args=[comentario.conteudo.slug])
    elif comentario.categoria_id:
        titulo = comentario.categoria.nome
        caminho = reverse('conteudo:categoria', args=[comentario.categoria.slug])
    else:
        titulo = comentario.pagina_livre.titulo
        caminho = reverse('conteudo:pagina_livre', args=[comentario.pagina_livre.slug])
    return (titulo, caminho)


# ── 1) Envio site → Teams ──────────────────────────────────────────────

def enviar_comentario_para_teams(comentario, request=None):
    """Envia o comentário recém-criado para o canal GECEB no Teams.

    Best-effort: qualquer falha (webhook não configurado, rede fora do ar,
    etc.) é registrada em teams_status='erro' e no log, mas NUNCA impede o
    comentário de já ter sido salvo normalmente no site.
    """
    webhook_url = getattr(settings, 'TEAMS_WEBHOOK_URL', '')
    if not webhook_url:
        return  # integração não configurada ainda — silencioso, comportamento de hoje

    requests = _requests()
    if requests is None:
        return

    titulo, caminho = _titulo_e_link(comentario)
    link_absoluto = request.build_absolute_uri(caminho) if request and caminho else ''

    payload = {
        'comentario_id': comentario.pk,
        'titulo': titulo,
        'nome': comentario.nome,
        'email': comentario.email or '(não informado)',
        'data': timezone.localtime(comentario.data_criacao).strftime('%d/%m/%Y %H:%M'),
        'texto': comentario.texto,
        'url': link_absoluto,
    }

    try:
        resposta = requests.post(webhook_url, json=payload, timeout=10)
        resposta.raise_for_status()
        comentario.teams_status = comentario.TEAMS_ENVIADO
        comentario.teams_data_envio = timezone.now()
        comentario.save(update_fields=['teams_status', 'teams_data_envio'])
    except Exception:
        logger.exception('Falha ao enviar comentário #%s para o Teams', comentario.pk)
        comentario.teams_status = comentario.TEAMS_ERRO
        comentario.save(update_fields=['teams_status'])


# ── 2) Autenticação Microsoft Graph (client credentials) ──────────────

def obter_token_graph():
    """Obtém um access token de aplicação (client credentials) para a Graph API.

    Devolve None se as credenciais (TEAMS_CLIENT_ID/SECRET/TENANT_ID) ainda
    não foram configuradas — permite o sistema rodar hoje sem elas.
    """
    tenant_id = getattr(settings, 'TEAMS_TENANT_ID', '')
    client_id = getattr(settings, 'TEAMS_CLIENT_ID', '')
    client_secret = getattr(settings, 'TEAMS_CLIENT_SECRET', '')
    if not (tenant_id and client_id and client_secret):
        return None

    requests = _requests()
    if requests is None:
        return None

    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    dados = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
    }
    try:
        resp = requests.post(url, data=dados, timeout=10)
        resp.raise_for_status()
        return resp.json().get('access_token')
    except Exception:
        logger.exception('Falha ao obter token da Microsoft Graph')
        return None


def _graph_get(token, caminho, params=None):
    requests = _requests()
    resp = requests.get(
        f'{GRAPH_BASE}{caminho}',
        headers={'Authorization': f'Bearer {token}'},
        params=params or {},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


# ── 3) Vincular mensagens já postadas no canal ao comentário certo ────

def vincular_mensagens_pendentes():
    """Para comentários com teams_status='enviado' (já mandados ao Power
    Automate, mas ainda sem o ID da mensagem do Teams), procura nas
    mensagens recentes do canal o marcador 'ID do comentário: N' e grava
    teams_message_id. Devolve quantos foram vinculados."""
    from conteudo.models import Comentario

    token = obter_token_graph()
    team_id = getattr(settings, 'TEAMS_TEAM_ID', '')
    channel_id = getattr(settings, 'TEAMS_CHANNEL_ID', '')
    if not (token and team_id and channel_id):
        return 0

    pendentes = list(
        Comentario.objects.filter(teams_status=Comentario.TEAMS_ENVIADO, teams_message_id='')
    )
    if not pendentes:
        return 0

    marcadores = {f'ID do comentário: {c.pk}': c for c in pendentes}

    try:
        dados = _graph_get(token, f'/teams/{team_id}/channels/{channel_id}/messages', params={'$top': 50})
    except Exception:
        logger.exception('Falha ao listar mensagens do canal do Teams')
        return 0

    vinculados = 0
    for msg in dados.get('value', []):
        corpo = (msg.get('body') or {}).get('content', '') or ''
        for marcador, comentario in list(marcadores.items()):
            if marcador in corpo:
                comentario.teams_message_id = msg['id']
                comentario.teams_status = Comentario.TEAMS_VINCULADO
                comentario.save(update_fields=['teams_message_id', 'teams_status'])
                del marcadores[marcador]
                vinculados += 1
    return vinculados


# ── 4) Verificar respostas da equipe no Teams ──────────────────────────

def verificar_respostas():
    """Para comentários já vinculados (teams_message_id preenchido) e ainda
    sem resposta, consulta as replies daquela mensagem via Graph. Se houver
    uma resposta nova de um remetente autorizado, grava em
    Comentario.resposta/data_resposta (os MESMOS campos usados pelo admin
    manualmente) e marca teams_status='respondido'. Devolve quantos comentários
    receberam resposta nesta rodada."""
    from conteudo.models import Comentario

    token = obter_token_graph()
    team_id = getattr(settings, 'TEAMS_TEAM_ID', '')
    channel_id = getattr(settings, 'TEAMS_CHANNEL_ID', '')
    if not (token and team_id and channel_id):
        return 0

    membros_autorizados = _lista_membros_autorizados()

    vinculados = Comentario.objects.filter(
        teams_status=Comentario.TEAMS_VINCULADO,
    ).exclude(teams_message_id='')

    respondidos = 0
    for comentario in vinculados:
        comentario.teams_ultima_verificacao = timezone.now()
        try:
            dados = _graph_get(
                token,
                f'/teams/{team_id}/channels/{channel_id}/messages/{comentario.teams_message_id}/replies',
                params={'$top': 50},
            )
        except Exception:
            logger.exception('Falha ao consultar respostas do comentário #%s no Teams', comentario.pk)
            comentario.save(update_fields=['teams_ultima_verificacao'])
            continue

        replies = dados.get('value', [])
        # Graph devolve mais recente primeiro — pega a mais antiga válida (1ª resposta da equipe)
        for reply in sorted(replies, key=lambda r: r.get('createdDateTime', '')):
            remetente_id = ((reply.get('from') or {}).get('user') or {}).get('id')

            if membros_autorizados:
                email_remetente = _resolver_email_usuario(token, remetente_id) if remetente_id else ''
                if email_remetente not in membros_autorizados:
                    continue  # remetente não está na lista de e-mails autorizados do GECEB
            # Sem lista configurada: confia na própria restrição do canal do Teams
            # (só membros do GECEB conseguem postar/responder ali).

            texto_resposta = ((reply.get('body') or {}).get('content', '') or '').strip()
            if not texto_resposta:
                continue

            comentario.resposta = texto_resposta
            comentario.data_resposta = timezone.now()
            comentario.teams_status = Comentario.TEAMS_RESPONDIDO
            comentario.save(update_fields=['resposta', 'data_resposta', 'teams_status', 'teams_ultima_verificacao'])
            respondidos += 1
            break
        else:
            comentario.save(update_fields=['teams_ultima_verificacao'])

    return respondidos


def _lista_membros_autorizados():
    bruto = getattr(settings, 'TEAMS_MEMBROS_AUTORIZADOS', '')
    return {e.strip().lower() for e in bruto.split(',') if e.strip()}


def _resolver_email_usuario(token, user_id):
    """Consulta a Graph para descobrir o e-mail (mail ou userPrincipalName)
    de quem enviou a resposta, a partir do ID de usuário do Azure AD."""
    try:
        dados = _graph_get(token, f'/users/{user_id}', params={'$select': 'mail,userPrincipalName'})
        return (dados.get('mail') or dados.get('userPrincipalName') or '').lower()
    except Exception:
        logger.exception('Falha ao resolver e-mail do usuário %s no Teams', user_id)
        return ''
