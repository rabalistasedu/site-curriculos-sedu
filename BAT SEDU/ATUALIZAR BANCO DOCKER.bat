@echo off
chcp 65001 >nul
set PYTHONUTF8=1
title ATUALIZAR BANCO DOCKER - Site Curriculos SEDU
color 0B

REM ============================================================
REM  ATUALIZAR BANCO DO DOCKER (PostgreSQL) COM O BANCO LOCAL
REM  Use sempre que quiser que o site rodando no Docker (Postgres)
REM  fique com os mesmos dados do seu ambiente local (SQLite).
REM
REM  O que ele faz, na ordem:
REM   1. Exporta todos os dados do banco local (SQLite) para um
REM      arquivo temporario (dump_local.json)
REM   2. Sobe os containers do Docker, se nao estiverem rodando
REM   3. Aplica as migracoes no banco Postgres do Docker
REM   4. Limpa os dados atuais do Postgres do Docker
REM   5. Importa o dump_local.json dentro do Postgres do Docker
REM
REM  Nao mexe no seu banco local (SQLite) em nenhum momento -
REM  so LE dele para copiar os dados para o Docker.
REM
REM  Funciona em qualquer computador: usa a pasta onde este
REM  .bat esta salvo (BAT SEDU), subindo um nivel para o projeto.
REM ============================================================

cd /d "%~dp0.."

echo.
echo ============================================================
echo   ATUALIZAR BANCO DOCKER - SITE CURRICULOS SEDU
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

REM -- 1. Exporta os dados do banco local (SQLite) -------------
echo [1/5] Exportando dados do banco local (SQLite)...
venv\Scripts\python.exe manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission -e admin.logentry -e sessions.session --indent 2 -o dump_local.json
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao exportar o banco local. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 2. Sobe os containers do Docker --------------------------
echo [2/5] Subindo os containers do Docker ^(se nao estiverem rodando^)...
docker compose up -d
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO: nao foi possivel subir os containers do Docker.
    echo Verifique se o Docker Desktop esta aberto e rodando.
    pause
    exit /b 1
)

echo        Aguardando o banco Postgres do Docker ficar pronto...
timeout /t 8 /nobreak >nul

REM -- 3. Aplica as migracoes no Postgres do Docker -------------
echo [3/5] Aplicando migracoes no Postgres do Docker...
docker compose exec -T web python manage.py migrate
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao migrar o banco do Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 4. Limpa os dados atuais do Postgres do Docker -----------
echo [4/5] Limpando os dados atuais do Postgres do Docker...
docker compose exec -T web python manage.py flush --no-input

REM -- 5. Importa o dump do banco local para o Docker ------------
echo [5/5] Importando os dados do banco local para o Docker...
docker compose exec -T web python manage.py loaddata dump_local.json
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao importar os dados no Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   PRONTO! O banco do Docker (Postgres) agora tem os mesmos
echo   dados do seu banco local (SQLite).
echo   Site no Docker: http://localhost:8000/
echo ============================================================
echo.
pause
