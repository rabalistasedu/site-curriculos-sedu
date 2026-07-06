# Como rodar o Site Currículo SEDU

## Requisitos

- **Python 3.10+** (baixe em https://www.python.org/downloads/)
- Funciona em **Mac** e **Windows** da mesma forma

---

## Passo a passo (primeira vez)

### 1. Abra o terminal (Mac) ou Prompt de Comando (Windows)

No Mac: abra o aplicativo "Terminal"
No Windows: tecle `Win + R`, digite `cmd` e pressione Enter

### 2. Navegue até a pasta do projeto

```bash
cd caminho/para/Site Curriculos SEDU
```

### 3. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

Ative o ambiente:
- **Mac/Linux**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Crie o banco de dados

```bash
python manage.py migrate
```

### 6. Popule as categorias

```bash
python manage.py popular_categorias
```

### 7. Crie o usuário administrador

```bash
python manage.py createsuperuser
```

Ele vai pedir:
- Nome de usuário (ex: `admin`)
- E-mail (ex: `gerenciadecurriculo@sedu.es.gov.br`)
- Senha (escolha uma senha forte)

### 8. Rode o servidor

```bash
python manage.py runserver
```

### 9. Acesse no navegador

- **Site público**: http://127.0.0.1:8000/
- **Painel admin**: http://127.0.0.1:8000/admin/

---

## Uso diário

Sempre que quiser rodar o site:

```bash
cd caminho/para/Site Curriculos SEDU
source venv/bin/activate        # Mac
venv\Scripts\activate           # Windows
python manage.py runserver
```

Para parar o servidor: pressione `Ctrl + C`

---

## Opção alternativa: Docker

Se preferir usar Docker (precisa instalar Docker Desktop):

```bash
docker-compose up --build
```

O site estará em http://localhost:8000/

---

## Transferir do Mac para o Windows

1. Copie TODA a pasta "Site Curriculos SEDU" para um pendrive ou nuvem
2. No Windows, siga os passos 1-9 acima
3. O banco de dados (db.sqlite3) vai junto — seus dados são preservados!

**Importante**: o arquivo `db.sqlite3` contém todo o conteúdo do site.
Se quiser começar do zero no Windows, delete esse arquivo e refaça os passos 5-7.
