@echo off
chcp 65001 >nul
title SITE CURRICULOS SEDU - Servidor local
color 0B

REM ============================================================
REM  INICIAR SITE CURRICULOS SEDU
REM  Funciona em qualquer computador: usa sempre a pasta onde
REM  este arquivo .bat esta salvo (nao depende do caminho C:\...)
REM ============================================================

cd /d "%~dp0"

echo.
echo ============================================================
echo   SITE CURRICULOS SEDU - INICIANDO...
echo   Pasta: %~dp0
echo ============================================================
echo.

REM ── 1. Garante que o ambiente virtual (venv) existe ─────────
if not exist "venv\Scripts\python.exe" (
    echo [1/3] Ambiente virtual nao encontrado. Criando agora...
    echo        ^(isso so acontece na primeira vez, aguarde ~2 min^)
    python -m venv venv
    if errorlevel 1 (
        color 0C
        echo.
        echo ERRO: Python nao encontrado neste computador.
        echo Instale em https://www.python.org/downloads/
        echo e marque a opcao "Add Python to PATH" na instalacao.
        echo.
        pause
        exit /b 1
    )
    echo [1/3] Instalando o Django e dependencias...
    venv\Scripts\python.exe -m pip install --quiet -r requirements.txt
) else (
    echo [1/3] Ambiente virtual OK.
)

REM ── 2. Aplica atualizacoes do banco de dados (se houver) ────
echo [2/3] Verificando o banco de dados...
venv\Scripts\python.exe manage.py migrate --noinput >nul 2>&1

REM ── 3. Abre o navegador e inicia o servidor ─────────────────
echo [3/3] Iniciando o servidor...
echo.
echo ============================================================
echo   SITE NO AR!
echo.
echo   Site .....: http://127.0.0.1:8000/
echo   Admin ....: http://127.0.0.1:8000/admin/
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
