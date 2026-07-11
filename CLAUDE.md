# Site Currículos SEDU — Contexto do Projeto (v3 — atualizado em 2026-07-11)

## O que é este projeto

Site da **Gerência de Currículo da Educação Básica (GECEB)**, da Secretaria de Estado da Educação do Espírito Santo (SEDU). Migração do site WordPress/Elementor em `curriculo.sedu.es.gov.br/curriculo/` para Django moderno.

O dono do projeto (**Dan**) não é programador — ele trabalha na SEDU e precisa de instruções claras, em português, para qualquer operação no terminal. Sempre explique comandos passo a passo e forneça comandos prontos para copiar e colar.

## 🚦 Estado atual (por onde começar uma conversa nova)

- O site está **completo e funcional localmente**, com 231+ conteúdos migrados do WordPress no `db.sqlite3` local.
- **Deploy**: o PythonAnywhere foi **abandonado** (decisão de 2026-07-10). O destino final é o servidor da SEDU em `curriculo.sedu.es.gov.br`. Enquanto isso, demonstrações são feitas localmente via ngrok.
- **Leva mais recente (2026-07-11, fim do dia — "parte 2")**: banner/hero da home mais baixo, carrossel ocupa a coluna lateral inteira quando não há cartazes, carrossel vazio (sem imagens) não renderiza mais, seletor "Categoria pai" hierárquico no admin, barra superior com 5 botões fixos discretos + ícone de localização (Google Maps) + painel "Botões da Barra Superior" no admin (/admin/barra-superior/), busca agora encontra também categorias/botões. Detalhes no histórico item 16.
- **Última leva de mudanças (2026-07-11)**: botões da home menores/quadrados, correção dos cartazes que sumiam com zoom, menu "3 pontinhos" (⋯) na barra superior, carrossel de imagens, campos de visibilidade por botão, exclusão de botões pelo Painel Central, imagem por URL em Banner/Cartaz. Detalhes na seção "Histórico de implementação".
- **Importação do conteúdo remanescente CONCLUÍDA (2026-07-11)**: os 134 itens que faltavam do portal antigo foram importados (91 itinerários de formação técnica, 21 ementas EM, 16 volumes do currículo, 6 diversos) — ver seção "Importação do portal antigo". A comparação portal antigo × novo agora dá FALTA: 0. ⚠️ Isso foi feito no banco DESTA máquina; na máquina do Dan é preciso rodar `python manage.py importar_remanescentes` (idempotente) após o `git pull`.
- **Regra de ouro do Painel Central** (`Especificacao_Painel_Admin_Site_Curriculos.md`): sempre ADICIONAR funcionalidades, nunca substituir/quebrar o que já funciona. O Dan reforça isso a cada pedido.
- **Migrações pendentes do último commit**: `conteudo/0012` (Carrossel, url_imagem, mostrar_menu_superior/mostrar_navegue_area), `conteudo/0013` (icone_imagem em Conteudo), `conteudo/0014` (icone_imagem em Categoria) e `painel/0002` (EstiloBotao.tamanho) precisam de `python manage.py migrate` em qualquer ambiente novo.
- Trabalho não commitado deve ser subido pelo Dan com o `.bat` "Subir GitHub SEDU" do Desktop dele.

## Stack

- **Django 5.2** com Python 3.13 (local) / Python 3.11 (PythonAnywhere, histórico)
- **SQLite** em desenvolvimento e produção (por enquanto)
- **Venv** em `venv/` (Windows: `venv\Scripts\activate`)
- CSS puro (sem frameworks), Font Awesome 6 (CDN), Google Fonts (Inter)
- **Apps Django**: `conteudo` (site + admin) e `painel` (Painel Central Administrativo)
- **Versionamento: GitHub** — https://github.com/rabalistasedu/site-curriculos-sedu.git (remoto `origin`)
- Ambiente de desenvolvimento atual: **Windows 11** (pasta `C:\ridan\Claude\Projects\Site Curriculos SEDU`)

## Estrutura do projeto

```
curriculo_sedu/          # Projeto Django (settings, urls, wsgi)
conteudo/                # App principal do site
  models.py              # Categoria, Conteudo, Anexo, Banner, Cartaz, Carrossel,
                         #   CarrosselImagem, ConfiguracaoSite, Comentario
  views.py               # home (com carrosséis), categoria_detalhe, conteudo_detalhe, busca
  admin.py               # Admin customizado: badges, widgets visuais, moderação,
                         #   inlines de Anexo e CarrosselImagem
  admin_views.py         # organizar_view (/admin/organizar/) e adicionar_arquivos_view
  forms.py               # ConteudoAdminForm, BannerAdminForm, CategoriaAdminForm, ConfiguracaoSiteAdminForm
  widgets.py             # CategoriaPicker (3 níveis), IconPicker, RichTextWidget
  busca_utils.py         # Busca sem acento (filtrar_por_texto, BuscaSemAcentoMixin)
  context_processors.py  # site_config (config + menu_categorias, filtrado por mostrar_menu_superior)
  migrations/            # 0001 inicial → 0014 (icone_imagem em Categoria)
  management/commands/   # ver seção "Management commands"
painel/                  # App do Painel Central Administrativo (2026-07-10)
  models.py              # Vinculo (publicação multi-destino), EstiloBotao (aparência por botão)
  views.py               # painel_central_view (árvore + publicar + criar/excluir botão),
                         #   conteudos_view (listagem geral com ações em lote)
  urls.py                # namespace 'painel'
templates/
  base.html              # Layout base (header, nav com menu ⋯, footer, ícone de admin)
                         #   — carrega CSS/JS com ?v=AAAAMMDD-N (cache-busting)
  home.html              # Home: hero/banners, texto editável, recentes + navegue por área,
                         #   cartazes laterais + carrosséis, botão/painel "Eventos" mobile
  carrossel_widget.html  # Widget do carrossel (visual padrão OU iframe com código do admin)
  categoria.html         # Conteúdos com filtros, banners de categoria, índice geral, anexos
  conteudo_detalhe.html  # Detalhe + comentários moderados
  busca.html             # Resultados de busca
  admin/
    index.html           # Dashboard do admin com botões: Organizador, Painel de Arquivos,
                         #   Painel Administrativo Completo (banner roxo)
    organizar.html       # Organizador de Conteúdo
    adicionar_arquivos.html  # Painel Adicionar Arquivos (3 passos)
    painel_central.html  # Tela 1 do Painel Central (árvore + composição/publicação)
    painel_arvore_no.html    # Nó recursivo da árvore (include)
    painel_conteudos.html    # Tela 2 (Conteúdo para modificar ou configurar)
static/
  css/style.css          # Design system completo (blocos datados no final: "AJUSTES 2026-07-10",
                         #   "AJUSTES 2026-07-11")
  css/admin_picker.css   # Estilos dos widgets visuais do admin
  js/main.js             # Slider do hero, menu ⋯ da barra superior, autoplay do carrossel
  img/                   # brasao-es.png (brasão ES usado no header), logogov.png (original
                         #   com texto — não usado mais no header), gerenciaok.png (GECEB),
                         #   hero-ilustracao.png
staticfiles/             # Gerado por collectstatic — NÃO editar, não versionado
media/                   # Uploads (banners/, destaques/, cartazes/, carrossel/, anexos/)
                         #   ⚠️ media/ É versionado no Git (51+ arquivos) — os uploads viajam
                         #   entre computadores pelo GitHub. Só db.sqlite3 fica de fora.
db.sqlite3               # Banco populado (231+ conteúdos) — NÃO versionado no Git
INICIAR SITE.bat         # Atalho do Dan para subir o servidor local
ngrok.exe / ngrok_compartilhar.py  # Compartilhar demonstração local via ngrok
Especificacao_Painel_Admin_Site_Curriculos.md  # Especificação oficial do Painel Central
MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md       # Estratégia da migração final para a SEDU
EXEMPLOS_HTACCESS.md / TESTE_MANUAL_URLS.md    # Apoio à migração final
```

