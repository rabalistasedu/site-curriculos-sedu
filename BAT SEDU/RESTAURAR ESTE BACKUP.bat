@echo off
chcp 65001 >nul
set PYTHONUTF8=1
title RESTAURAR BACKUP DOCKER - Site Curriculos SEDU
color 0B

REM ============================================================
REM  RESTAURAR BACKUP COMPLETO DO DOCKER (banco + midia + codigo)
REM  Recria o site Docker (Postgres + Django) neste computador,
REM  usando os arquivos que estao DENTRO DESTA MESMA PASTA:
REM   - codigo_projeto.zip   (codigo do site)
REM   - banco_postgres.sql   (dados do banco Postgres)
REM   - media_data.tar.gz    (arquivos de midia enviados no site)
REM
REM  Requisito neste computador antes de rodar:
REM   - Docker Desktop instalado e ABERTO
REM
REM  Este arquivo eh copiado automaticamente para dentro de cada
REM  pasta de backup pelo "BACKUP DOCKER COMPLETO.bat". Para usar
REM  em outro computador: copie a pasta de backup inteira (ela
REM  contem este .bat e os 3 arquivos acima) e de dois cliques
REM  aqui.
REM
REM  NAO mexe em nada de outro projeto ja existente neste PC -
REM  cria uma pasta NOVA para o site restaurado.
REM ============================================================

cd /d "%~dp0"

echo.
echo ============================================================
echo   RESTAURAR BACKUP DOCKER - SITE CURRICULOS SEDU
echo   Pasta deste backup: %CD%
echo ============================================================
echo.

if not exist "codigo_projeto.zip" (
    color 0C
    echo ERRO: "codigo_projeto.zip" nao encontrado nesta pasta.
    echo Este arquivo .bat precisa ficar DENTRO da pasta do backup,
    echo junto com codigo_projeto.zip, banco_postgres.sql e
    echo media_data.tar.gz.
    echo.
    pause
    exit /b 1
)

if not exist "banco_postgres.sql" (
    color 0C
    echo ERRO: "banco_postgres.sql" nao encontrado nesta pasta.
    echo.
    pause
    exit /b 1
)

if not exist "media_data.tar.gz" (
    color 0C
    echo ERRO: "media_data.tar.gz" nao encontrado nesta pasta.
    echo.
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERRO: o Docker Desktop nao parece estar aberto/rodando.
    echo Abra o Docker Desktop, espere ele ficar pronto, e rode
    echo este arquivo de novo.
    echo.
    pause
    exit /b 1
)

set DESTINO_PADRAO=%~dp0Site_Restaurado
set /p DESTINO="Pasta onde instalar o site (ENTER = %DESTINO_PADRAO%): "
if "%DESTINO%"=="" set DESTINO=%DESTINO_PADRAO%

if exist "%DESTINO%\manage.py" (
    color 0C
    echo ERRO: ja existe um site em "%DESTINO%".
    echo Escolha outra pasta de destino para nao sobrescrever nada.
    echo.
    pause
    exit /b 1
)

echo.
echo Instalando em: %DESTINO%
echo.

mkdir "%DESTINO%" 2>nul

REM -- 1. Extrai o codigo do projeto --------------------------------
echo [1/6] Extraindo o codigo do projeto...
powershell -NoProfile -Command "Expand-Archive -Path '%~dp0codigo_projeto.zip' -DestinationPath '%DESTINO%' -Force"
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao extrair o codigo do projeto. Leia a mensagem acima.
    pause
    exit /b 1
)

cd /d "%DESTINO%"

REM -- 2. Constroi a imagem Docker do site --------------------------
echo [2/6] Construindo a imagem Docker do site (pode demorar alguns minutos)...
docker compose build
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao construir a imagem Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 3. Sobe somente o banco Postgres, ainda vazio -----------------
echo [3/6] Subindo o banco Postgres (vazio, pronto para restaurar)...
docker compose up -d db
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao subir o banco Postgres. Leia a mensagem acima.
    pause
    exit /b 1
)

echo        Aguardando o banco Postgres ficar pronto...
timeout /t 10 /nobreak >nul

REM -- 4. Restaura os dados do banco ----------------------------------
echo [4/6] Restaurando os dados do banco Postgres...
docker compose exec -T db psql -U curriculo_sedu -d curriculo_sedu < "%~dp0banco_postgres.sql"
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao restaurar os dados do banco. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 5. Sobe o site e restaura os arquivos de midia -----------------
echo [5/6] Subindo o site e restaurando os arquivos de midia...
docker compose up -d web
timeout /t 8 /nobreak >nul
docker compose exec -T web tar xzf - -C /app/media < "%~dp0media_data.tar.gz"

REM -- 6. Confere as migracoes do banco ---------------------------------
echo [6/6] Conferindo as migracoes do banco...
docker compose exec -T web python manage.py migrate

echo.
echo ============================================================
echo   RESTAURACAO CONCLUIDA COM SUCESSO!
echo.
echo   Site instalado em: %DESTINO%
echo   Acesse no navegador: http://localhost:8000/
echo ============================================================
echo.
pause
