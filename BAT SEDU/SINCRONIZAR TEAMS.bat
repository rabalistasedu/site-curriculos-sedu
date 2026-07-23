@echo off
chcp 65001 >nul
title SINCRONIZAR TEAMS - Site Curriculos SEDU
color 0B

REM ============================================================
REM  SINCRONIZAR COMENTARIOS COM O MICROSOFT TEAMS (GECEB)
REM
REM  O que ele faz:
REM   1. Verifica se ja tem mensagem no Teams para comentarios
REM      enviados recentemente (vincula pelo ID do comentario)
REM   2. Verifica se chegou resposta nova da equipe no Teams e,
REM      se sim, traz para o site (mesmo campo que o admin usa)
REM
REM  Seguro rodar quantas vezes quiser. Se as credenciais do
REM  Azure AD (TEAMS_CLIENT_ID etc.) ainda nao foram configuradas
REM  pela TI da SEDU, ele so avisa e nao faz nada -- nao quebra
REM  nada, so nao tem o que sincronizar ainda.
REM
REM  Para rodar sozinho a cada poucos minutos: registre este
REM  arquivo no Agendador de Tarefas do Windows (Task Scheduler),
REM  repetindo a cada 3-5 minutos.
REM ============================================================

cd /d "%~dp0.."

echo.
echo ============================================================
echo   SINCRONIZAR TEAMS - SITE CURRICULOS SEDU
echo ============================================================
echo.

if not exist "venv\Scripts\python.exe" (
    color 0C
    echo ERRO: ambiente Python (venv) nao encontrado.
    echo Rode primeiro o "ATUALIZAR BANCO.bat" ou "INICIAR SISTEMA.bat".
    echo.
    pause
    exit /b 1
)

venv\Scripts\python.exe manage.py sincronizar_teams

echo.
pause