## Modelos — app `conteudo`

### Categoria (= "botão" do site)
- `nome`, `slug`, `descricao` (HTML do texto introdutório), `icone` (classe Font Awesome), `imagem` ("Imagem de capa" — hoje sem uso nos templates, reservada para o futuro), `ordem`, `ativa`
- **`icone_imagem`** (FileField, `icones_categoria/`, opcional, migração 0014) — ícone do BOTÃO enviado como imagem (qualquer formato, inclusive .ico); tem prioridade sobre `icone`/`icone_display`. Renderizado como `<img class="icone-personalizado">` com a classe `sem-fundo` no container (`category-icon`/`topic-icon`, e `chip-icone-personalizado` no `subcategory-chip`) — a imagem se ajusta ao espaço do ícone via `object-fit: contain` sem cortar, tanto no botão principal (home) quanto em subbotões (índice geral e página de categoria). Editável no admin de Categoria ("Aparência") e em lote no Painel Central (seção "Aparência dos botões marcados" → "Ícone do(s) botão(ões) marcado(s)")
- `categoria_pai` (FK self, CASCADE) — hierarquia SEM limite de níveis (adjacency list); o site exibe bem até 3 níveis
- **`mostrar_menu_superior`** (bool, default True, migração 0012) — se False, o botão some da barra azul do topo E da lista "Navegação" do rodapé (o `context_processors.site_config` filtra `menu_categorias` por esse campo). Vale para botões do nível principal
- **`mostrar_navegue_area`** (bool, default True, migração 0012) — se False, o botão some da seção "Navegue por área" da home (filtro na view `home`). Vale para botões do nível principal
- Ambos editáveis no admin de Categoria (seção "📍 Onde este botão aparece") e em lote no Painel Central
- Propriedade `icone_display` — ícone cadastrado ou escolhido automaticamente pelo nome (usada apenas quando `icone_imagem` está vazio)
- No admin: `icone` usa IconPicker; `slug` tem `autocomplete="off"` (o navegador às vezes sugere lixo do histórico — não é bug do site)

### Conteudo
- Tipos: `documento`, `video`, `post`, `link`, `pagina` | Status: `rascunho`, `publicado`, `arquivado`
- Campos: `titulo`, `slug`, `resumo`, `corpo` (HTML), `arquivo`, `url_video`, `url_externa`, `imagem_destaque`, `autor`
- `categoria` (FK, **SET_NULL**) — vínculo primário; o Painel Central soma outros locais via `Vinculo`
- `icone_manual` (IconPicker no admin) — sobrepõe o `icone_criativo` automático por palavra-chave
- `icone_imagem` (FileField, `icones/`, opcional, migração 0013) — ícone personalizado enviado como imagem (qualquer formato, inclusive .ico); tem prioridade sobre `icone_manual`/`icone_criativo`. Nos templates, renderizado como `<img class="icone-personalizado">` dentro do container do ícone (`card-image-placeholder`/`list-icon`/`sidebar-item`), com a classe `sem-fundo` no container para remover o gradiente de fundo por trás (não prejudica a estética de imagens com fundo transparente)
- `destaque` (bool) — seção Destaques da home | `recente` (bool) — seção "Conteúdos recentes" (curada)
- `ordem` (int) — ordenação manual; nas listagens de categoria, `ordem=0` = sem posição (vai pro fim)
- **Agendamento**: status Publicado + `data_publicacao` futura = invisível até a data (`ConteudoQuerySet.publicados()`)
- Propriedades: `tipo_icone`, `icone_criativo`, `extensao_arquivo`, `get_video_embed_url()`
- No admin, a categoria é escolhida via botões visuais (CategoriaPicker)

### Anexo
Arquivos múltiplos anexados a **Conteudo OU Categoria** (FKs duais mutuamente exclusivos, ambas nullable).
- `arquivo` (upload_to `anexos/%Y/%m/`), `nome` (opcional), `ordem`
- Propriedades: `extensao`, `nome_exibicao`
- Inlines no admin de Conteudo e de Categoria (3 linhas extras)
- No site: seção "Arquivos para download" na página da categoria — cards verticais com ícone colorido por tipo (PDF vermelho, Word azul, Excel verde, PPT laranja, vídeo roxo, imagem ciano)

### Banner
Banners rotativos do hero — na home (`categoria=None`) ou dentro de uma categoria.
- `titulo`, `subtitulo`, `imagem` (**opcional desde a 0012**), **`url_imagem`** (URL externa; tem prioridade sobre o arquivo), `link`, `tamanho` (pequeno 260px / médio 400px / grande 520px de altura), `ordem`, `ativo`, `categoria`
- Property **`imagem_src`** — devolve `url_imagem` ou `imagem.url`; os templates SEMPRE usam `imagem_src`
- A imagem nunca é cortada/distorcida: fundo borrado (letterbox) + `object-fit: contain`
- Área de exibição escolhida via CategoriaPicker com opção "Página inicial"

### Cartaz
Cartazes de eventos nas laterais da home.
- `titulo`, `imagem` (**opcional**), **`url_imagem`** (prioridade sobre arquivo), `link`, `lado` (esquerdo/direito), `tamanho` (pequeno 90px / médio 140px / grande 200px), `ordem`, `ativo` + property `imagem_src`
- **Desktop (>1400px)**: colunas laterais dentro da área branca (`.home-conteudo`), presas por `position: sticky` — nunca invadem banner nem rodapé
- **Faixa 1001–1400px (notebook / zoom 110%)**: o conteúdo central encolhe (`max-width: calc(100vw - 240px)`) e os cartazes ficam com 96px, mas **SEMPRE visíveis** (correção de 2026-07-11 — antes sumiam com zoom)
- **≤1000px**: colunas somem e entra o botão flutuante "Eventos" (painel deslizante com grade)

