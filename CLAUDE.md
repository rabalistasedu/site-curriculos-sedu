# Site Currículos SEDU — Contexto do Projeto

## O que é este projeto

Site da **Gerência de Currículo da Educação Básica (GECEB)**, da Secretaria de Estado da Educação do Espírito Santo (SEDU). Migração do site WordPress/Elementor em `curriculo.sedu.es.gov.br/curriculo/` para Django moderno.

O dono do projeto (**Dan**) não é programador — ele trabalha na SEDU e precisa de instruções claras, em português, para qualquer operação no terminal. Sempre explique comandos passo a passo.

## Stack

- **Django 5.2** com Python 3.13 (local) / Python 3.11 (PythonAnywhere)
- **SQLite** em desenvolvimento e também em produção (por enquanto)
- **Venv** em `venv/`
- CSS puro (sem frameworks CSS), Font Awesome 6 para ícones, Google Fonts (Inter)
- **Deploy atual: PythonAnywhere** (https://rabalista.pythonanywhere.com) — ver seção "Deploy" abaixo
- **Versionamento: GitHub** — https://github.com/DanBalista/site-curriculos-sedu.git

## Estrutura do projeto

```
curriculo_sedu/          # Projeto Django (settings, urls, wsgi)
conteudo/                # App principal
  models.py              # Categoria, Conteudo, Banner, Comentario, Cartaz, ConfiguracaoSite, Anexo
  views.py               # home, categoria_detalhe, conteudo_detalhe, busca (com anexos_categoria no context)
  admin.py               # Admin customizado com badges, widgets visuais, moderação, inlines de Anexo
  admin_views.py         # View customizada organizar_view (/admin/organizar/) para gerenciar conteúdos
  forms.py               # ConteudoAdminForm, BannerAdminForm, CategoriaAdminForm, ConfiguracaoSiteAdminForm
  widgets.py             # CategoriaPicker (3 níveis), IconPicker (grade de ícones) e RichTextWidget (editor com formatação)
  urls.py                # app_name='conteudo'
  context_processors.py  # site_config (config + menu_categorias global)
  migrations/            # 0001 inicial → 0011_anexo_categoria (Anexo com FK dual)
  management/commands/
    popular_categorias.py   # Seed de categorias e subcategorias
    popular_descricoes.py   # Textos introdutórios das categorias (HTML)
    migrar_conteudo.py      # 102 itens de conteúdo migrados do WordPress
    migrar_orientacoes.py   # 129 documentos de Orientações Curriculares do WordPress
    migrar_ifa.py           # Itinerários Formativos de Aprofundamento (IFA): 10 subcategorias, 14 docs
    organizar_curriculo_atual.py  # Divide "Currículo Atual" em sub-botões por etapa de ensino
    migrar_material_apoio.py      # Subcategoria "Material de Apoio" dentro de Currículo Atual (5 docs)
    migrar_projetos_integradores.py  # Categoria principal "Projetos Integradores" (5 subcategorias)
    migrar_rpe.py            # Categoria "Rotinas Pedagógicas Escolares (RPE)" (8 subcategorias, 42 docs)
    migrar_olimpiadas.py     # Categoria "Olimpíadas" (9 subcategorias, 9 links oficiais)
    curar_recentes.py        # Marca a curadoria oficial de "Conteúdos recentes" da home
templates/
  base.html              # Layout base (header, nav dinâmica, footer, ícone discreto de admin)
  home.html              # Home: hero/banners, "Conteúdos recentes" (esquerda) + "Navegue por área" (direita)
  categoria.html         # Lista de conteúdos com filtros, banners de categoria, índice geral (55 botões), seção de anexos
  conteudo_detalhe.html  # Detalhe de conteúdo + seção de comentários (com moderação)
  busca.html             # Resultados de busca
  admin/
    index.html           # Dashboard customizado do admin (estende admin/base_site.html) com botão "Abrir Organizador"
    organizar.html       # Interface visual do Organizador — breadcrumb, subcategorias, conteúdos, busca, ordem inline
static/
  css/style.css          # Design system completo
  css/admin_picker.css   # Estilos dos widgets visuais do admin (CategoriaPicker, IconPicker)
  js/main.js             # Slider do hero, menu mobile
  img/                   # logogov.png (Governo ES), gerenciaok.png (GECEB), hero-ilustracao.png (ilustração do banner da home)
staticfiles/             # Gerado por collectstatic (produção/PythonAnywhere) — não editar
media/                   # Uploads (banners/, destaques/) — não versionado no Git
db.sqlite3               # Banco já populado com 231+ conteúdos (102 originais + 129 orientações)
```

## Modelos principais

### Categoria
- `nome`, `slug`, `descricao` (HTML para textos introdutórios), `icone` (classe Font Awesome)
- `categoria_pai` (FK self) — hierarquia de 2 níveis
- `ordem`, `ativa`, `imagem`
- No admin, o campo `icone` usa a mesma grade visual (`IconPicker`) do Conteúdo
- O campo `slug` tem `autocomplete="off"` porque o navegador às vezes sugere preencher automaticamente com um valor salvo do histórico (não é um erro do site — se aparecer algo estranho no campo "URL amigável" ao criar uma categoria nova, é só apagar e digitar o correto)

### Conteudo
- Tipos: `documento`, `video`, `post`, `link`, `pagina`
- Status: `rascunho`, `publicado`, `arquivado`
- Campos: `titulo`, `slug`, `resumo`, `corpo` (HTML), `arquivo`, `url_video`, `url_externa`, `imagem_destaque`
- `icone_manual` (opcional) — ícone Font Awesome escolhido no admin via grade visual (IconPicker); se vazio, usa `icone_criativo` (automático por palavra-chave)
- `destaque` (bool) — aparece na home
- **Agendamento**: status "Publicado" com `data_publicacao` futura — o conteúdo só aparece no site quando a data/hora chegar (via `ConteudoQuerySet.publicados()` que filtra `data_publicacao__lte=timezone.now()`)
- `recente` (bool) — se marcado, aparece na seção "Conteúdos recentes" da home (lista lateral esquerda). Se desmarcado, o item continua aparecendo normalmente na categoria escolhida, só não vai para essa lista. Editável direto na tabela do admin ou no formulário de edição (checkbox logo abaixo de "Destaque")
- Propriedades: `tipo_icone`, `icone_criativo` (prioriza `icone_manual`, senão detecta por texto), `extensao_arquivo`, `get_video_embed_url()`
- No admin, a categoria de publicação é escolhida clicando em um botão visual (`CategoriaPicker`), não em um dropdown

### Banner
Banners rotativos — na home (`categoria=None`) ou dentro de uma categoria específica (`categoria=<FK>`). Campos: `titulo`, `subtitulo`, `imagem`, `link`, `ordem`, `ativo`, `categoria`, `tamanho` (`pequeno`/`medio`/`grande`, controla a altura de exibição).
- No admin, a área de exibição também é escolhida via botão visual (`CategoriaPicker` com opção extra "Página inicial")
- A imagem nunca é cortada nem distorcida no site — o CSS usa a própria imagem borrada como fundo (efeito letterbox) atrás da imagem original em tamanho real (`object-fit: contain`)

### Comentario
Sistema de comentários com moderação, substituindo o Disqus do WordPress. Campos: `conteudo` (FK), `nome`, `email`, `texto`, `aprovado` (bool, padrão `False`), `data_criacao`.
- Comentários enviados no site ficam pendentes até serem aprovados no admin (`ComentarioAdmin`)
- Ações em lote no admin: Aprovar, Reprovar/ocultar e Excluir permanentemente
- Só comentários com `aprovado=True` aparecem na página de detalhe do conteúdo

### Cartaz
Cartazes de eventos na home. Campos: `titulo`, `imagem` (upload_to `cartazes/`), `link`, `lado` (`esquerdo`/`direito`), `tamanho` (`pequeno` 90px / `medio` 140px / `grande` 200px), `ordem`, `ativo`.
- **Desktop (>1400px)**: posição fixa nas laterais, tamanho configurável sem distorcer imagem
- **Mobile/Tablet (<=1400px)**: botão flutuante "Eventos" no canto inferior direito; ao clicar, abre painel deslizante de baixo para cima com grade de cartazes

### ConfiguracaoSite
Singleton (pk=1). `nome_site`, `descricao`, `email_contato`, `telefone`, `endereco`, `logo`, `favicon`.
- `home_titulo` e `home_texto` — título e texto que aparecem na home, logo abaixo do banner/hero. Editáveis no admin em "Configuração do site" → seção "📝 Texto da página inicial", com um editor de texto simples (`RichTextWidget`) com negrito, itálico, sublinhado, alinhamento e lista — sem depender de bibliotecas externas (usa `contenteditable` + `document.execCommand`, salva HTML no campo).

### Anexo
Modelo para anexar múltiplos arquivos (PDF, Word, Excel, PowerPoint, vídeo, imagem, etc.) a **Conteudo** ou **Categoria**.
- FKs duais (mutualmente exclusivos): `conteudo` (nullable) ou `categoria` (nullable) — um anexo pertence a exatamente um ou outro
- `arquivo` (FileField, upload_to `'anexos/%Y/%m/'`) — PDF, Word, Excel, PowerPoint, vídeo, imagem, ZIP, etc.
- `nome` (CharField, opcional) — nome exibido no site; se vazio, usa o nome do arquivo
- `ordem` (PositiveIntegerField) — ordena anexos pela sequência definida no admin
- Propriedades: `extensao` (retorna ex: "PDF"), `nome_exibicao` (nome ou nome do arquivo)
- Tabular inline no admin (ambas as classes, 3 campos editáveis: arquivo, nome, ordem)
- No site, aparece em seção visual na página de categoria com cards em lista vertical, ícones coloridos por tipo

## URLs

```
/                             → home
/admin/                       → Django Admin (com botão "Abrir Organizador")
/admin/organizar/             → Organizador de Conteúdo (painel visual para gerenciar categorias e conteúdos)
/admin/organizar/?cat=<id>    → Organizador filtrando uma categoria específica
/busca/?q=termo               → busca textual
/categoria/<slug>/            → lista de conteúdos com filtros (inclui anexos da categoria)
/categoria/<slug>/?tipo=X     → filtro por tipo (documento, video, post, link)
/conteudo/<slug>/             → detalhe de conteúdo
```

## Categorias atuais (10 principais + subcategorias)

1. **Documentos Curriculares** (fas fa-book) — subcategorias: Currículo Atual (com 5 sub-botões por etapa: Educação Infantil, EF Anos Iniciais, EF Anos Finais, Ensino Médio, Material de Apoio), Orientações Curriculares, Cadernos Metodológicos, Mapas de Progressão, Ementas Curriculares, Rotinas de Recomposição, Espaços Potencialmente Educativos
2. **Orientações Curriculares** (fas fa-compass) — 129 documentos migrados do WordPress, 16 subcategorias: EF Anos Iniciais, EF Anos Finais, EM Formação Geral Básica, 3 grupos IFA, 9 Itinerários, Anos Anteriores
3. **Itinerários Formativos de Aprofundamento (IFA)** (fas fa-route) — 10 subcategorias, 14 documentos
4. **Projetos Integradores** (fas fa-diagram-project) — 5 subcategorias (Documentos Gerais, Linguagens e Ciências Humanas 2ªDiurno, Ciências da Natureza e Matemática 2ªDiurno, Linguagens 1ªNoturno, CHSA 2ªNoturno)
5. **Rotinas Pedagógicas Escolares (RPE)** (fas fa-calendar-check) — 8 subcategorias (Língua Portuguesa/Matemática × EF/EM × Estudante/Professor), 42 documentos (apostilas por ano/série e trimestre)
6. **Programas** (fas fa-project-diagram) — subcategorias: Educar para a Paz, Mais Leitores, Educação Ambiental, Sucesso Escolar
7. **Livro Didático** (fas fa-book-reader)
8. **Modalidades e Diversidade** (fas fa-users) — subcategorias: EJA — Documentos, Educação do Campo, Educação Quilombola, Educação Indígena, Relações Étnico-Raciais, Socioeducação
9. **Olimpíadas** (fas fa-trophy) — 9 subcategorias: OBF, OBFEP, OLITEF, Movimento Meninas Olímpiadas, Olimpíada do Empreendedorismo, Biologia Sintética, Prêmio Jovem Cientista, Olimpíada do Bem Público (FGV), Programa Jovem Senador. Texto introdutório migrado do WordPress
10. **Institucional** (fas fa-landmark)

## Design system (CSS)

Variáveis principais em `style.css`:
- `--primary: #2d5a8e` (azul do header e acentos)
- `--primary-dark: #1e3a5f`
- `--text: #1a1a2e`, `--text-light: #4a5568`
- `--bg: #ffffff`, `--bg-alt: #f7f8fa`
- Font: Inter, system-ui

Header: fundo `--primary`, logos 50px (`logogov.png` à esquerda, `gerenciaok.png` à direita, ambos com fundo transparente), nav com dropdown implícito, busca inline, largura 100% com padding 32px. Responsivo com breakpoints em 1024px, 768px e 400px (hamburger menu no mobile).

Componentes: `.content-card`, `.category-card`, `.content-list .list-item`, `.filter-chip`, `.subcategory-chip`, `.page-intro-body` (texto introdutório com borda azul à esquerda).

## Decisões de design já tomadas

1. **Header sem filtros CSS nos logos** — brightness/blend-mode removidos, logos exibidos com cores originais
2. **Textos introdutórios** aparecem entre os filtros de tipo e o grid de conteúdo (não no header)
3. **Cards da home** usam `|striptags|truncatewords:10` para descrições limpas
4. **Conteúdo migrado** via web scraping do WordPress — 102 itens com links para PDFs e Google Drive
5. **16 categorias** têm textos introdutórios em HTML (populados via `popular_descricoes.py`)
6. **Anexos em lista vertical** — não em grid responsivo — porque arquivos anexados a categorias (especialmente em Itinerários, IFA, RPE) são geralmente 3-5 itens específicos, não uma coleção grande; layout vertical é mais legível
7. **FK dual (mutualmente exclusivo) no Anexo** — `conteudo` OU `categoria`, não ambos — simplifica a constraint (CHECK na migração) e a lógica admin; se um anexo virar comum entre ambos no futuro, usar ManyToMany ou GenericForeignKey
8. **Organizador como view customizada no admin** — não como app separado — mantém integração total com Django admin (permissões, autenticação, interface) e acesso via `/admin/organizar/` visualmente alinhado
9. **CategoriaPicker com 3 níveis (netos)** — renderiza botões aninhados em subgrupos visuais — era necessário para categorias como "Ensino Médio" (neto de "Currículo Atual" → "Documentos Curriculares")
10. **Logo pulsante em páginas internas** — convida o usuário a voltar à home com um efeito suave de ondulação + crescimento ao hover; só aparece fora da home para não distrair na página inicial
11. **Ícones em títulos de seções** — "Conteúdos recentes" tem ícone de varinha mágica (`fas fa-wand-magic-sparkles`), "Navegue por área" tem ícone de bússola (`fas fa-compass`) — reforça a navegação visual
12. **Centralização do "Currículo Atual"** — botão destaque em gradê azul com ícone + texto perfeitamente centrados — visualmente mais importante e diferenciado dos outros cards

## Deploy (PythonAnywhere)

O site está publicado para teste em **https://rabalista.pythonanywhere.com** (ver também "Onde os arquivos ficam armazenados" mais abaixo).

- **Usuário PythonAnywhere:** `rabalista`
- **Pasta do projeto no servidor:** `/home/rabalista/site-curriculos-sedu/`
- **Arquivo WSGI:** `/var/www/rabalista_pythonanywhere_com_wsgi.py` (força `ALLOWED_HOSTS = ['*']` e `DEBUG = False` após carregar o settings — remover essa sobrescrita se `ALLOWED_HOSTS` for restringido no `settings.py` futuramente)
- **Static files** (aba Web → Static files): URL `/static/` → Directory `/home/rabalista/site-curriculos-sedu/staticfiles`
- **Media files** (uploads): URL `/media/` → Directory `/home/rabalista/site-curriculos-sedu/media`

Fluxo para publicar mudanças feitas localmente (script único, copiar e colar no Bash do PythonAnywhere):

```bash
cd ~/site-curriculos-sedu && git fetch origin main && git reset --hard origin/main && source venv/bin/activate && python manage.py migrate && python manage.py collectstatic --noinput --clear && echo "==== PRONTO! Va na aba Web e clique em Reload ===="
```

Depois, na aba **Web** do PythonAnywhere, clicar em **Reload**.

**Por que `git reset --hard origin/main` em vez de `git pull`** (correção 2026-07-07):
- `staticfiles/` foi removido do controle de versão do Git (`git rm -r --cached staticfiles` + adicionado ao `.gitignore`). Antes, essa pasta estava versionada, e como o `collectstatic` MODIFICA os arquivos dela no servidor, o `git pull` seguinte falhava com *"Your local changes would be overwritten by merge"* — travando toda a atualização (o site continuava mostrando a versão antiga). Sintoma clássico: "subi pro GitHub mas o PythonAnywhere não muda".
- `git reset --hard origin/main` força o servidor a ficar idêntico ao GitHub, descartando qualquer modificação local (inclusive dos staticfiles gerados). É **seguro** porque `db.sqlite3` (banco) e `media/` (uploads) são gitignored / untracked — o reset não os toca.
- `collectstatic --noinput --clear` apaga a pasta `staticfiles` antiga antes de recopiar, garantindo que CSS/JS antigos sumam de vez.
- **Cache-busting do CSS**: `templates/base.html` carrega o CSS com `?v=AAAAMMDD-N` (ex.: `?v=20260707-4`). Ao mudar o CSS, incrementar esse número força o navegador a baixar a versão nova (senão ele usa a cacheada). É a linha `<link rel="stylesheet" href="{% static 'css/style.css' %}?v=...">`.

**Armadilha adicional já resolvida (2026-07-07): mapeamento de Static files desatualizado na aba Web** — mesmo com o Git e o `collectstatic` 100% corretos, o site continuava mostrando CSS/HTML antigos. Causa: na aba **Web → Static files**, o campo Directory do `/static/` apontava para `/home/rabalista/staticfiles` (pasta solta, de uma configuração antiga), em vez de `/home/rabalista/site-curriculos-sedu/staticfiles` (onde o `collectstatic` realmente escreve). Já foi corrigido manualmente na aba Web. **Se o problema voltar a acontecer no futuro** (site sempre desatualizado mesmo com deploy correto), primeiro confira essa tabela na aba Web:

| URL | Directory correto |
|---|---|
| `/static/` | `/home/rabalista/site-curriculos-sedu/staticfiles` |
| `/media/` | `/home/rabalista/site-curriculos-sedu/media` |

Para diagnosticar isso rapidamente no Bash do PythonAnywhere sem depender do navegador (que pode estar com cache), rodar:
```bash
curl -s https://rabalista.pythonanywhere.com/static/css/style.css | grep -c logoPulse
```
Se o número vier `0` mesmo depois do deploy, é o mapeamento de Static files que está errado (não o Git).

### Migração de WordPress para Django (Produção em `curriculo.sedu.es.gov.br`)

**Situação:** O novo Django vai ser publicado em `curriculo.sedu.es.gov.br` (onde hoje está o WordPress). Todos os ~1000 arquivos migrados têm links que apontam para `/curriculo/wp-content/uploads/...` — remover o WordPress quebraria todos esses links.

**Solução:** Manter o WordPress rodando em um **subdomínio** (`wordpress.curriculo.sedu.es.gov.br`) e usar **reescrita Apache** para redirecionar automaticamente as requisições `/wp-content/` para lá. Sem duplicar arquivos e sem alterar nenhum link no banco de dados.

**Documentação completa:**
- 📘 [MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md) — Estratégia completa, cronograma e decisões
- 🔧 [EXEMPLOS_HTACCESS.md](EXEMPLOS_HTACCESS.md) — Códigos prontos para copiar/colar (Opção 1: subdomínio; Opção 2: pasta local)
- 🧪 [TESTE_MANUAL_URLS.md](TESTE_MANUAL_URLS.md) — Comandos `curl` para validar que os links funcionam após migração

**Resumo rápido:**
1. Criar subdomínio `wordpress.curriculo.sedu.es.gov.br` (ou pasta `/wp-backup/`)
2. Copiar WordPress completo para lá
3. Configurar reescrita no `.htaccess` do domínio principal
4. Publicar novo Django em `curriculo.sedu.es.gov.br`
5. Testar com comandos no documento de testes

### Sincronização de Dados Entre Local e SEDU (Banco de Dados)

**Importante:** O arquivo `db.sqlite3` NÃO é versionado no Git (está em `.gitignore`). Isso significa:
- Cada ambiente (seu PC local, servidor SEDU) tem seu próprio banco de dados separado
- Dados adicionados via admin local **NÃO aparecem automaticamente em SEDU**
- Código Python (models, views, migrations) sobe para GitHub e é sincronizado, mas dados não

**Estratégia Recomendada: Backup Manual e Upload**

Dan pode usar esta abordagem simples (não requer código):

1. **Trabalhar localmente** — adicione conteúdos, categorias, banners via admin em `http://127.0.0.1:8000/admin/`
2. **Fazer backup do banco local:**
   ```bash
   # Windows/Mac/Linux — no terminal da pasta do projeto
   cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
   # Ou copie manualmente o arquivo db.sqlite3 para uma pasta de backup
   ```
3. **Subir código para GitHub** (como sempre, via `.bat` ou git push):
   ```bash
   git add -A
   git commit -m "Nova categoria/conteúdo"
   git push origin main
   ```
4. **Subir o banco para SEDU** via cPanel ou SFTP:
   - **Via cPanel:** File Manager → navegue para `/home/rabalista/site-curriculos-sedu/`
     - Delete o `db.sqlite3` antigo
     - Upload do seu arquivo `db.sqlite3` local (o backup)
   - **Via SFTP (mais seguro):**
     ```bash
     sftp rabalista@rabalista.pythonanywhere.com
     cd site-curriculos-sedu
     rename db.sqlite3 db.sqlite3.backup
     put C:\Users\ridan\Claude\Projects\Site Curriculos SEDU\db.sqlite3 db.sqlite3
     exit
     ```
5. **Reload no PythonAnywhere:**
   - Acesse painel PythonAnywhere
   - Aba **Web** → clique **Reload** (botão verde)
6. ✅ **Pronto!** Django carrega o novo banco e site mostra os dados novos

**Fluxo Resumido:**
```
Local (PC)                GitHub                    SEDU (servidor)
Adiciona no admin   →   Sobe código via push   →   Puxa código
Salva em db.sqlite3 →   (dados NÃO vão)        →   db.sqlite3 antigo
    ↓                                               ↑
    └─── Backup manual ──→ Upload via SFTP ───────┘
         do db.sqlite3
```

**Cuidados Importantes:**

1. **Migrations devem estar sincronizadas:** Se você mudou modelos Django, execute no Bash do PythonAnywhere antes de trocar o banco:
   ```bash
   cd ~/site-curriculos-sedu && python manage.py migrate
   ```

2. **Dados em SEDU são perdidos:** Se o servidor tinha dados que não estão no seu backup local, eles sumirem após o upload. **Sempre faça backup do banco SEDU antes de trocar:**
   ```bash
   # No Bash PythonAnywhere:
   cp ~/site-curriculos-sedu/db.sqlite3 ~/db.sqlite3.backup.sedu
   ```

3. **Permissões do arquivo:** Após upload, garanta que o arquivo tem permissões certas:
   ```bash
   chmod 644 ~/site-curriculos-sedu/db.sqlite3
   ```

4. **Horário do servidor:** Se conteúdos estão agendados com `data_publicacao` futura, verifique se a hora do servidor está correta:
   ```bash
   # No Bash PythonAnywhere:
   date
   ```

5. **Tamanho do banco:** SQLite funciona bem até ~500MB. Se o banco ficar muito grande, migrar para PostgreSQL será necessário. Ver tamanho:
   ```bash
   # No Bash PythonAnywhere:
   ls -lh ~/site-curriculos-sedu/db.sqlite3
   ```

**Como Verificar se Funcionou:**

```bash
# No seu PC, abra http://127.0.0.1:8000/admin/ e veja conteúdo X
# Depois, 5 minutos após fazer reload em SEDU, abra:
# https://rabalista.pythonanywhere.com/admin/ e veja se conteúdo X aparece
```

Ou via linha de comando (verificar contagem de conteúdos):
```bash
# Local:
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM conteudo_conteudo;"

# SEDU (Bash PythonAnywhere):
cd ~/site-curriculos-sedu && sqlite3 db.sqlite3 "SELECT COUNT(*) FROM conteudo_conteudo;"
```

Se os números forem iguais, o banco foi sincronizado com sucesso ✅

**Frequência Recomendada:**
- Sincronizar 1x por semana ou sempre que adicionar conteúdo importante
- Manter backups por pelo menos 1 mês (para poder reverter se necessário)
- Documentar a data de cada backup

**Alternativa: Management Commands (Para o Futuro)**
Se quiser automatizar (requer código Python), usar `management/commands/` para recriar dados programaticamente. Ver seção "Management commands disponíveis" acima. Mas por enquanto, a estratégia manual é a mais simples e funciona perfeitamente.

## Como rodar

```bash
cd "Site Curriculos SEDU"
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/ (criar superuser com `python manage.py createsuperuser`)

**Importante ao testar CSS**: sempre force recarregamento sem cache após fazer alterações CSS:
- **Windows/Linux**: Ctrl+Shift+R
- **Mac**: Cmd+Shift+R
- Sem isso, o navegador mostra a versão antiga do CSS em cache

## Management commands disponíveis

```bash
python manage.py popular_categorias    # Cria categorias e subcategorias
python manage.py popular_descricoes    # Textos introdutórios das categorias
python manage.py migrar_conteudo       # 102 itens de conteúdo do site original
python manage.py migrar_orientacoes    # 129 documentos de Orientações Curriculares
python manage.py migrar_ifa            # Itinerários Formativos de Aprofundamento (IFA)
python manage.py organizar_curriculo_atual  # Sub-botões por etapa em "Currículo Atual"
python manage.py migrar_material_apoio      # Subcategoria "Material de Apoio" em Currículo Atual
python manage.py migrar_projetos_integradores  # Categoria "Projetos Integradores" (Navegue por área)
python manage.py migrar_rpe                    # Categoria "Rotinas Pedagógicas Escolares (RPE)"
python manage.py migrar_olimpiadas             # Categoria "Olimpíadas" com 9 subcategorias
python manage.py curar_recentes                 # Marca a seleção oficial de "Conteúdos recentes"
```

Todos são idempotentes (usam `get_or_create` ou verificam existência). Os comandos
`migrar_ifa` e `organizar_curriculo_atual` são autossuficientes: se o documento já
existe no banco (de outra migração), eles MOVEM para a categoria/etapa correta em vez
de duplicar. Usam slugs FIXOS para nunca criar subcategorias duplicadas.

## O que já foi feito

- [x] Estrutura completa do Django (models, views, admin, templates, CSS)
- [x] Admin personalizado com badges coloridos, filtros e ações em lote
- [x] Template base responsivo com header, nav dinâmica e footer
- [x] Página home reorganizada: "Conteúdos recentes" à esquerda, "Navegue por área" à direita
- [x] Página de categoria com subcategorias, filtros por tipo e textos introdutórios
- [x] Página-índice "Documentos Curriculares" com os 55 botões de subcategorias (como no site antigo), em ordem alfabética
- [x] Página de detalhe de conteúdo com relacionados
- [x] Busca textual
- [x] Migração de 102 conteúdos do site original WordPress
- [x] 16 textos introdutórios das categorias extraídos do site original
- [x] Header com logos (`logogov.png` Governo ES + `gerenciaok.png` GECEB) com fundo transparente e tamanhos iguais
- [x] Ícones criativos por palavra-chave (substituem a seta genérica de "link externo")
- [x] Seletor visual de ícone por conteúdo no admin (`IconPicker`), sobrepondo o automático
- [x] Sistema de comentários com moderação no admin (substitui o Disqus do WordPress)
- [x] Ícone discreto de acesso ao admin no rodapé do site
- [x] Admin com seleção visual de categoria/área (`CategoriaPicker`), tanto para Conteúdo quanto para Banner
- [x] Banners rotativos por área (home ou categoria específica), com imagem nunca cortada/distorcida e tamanho configurável (pequeno/médio/grande)
- [x] Deploy de teste em produção no PythonAnywhere (https://rabalista.pythonanywhere.com)
- [x] Agendamento de publicação por data/hora futura (conteúdo fica invisível até a data chegar)
- [x] Cartazes de eventos na home com tamanho configurável (pequeno/médio/grande) — desktop mostra nas laterais, mobile/tablet via botão flutuante
- [x] Responsividade completa para celulares e tablets (breakpoints 1024px, 768px, 400px)
- [x] Exclusão de comentários no admin (ação em lote + botão individual)
- [x] Cartazes laterais limitados à área branca de conteúdo (JavaScript dinâmico mede header+banner+intro e footer a cada scroll)
- [x] Texto da home ("Currículo do Espírito Santo — Referencial...") movido para abaixo do banner/hero e editável no admin com formatação (negrito, itálico, alinhamento, lista)
- [x] Ordem mobile corrigida: "Conteúdos recentes" aparece antes de "Navegue por área" (estava invertido)
- [x] Menu mobile (hamburger) corrigido — os itens do menu apareciam cortados na lateral direita por um bug de `flex-basis` no CSS
- [x] Seletor visual de ícone (`IconPicker`) também no admin de Categoria, não só em Conteúdo
- [x] Todos os conteúdos "link" que apontavam para páginas de texto do WordPress antigo foram convertidos em páginas nativas (`tipo='pagina'`), com comentários moderados no admin Django — migração concluída em 2026-07-06 (ver nota abaixo sobre as exceções que não puderam ser migradas)
- [x] Categoria "Orientações Curriculares" com 129 documentos migrados do WordPress (16 subcategorias: EF Anos Iniciais/Finais, EM Formação Geral Básica, IFAs, Itinerários, Anos anteriores) — comando `migrar_orientacoes.py`
- [x] Categoria principal "Itinerários Formativos de Aprofundamento (IFA)" (Navegue por área) com 10 subcategorias e 14 documentos — comando `migrar_ifa.py` (move docs existentes ou cria; slugs fixos; remove subcategorias vazias)
- [x] "Currículo Atual" (dentro de Documentos Curriculares) dividido em sub-botões por etapa de ensino (Educação Infantil, EF Anos Iniciais, EF Anos Finais, Ensino Médio, Material de Apoio), como os acordeões do site antigo — comandos `organizar_curriculo_atual.py` e `migrar_material_apoio.py`. Resoluções e Tema Integrador ficam como documentos gerais direto em "Currículo Atual"
- [x] Categoria principal "Projetos Integradores" (Navegue por área, logo após IFA) com texto introdutório e 5 subcategorias, migrado de `curriculo.sedu.es.gov.br/curriculo/projetointegrador/` — comando `migrar_projetos_integradores.py`. Os 3 documentos gerais dos IFAs que também aparecem nessa página do WordPress NÃO foram duplicados aqui — permanecem só em "Itinerários Formativos de Aprofundamento (IFA)"
- [x] Categoria principal "Rotinas Pedagógicas Escolares (RPE)" (Navegue por área, logo após Projetos Integradores) com texto introdutório e 42 apostilas (Língua Portuguesa/Matemática, EF/EM, Estudante/Professor, por ano/série e trimestre), migrado de `curriculo.sedu.es.gov.br/curriculo/rpe/` — comando `migrar_rpe.py`. A página original tem 4 níveis de hierarquia (Matéria > Público > Etapa > Ano > Trimestre); como o site só suporta 2 níveis, viraram 8 subcategorias (Matéria + Público + Etapa) com o Ano/Trimestre como título de cada documento. O item antigo "Rotina Pedagógica Escolar — RPE" (link genérico para a página do WordPress, sem os arquivos reais) foi removido
- [x] Menu do topo corrigido: em telas ≤1400px os ícones dos links de navegação são ocultados para os textos das categorias não ficarem cortados
- [x] Cartazes laterais presos à área branca via CSS puro (`position: sticky`) — os cartazes agora são filhos da seção branca de conteúdo (`.home-conteudo`, `position: relative`); cada coluna é `position: absolute` presa ao topo e à base dessa seção e o bloco interno (`.cartazes-inner`) usa `position: sticky; top: 88px` para acompanhar a rolagem. Como são filhos da área branca, é fisicamente impossível invadirem o banner/faixa azul (acima) ou o rodapé (abaixo). Substituiu a abordagem anterior por JavaScript, que era frágil
- [x] Nova ilustração do banner da home (`hero-ilustracao.png`) preenchendo o quadrante inteiro do banner (`object-fit: cover`, sem opacidade reduzida); quadro do texto "Currículo do Espírito Santo" abaixo do banner reduzido (fonte e padding menores) para que o banner de imagem fique visualmente maior que o quadro de texto
- [x] Categoria principal "Olimpíadas" (Navegue por área) reorganizada com texto introdutório completo e 9 subcategorias oficiais migradas de `curriculo.sedu.es.gov.br/curriculo/olimpiadas/`: OBF, OBFEP, OLITEF, Movimento Meninas Olímpiadas, Empreendedorismo, Biologia Sintética, Prêmio Jovem Cientista, Bem Público (FGV), Programa Jovem Senador. Cada olimpíada tem um link "Saiba mais" para o site oficial — comando `migrar_olimpiadas.py`. Subcategorias antigas ("Olimpíadas de Física/Matemática/Biologia", "Educação Financeira", "Empreendedorismo", "Outras Competições") foram substituídas
- [x] Seção "Conteúdos recentes" da home passa a ser **curada** — antes mostrava automaticamente os 8 mais recentes por `data_publicacao`, agora mostra apenas itens marcados com o novo campo `recente=True`. Checkbox "Aparecer em Conteúdos recentes" fica logo abaixo de "Destaque" no admin, tanto no formulário quanto editável direto na lista (`list_editable`). Migração `0009_conteudo_recente`
- [x] Comando `curar_recentes.py` — como o `db.sqlite3` não é versionado no Git (cada ambiente tem o seu banco), esse comando marca automaticamente a seleção oficial de 5 itens em "Conteúdos recentes" (por URL, igual aos comandos de migração), sem precisar clicar manualmente no admin em cada ambiente (local, PythonAnywhere, outro computador). É a fonte da verdade da curadoria — para trocar a seleção, edite a lista `URLS_RECENTES` no arquivo e rode o comando de novo (ele marca os da lista e desmarca quem não estiver mais nela). Idempotente
- [x] Barra inferior do rodapé reduzida ao mínimo (18px de altura, fonte 11px), fundo azul médio `#3b6fa8` com texto branco, tudo em uma única linha (© + ícone admin lado a lado). Antes tinha padding grande e opacidade baixa
- [x] Scrollbar interna adicionada às seções "Conteúdos recentes" (esquerda) e "Navegue por área" (direita) da home — `max-height: 600px; overflow-y: auto` com scrollbar estilizada em azul. Necessário porque essas seções tendem a crescer muito com adição de novos conteúdos/categorias
- [x] Botão flutuante "Eventos" (cartazes mobile) só aparece agora em telas ≤900px (antes ≤1400px, o que fazia ele aparecer atrás/sobreposto a elementos do desktop pequeno)
- [x] Modelo `Anexo` criado — permite anexar múltiplos arquivos (PDF, Word, Excel, PowerPoint, vídeo, imagem, ZIP, etc.) a Conteudo ou Categoria — FK dual (mutualmente exclusivo) + campo `ordem` para sequência
- [x] Tabular inline `AnexoConteudoInline` no admin de Conteudo e `AnexoCategoriaInline` no admin de Categoria — 3 campos editáveis direto (arquivo, nome, ordem), 3 extras vazios por padrão
- [x] Campo `ordem` (PositiveIntegerField) adicionado a Conteudo para permitir ordenação manual — editável inline na tabela do admin (`list_editable`)
- [x] Organizador de Conteúdo (`/admin/organizar/`) — painel visual dentro do admin para:
  - Navegar por categoria/subcategoria e visualizar seus conteúdos em ordem
  - Criar novas subcategorias dentro de uma categoria selecionada (abre em nova aba)
  - Mover conteúdos entre categorias via formulário de busca de todo o site
  - Editar ordem inline (campo texto) e salvar alterações
  - Buscar conteúdos do site para adicionar/mover para a categoria atual
  - Visualização precisa: mostra exatamente o que aparece no site (subcategorias e conteúdos corretos)
- [x] CategoriaPicker widget atualizado para suportar 3 níveis de hierarquia (categoria → subcategoria → neto) — exibe categorias filhas com seus netos em subgrupos visuais, cada um com sua própria linha de botões
- [x] Seção de anexos nas páginas de categoria — exibe arquivos anexados à categoria em cards verticais bonitos:
  - Cada arquivo é um card com: ícone colorido por tipo (PDF vermelho, Word azul, Excel verde, PPT laranja, vídeo roxo)
  - Nome do arquivo em destaque + "Clique para abrir ou baixar" em cinza
  - Badge colorido com extensão (ex: "PDF" em fundo vermelho claro)
  - Ícone de download discreto no canto direito (aparece em hover)
  - Borda azul à esquerda (visual alinhado com cards de conteúdo do site)
  - Layout responsivo em lista vertical, gap entre cards, fundo cinza suave
- [x] Logo "Currículo Espírito Santo" com efeito pulsante em páginas internas (categoria, conteúdo, busca) — convida o usuário a retornar à home:
  - Borda branca translúcida + fundo branco translúcido em torno do logo
  - Anel externo se expandindo continuamente (efeito de ondulação radiante)
  - Pulso no shadow + fundo alternando a cada 2s
  - Ao passar mouse: cresce 6%, brilho branco de 24px, borda fica sólida branca, pulso para
  - Na home, o logo fica normal (sem pulso)
- [x] Ícone de navegação adicionado ao título "Navegue por área" na home — usa a classe `fas fa-compass` (bússola) antes do texto, alinhado com o ícone "Conteúdos recentes"
- [x] Botão "Currículo Atual" totalmente centralizado — ícone + texto alinhados no centro do botão azul degradê:
  - `.area-card-featured` com `justify-content: center` + `align-items: center`
  - `.area-text` transformado em flex column com `align-items: center` + `justify-content: center`
  - Texto (`h3`) com `text-align: center` e `margin: 0`
  - Ícone com `margin: 0` para não desalinhar

## O que falta / próximos passos possíveis

- [ ] Adicionar imagens de destaque aos demais conteúdos
- [ ] Refinamentos visuais conforme feedback do Dan e aprovação do chefe
- [ ] Migrar para domínio oficial `curriculo.sedu.es.gov.br` + certificado SSL
- [ ] Deploy final com Docker + PostgreSQL para produção definitiva
- [ ] Testar em Windows (ambiente de trabalho do Dan)
- [ ] Adicionar paginação nas listagens de conteúdo

## Notas importantes

- O banco `db.sqlite3` já contém todos os dados migrados. Não precisa rodar os commands novamente a menos que queira resetar.
- Os conteúdos tipo `link` e `documento` apontam para URLs externas (Google Drive, SEDU, etc.) — os arquivos PDF não estão armazenados localmente.
- O site original em WordPress está em: `curriculo.sedu.es.gov.br/curriculo/`
- O usuário não tem conhecimento de programação — sempre forneça comandos prontos para copiar e colar.
- **Anexos**: No admin, ao editar uma Categoria ou Conteudo, existe uma seção "📎 Arquivos anexados" com tabela inline para adicionar até 3 arquivos por vez (clique "Adicionar mais linhas" para expandir). Formatos suportados: PDF, Word (.doc, .docx), Excel (.xls, .xlsx), PowerPoint (.ppt, .pptx), vídeo (.mp4, .avi, .mov, .mkv, .webm), imagem (.jpg, .jpeg, .png, .gif, .webp), ZIP, TXT, CSV, OpenDocument, etc. No site, anexos de categoria aparecem em seção visual acima dos conteúdos, cada arquivo é um card com ícone colorido, nome, extensão e link para download. Ordem editável no admin.
- **Organizador de Conteúdo** (`/admin/organizar/`): Painel visual dentro do admin (acessível via botão "Abrir Organizador" no dashboard ou via URL direta) para gerenciar categorias e conteúdos:
  - Navegue pela hierarquia clicando em categorias/subcategorias (breadcrumb no topo)
  - Veja todos os conteúdos da categoria selecionada + suas subcategorias em lista com ordem inline (campo texto)
  - Crie novas subcategorias dentro da categoria atual (botão "Criar nova subcategoria" abre em nova aba)
  - Mova conteúdos de outras categorias para a atual via busca (busca todos os conteúdos do site)
  - Reordene itens editando o campo `ordem` direto na tabela e clicando "Salvar ordem"
  - A precisão é crítica: mostra exatamente o que aparece no site (não mostra conteúdos das subcategorias do mesmo nível, só da categoria selecionada + suas filhas)
- Widgets visuais do admin (`CategoriaPicker`, `IconPicker`) carregam o Font Awesome via CDN na própria `Media` da classe, pois o admin do Django não inclui o CDN usado no site público (`templates/base.html`).
- O CSS dos widgets (`admin_picker.css`) usa `!important` em vários pontos porque o CSS padrão do Django Admin estiliza `<label>` genericamente (largura fixa, `display: block`), o que sobrescreveria a grade de botões sem isso.
- **Cartazes**: no admin, ao criar/editar um cartaz, escolha o tamanho na seção "Posição e exibição" — a imagem nunca será distorcida. Em desktop (>1400px), aparecem nas laterais **dentro da área branca de conteúdo** (são filhos da seção `.home-conteudo`, presos por `position: sticky` — nunca invadem o banner, a faixa azul do texto nem o rodapé, em nenhuma posição de rolagem); em mobile/tablet (≤1400px), um botão flutuante "Eventos" abre um painel deslizante com todos os cartazes ativos em grade. O botão só aparece se houver pelo menos um cartaz com "Ativo" marcado. **Importante**: se um dia forem adicionadas outras seções brancas entre o banner e a seção `.home-conteudo` (ex.: "Destaques"), os cartazes continuarão presos só à `.home-conteudo` — para cobrir mais áreas, mover as colunas `.cartazes-lateral` para um contêiner `position: relative` que envolva toda a região branca desejada.
- **Anexos — Visual refinado**: arquivos anexados a categorias aparecem em seção visual bonita com:
  - Cards individuais em lista vertical (não inline)
  - Borda azul à esquerda (5px) para alinhamento com design do site
  - Ícone colorido por tipo (PDF #dc2626 vermelho, Word #2563eb azul, Excel #059669 verde, PPT #d97706 laranja, Vídeo #7c3aed roxo, Imagem #0891b2 ciano, Padrão #6b7280 cinza)
  - Nome do arquivo em destaque (font-weight: 600) + "Clique para abrir ou baixar" em cinza abaixo
  - Badge colorido com extensão (fundo suave + cor correspondente ao ícone, border-radius: 20px)
  - Ícone de download discreto à direita, opacity 0.6 em repouso, opacity 1 em hover
  - Efeito hover suave: borda ativa, shadow maior, slide 3px à direita
  - Container `.anexos-section`: fundo cinza, border, border-radius, padding — visual similar a card
- **Cache do navegador ao testar mudanças de CSS**: depois de publicar uma alteração visual (deploy no PythonAnywhere ou até localmente), se a mudança não aparecer, force um recarregamento sem cache (Ctrl+Shift+R no Windows/Linux, Cmd+Shift+R no Mac) antes de concluir que há um bug — várias vezes durante o desenvolvimento o código já estava correto mas o navegador ainda mostrava o CSS antigo salvo em cache.
- **Logo pulsante em páginas internas**: o logo "Currículo Espírito Santo" tem um efeito de pulso suave (anel externo expandindo, brilho alternando) em todas as páginas EXCETO na home. Implementado via:
  - Template: `base.html` tem `{% block logo_class %}{% endblock %}`
  - Páginas internas (`categoria.html`, `conteudo_detalhe.html`, `busca.html`) definem `{% block logo_class %}logo-pulse{% endblock %}`
  - CSS: `.logo.logo-pulse` com animação `logoPulse` (2s) + `:hover` que para o pulso e cresce o logo
  - Propósito: convida o usuário a retornar à home com microrinteração sutil ao mudar de página
- **Fluxo de trabalho com Git**: toda alteração de código feita localmente precisa ser sincronizada com o GitHub:
  1. **Commit e push locais**: clique 2x no `.bat` "Subir GitHub SEDU" na sua área de trabalho (Desktop) — ele faz `git add -A`, `git commit` com mensagem customizável, e `git push origin main` automaticamente
  2. **Sincronizar com PythonAnywhere**: acesse o terminal bash do PythonAnywhere e execute:
     ```bash
     cd ~/site-curriculos-sedu
     git pull origin main
     python manage.py migrate
     python manage.py collectstatic --noinput
     ```
  3. **Reload no PythonAnywhere**: na aba **Web** do painel PythonAnywhere, clique em **Reload** para aplicar as mudanças
  - **Importante**: o site publicado em PythonAnywhere só recebe mudanças via `git pull` — as alterações locais não aparecem lá automaticamente. Sempre complete os 3 passos acima.
- **Migração das páginas do WordPress concluída em 2026-07-06**: dos 41 itens que ainda apontavam para `curriculo.sedu.es.gov.br/curriculo/...`, a maioria foi convertida para páginas nativas (`tipo='pagina'`, com HTML extraído da página original e comentários moderados no admin Django). 3 itens não puderam ser migrados com segurança e precisam de decisão do Dan:
  - **pk 58 "GEEPEI — Espaços Potencialmente Educativos e Inovadores"**: a URL antiga (`/geepei/`) hoje mostra o conteúdo de outro item ("Mitigação de Desigualdades..."). O conteúdo original do GEEPEI não foi encontrado nessa URL nem em nenhuma outra do site antigo.
  - **pk 20 "Orientações Curriculares 2024"** e **pk 21 "Orientações Curriculares 2023"**: ambos apontavam para a mesma URL (`/orientacoescurriculares/`), que hoje só exibe a versão **2026** — as versões de 2023 e 2024 não existem mais nesse endereço.
  - (O item "Rotina Pedagógica Escolar — RPE" que também estava nessa lista de pendências já havia sido tratado à parte pelo comando `migrar_rpe.py`, ver item acima.)
  - Lembrete: como o `db.sqlite3` não é versionado no Git, essa migração de conteúdo só existe no banco local até ser copiada manualmente para o PythonAnywhere.
