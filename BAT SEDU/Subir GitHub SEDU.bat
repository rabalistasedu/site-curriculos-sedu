@echo off
chcp 65001 >nul
title Subir Site SEDU para GitHub
color 0A

echo ============================================
echo   SUBIR SITE CURRICULOS SEDU PARA GITHUB
echo ============================================
echo.

:: Entra na pasta do projeto (a pasta acima de onde este .bat esta salvo)
cd /d "%~dp0.."

echo Pasta do projeto: %CD%
echo.

:: Mostra o que mudou
echo Verificando alteracoes...
echo.
git status --short

echo.
echo ============================================

:: Pede a mensagem do commit
set /p MSG="Digite a mensagem do commit (ou aperte ENTER para usar padrao): "

if "%MSG%"=="" set MSG=Atualizacao do site SEDU

echo.
echo Enviando para o GitHub...
echo.

git add -A
git commit -m "%MSG%"

:: Baixa novidades do GitHub antes de enviar (evita o erro "fetch first"
:: quando houve commit feito em outro computador ou pelo site do GitHub)
echo.
echo Baixando novidades do GitHub (se houver)...
git pull --no-rebase origin main

git push origin main

echo.
if %ERRORLEVEL%==0 (
    color 0A
    echo ============================================
    echo   PRONTO! Tudo enviado para o GitHub!
    echo ============================================
) else (
    color 0C
    echo ============================================
    echo   ERRO! Verifique a mensagem acima.
    echo ============================================
)

echo.
pause