### Carrossel + CarrosselImagem (novos em 2026-07-11, migração 0012)
Carrossel de imagens com passagem automática, exibido **junto com os cartazes** na home (mesmas regras de sticky/área branca).
- `Carrossel`: `titulo`, `ativo` ("Ativar carrossel" — desmarcado = não aparece), `lado` (esquerdo/direito), `largura`/`altura` (px, configuráveis), `intervalo` (segundos entre imagens), `ordem`, `codigo_html`
- `CarrosselImagem` (inline no admin, **5 linhas prontas** + link "Adicionar outra"): `imagem` (arquivo) OU `url_imagem` (prioridade), `link` opcional por imagem, `ordem` + property `imagem_src`
- **Visual padrão** (`templates/carrossel_widget.html` + CSS `.carrossel-*` + JS em `main.js`): vertical com scroll-snap, indicadores laterais rosa/azul, setas de navegação, autoplay — inspirado no mockup Tailwind que o Dan enviou
- **`codigo_html` (avançado)**: se preenchido, o site renderiza esse HTML completo dentro de um **`<iframe srcdoc>` isolado** (Tailwind CDN etc. não afetam o CSS do site). O marcador **`<!--IMAGENS-->`** (ou `{{IMAGENS}}`) é substituído pelas imagens cadastradas (função `_montar_carrossel_html` em `conteudo/views.py`). Trocar o código + salvar = trocar a aparência
- As imagens dos carrosséis também entram no painel "Eventos" do celular

### ConfiguracaoSite
Singleton (pk=1). `nome_site`, `descricao`, `home_titulo`, `home_texto` (RichTextWidget — negrito/itálico/alinhamento/lista via `contenteditable`, salva HTML), `email_contato`, `telefone`, `endereco`, `logo`, `favicon`.

### Comentario
Comentários com moderação (substitui o Disqus). `conteudo` (FK), `nome`, `email`, `texto`, `aprovado` (default False), `data_criacao`. Só aparecem no site após aprovação no admin; ações em lote: aprovar, reprovar/ocultar, excluir.

## Modelos — app `painel`

- **`Vinculo(conteudo, categoria, ordem, pulsante)`** — publica o MESMO conteúdo em vários locais sem duplicar. `Conteudo.categoria` continua sendo o vínculo primário; vínculos SOMAM locais. `categoria_detalhe` une os dois: `Q(categoria__in=...) | Q(vinculos__categoria__in=...)` + `distinct()`. `unique_together (conteudo, categoria)`
- **`EstiloBotao(categoria OneToOne)`** — aparência opcional do botão: `cor_fundo`, `cor_texto`, `fonte`, `tamanho_fonte`, `alinhamento`, `tamanho` (pequeno/médio/grande, migração `painel.0002`), `pulsante`. Property `css_inline` aplicada nos templates (chips de subcategoria, topic-grid, cards da home). Property `classe_tamanho` (`botao-tam-pequeno`/`botao-tam-grande`/vazio) some no template como classe extra — vale para o botão E os subbotões de dentro dele, nos locais marcados. Sem registro = aparência automática
- Efeito pulsante no site: classe `.btn-pulse` (animação `btnPulse`); vem de `EstiloBotao.pulsante` (botões) ou `Vinculo.pulsante` (cards, via set `pulsantes` no contexto)

## URLs

```
/                                → home
/busca/?q=termo                  → busca textual (ignora acentos/maiúsculas)
/categoria/<slug>/               → categoria (subcategorias, filtros ?tipo=X, banners, anexos)
/conteudo/<slug>/                → detalhe de conteúdo + comentários
/admin/                          → Django Admin (dashboard com botões para os 3 painéis)
/admin/organizar/                → Organizador de Conteúdo (?cat=<id> filtra categoria)
/admin/barra-superior/           → Botões da Barra Superior (marcar/ordem/criar/editar/excluir)
/admin/adicionar-arquivos/       → Painel Adicionar Arquivos (3 passos)
/admin/painel-central/           → Painel Administrativo Completo (Tela 1)
/admin/painel-central/conteudos/ → Conteúdo para modificar ou configurar (Tela 2)
```

## Ferramentas administrativas (4 camadas — todas coexistem)

1. **Django Admin tradicional** (`/admin/`) — CRUD completo com widgets visuais (CategoriaPicker, IconPicker), badges, ações em lote, inlines de anexos. Inclui os novos: Carrosséis e campos de visibilidade da Categoria.
2. **Organizador de Conteúdo** (`/admin/organizar/`) — navegar pela hierarquia, criar subcategorias, mover conteúdos entre categorias via busca, reordenar inline. Mostra exatamente o que aparece no site.
3. **Painel Adicionar Arquivos** (`/admin/adicionar-arquivos/`) — subir arquivos em lote: escolher categoria → nomear grupo (cria/reutiliza subcategoria) → subir arquivos com nomes opcionais.
4. **Painel Administrativo Completo** (`/admin/painel-central/`, app `painel`, banner roxo no dashboard):
   - **Tela 1**: árvore completa de botões com checkboxes em cascata + pesquisa (sem acento). Painel direito com seções: Conteúdo (com select **"O que você vai postar?"** — Automático/Documento/Vídeo/Post/Link — `tipo_conteudo` no POST; JS mostra/oculta os campos certos: Vídeo revela "URL do vídeo", oculta Texto/Link; Documento oculta Texto/Link e destaca Anexos; Post/Link mostram Texto e Link, ocultam Anexos), Link/URL (nome amigável), Anexos (linhas dinâmicas), Texto da área, **Ícone** (IconPicker + upload de imagem personalizada `icone_imagem`, qualquer formato incl. .ico, sem fundo), Aparência dos botões (cores, fonte, **tamanho do botão** — pequeno/médio/grande, alinhamento, pulsante), **Página inicial — visibilidade** (selects `vis_menu`/`vis_area`: Não alterar / Sim / Não → gravam `mostrar_menu_superior`/`mostrar_navegue_area` dos botões marcados) e Publicação (status, agendamento, destaque, recentes, pulsante, ordem). Salvar distribui para TODOS os destinos marcados (cria `Vinculo` para cada um). Sem título + com arquivos = anexos de categoria. Se `tipo_conteudo` não for escolhido, o site continua deduzindo o tipo automaticamente pelo que foi preenchido (comportamento antigo preservado).
   - **Criar novo botão**: o select de "pai" lista **todos os níveis** da árvore (`_arvore_flat` com indentação por `nbsp`) — dá para criar botão dentro de qualquer botão.
   - **Excluir botão selecionado** (2026-07-11): botão vermelho abaixo da árvore, ação `excluir_nos`, confirmação dupla no JS. Exclui as categorias marcadas + subbotões (CASCADE). Conteúdos NÃO são excluídos (`Conteudo.categoria` é SET_NULL) — ficam recuperáveis na Tela 2.
   - **Tela 2**: todos os conteúdos com busca, paginação (60/pág), seleção múltipla; ações: Salvar (destaque/recentes/ordem em lote), Remover dos botões (desfaz vínculos + `categoria=None`), Excluir permanentemente (confirmação dupla).
   - Correção de layout (2026-07-11): selects com altura fixa 36px (texto não corta mais — era o bug do campo "Fonte"), `min-width: 0` nos filhos de `.pc-grid2/.pc-grid3`, grades viram 1 coluna abaixo de 980px.

