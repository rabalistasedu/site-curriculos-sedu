@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title INICIAR SITE + NGROK
color 0A

cd /d "%~dp0.."

echo.
echo ============================================================
echo   INICIAR SITE CURRICULOS SEDU + NGROK
echo ============================================================
echo.

echo [PASSO 1] Verificando ambiente...
if not exist venv (
    echo ERRO: venv nao encontrado!
    pause
    exit /b 1
)
echo OK

echo.
echo [PASSO 2] Iniciando Django em background...
start "Django Server" cmd /k "venv\Scripts\activate && python manage.py runserver"
timeout /t 3

echo.
echo [PASSO 3] Testando conexao...
venv\Scripts\python.exe teste_ngrok.py
if errorlevel 1 (
    echo.
    echo AVISO: Alguns testes falharam. Continuando mesmo assim...
    timeout /t 2
)

echo.
echo [PASSO 4] Iniciando ngrok para compartilhar...
echo.
set PYTHONIOENCODING=utf-8
venv\Scripts\python.exe ngrok_compartilhar.py

endlocal
