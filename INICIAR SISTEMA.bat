@echo off
chcp 65001 >nul
title SITE CURRICULOS SEDU - Servidor local
color 0B

REM ============================================================
REM  INICIAR SISTEMA - SITE CURRICULOS SEDU
REM  Versao para usar em QUALQUER computador (casa ou trabalho).
REM
REM  Diferencas para o INICIAR SITE.bat antigo:
REM   - Detecta venv copiado de outra maquina e recria sozinho
REM     (o venv guarda caminhos do computador onde foi criado)
REM   - Garante que o usuario do admin "rabalista" existe
REM     (se nao existir, cria com a senha padrao sedu2026 -
REM      troque depois em /admin/ ^> Usuarios)
REM ============================================================

cd /d "%~dp0"

echo.
echo ============================================================
echo   SITE CURRICULOS SEDU - INICIANDO...
echo   Pasta: %CD%
echo ============================================================
echo.

REM -- 1. Ambiente Python (venv) -------------------------------
set VENV_OK=1
if not exist "venv\Scripts\python.exe" set VENV_OK=0
if "%VENV_OK%"=="1" (
    venv\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 set VENV_OK=0
)
if "%VENV_OK%"=="0" (
    echo [1/4] Ambiente Python ausente ou veio de outra maquina.
    echo        Recriando agora ^(so na primeira vez, ~2 min^)...
    if exist "venv" rmdir /s /q venv
    python -m venv venv
    if errorlevel 1 (
        color 0C
        echo.
        echo ERRO: Python nao encontrado neste computador.
        echo Instale em https://www.python.org/downloads/
        echo e marque "Add Python to PATH" na instalacao.
        echo.
        pause
        exit /b 1
    )
    echo        Instalando o Django e dependencias...
    venv\Scripts\python.exe -m pip install --quiet -r requirements.txt
) else (
    echo [1/4] Ambiente Python OK.
)

REM -- 2. Banco de dados em dia --------------------------------
echo [2/4] Verificando o banco de dados...
venv\Scripts\python.exe manage.py migrate --noinput >nul 2>&1

REM -- 3. Usuario do admin garantido ---------------------------
echo [3/4] Verificando o usuario do painel administrativo...
venv\Scripts\python.exe manage.py shell -c "from django.contrib.auth.models import User; u,c=User.objects.get_or_create(username='rabalista', defaults={'is_superuser':True,'is_staff':True}); c and (u.set_password('sedu2026') or u.save()); print('       Usuario CRIADO -> login: rabalista / senha: sedu2026 (troque em /admin/)' if c else '       Usuario rabalista OK.')"

REM -- 4. Abre o navegador e inicia o servidor -----------------
echo [4/4] Iniciando o servidor...
echo.
echo ============================================================
echo   SITE NO AR!
echo.
echo   Site .....: http://127.0.0.1:8000/
echo   Admin ....: http://127.0.0.1:8000/admin/  (login: rabalista)
echo.
echo   Para PARAR o servidor: aperte Ctrl+C nesta janela
echo   (ou simplesmente feche esta janela)
echo ============================================================
echo.

start "" http://127.0.0.1:8000/

venv\Scripts\python.exe manage.py runserver

echo.
echo Servidor encerrado.
pause