5. **Botões da Barra Superior** (`/admin/barra-superior/`, cartão ciano no dashboard) — tela simples para marcar quais botões principais aparecem na barra azul do topo (grava `mostrar_menu_superior` — vale também para o rodapé), mudar a ordem e criar/editar/excluir botões. Pedido do Dan de 2026-07-11: a barra exibe fixos Documentos Curriculares, Programas, Projetos Integradores, Olimpíadas e Institucional.

## Comportamentos importantes do front-end

- **Barra superior com menu "3 pontinhos" (⋯)**: quando os botões de categoria não cabem na barra azul, os excedentes vão automaticamente para um dropdown ⋯ (elementos `#navMore`/`#navMoreMenu` em `base.html`, lógica em `main.js` — recalcula no `resize`, que também dispara com zoom do navegador; folga de 6px contra arredondamento). No celular (≤768px) vale o hamburger e o ⋯ é desativado.
- **"Navegue por área" E "Conteúdos recentes" com botões quadrados** (2026-07-11): ambos em grid de 3 colunas (2 em ≤480px), ícone em cima + texto embaixo (13px). Nos quadrados de áreas a descrição pequena é ocultada; nos de recentes aparecem categoria/data pequenas (10px) e o título é limitado a 3 linhas (`-webkit-line-clamp`). O botão **"Currículo Atual" é uma pílula compacta CENTRALIZADA ACIMA das duas colunas** (div `.curriculo-atual-topo`, antes do `.home-split`). Ele é **hardcoded** no `home.html` (slug `curriculo-atual`), não vem do loop de categorias.
- **Cartazes/carrosséis nunca somem com zoom**: ver tabela de breakpoints na seção do modelo Cartaz. Botão "Eventos" agora entra em ≤1000px (mesma faixa em que as laterais somem — sem "faixa morta").
- **Cache-busting**: `base.html` carrega `style.css` e `main.js` com `?v=AAAAMMDD-N` (hoje `20260711-1`). **Sempre incrementar ao mudar CSS/JS**, senão o navegador usa a versão cacheada. Ao testar: Ctrl+Shift+R.
- **Logo pulsante** nas páginas internas (bloco `{% block logo_class %}logo-pulse{% endblock %}` em categoria/conteúdo/busca) — na home fica normal.
- **Botão "Voltar página inicial" no rodapé** (2026-07-11): pílula discreta logo ACIMA da barra do cadeado/copyright, colada na margem direita do conteúdo (wrapper `.footer-voltar-wrap` flex justify-end em `base.html`). Pulsa com brilho BRANCO (`voltarPulse` — o pulso azul padrão sumiria no rodapé azul) APENAS fora da home, via `{% if request.path != '/' %}` (o context processor `django.template.context_processors.request` está ativo).
- **VLibras** (2026-07-11): widget oficial gov.br de tradução para Libras em `base.html` (markup `div vw` + script `vlibras-plugin.js` antes do main.js — código de vlibras.gov.br/doc/widget). Botão de acesso estilizado discreto em `style.css` (`div[vw-access-button]`: scale 0.72 + opacity 0.75, canto direito). O site antigo também usava VLibras (tinha `dns-prefetch` para vlibras.gov.br). Requer internet para carregar o script externo.
- **Home**: colunas "Conteúdos recentes" e "Navegue por área" do mesmo tamanho, ambas com scrollbar interna azul quando crescem.

## Categorias atuais (10 principais + subcategorias)

1. **Documentos Curriculares** (fas fa-book) — página-índice geral (55 botões de todas as subcategorias, ordem alfabética; `SLUG_INDICE_GERAL = 'documentos-curriculares'` na view). Subcategorias próprias: Currículo Atual (com 5 sub-botões por etapa: Educação Infantil, EF Anos Iniciais, EF Anos Finais, Ensino Médio, Material de Apoio), Orientações Curriculares, Cadernos Metodológicos, Mapas de Progressão, Ementas Curriculares, Rotinas de Recomposição, Espaços Potencialmente Educativos
2. **Orientações Curriculares** (fas fa-compass) — 129 documentos, 16 subcategorias
3. **Itinerários Formativos de Aprofundamento (IFA)** (fas fa-route) — 10 subcategorias, 14+ documentos
4. **Projetos Integradores** (fas fa-diagram-project) — 5 subcategorias
5. **Rotinas Pedagógicas Escolares (RPE)** (fas fa-calendar-check) — 8 subcategorias, 42 apostilas
6. **Programas** (fas fa-project-diagram) — Educar para a Paz, Mais Leitores, Educação Ambiental, Sucesso Escolar
7. **Livro Didático** (fas fa-book-reader)
8. **Modalidades e Diversidade** (fas fa-users) — EJA, Campo, Quilombola, Indígena, Étnico-Raciais, Socioeducação
9. **Olimpíadas** (fas fa-trophy) — 9 subcategorias com links "Saiba mais" oficiais
10. **Institucional** (fas fa-landmark)

Obs.: o Dan cria/exclui botões de teste pelo Painel Central, então a lista real no banco pode ter itens extras temporários (ex.: "teste", "uso").

## Design system (CSS)

Variáveis principais em `style.css`: `--primary: #2d5a8e`, `--primary-dark`, `--accent: #e8593c`, `--bg`, `--bg-alt`, `--surface`, `--text`, fonte Inter.
Componentes: `.content-card`, `.category-card`, `.area-card` (+ `.area-card-featured`), `.topic-grid/.topic-btn`, `.content-list .list-item`, `.filter-chip`, `.subcategory-chip`, `.page-intro-body`, `.anexos-section`, `.cartaz-item`, `.carrossel-widget`, `.btn-pulse`, `.nav-more/.nav-more-menu`.
Breakpoints: 1400px (faixa dos cartazes/ícones do nav), 1024px, 1000px (cartazes→botão Eventos), 980px (grades do Painel Central), 900px, 768px (mobile/hamburger), 480px, 400px.
**Convenção**: ajustes novos entram em blocos datados no FINAL do `style.css` ("AJUSTES 2026-07-10", "AJUSTES 2026-07-11") — cuidado com a ordem de cascata ao sobrescrever regras antigas.

## Decisões de design já tomadas

