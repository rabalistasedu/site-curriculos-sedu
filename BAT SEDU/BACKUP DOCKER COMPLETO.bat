@echo off
chcp 65001 >nul
set PYTHONUTF8=1
title BACKUP DOCKER COMPLETO - Site Curriculos SEDU
color 0B

REM ============================================================
REM  BACKUP COMPLETO DO AMBIENTE DOCKER (banco + midia + codigo)
REM  Gera uma pasta com tudo que eh preciso para recriar o site
REM  Docker (com o banco Postgres populado) em qualquer outro
REM  computador Windows - inclusive no servidor da SEDU.
REM
REM  O que ele faz, na ordem:
REM   1. Sobe os containers do Docker, se nao estiverem rodando
REM   2. Exporta o banco Postgres do Docker (banco_postgres.sql)
REM   3. Exporta os arquivos de midia do Docker (media_data.tar.gz)
REM   4. Empacota o codigo do projeto (codigo_projeto.zip)
REM   5. Copia o restaurador para dentro da pasta do backup
REM
REM  NAO mexe no seu banco local (SQLite) nem no site local -
REM  so LE o que ja esta rodando no Docker.
REM
REM  Cada backup fica em uma pasta separada, com data e hora,
REM  dentro de "docker_backups". Para levar para outro PC, basta
REM  copiar essa pasta inteira (pendrive, nuvem, etc.) e la abrir
REM  o arquivo "RESTAURAR ESTE BACKUP.bat" que fica dentro dela.
REM ============================================================

cd /d "%~dp0.."

echo.
echo ============================================================
echo   BACKUP DOCKER COMPLETO - SITE CURRICULOS SEDU
echo   Pasta do projeto: %CD%
echo ============================================================
echo.

if not exist "venv\Scripts\python.exe" (
    color 0C
    echo ERRO: ambiente Python ^(venv^) nao encontrado.
    echo Rode primeiro o "ATUALIZAR BANCO.bat" ou o "INICIAR SISTEMA.bat".
    echo.
    pause
    exit /b 1
)

if not exist "BAT SEDU\RESTAURAR ESTE BACKUP.bat" (
    color 0C
    echo ERRO: "BAT SEDU\RESTAURAR ESTE BACKUP.bat" nao encontrado.
    echo Ele precisa existir para ser copiado junto com cada backup.
    echo.
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERRO: o Docker Desktop nao parece estar aberto/rodando.
    echo Abra o Docker Desktop e espere ele ficar pronto, depois
    echo rode este arquivo de novo.
    echo.
    pause
    exit /b 1
)

REM -- Descobre data/hora para nomear a pasta do backup ------------
for /f "delims=" %%T in ('venv\Scripts\python.exe -c "import datetime; print(datetime.datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S'))"') do set CARIMBO=%%T

set PASTA=docker_backups\backup_%CARIMBO%

echo Pasta deste backup: %PASTA%
echo.

mkdir "%PASTA%" 2>nul

REM -- 1. Sobe os containers do Docker ------------------------------
echo [1/5] Subindo os containers do Docker (se nao estiverem rodando)...
docker compose up -d
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO: nao foi possivel subir os containers do Docker.
    pause
    exit /b 1
)

echo        Aguardando o banco Postgres do Docker ficar pronto...
timeout /t 8 /nobreak >nul

REM -- 2. Exporta o banco Postgres do Docker -------------------------
echo [2/5] Exportando o banco Postgres do Docker...
docker compose exec -T db pg_dump -U curriculo_sedu curriculo_sedu > "%PASTA%\banco_postgres.sql"
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao exportar o banco Postgres do Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 3. Exporta os arquivos de midia do Docker ----------------------
echo [3/5] Exportando os arquivos de midia do Docker...
docker compose exec -T web tar czf - -C /app/media . > "%PASTA%\media_data.tar.gz"
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao exportar os arquivos de midia do Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 4. Empacota o codigo do projeto -----------------------------------
echo [4/5] Empacotando o codigo do projeto...
powershell -NoProfile -Command "$excluir = @('venv','staticfiles','docker_backups','.git','.claude','__pycache__','ngrok','ngrok.exe','BKPbat','dump_local.json'); $itens = Get-ChildItem -Force | Where-Object { $excluir -notcontains $_.Name }; Compress-Archive -Path $itens.FullName -DestinationPath '%PASTA%\codigo_projeto.zip' -Force"
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao empacotar o codigo do projeto. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 5. Copia o restaurador para dentro da pasta do backup ---------------
echo [5/5] Copiando o restaurador para dentro do backup...
copy /y "BAT SEDU\RESTAURAR ESTE BACKUP.bat" "%PASTA%\RESTAURAR ESTE BACKUP.bat" >nul

echo.
echo ============================================================
echo   BACKUP CONCLUIDO COM SUCESSO!
echo.
echo   Pasta gerada: %CD%\%PASTA%
echo.
echo   Para levar o site Docker (com banco e midia) para outro
echo   computador: copie essa pasta inteira (pendrive, nuvem,
echo   e-mail, etc.) e la, com o Docker Desktop instalado e
echo   aberto, de dois cliques no arquivo dentro dela chamado
echo   "RESTAURAR ESTE BACKUP.bat".
echo ============================================================
echo.
pause
