@echo off
chcp 65001 >nul
title COMPARTILHAR SITE COM GERENTE
color 0A

echo.
echo ============================================================
echo   COMPARTILHAR SITE CURRICULOS SEDU COM GERENTE
echo ============================================================
echo.

echo LINKS DISPONIVEIS:
echo.

echo [1] NGROK (INTERNET - RECOMENDADO):
echo     Seu gerente pode acessar de qualquer lugar
echo     Valido por 2 horas
echo.

echo [2] LOCAL (mesma rede WiFi):
echo     Abra CMD e digite: ipconfig
echo     Procure "IPv4 Address" (ex: 192.168.1.100)
echo     Use: http://192.168.1.100:8000
echo.

echo ============================================================
echo.

cd /d "C:\ridan\Claude\Projects\Site Curriculos SEDU\ngrok"

echo Iniciando ngrok...
echo.

ngrok http 8000