1. Header sem filtros CSS nos logos (cores originais, `brasao-es.png` + `gerenciaok.png`, ambos 50px)
2. Textos introdutórios entre os filtros e o grid de conteúdo
3. Cards da home com `|striptags|truncatewords` para descrições limpas
4. Conteúdo migrado via web scraping do WordPress (links para PDFs/Google Drive — arquivos NÃO são locais)
5. 16 categorias com textos introdutórios HTML (`popular_descricoes.py`)
6. Anexos em lista vertical (3-5 itens por categoria, mais legível que grid)
7. FK dual mutuamente exclusiva no Anexo (conteudo OU categoria)
8. Painéis administrativos como views customizadas DENTRO do admin (permissões/autenticação nativas)
9. CategoriaPicker com 3 níveis (netos) em subgrupos visuais
10. Logo pulsante só fora da home
11. Ícones nos títulos das seções da home (varinha mágica + bússola)
12. "Currículo Atual" destacado, centralizado — desde 2026-07-11 como pílula compacta
13. Vínculo primário (`Conteudo.categoria`) + vínculos extras (`painel.Vinculo`) para publicação multi-destino sem duplicar
14. Carrossel personalizado renderizado em `<iframe srcdoc>` isolado (código externo não quebra o CSS do site)
15. Excluir botão nunca exclui conteúdo (SET_NULL) — recuperável na Tela 2 do Painel Central

## Histórico de implementação (cronológico)

### Base do projeto (junho/2026)
Estrutura Django completa; migração de 102 conteúdos + textos introdutórios do WordPress; admin com widgets visuais; comentários com moderação; banners por área; agendamento de publicação; cartazes laterais; responsividade completa; busca sem acento; deploy de teste no PythonAnywhere.

### 2026-07-06 — Migração de páginas WordPress
41 itens "link" convertidos em páginas nativas (`tipo='pagina'`). 3 não migráveis (conteúdo sumiu do site antigo): pk 58 GEEPEI, pk 20/21 Orientações 2024/2023 — depois **arquivados** pelo comando `resolver_pendencias` (2026-07-10).

### 2026-07-07 — Correções de deploy PythonAnywhere
`staticfiles/` removido do Git (+ `.gitignore`); fluxo com `git reset --hard origin/main`; cache-busting `?v=` no CSS; corrigido mapeamento errado de Static files na aba Web (ver seção Deploy).

### Conteúdo migrado por comandos (julho/2026)
Orientações Curriculares (129 docs), IFA (10 subcats), Currículo Atual dividido por etapas + Material de Apoio, Projetos Integradores, RPE (42 apostilas), Olimpíadas (9 oficiais), curadoria de "Conteúdos recentes" (`recente=True` + `curar_recentes`), Antigos IFA movidos para subcategoria de Currículo Atual.

### 2026-07-10 — Painel Central Administrativo (app `painel`) + decisões
- Implementadas as Partes 1–5 da Especificação (Vinculo, EstiloBotao, Telas 1 e 2, efeito pulsante) — NADA do admin antigo foi alterado.
- **Decisão: PythonAnywhere abandonado**; destino final é o servidor da SEDU; demonstração via ngrok (`ALLOWED_HOSTS=['*']` temporário no settings — restringir no deploy SEDU).
- Ajustes visuais: colunas da home do mesmo tamanho, "Currículo Atual" sticky, cartazes com largura responsiva.

### 2026-07-11 — Pedidos do Dan (última leva)
1. **Botões da home menores**: "Navegue por área" com botões QUADRADOS em 3 colunas (ícone em cima, texto 13px — letra maior que antes); "Currículo Atual" virou pílula compacta. Depois, no mesmo dia: "Conteúdos recentes" ganhou o MESMO formato quadrado (títulos limitados a 3 linhas) e o "Currículo Atual" foi movido para o centro, ACIMA das duas colunas (`.curriculo-atual-topo`). CSS no bloco "AJUSTES 2026-07-11".
2. **Cartazes não somem mais com zoom**: limite caiu de 1400px→1000px; na faixa 1001–1400px o conteúdo encolhe e os cartazes ficam de 96px mas visíveis; botão "Eventos" agora em ≤1000px (eliminada a faixa morta 900–1000px).
3. **Menu ⋯ na barra superior**: excedentes da nav vão para dropdown; recalcula em resize/zoom; hamburger intacto no mobile.
4. **Visibilidade por botão** (migração 0012): `Categoria.mostrar_menu_superior` e `Categoria.mostrar_navegue_area` — admin de Categoria + Painel Central (selects `vis_menu`/`vis_area` em lote).
5. **Painel Central**: excluir botões marcados (ação `excluir_nos`, dupla confirmação); criar botão dentro de qualquer nível (`_arvore_flat`); correção dos campos/selects cortados (altura 36px, min-width 0, grades responsivas).
6. **Carrossel** (`Carrossel` + `CarrosselImagem`): junto aos cartazes, autoplay, tamanho configurável, 5 linhas de imagem (arquivo ou URL), `codigo_html` avançado com marcador `<!--IMAGENS-->` renderizado em iframe isolado.
7. **Imagem por URL** em Banner e Cartaz (`url_imagem` + property `imagem_src`; campos `imagem` viraram opcionais).
8. **Ícone personalizado em Conteudo** (`icone_imagem`, migração `conteudo.0013`): upload de imagem (qualquer formato, inclusive .ico) para usar no lugar do ícone Font Awesome. Editável no admin de Conteudo ("🎨 Ícone do card") e no Painel Central (seção "Ícone do card"). Tem prioridade sobre `icone_manual`/automático nos 5 pontos onde `icone_criativo` aparece (home destaques/recentes, categoria content-grid, busca, sidebar de relacionados).
9. **Cards de conteúdo mais compactos**: `.content-grid`/`.content-card` (categoria e home) reduzidos — colunas de 280px→180px, placeholder de ícone 110px→64/100px, padding do corpo 20px→12px, título 16px→13,5px (2 linhas), mesmo espírito visual dos quadrados de "Navegue por área"/"Conteúdos recentes".
10. **Tamanho dos botões no Painel Central** (`EstiloBotao.tamanho`, migração `painel.0002`): select Pequeno/Médio/Grande na seção "Aparência dos botões marcados", aplica classes `botao-tam-pequeno`/`botao-tam-grande` em `area-card` (home), `topic-btn` (índice geral) e `subcategory-chip` (subcategorias) — vale para o botão e os subbotões de dentro dele, nos locais marcados.
11. **Brasão do ES no header refeito** (`static/img/brasao-es.png`): o antigo `logogov.png` tinha o brasão + o texto "GOVERNO DO ESTADO DO ESPÍRITO SANTO" embaixo — espremido em 50px de altura, o brasão ficava minúsculo e desfocado. Foi gerado (via Pillow) um recorte só do brasão, com realce de saturação/contraste (+18%/+6%), 323×340px nativos (nítido em telas retina). Agora exibe 48×50px — mesmo tamanho do logo GECEB (49×50px). O `logogov.png` original foi mantido na pasta como referência, mas não é mais usado.
12. **Ícone personalizado nos BOTÕES de categoria** (`Categoria.icone_imagem`, migração `conteudo.0014`): mesmo recurso do item 8, mas para o botão/subbotão em si (não o conteúdo dentro dele) — corrige o problema relatado pelo Dan de o ícone automático (pasta genérica) aparecer "cortado"/sem graça quando ele queria uma imagem própria. Editável no admin de Categoria (seção "Aparência", ao lado do IconPicker) e em lote no Painel Central. ⚠️ Detalhe técnico: como o mesmo arquivo enviado é reaproveitado para vários destinos na view `_publicar`, é preciso `.seek(0)` antes de cada `.save()` — senão os destinos além do primeiro gravam arquivo vazio (o cursor de leitura já estava no fim). **Obs.: o campo separado `botao_icone_imagem` deste item foi depois UNIFICADO com o campo `icone_imagem` — ver item 14.**
13. **Correção do ajuste de imagem nos botões de categoria** (mesmo dia, depois do item 12): `.category-icon`/`.topic-icon` são CÍRCULOS (`border-radius:50%`), mas a imagem enviada por Dan tinha fundo branco sólido (não transparente) — com `object-fit:contain` a imagem ficava pequena "boiando" dentro do círculo sem preenchê-lo (o fundo branco se perdia no cartão branco, dando impressão de ícone minúsculo/deslocado). Corrigido para `object-fit:cover` + `overflow:hidden` no container em `category-icon`/`topic-icon` (a imagem preenche 100% do círculo, cortada nas bordas para caber — como foto de perfil) e `.chip-icone-personalizado` (subcategory-chip) aumentado de 16px→22px com `border-radius:50%` + `cover`. ⚠️ Importante: isso é DIFERENTE do ícone de CONTEUDO (item 8), que continua em `object-fit:contain` (sem cortar) porque ali o uso esperado é ícone transparente tipo glifo, não foto/ilustração cheia — não confundir os dois contextos ao mexer em `.icone-personalizado` no CSS (a classe é compartilhada, mas os seletores `.category-icon .icone-personalizado`/`.topic-icon .icone-personalizado` sobrescrevem para cover apenas nesse contexto).
14. **Unificação do campo de ícone no Painel Central + correção do card de conteúdo cortado** (mesmo dia, depois do item 13 — 3 problemas relatados pelo Dan de uma vez):
    - **(a) Card de conteúdo cortava a imagem**: o ícone personalizado do CARD DE CONTEÚDO estava saindo com `object-fit:cover` (cortado) em vez de `contain`, porque a regra `.card-image img { object-fit: cover }` (usada nas imagens de destaque, linha ~498) vencia a genérica `.icone-personalizado { contain }` por especificidade (0,0,1,1 > 0,0,1,0). Corrigido com `.card-image .icone-personalizado { object-fit: contain; padding: 10px }` (0,0,2,0, vence). Agora o card de conteúdo mostra a imagem INTEIRA (contain), enquanto o BOTÃO de categoria continua preenchendo o círculo (cover, item 13) — dois comportamentos propositais.
    - **(b) e (c) Dois campos de ícone confusos + "Nada para publicar"**: havia DOIS uploads de imagem no painel (`icone_imagem` na seção "Ícone do card" = ícone do CONTEÚDO, só usado com título; e `botao_icone_imagem` na seção "Aparência" = ícone do BOTÃO). O Dan subia a imagem no campo errado e (1) ela não aparecia, ou (2) recebia "Nada para publicar" porque `icone_imagem` sem título era ignorado. **Unificado em UM só campo** ("🎨 Ícone (opcional)", nome `icone_imagem`): se há **título**, vira o ícone do **conteúdo** criado; se **não** há título (só botões marcados), vira o ícone dos **botões marcados** (a view seta `conteudo_criado` e, no bloco 4b, aplica `icone_imagem` — ou o FA do IconPicker via `icone` — aos destinos quando nenhum conteúdo foi criado). O campo `botao_icone_imagem` foi REMOVIDO do template (a view ainda o aceita como fallback de compatibilidade). Com isso, **salvar só o ícone (ou só cor/tamanho, só visibilidade, só texto) é sempre permitido** — a mensagem de aviso só aparece em submissão 100% vazia. Caixa azul de ajuda "Como funciona" explica a regra no painel.
