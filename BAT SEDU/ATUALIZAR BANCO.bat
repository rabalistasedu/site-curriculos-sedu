@echo off
chcp 65001 >nul
title ATUALIZAR BANCO - Site Curriculos SEDU
color 0E

REM ============================================================
REM  ATUALIZAR BANCO DE DADOS
REM  Use depois de copiar a pasta para outro computador ou
REM  depois de baixar atualizacoes do GitHub.
REM
REM  O que ele faz, na ordem:
REM   1. Conserta o ambiente Python se veio copiado de outra
REM      maquina (o venv guarda caminhos do computador antigo)
REM   2. Baixa o codigo mais recente do GitHub (se tiver internet)
REM   3. Aplica as migracoes pendentes no banco
REM   4. Importa conteudos do portal antigo que faltarem
REM      (seguro: nunca duplica nem apaga nada)
REM
REM  Funciona em qualquer computador: usa a pasta onde este
REM  .bat esta salvo (BAT SEDU), subindo um nivel para o projeto.
REM ============================================================

cd /d "%~dp0.."

echo.
echo ============================================================
echo   ATUALIZAR BANCO - SITE CURRICULOS SEDU
echo   Pasta do projeto: %CD%
echo ============================================================
echo.

REM -- 1. Ambiente Python (venv) -------------------------------
REM Um venv copiado de outra maquina aponta para o Python do
REM computador antigo e quebra. Este teste detecta e recria.
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

REM -- 2. Codigo mais recente do GitHub (opcional) -------------
echo [2/4] Buscando atualizacoes no GitHub...
git pull --no-rebase origin main
if errorlevel 1 (
    echo        Aviso: nao foi possivel baixar do GitHub agora
    echo        ^(sem internet?^). Seguindo com o que esta na pasta.
)

REM -- 3. Migracoes do banco -----------------------------------
echo [3/4] Aplicando migracoes no banco de dados...
venv\Scripts\python.exe manage.py migrate
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao migrar o banco. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 4. Importa o que faltar do portal antigo ----------------
echo [4/4] Importando conteudos do portal antigo que faltarem...
echo        ^(seguro: so cria o que nao existe, nunca duplica^)
venv\Scripts\python.exe manage.py importar_remanescentes

echo.
echo ============================================================
echo   PRONTO! Banco atualizado.
echo   Pode fechar esta janela e iniciar o site normalmente.
echo ============================================================
echo.
pause
