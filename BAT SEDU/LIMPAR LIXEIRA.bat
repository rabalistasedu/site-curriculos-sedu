@echo off
chcp 65001 >nul
title LIMPAR LIXEIRA - Site Curriculos SEDU
color 0B

REM ============================================================
REM  LIMPAR LIXEIRA (exclusao automatica apos 30 dias)
REM
REM  O que ele faz:
REM   Exclui DEFINITIVAMENTE os botoes e conteudos que estao na
REM   lixeira (Admin -> Lixeira) ha mais de 30 dias. Antes disso,
REM   continuam recuperaveis normalmente.
REM
REM  OPCIONAL: essa mesma limpeza ja acontece sozinha toda vez que
REM  alguem abre a tela "Lixeira" no admin -- este .bat so serve
REM  para quem quiser garantir a limpeza mesmo que a tela nunca
REM  seja aberta. Seguro rodar quantas vezes quiser.
REM
REM  Para rodar sozinho todo dia: registre este arquivo no
REM  Agendador de Tarefas do Windows (Task Scheduler), 1x por dia.
REM ============================================================

cd /d "%~dp0.."

echo.
echo ============================================================
echo   LIMPAR LIXEIRA - SITE CURRICULOS SEDU
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

venv\Scripts\python.exe manage.py limpar_lixeira_expirada

echo.
pause
