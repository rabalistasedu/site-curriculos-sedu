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
  models.py              # Categoria, Conteudo, Banner, Comentario, Cartaz, ConfiguracaoSite
  views.py               # home, categoria_detalhe, conteudo_detalhe, busca
  admin.py               # Admin customizado com badges, widgets visuais, moderação
  forms.py               # ConteudoAdminForm, BannerAdminForm, CategoriaAdminForm, ConfiguracaoSiteAdminForm
  widgets.py             # CategoriaPicker, IconPicker (grade de ícones) e RichTextWidget (editor com formatação)
  urls.py                # app_name='conteudo'
  context_processors.py  # site_config (config + menu_categorias global)
  migrations/            # 0001 inicial → 0008 (config_home_texto)
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
  categoria.html         # Lista de conteúdos com filtros, banners de categoria, índice geral (55 botões)
  conteudo_detalhe.html  # Detalhe de conteúdo + seção de comentários (com moderação)
  busca.html             # Resultados de busca
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

## URLs

```
/                          → home
/admin/                    → Django Admin
/busca/?q=termo            → busca textual
/categoria/<slug>/         → lista de conteúdos com filtros
/categoria/<slug>/?tipo=X  → filtro por tipo (documento, video, post, link)
/conteudo/<slug>/          → detalhe de conteúdo
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

## Deploy (PythonAnywhere)

O site está publicado para teste em **https://rabalista.pythonanywhere.com** (ver também "Onde os arquivos ficam armazenados" mais abaixo).

- **Usuário PythonAnywhere:** `rabalista`
- **Pasta do projeto no servidor:** `/home/rabalista/site-curriculos-sedu/`
- **Arquivo WSGI:** `/var/www/rabalista_pythonanywhere_com_wsgi.py` (força `ALLOWED_HOSTS = ['*']` e `DEBUG = False` após carregar o settings — remover essa sobrescrita se `ALLOWED_HOSTS` for restringido no `settings.py` futuramente)
- **Static files** (aba Web → Static files): URL `/static/` → Directory `/home/rabalista/site-curriculos-sedu/staticfiles`
- **Media files** (uploads): URL `/media/` → Directory `/home/rabalista/site-curriculos-sedu/media`

Fluxo para publicar mudanças feitas localmente:

```bash
# No terminal Bash do PythonAnywhere
cd ~/site-curriculos-sedu
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

Depois, na aba **Web** do PythonAnywhere, clicar em **Reload**.

## Como rodar

```bash
cd "Site Curriculos SEDU"
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/ (criar superuser com `python manage.py createsuperuser`)

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
- Widgets visuais do admin (`CategoriaPicker`, `IconPicker`) carregam o Font Awesome via CDN na própria `Media` da classe, pois o admin do Django não inclui o CDN usado no site público (`templates/base.html`).
- O CSS dos widgets (`admin_picker.css`) usa `!important` em vários pontos porque o CSS padrão do Django Admin estiliza `<label>` genericamente (largura fixa, `display: block`), o que sobrescreveria a grade de botões sem isso.
- **Cartazes**: no admin, ao criar/editar um cartaz, escolha o tamanho na seção "Posição e exibição" — a imagem nunca será distorcida. Em desktop (>1400px), aparecem nas laterais **dentro da área branca de conteúdo** (são filhos da seção `.home-conteudo`, presos por `position: sticky` — nunca invadem o banner, a faixa azul do texto nem o rodapé, em nenhuma posição de rolagem); em mobile/tablet (≤1400px), um botão flutuante "Eventos" abre um painel deslizante com todos os cartazes ativos em grade. O botão só aparece se houver pelo menos um cartaz com "Ativo" marcado. **Importante**: se um dia forem adicionadas outras seções brancas entre o banner e a seção `.home-conteudo` (ex.: "Destaques"), os cartazes continuarão presos só à `.home-conteudo` — para cobrir mais áreas, mover as colunas `.cartazes-lateral` para um contêiner `position: relative` que envolva toda a região branca desejada.
- **Cache do navegador ao testar mudanças de CSS**: depois de publicar uma alteração visual (deploy no PythonAnywhere ou até localmente), se a mudança não aparecer, force um recarregamento sem cache (Ctrl+Shift+R no Windows/Linux, Cmd+Shift+R no Mac) antes de concluir que há um bug — várias vezes durante o desenvolvimento o código já estava correto mas o navegador ainda mostrava o CSS antigo salvo em cache.
- **Fluxo de trabalho obrigatório**: toda alteração de código feita nesta pasta local também precisa ser enviada ao GitHub (`git add`, `git commit`, `git push origin main`) para não ficar dessincronizada — o site publicado no PythonAnywhere só recebe as mudanças fazendo `git pull` de lá. Sempre que uma sessão terminar com alterações no código, confirme que o `git push` foi feito.
- **Migração das páginas do WordPress concluída em 2026-07-06**: dos 41 itens que ainda apontavam para `curriculo.sedu.es.gov.br/curriculo/...`, a maioria foi convertida para páginas nativas (`tipo='pagina'`, com HTML extraído da página original e comentários moderados no admin Django). 3 itens não puderam ser migrados com segurança e precisam de decisão do Dan:
  - **pk 58 "GEEPEI — Espaços Potencialmente Educativos e Inovadores"**: a URL antiga (`/geepei/`) hoje mostra o conteúdo de outro item ("Mitigação de Desigualdades..."). O conteúdo original do GEEPEI não foi encontrado nessa URL nem em nenhuma outra do site antigo.
  - **pk 20 "Orientações Curriculares 2024"** e **pk 21 "Orientações Curriculares 2023"**: ambos apontavam para a mesma URL (`/orientacoescurriculares/`), que hoje só exibe a versão **2026** — as versões de 2023 e 2024 não existem mais nesse endereço.
  - (O item "Rotina Pedagógica Escolar — RPE" que também estava nessa lista de pendências já havia sido tratado à parte pelo comando `migrar_rpe.py`, ver item acima.)
  - Lembrete: como o `db.sqlite3` não é versionado no Git, essa migração de conteúdo só existe no banco local até ser copiada manualmente para o PythonAnywhere.