15. **Rodapé: "Voltar página inicial" + VLibras** (fim do dia): pílula discreta de volta à home no fim da coluna Navegação do footer, pulsante (brilho branco) só fora da home; e o widget oficial VLibras (gov.br) com botão de acesso reduzido/semitransparente no canto direito. Detalhes na seção "Comportamentos importantes do front-end".
16. **Parte 2 do dia (após os créditos voltarem)** — plano do PPTX "acertar a home page espaco" + pedidos por texto:
    - **Home mais compacta**: hero/banner reduzido (médio 400→240px, pequeno 260→170, grande 520→340, ilustração padrão 340→210, mobile 150) — imagem continua inteira (`contain`); o bloco "Currículo do Espírito Santo" (home-intro) fica em fluxo e acompanha qualquer altura; colunas Recentes/Navegue ganharam scroll até 560px (era 420). Bloco CSS "AJUSTES 2026-07-11 (parte 2)".
    - **Carrossel coluna cheia (regra POR LADO)**: sem cartaz ativo NAQUELE lado (esquerdo/direito, avaliado separadamente), o template põe `col-cheia` na coluna → o carrossel estica para `calc(100vh - 104px)` com `height:100% !important` (vence o tamanho do admin), preso (sticky) como os cartazes. Com cartaz no mesmo lado, dividem o espaço como antes. (A 1ª versão exigia zero cartazes nos DOIS lados — o Dan corrigiu: a regra é por lado.)
    - **Carrossel fantasma corrigido**: carrossel ativo mas SEM imagens válidas (e sem código HTML) não renderiza mais — era a impressão de "Ativar carrossel não funciona" (a moldura vazia aparecia).
    - **Seletor "Categoria pai" hierárquico** no Django Admin (foto do Dan mostrava lista aleatória "Pai → Filho"): `CategoriaAdminForm.__init__` injeta choices em árvore ordenada com recuo/└ (mesmo estilo do Painel Central), excluindo a própria categoria; desembrulha o `RelatedFieldWidgetWrapper`.
    - **Barra superior**: 5 botões FIXOS definidos pelo Dan (Documentos Curriculares, Programas, Projetos Integradores, Olimpíadas, Institucional — via `mostrar_menu_superior`, que continua valendo tb p/ rodapé); estilo discreto (branco, sem negrito, CENTRALIZADOS na barra, 12px, pílula translúcida `rgba(255,255,255,.13)`; barra do topo abaixada de 72px→58px); **ícone de localização** (`.nav-localizacao`, fa-location-dot) à direita da busca abrindo o endereço da ConfiguracaoSite no Google Maps (`maps/search/?api=1&query=`); **novo painel admin** `/admin/barra-superior/` (view `barra_superior_view` em admin_views.py, template `admin/barra_superior.html`, cartão ciano no dashboard) — checkbox "na barra?", ordem, atalhos criar/editar/excluir.
    - **Busca acha tudo**: a view `busca` agora também procura em `Categoria` (nome + descrição, sem acento) e mostra a seção "Botões e áreas do site" (chips) acima dos conteúdos; "nenhum resultado" só aparece se AMBAS as listas vierem vazias.
