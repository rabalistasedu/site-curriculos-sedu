"""
Django settings for curriculo_sedu project.
Site: Currículo do Espírito Santo — SEDU/ES
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de um arquivo .env na raiz do projeto (ao lado do manage.py),
# se ele existir. Não sobrescreve variáveis de ambiente já definidas pelo sistema
# (ex.: as do docker-compose.yml) — apenas preenche o que ainda não foi setado.
# Sem .env nenhum: comportamento 100% igual a antes (os.environ.get com os
# valores padrão de sempre).
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-!8dxyco9l*l9o!6ojg4o(j-q158bg!v9@*5i=l8$wj)(-8@p_%'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']  # Permite todos os hosts em desenvolvimento (restringir antes da produção na SEDU)

# Permite acessar o painel administrativo pelo ngrok
CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
    "https://*.ngrok-free.dev",
    "https://*.ngrok.app",
]

# ── Domínios conhecidos do projeto (oficial + homologação) ─────────────
# Hardcoded uma única vez aqui — o código nunca precisa ser editado na troca
# de ambiente (local → homologação → oficial). Usado apenas para deixar o
# admin/CSRF funcionando de imediato em qualquer um deles; qualquer link
# gerado dinamicamente (ex.: para o card do Teams) usa o host da própria
# requisição (request.build_absolute_uri), então também se ajusta sozinho.
DOMINIOS_CONHECIDOS = [
    'curriculo.sedu.es.gov.br',     # oficial
    'curriculohm.sedu.es.gov.br',   # homologação
    'curriculodev.sedu.es.gov.br',  # homologação
]
CSRF_TRUSTED_ORIGINS += [f'https://{dominio}' for dominio in DOMINIOS_CONHECIDOS]

# ── Apps ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'conteudo',
    'painel',
    'inteligencia',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'inteligencia.middleware.AnalyticsMiddleware',
]

ROOT_URLCONF = 'curriculo_sedu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'conteudo.context_processors.site_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'curriculo_sedu.wsgi.application'

# ── Banco de dados ────────────────────────────────────────────────────
# SQLite para desenvolvimento local (funciona igual no Mac e Windows).
# Dentro do Docker (docker-compose.yml define DOCKER_POSTGRES=1), usa
# PostgreSQL — sem a variável de ambiente, o comportamento é idêntico
# ao de sempre (SQLite), então rodar localmente continua igual.
if os.environ.get('DOCKER_POSTGRES') == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'curriculo_sedu'),
            'USER': os.environ.get('POSTGRES_USER', 'curriculo_sedu'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'curriculo_sedu'),
            'HOST': os.environ.get('POSTGRES_HOST', 'db'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Validação de senha ────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Idioma e fuso horário (Brasil) ────────────────────────────────────
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ── Arquivos estáticos (CSS, JS, imagens do tema) ────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ── Arquivos de mídia (uploads: PDFs, imagens, vídeos) ────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Upload ────────────────────────────────────────────────────────────
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Integração de Comentários com o Microsoft Teams (grupo GECEB) ──────
# Todas vazias por padrão — a integração fica desligada (no-op) até serem
# configuradas via variável de ambiente. Nada do site quebra sem elas.
#
# TEAMS_WEBHOOK_URL       → URL do fluxo Power Automate (modelo "Publicar em
#                           um canal quando um webhook for recebido"), usada
#                           para enviar cada novo comentário ao Teams.
# TEAMS_CLIENT_ID/SECRET/
# TEAMS_TENANT_ID         → credenciais do App Registration no Azure AD
#                           (fornecidas pela TI da SEDU), usadas só para LER
#                           mensagens/respostas do canal via Microsoft Graph.
# TEAMS_TEAM_ID           → ID do Team (grupo) GECEB no Teams.
# TEAMS_CHANNEL_ID        → ID do canal dentro do Team onde os comentários
#                           são postados.
# TEAMS_MEMBROS_AUTORIZADOS → e-mails separados por vírgula; se vazio, aceita
#                           resposta de qualquer membro do canal (a própria
#                           restrição de acesso ao canal do Teams já limita
#                           quem pode responder).
TEAMS_WEBHOOK_URL = os.environ.get('TEAMS_WEBHOOK_URL', '')
TEAMS_CLIENT_ID = os.environ.get('TEAMS_CLIENT_ID', '')
TEAMS_CLIENT_SECRET = os.environ.get('TEAMS_CLIENT_SECRET', '')
TEAMS_TENANT_ID = os.environ.get('TEAMS_TENANT_ID', '')
TEAMS_TEAM_ID = os.environ.get('TEAMS_TEAM_ID', '')
TEAMS_CHANNEL_ID = os.environ.get('TEAMS_CHANNEL_ID', '')
TEAMS_MEMBROS_AUTORIZADOS = os.environ.get('TEAMS_MEMBROS_AUTORIZADOS', '')
