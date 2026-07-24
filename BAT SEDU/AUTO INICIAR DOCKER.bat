@echo off
chcp 65001 >nul
title AUTO INICIAR DOCKER - Site Curriculos SEDU

REM ============================================================
REM  AUTO INICIAR DOCKER - liga os containers do site sozinho
REM
REM  O que ele faz, sem precisar digitar nada no terminal:
REM   1. Abre o Docker Desktop, se ainda nao estiver aberto
REM   2. Espera o "motor" do Docker terminar de ligar (pode
REM      demorar 1-2 minutos no computador ligar)
REM   3. Levanta os containers do site sozinho (equivalente a
REM      digitar "docker compose up -d" na mao)
REM
REM  Para funcionar automaticamente toda vez que o Windows liga,
REM  este arquivo precisa estar na pasta de Inicializacao do
REM  Windows (Startup) -- ver instrucoes no CLAUDE.md / README,
REM  ou pedir para o assistente colocar para voce.
REM
REM  Registra tudo em "auto_iniciar_docker_log.txt" (nesta mesma
REM  pasta) -- se quiser conferir se funcionou, abra esse arquivo.
REM ============================================================

cd /d "%~dp0.."

set LOGFILE=%~dp0auto_iniciar_docker_log.txt
echo ============================================================ >> "%LOGFILE%"
echo %DATE% %TIME% - Iniciando... >> "%LOGFILE%"

REM Passo 1: abre o Docker Desktop se ele nao estiver rodando ainda.
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %DATE% %TIME% - Docker Desktop nao esta aberto. Abrindo... >> "%LOGFILE%"
    if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
        start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
    ) else (
        echo %DATE% %TIME% - Docker Desktop.exe nao encontrado no caminho padrao. Abra manualmente. >> "%LOGFILE%"
    )
)

REM Passo 2: espera o motor do Docker responder (ate 5 minutos).
set TENTATIVAS=0
:esperar
set /a TENTATIVAS+=1
docker info >nul 2>&1
if %ERRORLEVEL% EQU 0 goto pronto
if %TENTATIVAS% GEQ 30 (
    echo %DATE% %TIME% - Docker nao respondeu depois de 5 minutos. Abra o Docker Desktop manualmente e rode este arquivo de novo. >> "%LOGFILE%"
    goto fim
)
timeout /t 10 /nobreak >nul
goto esperar

REM Passo 3: levanta os containers do site.
:pronto
echo %DATE% %TIME% - Docker pronto. Levantando containers... >> "%LOGFILE%"
docker compose up -d >> "%LOGFILE%" 2>&1
echo %DATE% %TIME% - Pronto! Containers levantados (ou ja estavam rodando). Site em http://localhost:8000/ >> "%LOGFILE%"

:fim