- Versão de cache do CSS evoluiu ao longo do dia: `?v=20260711-1` → `-2` (pílula do Currículo Atual + recentes quadrados) → `-3` (ícone personalizado em Conteudo, cards compactos, tamanho de botão) → `-4` (ícone personalizado em Categoria/botões) → `-5` (correção do ajuste de imagem — cover nos botões) → `-6` (card de conteúdo volta a contain) → `-7` (botão voltar no rodapé + VLibras). JS ficou em `?v=20260711-1`.
- Testado: páginas 200, ações do painel via test client, submissão completa do Painel Central, ícone-só sem título aplicado a pai+sub (212 bytes cada, sem truncamento), ícone com título indo para o conteúdo e NÃO para o botão, card de conteúdo com `object-fit:contain` confirmado via computed style, campo `botao_icone_imagem` confirmado removido do HTML.

## Deploy

### Situação atual
> **O PythonAnywhere NÃO é mais usado (decisão de 2026-07-10).** Destino final: servidor da SEDU em
> `https://curriculo.sedu.es.gov.br/curriculo/` (ver `MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md`).
> Demonstrações: locais, via ngrok. `ALLOWED_HOSTS = ['*']` é temporário — restringir no deploy SEDU.

### Migração WordPress → Django (produção SEDU)
Os ~1000 arquivos migrados têm links para `/curriculo/wp-content/uploads/...`. Estratégia: manter o WordPress em um subdomínio (`wordpress.curriculo.sedu.es.gov.br`) e reescrever `/wp-content/` via `.htaccess` do Apache — sem duplicar arquivos nem alterar o banco. Documentos: `MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md` (estratégia), `EXEMPLOS_HTACCESS.md` (códigos prontos), `TESTE_MANUAL_URLS.md` (validação com curl).

### Referência histórica — PythonAnywhere (https://rabalista.pythonanywhere.com, usuário `rabalista`)
- Projeto em `/home/rabalista/site-curriculos-sedu/`; WSGI em `/var/www/rabalista_pythonanywhere_com_wsgi.py` (força ALLOWED_HOSTS/DEBUG — remover se o settings for restringido)
- Aba Web → Static files: `/static/` → `/home/rabalista/site-curriculos-sedu/staticfiles` e `/media/` → `.../media` (⚠️ armadilha resolvida em 2026-07-07: o Directory apontava para pasta antiga solta e o site parecia "nunca atualizar"; diagnóstico rápido: `curl -s .../static/css/style.css | grep -c logoPulse` → 0 = mapeamento errado)
- Fluxo de publicação (script único no Bash de lá):
  ```bash
  cd ~/site-curriculos-sedu && git fetch origin main && git reset --hard origin/main && source venv/bin/activate && python manage.py migrate && python manage.py collectstatic --noinput --clear && echo "==== PRONTO! Va na aba Web e clique em Reload ===="
  ```
  Usa `git reset --hard` (não `git pull`) porque `staticfiles/` saiu do Git e o pull travava com "local changes would be overwritten". `db.sqlite3` é untracked (seguro). ⚠️ Atenção: `media/` HOJE é versionado — um `reset --hard` no servidor sobrescreve uploads feitos direto lá com a versão do GitHub.

### Sincronização do banco entre ambientes
`db.sqlite3` NÃO é versionado — cada ambiente tem o seu. Código sincroniza via GitHub; **dados não**.
- Estratégia manual: backup do `db.sqlite3` local → upload por SFTP/gerenciador de arquivos no servidor → `python manage.py migrate` lá (se houve migração nova) → reload. SEMPRE fazer backup do banco do servidor antes de trocar.
- Verificação: `sqlite3 db.sqlite3 "SELECT COUNT(*) FROM conteudo_conteudo;"` nos dois lados — números iguais = ok.
- Alternativa reprodutível: os management commands recriam categorias/conteúdos migrados em qualquer banco (são idempotentes).

## Como rodar

```bash
cd "C:\ridan\Claude\Projects\Site Curriculos SEDU"
venv\Scripts\activate            # Windows (Mac/Linux: source venv/bin/activate)
python manage.py migrate         # aplica migrações pendentes (ex.: 0012)
python manage.py runserver
```
- Site: http://127.0.0.1:8000/ | Admin: http://127.0.0.1:8000/admin/ (superusers locais: `ridan` e `rabalista`)
- O Dan usa os atalhos `.bat` (2026-07-11 — feitos para ele levar a pasta completa para o computador do trabalho, usuário Windows `rabalista`):
  - **`INICIAR SISTEMA.bat`** (raiz): versão portátil do INICIAR SITE.bat — detecta venv copiado de outra máquina e o recria sozinho (o venv guarda em `pyvenv.cfg` o caminho do Python da máquina onde nasceu), roda `migrate`, garante que o superuser `rabalista` existe (se não existir, cria com senha `sedu2026` — o get_or_create NUNCA mexe no usuário se ele já existe) e sobe o servidor abrindo o navegador.
  - **`BAT SEDU/ATUALIZAR BANCO.bat`**: conserta o venv se preciso → `git pull` (não-fatal sem internet) → `migrate` → `importar_remanescentes` (idempotente). Usar após copiar a pasta ou baixar atualizações.
  - `INICIAR SITE.bat` antigo continua na pasta e funcionando (regra de nunca quebrar o que existe).
  - ⚠️ Os `.bat` precisam ser **ASCII puro**: caracteres UTF-8 multibyte (─, ç, ã) deslocam o parser do cmd.exe e geram comandos-lixo ("'utro' não é reconhecido..."). Já corrigido nos três.
- Para compartilhar demo: ngrok (`ngrok_compartilhar.py`).
- **Ao testar CSS/JS**: incrementar o `?v=` no `base.html` e recarregar com Ctrl+Shift+R.

### Fluxo de trabalho com Git
1. **Dan**: clique 2x no `.bat` "Subir GitHub SEDU" (em `BAT SEDU/`, com atalho no Desktop) — faz `git add -A` + commit + **`git pull --no-rebase`** + push para `origin main`. (Corrigido em 2026-07-11: o caminho antigo `C:\Users\ridan\...` foi trocado por `%~dp0..` — funciona de qualquer pasta — e o pull automático evita o erro "fetch first".)
2. Em outro ambiente: `git pull` + `python manage.py migrate` (+ `collectstatic` se for produção) + reload.
3. O outro `.bat` ("COMPARTILHAR COM GERENTE") abre o ngrok na porta 8000 para demonstrações; o settings tem `CSRF_TRUSTED_ORIGINS` para domínios do ngrok (commit "codigo ngrok" vindo de outra máquina).

## Management commands (todos idempotentes)

