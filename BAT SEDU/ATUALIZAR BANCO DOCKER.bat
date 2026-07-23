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
REM   3. Copia os arquivos de midia locais (media\) para dentro
REM      do Docker (icones, imagens, banners, anexos, etc.)
REM   4. Aplica as migracoes no banco Postgres do Docker
REM   5. Limpa os dados atuais do Postgres do Docker
REM   6. Importa o dump_local.json dentro do Postgres do Docker
REM
REM  Nao mexe no seu banco local (SQLite) nem na sua pasta media\
REM  em nenhum momento - so LE deles para copiar para o Docker.
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
REM  --all e necessario por causa da Lixeira (Categoria/Conteudo
REM  soft-delete): sem essa flag, o dumpdata usa o manager padrao,
REM  que ESCONDE itens na lixeira. Isso pode gerar um Conteudo
REM  exportado apontando para uma Categoria que ficou de fora
REM  (por estar na lixeira), quebrando a chave estrangeira ao
REM  importar no Postgres. --all usa o manager que enxerga tudo,
REM  inclusive a lixeira, mantendo o Docker espelhado ao local.
echo [1/6] Exportando dados do banco local (SQLite)...
venv\Scripts\python.exe manage.py dumpdata --all --natural-foreign --natural-primary -e contenttypes -e auth.permission -e admin.logentry -e sessions.session --indent 2 -o dump_local.json
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao exportar o banco local. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 2. Reconstroi as imagens e sobe os containers do Docker --
REM  Reconstruir sempre garante que qualquer mudanca no
REM  requirements.txt (novas bibliotecas Python) seja aplicada
REM  dentro do Docker. Sem isso, o container pode tentar rodar
REM  codigo novo com bibliotecas antigas e falhar ao iniciar.
echo [2/6] Atualizando as imagens do Docker com as dependencias mais recentes...
docker compose build
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao reconstruir as imagens do Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

echo        Subindo os containers do Docker...
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

REM -- 3. Copia os arquivos de midia locais para o Docker -------
REM  A pasta media\ do Docker e um volume separado da sua pasta
REM  media\ local - copiar o banco de dados NAO copia os arquivos
REM  (icones, imagens, banners, anexos). Este passo copia tudo
REM  que existe na sua pasta media\ local para dentro do Docker,
REM  sem apagar nada que ja esteja la.
echo [3/6] Copiando arquivos de midia locais ^(icones, imagens, banners, anexos^) para o Docker...
docker compose cp media\. web:/app/media/
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao copiar os arquivos de midia para o Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 4. Aplica as migracoes no Postgres do Docker -------------
echo [4/6] Aplicando migracoes no Postgres do Docker...
docker compose exec -T web python manage.py migrate
if errorlevel 1 (
    color 0C
    echo.
    echo ERRO ao migrar o banco do Docker. Leia a mensagem acima.
    pause
    exit /b 1
)

REM -- 5. Limpa os dados atuais do Postgres do Docker -----------
echo [5/6] Limpando os dados atuais do Postgres do Docker...
docker compose exec -T web python manage.py flush --no-input

REM -- 6. Importa o dump do banco local para o Docker ------------
echo [6/6] Importando os dados do banco local para o Docker...
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
echo   PRONTO! O banco do Docker (Postgres) e a pasta de midia
echo   agora tem os mesmos dados do seu ambiente local.
echo   Site no Docker: http://localhost:8000/
echo ============================================================
echo.
pause