```bash
python manage.py popular_categorias              # Categorias e subcategorias base
python manage.py popular_descricoes              # Textos introdutórios (HTML)
python manage.py migrar_conteudo                 # 102 itens do site original
python manage.py migrar_orientacoes              # 129 docs de Orientações Curriculares
python manage.py migrar_ifa                      # IFA (10 subcategorias) — move em vez de duplicar
python manage.py organizar_curriculo_atual       # Sub-botões por etapa em "Currículo Atual"
python manage.py migrar_material_apoio           # "Material de Apoio" em Currículo Atual
python manage.py migrar_documentos_curriculo_atual  # Documentos das etapas do Currículo Atual
python manage.py migrar_antigos_ifa              # Antigos IFA → subcategoria de Currículo Atual (11 docs)
python manage.py migrar_projetos_integradores    # "Projetos Integradores" (5 subcategorias)
python manage.py migrar_rpe                      # RPE (8 subcategorias, 42 apostilas)
python manage.py migrar_olimpiadas               # "Olimpíadas" (9 subcategorias oficiais)
python manage.py curar_recentes                  # Seleção oficial de "Conteúdos recentes" (edite URLS_RECENTES)
python manage.py resolver_pendencias             # Arquivou os 3 itens sem conteúdo no site antigo
```
`migrar_ifa` e `organizar_curriculo_atual` MOVEM documentos existentes em vez de duplicar e usam slugs FIXOS.

## Importação do portal antigo (2026-07-11 — concluída nesta máquina)

Fluxo em 3 comandos (pasta `importacao/` no projeto), criado a partir do plano
"Plano_Importacao_Completa_Portal_Curriculo_SEDU" aprovado pelo Dan:

```bash
python importacao/inventariar_wordpress.py    # FASE 1: baixa via API REST do WP as 188 páginas
                                              #   + 1 post do portal antigo -> inventario_wordpress.json
python manage.py comparar_portais             # FASE 2: cruza inventário × banco -> relatorio_comparacao.md
                                              #   (match por URL, slug, título normalizado e apelidos de hubs)
python manage.py importar_remanescentes       # FASE 4: importa SÓ o que falta (aceita --dry-run)
```

- **O que foi importado** (134 itens, tudo como `tipo='link'` apontando para o portal antigo, que seguirá no ar como subdomínio): 91 itinerários de formação técnica → subcategoria NOVA "Formação Técnica e Profissional" (slug `formacao-tecnica-e-profissional`, dentro de IFA); 21 ementas EM → "Ementas Curriculares"; 16 volumes/visualizadores de PDF do currículo → sub-botões de Currículo Atual por etapa (com antiduplicação pelo link do PDF extraído do iframe); consulta pública IFA, edital rotinas 2025, 2 revistas Diálogos, notícia Árvore de Livros → categorias afins.
- **Garantias**: só `get_or_create` (idempotente — 2ª execução cria 0), nunca altera/exclui nada, log em `importacao/log_importacao_*.txt`, backup do banco antes (`db.sqlite3.backup-AAAAMMDD`, não versionado).
- **Páginas ignoradas de propósito** (`SLUGS_IGNORAR` em `comparar_portais.py`): `sobre` (é a home do site antigo), `politica-de-cookies`, `elementor-24030` (página vazia). Páginas-hub (rpe, olimpiadas, livrodidatico...) casam com botões existentes via `ALIASES_WP_CATEGORIA`.
- ⚠️ **O banco não viaja pelo Git**: na máquina do Dan, rodar os 3 comandos acima após `git pull` (o inventário já está versionado, então dá para pular a Fase 1 se o site antigo não mudou).
- Categoria reserva "Portal Antigo — a classificar" (oculta da home) só é criada se algum item não tiver destino conhecido — nesta execução não foi necessária.

## O que falta / próximos passos possíveis

- [ ] Refinamentos visuais conforme feedback do Dan e aprovação do chefe
- [ ] Migrar para o domínio oficial `curriculo.sedu.es.gov.br` + SSL (seguir o MANUAL)
- [ ] Restringir `ALLOWED_HOSTS` e revisar `DEBUG` no deploy da SEDU
- [ ] Deploy definitivo (avaliar Docker + PostgreSQL — há Dockerfile/docker-compose no repositório)
- [ ] Adicionar imagens de destaque aos demais conteúdos
- [ ] Paginação nas listagens de conteúdo do site público
- [ ] Possível: comando de seed para carrosséis/cartazes (dados não versionados)

## Armadilhas conhecidas (ler antes de "debugar")

1. **CSS/JS não atualiza** → é cache: incrementar `?v=` no `base.html` + Ctrl+Shift+R.
2. **Site em produção não atualiza** → conferir mapeamento de Static files da hospedagem e usar `git reset --hard` (não pull), ver seção Deploy.
3. **Campo "URL amigável" preenchido sozinho no admin** → autofill do navegador, não é bug (`autocomplete="off"` já aplicado).
4. **Dados criados no admin local não aparecem em outro ambiente** → `db.sqlite3` não é versionado; sincronizar banco manualmente ou usar commands.
5. **Regra de cascata do CSS**: os blocos datados no fim do `style.css` sobrescrevem regras anteriores de mesma especificidade — ao mexer em `.area-card`/`.cartazes-*`, verificar o bloco mais recente.
6. **`.claude/worktrees/`**: pode aparecer no `git status` com muitos arquivos deletados de worktrees antigas — ignorar, não é conteúdo do site.
7. **Nunca editar `staticfiles/`** — é gerado.
8. **Painel Central**: os checkboxes da árvore pertencem ao form de publicar (`form="form-publicar"`); o form de excluir copia os ids via JS no submit.
9. **Editei um template mas o site não muda (mesmo sem cache do navegador)** → o Django 5.x usa cache de templates e o servidor de preview roda com `--noreload`: REINICIE o `runserver` após editar arquivos `.html` de `templates/`.
10. **Push rejeitado ("fetch first" / "remote contains work")** → houve commit em outro computador ou pelo site do GitHub. Solução: `git pull --no-rebase origin main`, resolver conflitos se houver, e `git push`. O `.bat` "Subir GitHub SEDU" já faz o pull automaticamente antes do push (corrigido em 2026-07-11).
11. **Comentário de template `{# ... #}` NÃO pode ter quebra de linha** — o Django só suporta `{# #}` em UMA linha; se quebrar, o texto do comentário aparece LITERALMENTE na página (aconteceu em 2026-07-11 com o botão do rodapé e o VLibras — o Dan viu "coisas estranhas escritas" no site). Para comentários longos, usar `{% comment %}...{% endcomment %}`.
12. **Cuidado com o `.gitignore` em outros computadores**: em 2026-07-11 um commit feito em outra máquina ("codigo ngrok") substituiu por acidente o `.gitignore` inteiro pelo do venv (`*` — ignorar tudo). Foi corrigido no merge `2faca8e` mantendo a versão completa. Se o `.gitignore` aparecer com uma linha só (`*`), restaurar do histórico: `git checkout 2faca8e -- .gitignore`.
