# Site Currículos SEDU — Contexto do Projeto (v11 — atualizado em 2026-07-17 — Parte 14)

## O que é este projeto

Site da **Gerência de Currículo da Educação Básica (GECEB)**, da Secretaria de Estado da Educação do Espírito Santo (SEDU). Migração do site WordPress/Elementor em `curriculo.sedu.es.gov.br/curriculo/` para Django moderno.

O dono do projeto (**Dan**) não é programador — ele trabalha na SEDU e precisa de instruções claras, em português, para qualquer operação no terminal. Sempre explique comandos passo a passo e forneça comandos prontos para copiar e colar.

## 🚦 Estado atual (por onde começar uma conversa nova)

- O site está **completo e funcional localmente**, com 122 botões raiz (categorias hierárquicas), 538+ conteúdos migrados do WordPress, e **6 painéis administrativos** (Organizador, Adicionar Arquivos, Painel Central Tela 1, Tela 2, Barra Superior, **Estrutura de Árvores**).
- **Deploy**: o PythonAnywhere foi **abandonado** (decisão de 2026-07-10). O destino final é o servidor da SEDU em `curriculo.sedu.es.gov.br`. Enquanto isso, demonstrações são feitas localmente via ngrok.
- **Leva mais recente (2026-07-17 — "parte 14")**: **Subáreas vs Botões: campo `mostrar_como_card` para controlar duplicação** — (1) novo campo `Categoria.mostrar_como_card` (BooleanField, padrão True) distingue botões/subbotões estruturais (aparecem como chip + card grande) de subáreas rápidas (aparecem só como chip, sem duplicar); (2) função "Criar subárea nos botões marcados" agora cria com `mostrar_como_card=False` automaticamente; (3) "Criar novo botão" cria com `mostrar_como_card=True` (padrão); (4) campo editável no Django Admin de Categoria para ajuste manual. Detalhes no histórico item 28.
- **Leva anterior (2026-07-17 — "parte 13")**: **Currículo Atual virou botão raiz + Checkbox "Central?" para área central** — (1) Currículo Atual agora é uma categoria raiz (antes era filho de "Documentos Curriculares"), aparecendo como raiz em TODAS as árvores (Estrutura de Árvores, Painel Central, Organizador, Barra Superior); (2) novo checkbox "Central?" no painel `/admin/barra-superior/` permite marcar QUALQUER botão raiz para aparecer na "área central" da home, ao lado da pílula "Currículo Atual"; (3) layout da home ajustado com `flex-wrap` para suportar múltiplos botões na central (quebra automaticamente se não couber). Detalhes no histórico item 27.
- **Leva anterior (2026-07-16 — "parte 12")**: **Estrutura de Árvores + Subbotões melhorados** — (1) campo de upload de imagem de ícone adicionado ao modal de criar botão na Estrutura de Árvores (faltava; agora dá pra criar botão com nome + URL + anexos + ícone de imagem de uma vez); (2) subbotões agora aparecem como **cards grandes clicáveis** na página de categoria (borda azul, ícone grande, selo "Botão"), além dos chips no topo. Detalhes no histórico item 26.
- **Leva anterior (2026-07-13 — "parte 11")**: **Correção crítica de duplicação + Modal da Estrutura de Árvores** — conteúdos criados dentro de subbotões **não aparecem mais duplicados** na página do pai (view `categoria_detalhe` agora busca somente conteúdos da própria categoria, não de subcategorias). Modal de exclusão/mover restaura HTML corretamente, evitando corrupção. Formulário de criação com URL + múltiplos anexos funcionando. Lixo de testes (conteúdos "Link: ...") excluído. Detalhes no histórico item 25.
- **Leva anterior (2026-07-13 — "parte 10")**: **Novo módulo "Estrutura de Árvores"** — painel administrativo completo para gerenciar a hierarquia do site. Árvore interativa com 121 nós (profundidade ilimitada), busca instantânea sem acento, expandir/recolher, filtros, drag-and-drop para mover nós, CRUD completo (criar/editar/excluir botões), gerenciamento de conteúdo e anexos, biblioteca de ícones Font Awesome (96 ícones) + upload permanente de ícones personalizados (SVG, PNG, JPG, JPEG, WEBP, ICO), **ZERO alterações a funcionalidades existentes**. Views: `conteudo/arvore_views.py` (views + API AJAX). Template: `templates/admin/estrutura_arvores.html`. URLs: `/admin/estrutura-arvores/` e `/admin/estrutura-arvores/api/`. Dashboard: novo banner âmbar no índice admin. Função adicional: botão de excluir conteúdo (lixeira vermelha) ao lado de editar em cada linha da lista. Detalhes no histórico item 24.
- **Leva anterior (2026-07-13 — "parte 9")**: **ngrok UTF-8 + Video Streaming corrigido** — templates restaurados do commit anterior (último commit 82f5b92 tinha double-encoding UTF-8), vídeo renomeado para ASCII-only, nova view Django `serve_media` com suporte a HTTP Range Requests (206 Partial Content) para streaming via ngrok, scripts de teste e launcher automáticos. Detalhes no histórico item 23.
- **Leva anterior (2026-07-13 — "parte 8")**: **Respostas de visitantes + Votos 👍/👎** — novo modelo `Comentario.parent` (FK self) para threads aninhadas, campos `votos_positivos`/`votos_negativos`, endpoint AJAX `/comentario/<pk>/votar/` para votação sem reload, formulário inline "Responder" que abre/fecha animado, respostas aparecem recuadas com label "↩ resposta", cada resposta passa por moderação igual ao comentário. Migração `conteudo/0020` aplicada. Detalhes no histórico item 22.
- **Leva anterior (2026-07-13 — "parte 7")**: **Sistema de Comentários Moderados** — 3 estados: pendente/publicado/recusado. Campo de resposta do administrador exibido abaixo do comentário no site. Comentários NÃO aparecem em conteúdos tipo "link". Visual moderno com badge de contagem, aviso de moderação, botão gradiente. Admin totalmente reescrito com ações em lote (aprovar/recusar), badges coloridos de status, campos readonly para dados do visitante. Migração `conteudo/0019` aplicada. Detalhes no histórico item 21.
- **Leva anterior (2026-07-12 — "parte 6")**: **Carrossel admin melhorado** — agora exibe o arquivo atual ("Atualmente: carrossel/images.jpg"), checkbox "Limpar" para remover, e opção "Modificar" para trocar. As 3 imagens (1 vídeo MP4 + 2 JPGs) ficam visíveis. **Campo URL no "Editar botão selecionado"** — novo campo opcional que cria automaticamente um Conteúdo tipo "link" quando preenchido. Detalhes no histórico item 20.
- **Leva anterior (2026-07-12 — "parte 5")**: **Editar botão selecionado no Painel Central** — ao marcar 1 botão na árvore, aparece seção verde "Editar botão selecionado" com nome, descrição, ícone (FA + upload de imagem), e upload de anexo. AJAX carrega dados atuais; POST salva e redireciona. **Botões sem pai → "Botões novos criados"** — botões criados sem selecionar pai vão automaticamente para uma categoria raiz oculta. **CategoriaPicker dinâmico** — categorias sem subcategorias (como "Botões novos criados") agora aparecem no Django Admin e no Adicionar Arquivos. **Texto centralizado padrão** em todos os botões (.topic-btn, .card-body, subbotões). **Texto "→ Abrir para ver" removido** dos cards de subbotão. Detalhes no histórico item 19.
- **Leva anterior (2026-07-12 — "parte 4")**: **Rodapé sticky corrigido** — em páginas com pouco conteúdo (busca vazia, categorias vazias), o rodapé agora cola no fundo da viewport em vez de "flutuar" no meio. Implementado com flexbox no body + flex: 1 no main. Histórico completo no bloco "Histórico de implementação" item 18.
- **Leva anterior (2026-07-12 — "parte 3")**: **Busca da árvore do Painel Central corrigida** — sub-sub-botões agora aparecem quando se busca por nome, com ancestrais expandidos automaticamente. **Nova função: "Criar subárea nos botões marcados"** — permite criar subáreas (subbotões) dentro de 1 ou mais botões marcados na árvore do Painel Central, de uma vez. Detalhes no bloco item 17.
- **Leva anterior (2026-07-12 — "parte 2")**: **6 bugs corrigidos** — navegação embolada no mobile, carrossel "Eventos" funcionando como widget, carrossel confinado ao rodapé, comentário Django visível, anexos de conteúdo invisíveis, subbotões só como chips. Detalhes no bloco item 17.
- **Leva anterior (2026-07-11, fim do dia — "parte 2")**: banner/hero da home mais baixo, carrossel ocupa a coluna lateral inteira quando não há cartazes, carrossel vazio (sem imagens) não renderiza mais, seletor "Categoria pai" hierárquico no admin, barra superior com 5 botões fixos discretos + ícone de localização (Google Maps) + painel "Botões da Barra Superior" no admin (/admin/barra-superior/), busca agora encontra também categorias/botões. Detalhes no histórico item 16.
- **Última leva de mudanças (2026-07-11)**: botões da home menores/quadrados, correção dos cartazes que sumiam com zoom, menu "3 pontinhos" (⋯) na barra superior, carrossel de imagens, campos de visibilidade por botão, exclusão de botões pelo Painel Central, imagem por URL em Banner/Cartaz. Detalhes na seção "Histórico de implementação".
- **Importação do conteúdo remanescente CONCLUÍDA (2026-07-11)**: os 134 itens que faltavam do portal antigo foram importados (91 itinerários de formação técnica, 21 ementas EM, 16 volumes do currículo, 6 diversos) — ver seção "Importação do portal antigo". A comparação portal antigo × novo agora dá FALTA: 0. ⚠️ Isso foi feito no banco DESTA máquina; na máquina do Dan é preciso rodar `python manage.py importar_remanescentes` (idempotente) após o `git pull`.
- **Regra de ouro do Painel Central** (`Especificacao_Painel_Admin_Site_Curriculos.md`): sempre ADICIONAR funcionalidades, nunca substituir/quebrar o que já funciona. O Dan reforça isso a cada pedido.
- **Migrações aplicadas**: `conteudo/0012-0025` + `painel/0002`. Migração **`conteudo/0025`** (Categoria: mostrar_como_card) é a mais recente.
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
  media_views.py         # serve_media: view com suporte a HTTP Range Requests (206 Partial Content)
                         #   para streaming de vídeo via ngrok
  arvore_views.py        # estrutura_arvores_view + API AJAX completa para módulo Estrutura de Árvores
  admin.py               # Admin customizado: badges, widgets visuais, moderação,
                         #   inlines de Anexo e CarrosselImagem
  admin_views.py         # organizar_view, adicionar_arquivos_view, barra_superior_view
  forms.py               # ConteudoAdminForm, BannerAdminForm, CategoriaAdminForm, ConfiguracaoSiteAdminForm
  widgets.py             # CategoriaPicker (3 níveis), IconPicker, RichTextWidget
  busca_utils.py         # Busca sem acento (filtrar_por_texto, BuscaSemAcentoMixin)
  context_processors.py  # site_config (config + menu_categorias, filtrado por mostrar_menu_superior)
  migrations/            # 0001 inicial → 0025 (mostrar_como_card em Categoria)
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
    index.html           # Dashboard do admin com 6 banners coloridos: Organizador (azul), 
                         #   Adicionar Arquivos (verde), Painel Central (roxo), Barra Superior (ciano),
                         #   Estrutura de Árvores (âmbar/laranja)
    organizar.html       # Organizador de Conteúdo
    adicionar_arquivos.html  # Painel Adicionar Arquivos (3 passos)
    painel_central.html  # Tela 1 do Painel Central (árvore + composição/publicação)
    painel_arvore_no.html    # Nó recursivo da árvore (include)
    painel_conteudos.html    # Tela 2 (Conteúdo para modificar ou configurar)
    estrutura_arvores.html   # Módulo "Estrutura de Árvores": árvore interativa completa (121 nós),
                         #   pesquisa/filtros, CRUD, drag-and-drop, biblioteca de ícones, conteúdo/anexos
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
- **Estilo do título do card** (`texto_alinhamento`, `texto_fonte`, `texto_tamanho_fonte`, migração `conteudo.0016`, 2026-07-11): personaliza a aparência do `<h3>` do título nos 4 pontos onde ele aparece (home destaques, home recentes, categoria content-grid, busca) — property `texto_estilo_inline` monta o `style=` pronto, mesmo espírito do `EstiloBotao.css_inline` do app `painel` mas vivendo direto no Conteudo (cada conteúdo é único, sem precisar de tabela separada). Editável no admin ("🔤 Texto do card", seção colapsável) e no Painel Central (seção "Texto do card" — só se aplica quando um conteúdo é criado, ou seja, com Título preenchido).
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
- No admin de Cartaz, `lado` e `tamanho` são editáveis DIRETO NA LISTA (list_editable, 2026-07-11) — troca esquerdo/direito sem abrir o cartaz; idem `lado` no admin de Carrossel
- **Desktop (>1400px)**: colunas laterais dentro da área branca (`.home-conteudo`), presas por `position: sticky` — nunca invadem banner nem rodapé
- **Faixa 1001–1400px (notebook / zoom 110%)**: o conteúdo central encolhe (`max-width: calc(100vw - 240px)`) e os cartazes ficam com 96px, mas **SEMPRE visíveis** (correção de 2026-07-11 — antes sumiam com zoom)
- **≤1000px**: colunas somem e entra o botão flutuante "Eventos" (painel deslizante com grade)

### Carrossel + CarrosselImagem (novos em 2026-07-11, migração 0012)
Carrossel de imagens com passagem automática, exibido **junto com os cartazes** na home (mesmas regras de sticky/área branca).
- `Carrossel`: `titulo`, `ativo` ("Ativar carrossel" — desmarcado = não aparece), `lado` (esquerdo/direito), `largura`/`altura` (px, configuráveis), `intervalo` (segundos entre imagens), `ordem`, `codigo_html`
- `CarrosselImagem` (inline no admin, **5 linhas prontas** + link "Adicionar outra"): `imagem` (FileField desde a migração 0015 — aceita IMAGEM ou VÍDEO: mp4/webm/ogg/mov...) OU `url_imagem` (prioridade), `link` opcional por item, `ordem` + properties `imagem_src` e `eh_video` (detecta vídeo pela extensão). No site, vídeo sai como `<video autoplay muted loop playsinline>` e imagem como `<img>` INTEIRA (`object-fit: contain`) sobre um fundo borrado da própria imagem (`.carrossel-slide-fundo`) que preenche as sobras — nada é cortado nem distorcido, em qualquer tamanho do carrossel (coluna cheia, dividindo com cartaz, faixa 96px, mobile)
- **Visual padrão** (`templates/carrossel_widget.html` + CSS `.carrossel-*` + JS em `main.js`): vertical com scroll-snap, indicadores laterais rosa/azul, setas de navegação, autoplay — inspirado no mockup Tailwind que o Dan enviou
- **`codigo_html` (avançado)**: se preenchido, o site renderiza esse HTML completo dentro de um **`<iframe srcdoc>` isolado** (Tailwind CDN etc. não afetam o CSS do site). O marcador **`<!--IMAGENS-->`** (ou `{{IMAGENS}}`) é substituído pelas imagens cadastradas (função `_montar_carrossel_html` em `conteudo/views.py`). Trocar o código + salvar = trocar a aparência
- As imagens dos carrosséis também entram no painel "Eventos" do celular

### ConfiguracaoSite
Singleton (pk=1). `nome_site`, `descricao`, `home_titulo`, `home_texto` (RichTextWidget — negrito/itálico/alinhamento/lista via `contenteditable`, salva HTML), `email_contato`, `telefone`, `endereco`, `logo`, `favicon`.

### Comentario
Comentários moderados (3 estados, migração 0019 — 2026-07-13).
- `conteudo` (FK CASCADE), `nome`, `email` (opcional), `texto`, `data_criacao` (auto_now_add)
- **`status`** (CharField, choices: `pendente`/`publicado`/`recusado`, default=`pendente`) — controla visibilidade: só `publicado` aparece no site
- **`resposta`** (TextField, blank) — resposta do administrador, exibida abaixo do comentário no site com ícone de escudo e data
- **`data_resposta`** (DateTimeField, null/blank) — preenchida automaticamente pelo `save_model` do admin ao inserir resposta
- **`aprovado`** (BooleanField, `editable=False`, default=False) — campo legado mantido para compatibilidade; não sincroniza com `status`
- Property `publicado` → `self.status == 'publicado'`
- **Comentários NÃO aparecem** em conteúdos com `tipo='link'` — verificado na view com `exibir_comentarios = conteudo.tipo != 'link'`
- Admin: `ComentarioAdmin` com badges coloridos ⏳/✅/❌, ações em lote "Aprovar"/"Recusar", campos do visitante readonly, seção colapsável de resposta

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
   - **Editar botão selecionado** (2026-07-12): seção verde abaixo da árvore (visível só com 1 botão marcado). AJAX carrega dados atuais (nome, descrição, ícone); formulário permite editar nome, descrição, ícone (FA ou upload de imagem), e adicionar anexo. POST salva tudo e redireciona. Link direto para admin completo.
   - **Criar subárea nos botões marcados** (2026-07-12): seção azul abaixo de "Criar novo botão". Marca 1+ botões → digita nome → cria subárea DENTRO de cada marcado simultaneamente.
   - **Botões sem pai → "Botões novos criados"** (2026-07-12): `_criar_no()` roteia automaticamente para categoria raiz oculta (`slug='botoes-novos-criados'`), criada via `get_or_create`.
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

### 2026-07-13 — Novo módulo "Estrutura de Árvores" (parte 10)

Implementado painel administrativo completo e independente para gerenciar a hierarquia do site. **Seguiu 100% o plano `Plano_Modulo_Estrutura_de_Arvores.md` — ZERO alterações a funcionalidades existentes.**

**Arquivos criados:**
- `conteudo/arvore_views.py` — Views + API AJAX:
  - `estrutura_arvores_view` — renderiza template com dados iniciais
  - `arvore_api` — rota AJAX com handler para ações
  - `_montar_arvore_completa()` — constrói árvore com metadados (2 consultas: categorias + conteúdos/anexos por nó)
  - `_arvore_json()` — serializa para JSON (Frontend)
  - `_listar_icones_enviados()` — lista ícones do media/icones_categoria/ e media/icones/
  - Handlers AJAX: `_api_detalhes`, `_api_criar`, `_api_editar`, `_api_excluir`, `_api_mover`, `_api_reordenar`, `_api_upload_icone`, `_api_associar_conteudo`, `_api_upload_anexo`, `_api_remover_anexo`, `_api_excluir_conteudo` (novo)
  - Helpers: `_slug_unico()`, `_eh_descendente()` (ciclo detection)

- `templates/admin/estrutura_arvores.html` — Template completo ~1300 linhas:
  - **Header**: título, descrição, stats (121 botões, 538 conteúdos)
  - **Coluna esquerda (árvore)**: pesquisa instantânea sem acento (normalização NFC), expandir/recolher tudo, filtros (Todos, Com conteúdo, Vazios, Só raiz), botão criar botão raiz, botão criar subbotão (visível quando 1+ selecionado)
  - **Árvore interativa**: drag-and-drop para mover, toggle expand/collapse, ícones (FA ou imagem), badges (conteúdos, anexos, ID), busca com expansão automática de ancestrais
  - **Coluna direita (painel de detalhes)**: renderiza ao clicar em nó
    - Seção **Informações** (colapsável): ID, slug, ordem, pai, menu superior, navegue por área, subbotões, ícone
    - Seção **Editar**: nome, descrição, ordem, visibilidade, botões salvar/mover/excluir/admin completo
    - Seção **Ícone** (colapsável): ícone atual (FA ou imagem), input FA, upload imagem, checkbox limpar, 96 ícones FA com busca, ícones personalizados enviados (thumbnail gallery), upload para biblioteca
    - Seção **Conteúdos** (colapsável): lista com tipo/título, botão editar (link), **botão excluir (lixeira vermelha)** — novo, formulário associar novo (título, tipo dropdown, URL, arquivo)
    - Seção **Anexos** (colapsável): lista, upload + nome opcional, botão remover por anexo
  - **Modal de confirmação**: excluir nó (dupla confirmação com contagem de subnós)
  - **Modal de mover**: lista hierárquica com raiz + opção mover para dentro de qualquer nó (com verificação ciclo)
  - **Toast**: notificações (sucesso/erro, auto-dismiss 3s)
  - **CSS inline**: variáveis (cores âmbar/laranja), layout grid 2 colunas (responsivo ≤980px), componentes badge/botão/secção/modal/lista
  - **JS**: `EA` namespace com ~2500 linhas, AJAX via `_post()`, renderização dinâmica

**Arquivos modificados:**
- `curriculo_sedu/urls.py` — adicionadas 2 rotas:
  - `path('admin/estrutura-arvores/', admin.site.admin_view(estrutura_arvores_view), name='admin_estrutura_arvores')`
  - `path('admin/estrutura-arvores/api/', admin.site.admin_view(arvore_api), name='admin_arvore_api')`
  - `from conteudo.arvore_views import estrutura_arvores_view, arvore_api` (novo import)

- `templates/admin/index.html` — adicionado banner:
  - **Estrutura de Árvores** (âmbar/laranja gradient #d97706 → #92400e)
  - Ícone: fas fa-network-wired
  - Descrição: "Visualize, crie, edite, mova e exclua botões em qualquer nível da hierarquia do site. Gerencie ícones e conteúdos."
  - Link: "Abrir Estrutura"
  - Posicionado após "Botões da Barra Superior"

**Funcionalidades completas (conforme plano):**
- ✅ Visualizar árvore hierárquica ilimitada (121 nós, profundidade sem limite)
- ✅ Expandir/recolher (individual + tudo/recolher tudo)
- ✅ Pesquisa instantânea sem acento (com auto-expansão de ancestrais)
- ✅ Localização rápida: badges com contagem de conteúdos/anexos
- ✅ Filtragem por estado (com/vazios)
- ✅ Atualização dinâmica (recarregar árvore após ações)
- ✅ **CRUD completo**: criar botão (raiz ou subbotão), editar (nome/descrição/ordem/visibilidade), mover (drag-drop + modal hierárquico com detecção ciclo), excluir (dupla confirmação)
- ✅ Associação de conteúdo: 5 tipos (documento/vídeo/post/link/página), upload arquivo
- ✅ Gerenciamento anexos: upload + remoção por item
- ✅ Biblioteca de ícones: 96 Font Awesome (com busca), ícones personalizados (gallery com thumbnails), upload permanente em media/icones_categoria/
- ✅ Formatos suportados: SVG, PNG, JPG, JPEG, WEBP, ICO
- ✅ **Novo**: botão excluir conteúdo (lixeira vermelha) ao lado de editar — requisição do Dan

**Comportamento:**
- Sem autenticação: redireciona para login
- Sem permissão staff: acesso negado
- CSRF protegido em todos os endpoints POST
- Confirmação dupla em exclusões
- Detecção de ciclos ao mover nó (não permite mover para dentro de si mesmo)
- Validação de slug único ao criar/editar
- Conteúdos-órfãos recuperáveis via Tela 2 do Painel Central

**Compatibilidade:**
- URL nova: `/admin/estrutura-arvores/` (não conflita com existentes)
- Banner novo no dashboard (não altera existentes)
- Views/API isoladas em `arvore_views.py` (novo módulo)
- Template novo `estrutura_arvores.html`
- **Nenhuma alteração** a rotas públicas, models, admin, templates do site público, ou funcionalidades existentes
- Conteúdo público (`/`) totalmente intacto

### 2026-07-13 — Correção crítica de duplicação + Modal da Estrutura (parte 11)

**Bug crítico corrigido**: conteúdos criados dentro de subbotões **não aparecem mais duplicados** na página do pai.

**Problema**: quando o Dan criava um botão (categoria) com URL via Estrutura de Árvores, o sistema criava um Conteudo dentro daquele botão. Mas a view `categoria_detalhe` buscava conteúdos da categoria **E de todas as subcategorias** (`cats = [categoria] + list(subcategorias)`), então o conteúdo aparecia:
- Como card/link dentro do subbotão ✓
- **E também como card solto na página do pai** ✗ (duplicação visual)

**Solução**: mudar `categoria_detalhe` para buscar conteúdos **somente da própria categoria**, não de subcategorias. As subcategorias já aparecem como cards (subbotões) — seus conteúdos ficam dentro delas.
- Linha ~107 em `conteudo/views.py`: `cats = [categoria]` (removido `+ list(subcategorias)`)
- Filtro mantém os Vínculos normalmente (`Q(vinculos__categoria__in=cats)`)
- Página-índice ("Documentos Curriculares") não foi afetada (usa caminho separado)

**Melhorias complementares:**
1. **Modal da Estrutura de Árvores restaura HTML** — `fecharModal()` agora restaura sempre o HTML original (`eaModalTitulo`, `eaModalMsg`, `eaModalConfirm`), evitando corrupção ao abrir mover/excluir consecutivamente
2. **Formulário de criação com URL + múltiplos arquivos** — `abrirCriar()` substitui `prompt()` por modal completo, aceita `criarUrl` (input type="url") e `criarAnexos` (input type="file" multiple)
3. **Limpeza de lixo de testes** — excluídos 2 conteúdos "Link: ..." do banco (IDs 598, 599) criados durante testes anteriores
4. **Título do conteúdo criado por URL** — mudado de `f'Link: {nome}'` para simplesmente `nome` (sem prefixo confuso)

**Arquivos modificados:**
- `conteudo/views.py` — linha ~107: `cats = [categoria]` (removido subcategorias do filtro)
- `conteudo/arvore_views.py` — `_api_criar()`: título sem "Link: " prefixo
- `templates/admin/estrutura_arvores.html` — funções JS atualizadas: `fecharModal()` restaura HTML, `abrirCriar()` modal completo

**Testado:**
- Página `/categoria/orientacoes-curriculares/`: 16 subbotões visíveis, 0 conteúdos duplicados (antes: 16 subbotões + N conteúdos duplicados)
- Páginas `/categoria/curriculo-atual/`, `/categoria/documentos-curriculares/`: HTTP 200, layout correto
- Exclusão de botões: funciona (modal intacto após fecharModal)
- Mover botão: funciona (modal intacto após fecharModal)
- Criar com URL: cria Conteudo tipo "link" corretamente (sem prefixo "Link:")

**Compatibilidade 100%**: ZERO alterações quebradas — todos os outros painéis (Painel Central, Organizador, etc.) continuam funcionando normalmente.

### 2026-07-16 — Estrutura de Árvores + Subbotões Melhorados (parte 12)

**Duas melhorias complementares** para aperfeiçoar a criação e visualização de botões.

**1. Campo de imagem de ícone adicionado ao modal de criar botão (Estrutura de Árvores)**

O modal "Criar novo botão" / "Criar subbotão" tinha: Nome*, URL (opt), Anexos (opt), Ícone Font Awesome (opt). Faltava o **campo de upload de imagem de ícone** — só existia no formulário de edição. Backend já suportava `icone_imagem`.

Solução: adicionado `<input type="file" id="criarIconeImg">` ao modal + JS que coleta arquivo e envia via `fd.append('icone_imagem', iconeImg)`.

Resultado: ao criar botão/subbotão, preenche tudo de uma vez (nome + URL + anexos + ícone imagem).

**2. Subbotões aparecem como cards grandes clicáveis**

Subbotões só apareciam como chips pequenos no topo. Depois da correção da Parte 11 (que evita duplicação), é seguro trazer de volta os botões grandes.

Solução: em `categoria.html`, adicionado loop renderizando subbotões como `.content-card.content-card--subbotao` (borda azul, badge "BOTÃO", descrição).

Resultado: página mostra subbotões como cards grandes clicáveis + chips atalho no topo.

**Arquivos modificados:**
- `templates/admin/estrutura_arvores.html` — campo `criarIconeImg` adicionado
- `templates/categoria.html` — subbotões como `.content-card--subbotao`

**Testado:**
- Estrutura: criação com imagem funcionando (Django test client)
- Página: 3 subbotões em `/categoria/icone-teste/` renderizados como cards (confirmado via grep do HTML)

**⚠️ Templates alterados** — reiniciar servidor (`runserver`)

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
    - **Seletor "Categoria pai" hierárquico** no Django Admin (foto do Dan mostrava lista aleatória "Pai → Filho"): `CategoriaAdminForm.__init__` injeta choices em árvore ordenada com recuo/└ (mesmo estilo do Painel Central), excluindo a própria categoria; desembrulha o `RelatedFieldWidgetWrapper`. Depois ganhou **caixinha de PESQUISA** (`static/js/filtro_select.js`, genérico: qualquer `<select data-pesquisavel>` ganha filtro instantâneo sem acento) — ativa no "Categoria pai" (via `Media` do CategoriaAdmin) e no select "Criar novo botão" do Painel Central.
    - **Barra superior**: 5 botões FIXOS definidos pelo Dan (Documentos Curriculares, Programas, Projetos Integradores, Olimpíadas, Institucional — via `mostrar_menu_superior`, que continua valendo tb p/ rodapé); estilo discreto (branco, sem negrito, CENTRALIZADOS na barra, 12px, pílula translúcida `rgba(255,255,255,.13)`; barra do topo abaixada de 72px→58px); **ícone de localização** (`.nav-localizacao`, fa-location-dot) à direita da busca abrindo o endereço da ConfiguracaoSite no Google Maps (`maps/search/?api=1&query=`); **novo painel admin** `/admin/barra-superior/` (view `barra_superior_view` em admin_views.py, template `admin/barra_superior.html`, cartão ciano no dashboard) — checkbox "na barra?", ordem, atalhos criar/editar/excluir.
    - **Carrossel aceita QUALQUER arquivo (imagem/vídeo) e se ajusta sozinho** (plano "Plano_Implementacao_Ajustes_Homepage"): migração 0015 (ImageField→FileField), property `eh_video`, `<video>` no widget e no código personalizado (`_montar_carrossel_html`), `contain` + fundo borrado nos slides, admin aceita .mp4/.webm/etc.
    - **Rodapé no menor tamanho possível** (Item 2 do mesmo plano): paddings/fontes reduzidos (footer 10px, h3 11.5px, links 10.5px, pílula voltar 10.5px) — nada removido; ~138px no desktop.
    - **Busca acha tudo**: a view `busca` agora também procura em `Categoria` (nome + descrição, sem acento) e mostra a seção "Botões e áreas do site" (chips) acima dos conteúdos; "nenhum resultado" só aparece se AMBAS as listas vierem vazias.
- Versão de cache do CSS evoluiu ao longo do dia: `?v=20260711-1` → `-2` (pílula do Currículo Atual + recentes quadrados) → `-3` (ícone personalizado em Conteudo, cards compactos, tamanho de botão) → `-4` (ícone personalizado em Categoria/botões) → `-5` (correção do ajuste de imagem — cover nos botões) → `-6` (card de conteúdo volta a contain) → `-7` (botão voltar no rodapé + VLibras). JS ficou em `?v=20260711-1`.
- Testado: páginas 200, ações do painel via test client, submissão completa do Painel Central, ícone-só sem título aplicado a pai+sub (212 bytes cada, sem truncamento), ícone com título indo para o conteúdo e NÃO para o botão, card de conteúdo com `object-fit:contain` confirmado via computed style, campo `botao_icone_imagem` confirmado removido do HTML.

### 2026-07-12 — Correções de bugs de layout responsivo (parte 1)
1. **Navegação embolada no celular** — regra global `.home-split { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }` (de 2026-07-10) sobrescrevia media queries de mobile (≤860px) que mandavam empilhar em 1 coluna. Solução: limitar a regra a `@media (min-width: 861px)` — agora no celular home-split volta a 1 coluna (343px), deixando o layout legível.

2. **Carrossel "Sedu Informa" dividido em dois no painel "Eventos"** — as 2 imagens do carrossel estavam sendo "explodidas" em 2 cards separados com `href="#"` (links mortos), dando impressão de "dividido em dois e sem funcionar". Solução: incluir o carrossel INTEIRO no painel como widget funcional (`<div class="cartaz-painel-carrossel">{% include 'carrossel_widget.html' %}</div>`) — agora passa as imagens sozinho, com setas e autoplay. CSS: `.cartaz-painel-carrossel { grid-column: 1 / -1; }` (ocupa largura total). Teste: painel agora tem 1 carrossel funcional (2 slides, 2 setas) + 3 cartazes reais, 0 links mortos.

3. **Carrossel vazando para rodapé azul** — carrossel em coluna cheia (sem cartaz) tinha altura fixa (`calc(100vh - 104px)`) sem limite máximo, invadindo o rodapé em 137px no desktop. Solução: adicionar `max-height: 100%` a `.cartazes-lateral.col-cheia .cartazes-inner` — agora o carrossel é confinado ao trilho branco (`.home-conteudo`), respeitando as mesmas regras dos cartazes (nunca invade header/footer).

4. **Comentário Django multilinhas visível** — comentário `{# ... #}` com quebra de linha de 223–225 em home.html estava sendo renderizado como texto na página ("{% Cada carrossel entra INTEIRO no painel..."). Django só suporta `{# #}` em UMA linha. Solução: trocar por `{% comment %}...{% endcomment %}` (aceita múltiplas linhas).

- Versão de cache: CSS `?v=20260712-5` (incrementado de `-4`).
- Testado no navegador: desktop (1440×860): carrossel ocupa 619px (sem overflow), mobile (375×812): home-split 1 coluna (343px), painel Eventos com carrossel funcional 335px (largura cheia).

### 2026-07-12 — Correções de funcionalidade de anexos + subbotões (parte 2)
1. **Anexos de conteúdo não apareciam na página de detalhe** — quando o Dan criava um conteúdo via Painel Central com título + arquivos, o sistema salvava os Anexo ligados àquele Conteudo, mas a página `conteudo_detalhe.html` NUNCA exibia esses anexos. A seção "Arquivos para download" só existia em páginas de categoria, não de conteúdo. Solução: (a) adicionar `anexos = conteudo.anexos.all()` à view `conteudo_detalhe`, (b) reproduzir a seção `.anexos-section` do template de categoria no template de conteúdo, com os mesmos ícones coloridos por tipo (PDF, Word, Excel, PPT, vídeo, imagem). Agora: conteúdo com anexos mostra a seção; sem anexos, nada aparece.

2. **Subbotões não apareciam visualmente como cards grandes** — o Dan criava um subbotão (ex.: "Documentos Orientadores" dentro de "Educação Escolar Quilombola") e o botão era salvo no banco, mas SÓ aparecia como chip PEQUENO no topo da página da categoria pai. O Dan não via visualmente onde era para clicar / adicionar conteúdo. Solução: (a) adicionar as subcategorias à `content-grid` (mesmo array de cards) ANTES dos conteúdos, (b) estilizar cards de subbotão com borda azul 2px, ícone com fundo claro (`#e6efff`), texto "→ Abrir para ver / adicionar arquivos" no rodapé. Agora: subbotões aparecem como cards destacados no meio da página, ao lado dos conteúdos normais, ainda mantendo os chips no topo. (Nota: badge "BOTÃO" removido em revisão — card fica mais limpo apenas com nome + descrição + link.)

3. **Senha do usuário ridan restaurada** — havia sido resetada durante investigação anterior. Volta a `Sedu@2026`.

- Versão de cache: CSS `?v=20260712-6` (incrementado de `-5`).
- Arquivos modificados: `conteudo/views.py` (adicionar anexos à view), `templates/conteudo_detalhe.html` (seção de anexos), `templates/categoria.html` (subbotões como cards), `static/css/style.css` (estilos `.content-card--subbotao` e `.card-badge-botao`).
- Testado: "Documentos Orientadores" (subbotão de Quilombola) aparece como card no meio, tem 1 anexo visible, breadcrumb correto `Início / Educação Escolar Quilombola / Documentos Orientadores`.

### 2026-07-12 — Busca da árvore do Painel Central + Nova função "Criar subárea" (parte 3)
1. **Busca da árvore corrigida** — A busca por nome de sub-sub-botões agora os torna **visíveis com ancestrais expandidos automaticamente**. Problema: ao Dan pesquisar "ementa" para encontrar o subbotão "ementas" (dentro de "Documentos Orientadores" → "Educação Escolar Quilombola"), a árvore encontrava o botão mas o deixava fechado dentro do pai, impossível clicar. Solução: reescrever a lógica de busca em `templates/admin/painel_central.html` — (a) marca nós que batem direto, (b) mostra apenas o caminho até o match, (c) expande os `<ul>` de TODOS os ancestrais de qualquer match encontrado, (d) recolhe tudo ao limpar o campo. Impacto: todas as árvores (Organizador, Painel Central) agora usam filtro sem acento (`static/js/filtro_select.js`); a árvore principal acusa match em 3+ níveis.
   
2. **Nova seção: "Criar subárea nos botões marcados"** — Painel Central agora tem UM NOVO FORMULÁRIO (azul claro, após "Criar novo botão") que permite criar subáreas (subbotões) **DENTRO de botões marcados** sem abrir o select complicado. Fluxo: marque 1+ botões na árvore → digite o nome da nova subárea → clique "➕ Criar subárea dentro dos marcados" → a subárea é criada dentro de CADA botão marcado simultaneamente. Implementado: (a) novo template form em `painel_central.html` com input de nome + hidden destinos, (b) handler JS que copia IDs dos marcados no submit, (c) nova action `criar_subareas` em `painel/views.py` com view `_criar_subareas()` que cria Categoria para cada pai marcado em lote. Testado com 4 cenários: sucesso (1 pai), sucesso (3 pais), erro sem destinos, erro sem nome — todos ok via test client. Impacto: Dan agora cria subárea em "Projetos Integradores" digitando "Documentos Gerais" + enter, em vez de ir manual ao select "Criar novo botão" e escolher pai um a um. Atalho muito útil.

- Versão de cache: CSS/JS sem mudança (só lógica no template JS). Mantém `?v=20260712-6`.
- Arquivos modificados: `templates/admin/painel_central.html` (nova seção + JS handler + correção da busca), `painel/views.py` (nova action + view `_criar_subareas()`).
- Testado: busca por "ementa" no Painel Central mostra "ementas" visível com ancestrais abertos; criar subárea em 2+ botões ao mesmo tempo cria N cópias do nome correto no banco.

### 2026-07-12 — Rodapé sticky em todas as páginas (parte 4)
**Rodapé flutuando em páginas com pouco conteúdo** — Em páginas internas com pouco ou zero conteúdo (busca vazia, categoria vazia, "subteste"), o `<body>` não preenchia 100% da altura da viewport, deixando o rodapé "flutuando" no meio em vez de colar no fundo. Solução: adicionar `display: flex; flex-direction: column; min-height: 100vh;` ao `body`, e `flex: 1;` ao `.main`. Isso garante que o main estica para preencher o espaço restante, empurrando o footer para baixo. Testado: gap=0 em páginas vazias (desktop 1920×1080); gap negativo (scroll normal) em páginas com conteúdo.

- Versão de cache: CSS `?v=20260712-7` (incrementado de `-6`).
- Arquivos modificados: `static/css/style.css` (body flexbox + min-height 100vh, .main flex: 1), `templates/base.html` (cache-busting).
- Testado: `/categoria/subteste/` (pouco conteúdo, desktop) — gap=0; `/` (home, desktop) — gap=-507px (scroll normal); `/categoria/subteste/` (mobile) — gap=-262px (scroll normal).

### 2026-07-12 — Edição inline + CategoriaPicker dinâmico + UX do Painel Central (parte 5)
1. **Editar botão selecionado** — nova seção verde no Painel Central (abaixo da árvore, antes de "Excluir"). Ao marcar EXATAMENTE 1 botão na árvore, aparece formulário com: nome, descrição (textarea), ícone Font Awesome (input), upload de ícone personalizado (imagem), upload de anexo. AJAX GET (`_dados_botao`) carrega os dados atuais do botão; POST (`_editar_botao`) salva nome (+ gera novo slug), descrição, ícone, `icone_imagem`, e opcionalmente cria um Anexo ligado à categoria. Link direto para o admin completo do botão. Se marcar 0 ou 2+ botões, a seção desaparece.

2. **Botões sem pai → "Botões novos criados"** — `_criar_no()` em `painel/views.py` agora roteia botões criados sem selecionar pai para uma categoria raiz oculta ("Botões novos criados", slug `botoes-novos-criados`, `mostrar_menu_superior=False`, `mostrar_navegue_area=False`), criada automaticamente via `get_or_create`. O Dan não precisa mais se preocupar com botões "soltos" na raiz.

3. **CategoriaPicker dinâmico** — `conteudo/widgets.py` corrigido: categorias raiz SEM subcategorias (como "Botões novos criados") agora aparecem como botão selecionável no picker (antes eram silenciosamente ignoradas por `if not subs.exists(): continue`). Afeta: Django Admin (Adicionar Conteúdo, Adicionar Categoria) e Painel Adicionar Arquivos.

4. **Texto centralizado padrão** — adicionado `text-align: center` em `.topic-btn`, `.card-body`, `.card-body h3`, e `.content-card--subbotao .card-body` no CSS. Todos os botões novos e antigos ficam com texto centralizado.

5. **Texto "→ Abrir para ver / adicionar arquivos" removido** — footer com link azul nos cards de subbotão (`templates/categoria.html` linhas 141-143) foi deletado, deixando os cards mais limpos.

- Versão de cache: CSS `?v=20260712-8`.
- Arquivos modificados: `painel/views.py` (`_dados_botao`, `_editar_botao`, `_criar_no` com fallback para "Botões novos criados"), `templates/admin/painel_central.html` (seção editar + JS AJAX), `conteudo/widgets.py` (CategoriaPicker aceita categorias vazias), `templates/categoria.html` (removido footer subbotão), `static/css/style.css` (text-align center), `templates/base.html` (cache-busting `-8`).
- Testado: AJAX retorna dados corretos (nome "Ementas", descrição "Diretrizes Escolares"); POST redireciona 302; "Botões novos criados" aparece no CategoriaPicker do Admin e do Adicionar Arquivos (108-109 botões no picker).

### 2026-07-12 — Carrossel admin + Campo URL no Painel Central (parte 6)
1. **Carrossel admin: mostrar arquivos atuais** — trocar `FileInput` por `ClearableFileInput` em `CarrosselImagemInline.formfield_for_dbfield()`. Agora: (a) "Atualmente: carrossel/images.jpg" (link) — o arquivo atual é visível e clicável, (b) checkbox "Limpar" — permite remover o arquivo, (c) "Modificar:" — campo file para trocar. As 3 imagens existentes (1 vídeo MP4 + 2 JPGs) ficam legíveis. Antes: campo vazio, impossível saber o que tinha ou excluir.

2. **Campo URL no "Editar botão selecionado"** — novo campo `type="url"` na seção verde do Painel Central ("URL / Link (opcional)"). Quando preenchido no POST (`_editar_botao`), cria automaticamente um `Conteudo(tipo='link', url_externa=url, categoria=cat, status='publicado')`. Atalho para o Dan criar um link dentro do botão sem abrir o Painel Central completo.

- Versão de cache: sem mudança (CSS/JS não alterados).
- Arquivos modificados: `conteudo/admin.py` (CarrosselImagemInline widget), `templates/admin/painel_central.html` (campo URL), `painel/views.py` (`_editar_botao` com Conteudo.create).
- Testado: carrossel admin mostra 3 arquivos com opções limpar/modificar; campo URL no painel carrega vazio, pronto para preencher com URL; POST redirecionaria com sucesso.

### 2026-07-13 — Sistema de Comentários Moderados (parte 7)
Implementado do zero com base no `Plano_Sistema_de_Comentarios_Moderados.md` (Dan). **REGRA: nenhuma funcionalidade existente foi alterada.**

1. **Modelo `Comentario` expandido** (migração `conteudo/0019`):
   - Novo campo `status` (CharField, 3 escolhas): `pendente` (default), `publicado`, `recusado`
   - Novo campo `resposta` (TextField, blank=True): resposta do administrador exibida no site
   - Novo campo `data_resposta` (DateTimeField, null/blank): preenchido automaticamente ao salvar resposta
   - Campo `aprovado` (BooleanField legacy): mantido como `editable=False` para não quebrar nada
   - Property `publicado` → `self.status == 'publicado'`
   - Migração `0019_comentario_status_resposta.py` aplicada com sucesso

2. **`ComentarioAdmin` totalmente reescrito** (`conteudo/admin.py`):
   - `list_display`: nome, conteúdo (link), trecho do texto, `status_badge` (emoji colorido ⏳/✅/❌), `tem_resposta`, data
   - `list_filter`: status, data_criação
   - Ações em lote: "✅ Aprovar e publicar" → `status='publicado'`, "❌ Recusar" → `status='recusado'`
   - Campos readonly quando editando comentário existente: nome, email, texto, conteudo, data_criacao, data_resposta
   - Seção colapsável "Resposta do administrador" (fieldset)
   - `save_model`: preenche `data_resposta` automaticamente quando resposta é inserida; limpa quando removida

3. **View `conteudo_detalhe`** (`conteudo/views.py`):
   - `exibir_comentarios = conteudo.tipo != 'link'` — comentários NÃO aparecem em conteúdos tipo "link"
   - Exibe apenas `status='publicado'`
   - Cria novos com `status='pendente'`
   - Passa `exibir_comentarios` ao contexto do template

4. **Template `conteudo_detalhe.html`**:
   - Toda a seção de comentários dentro de `{% if exibir_comentarios %}`
   - Badge de contagem (`<span class="comment-count-badge">N</span>`) ao lado do título
   - Mensagem vazia com ícone: "Ainda não há comentários. Seja o primeiro!"
   - Bloco de resposta do admin (`.comment-resposta`) com ícone `fa-shield-halved` e data
   - Botão "Publicar Comentário" com gradiente azul e ícone fa-paper-plane
   - Aviso discreto: "Seu comentário será publicado após aprovação da equipe"

5. **CSS** (bloco "AJUSTES 2026-07-12 — Sistema de comentários" em `style.css`):
   - `.comentarios-section` — fundo alternado `#eef1f5`
   - `.comment-count-badge` — pílula arredondada azul com número
   - `.comment-item` — layout flex com avatar redondo
   - `.comment-resposta` — fundo `#e8f5e9` (verde claro), borda esquerda verde, ícone escudo
   - `.comment-submit-btn` — botão gradiente azul com glow ao hover, ícone fa-paper-plane
   - `.comment-empty` — texto itálico com borda pontilhada
   - `.comment-alert` — mensagem de sucesso/erro estilizada
   - `.comment-notice` — aviso de moderação discreto

- **Versão de cache**: CSS `?v=20260713-1` (incrementado de `-8`).
- **Arquivos modificados**: `conteudo/models.py` (Comentario expandido), `conteudo/migrations/0019_comentario_status_resposta.py` (nova migração), `conteudo/admin.py` (ComentarioAdmin reescrito), `conteudo/views.py` (exibir_comentarios + status), `templates/conteudo_detalhe.html` (seção comentários redesenhada), `static/css/style.css` (novo bloco CSS), `templates/base.html` (cache-busting `-1`).
- **Testado**: página `/conteudo/teste-5/` mostra formulário, badge, aviso; seção ausente em `/conteudo/link-externo/` (tipo='link'); admin `/admin/conteudo/comentario/` mostra ações em lote e badges coloridos.

### 2026-07-13 — Respostas de visitantes + Votos 👍/👎 em comentários (parte 8)
Implementado fluxo completo de respostas aninhadas e votação AJAX. **REGRA: nenhuma funcionalidade existente foi alterada.**

1. **Modelo `Comentario` expandido** (migração `conteudo/0020`):
   - Novo campo `parent` (ForeignKey self, null/blank, CASCADE) — vincula uma resposta ao comentário original
   - Novo campo `votos_positivos` (PositiveIntegerField, default=0) — contador de 👍
   - Novo campo `votos_negativos` (PositiveIntegerField, default=0) — contador de 👎

2. **Respostas aninhadas** (`conteudo/views.py`):
   - View `conteudo_detalhe` agora prefetch respostas (somente `status='publicado'`)
   - POST recebe `parent_id` hidden (optional) — se preenchido, cria resposta ligada ao comentário original
   - Respostas entram com `status='pendente'` (moderação igual aos comentários raízes)
   - Cada resposta pode ser respondida novamente (estrutura recursiva), mas o template exibe apenas 2 níveis (comentário + respostas diretas)

3. **Votação AJAX** (nova URL `/comentario/<pk>/votar/`):
   - POST com `voto=positivo` ou `voto=negativo`
   - Retorna JSON com `votos_positivos` e `votos_negativos` atualizados
   - Sem autenticação (visitante anônimo pode votar)
   - `@require_POST` + CSRF protegido
   - No template: JS desabilita os 2 botões de voto após click (1 voto por sessão, browser-local)

4. **Admin** (`conteudo/admin.py`):
   - Coluna "Tipo" (mostra "↩ Resposta" em roxo se tiver parent, senão vazio)
   - Coluna "Votos" (mostra 👍 N 👎 N em cores)
   - Campo `parent` visível na edição (readonly quando obj já existe)
   - Seção colapsável "👍 Votos dos visitantes" com `votos_positivos`/`votos_negativos` readonly

5. **Template `conteudo_detalhe.html`**:
   - Comentários raízes renderizam 2 botões: "Gostei" (👍) e "Não gostei" (👎) com contadores
   - Botão "Responder" que abre/fecha formulário inline (`display: none / block` com classe `.open`)
   - Formulário inline com campos nome/email/texto + hidden `parent_id` + botões "Enviar resposta" / "Cancelar"
   - Seção `.comment-replies` (recuada, linha azul à esquerda) com respostas do visitante
   - Cada resposta renderiza: avatar menor (roxo), label "↩ resposta", seus próprios botões 👍/👎 (sem "Responder" — máx 2 níveis)
   - JS: delegado ao form-submit; AJAX no click dos botões `.comment-vote-btn` (sem reload)

6. **CSS** (novo bloco "AJUSTES 2026-07-13 — Votos e respostas aninhadas"):
   - `.comment-actions` — flex container com botões
   - `.comment-vote-btn` — pílula cinza com 👍/👎, muda cor ao hover (.vote-pos verde, .vote-neg vermelho)
   - `.comment-vote-btn.voted-pos/voted-neg` — após votar, fica com fundo colorido e font-weight 700
   - `.comment-reply-btn` — pílula cinza com "Responder"
   - `.comment-inline-reply` — `display: none`, com classe `.open` fica `display: block`
   - `.comment-inline-reply.open` — formulário visível com fundo azul claro e borda esquerda
   - `.comment-replies` — margin-left 40px, borda-left 2px azul, padding-left 12px (recuo visual)
   - `.comment-item.comment-reply` — fundo semi-transparente, padding reduzido
   - `.comment-avatar-reply` — 28px (menor que raiz), roxo (#7c3aed)
   - `.comment-reply-label` — "↩ resposta" em roxo, fundo claro, border-radius 10px
   - Cache atualizado para `?v=20260713-2`

- **Versão de cache**: CSS `?v=20260713-2` (incrementado de `-1`).
- **Arquivos modificados**: `conteudo/models.py` (parent + votos), `conteudo/migrations/0020_comentario_parent_votos.py` (nova migração), `conteudo/urls.py` (nova rota votar_comentario), `conteudo/views.py` (prefetch respostas, parent_id no POST, view votar_comentario), `conteudo/admin.py` (coluna eh_resposta, votos_badge, parent no fieldset), `templates/conteudo_detalhe.html` (botões 👍/👎, formulário inline, respostas aninhadas, JS AJAX), `static/css/style.css` (novo bloco de estilos), `templates/base.html` (cache-busting `-2`).
- **Testado**: página `/conteudo/teste-5/` com comentário publicado + resposta: botões 👍/👎 funcionam via AJAX (contadores incrementam); "Responder" abre/fecha formulário inline; respostas aninhadas aparecem recuadas com label "↩ resposta"; cada resposta tem seus próprios 👍/👎.

### 2026-07-13 — ngrok UTF-8 + Video Streaming via Range Requests (parte 9)
Corrigidos **2 problemas críticos** com compartilhamento via ngrok. **REGRA: apenas adições, nada quebrado.**

1. **Double-encoding UTF-8 nos templates** (descoberto durante testes):
   - **Problema**: commit `82f5b92` ("codigo") salvou `templates/base.html`, `painel_central.html` e `painel_conteudos.html` com double-encoding UTF-8 (caracteres como "CurrÃ­culo", "EDUCAÃ‡ÃƒO" em vez de "Currículo", "EDUCAÇÃO").
   - **Causa**: editor de texto em outro computador (provavelmente Notepad/VSCode sem UTF-8 configurado) reabriu e re-salvou os arquivos em Latin-1, criando mojibake.
   - **Solução**: restaurados 3 templates do `HEAD~1` (commit anterior correto). Verificação completa: nenhum outro arquivo estava corrompido.
   - **Resultado**: site agora exibe "Currículo do Espírito Santo" e "Educação Básica" corretamente em localhost E via ngrok.

2. **Vídeo do carrossel não carregava via ngrok** (37MB, timeout/proxy issues):
   - **Problema**: Django dev server (`runserver`) não suporta HTTP Range Requests (206 Partial Content) nativamente. Browsers modernos pedem vídeos em chunks — sem Range Requests, ngrok/proxies têm timeout.
   - **Solução**: nova view Django `serve_media` em `conteudo/media_views.py` com suporte completo a Range Requests:
     - `HTTP 200` para requisição normal (serve vídeo inteiro)
     - `HTTP 206 Partial Content` para Range Requests (serve apenas bytes solicitados)
     - Streaming em chunks de 8KB (não sobrecarrega memória)
     - Header `ngrok-skip-browser-warning: true` (pula aviso do ngrok)
   - **URLs modificadas**: `curriculo_sedu/urls.py` agora roteia `/media/*` para `serve_media` em vez de `static()`.
   - **Resultado**: vídeo agora carrega normalmente via ngrok (testado com curl: `206 Partial Content` funcionando).

3. **Automação de testes e launcher** (2026-07-13):
   - `teste_ngrok.py` — script Python que valida antes de compartilhar (Django ok? Vídeo existe? UTF-8 correto?)
   - `BAT SEDU\INICIAR COM NGROK.bat` — launcher um-clique que: inicia Django + roda testes + compartilha ngrok
   - `BAT SEDU\COMPARTILHAR COM GERENTE.bat` — melhorado com `PYTHONIOENCODING=utf-8` + fallback para Python script
   - `NGROK_COMPARTILHAR.md` — guia em português com 3 opções de uso

4. **Documentação**:
   - `RESUMO_FIXES_2026_07_13.md` — resumo técnico completo
   - `README.md` — reescrito com tudo atualizado
   - Memory: `ngrok_fixes.md` — para futuras sessões

- **Versão de cache**: CSS `?v=20260713-2` (sem mudança de CSS).
- **Arquivos adicionados**: `conteudo/media_views.py` (nova view com Range Requests), `teste_ngrok.py` (validação), `BAT SEDU\INICIAR COM NGROK.bat` (launcher), `NGROK_COMPARTILHAR.md` (guia), `RESUMO_FIXES_2026_07_13.md` (resumo técnico).
- **Arquivos modificados**: `curriculo_sedu/urls.py` (router `/media/` → `serve_media`), `BAT SEDU\COMPARTILHAR COM GERENTE.bat` (UTF-8 + Python fallback), `README.md` (reescrito), `db.sqlite3` (vídeo path atualizado).
- **Arquivos restaurados**: `templates/base.html`, `templates/admin/painel_central.html`, `templates/admin/painel_conteudos.html` (do `HEAD~1`, desfazendo double-encoding).
- **Testado localmente**: Range Requests funcionando (`206 Partial Content`), site com UTF-8 correto, vídeo 37MB acessível.

### 2026-07-17 — Currículo Atual como botão raiz + Checkbox "Central?" (parte 13)

**Estrutural: hierarquia refatorada para colocar "Currículo Atual" no topo do site como categoria raiz independente.**

1. **"Currículo Atual" virou botão raiz** (decisão do Dan):
   - Antes: era subcategoria de "Documentos Curriculares" (categoria_pai FK apontava para "Documentos Curriculares")
   - Agora: `categoria_pai=None` (é raiz, como "Documentos Curriculares", "Programas", etc.)
   - Consequência esperada: sumiu da listagem "Documentos Curriculares" (que só mostra itens com `categoria_pai != None`)
   - Aparece como **raiz em TODAS as árvores**: Estrutura de Árvores, Painel Central, Organizador, Barra Superior
   - Mantém seus 8 subbotões (etapas), suporte completo a subáreas/anexos/URL (igual a qualquer botão raiz)
   - Fields `mostrar_menu_superior=False` e `mostrar_navegue_area=False` (evita aparecer na barra azul/Navegue por área — usa apenas a pílula central especial)

2. **Novo checkbox "Central?" no painel `/admin/barra-superior/`**:
   - Adicionado novo field `Categoria.mostrar_area_central` (BooleanField, default=False, migração `conteudo/0024`)
   - Dois checkboxes independentes: "Na barra?" (`mostrar_menu_superior`) e "Central?" (`mostrar_area_central`)
   - Qualquer botão raiz pode ser marcado para aparecer na área central (não apenas Currículo Atual)
   - Ordem usa o mesmo field "Ordem" existente em ambos os locais
   - View `barra_superior_view` atualizada para salvar ambos os fields em lote

3. **Área central na home** (`templates/home.html`):
   - Nova div `.curriculo-atual-topo` com `display: flex; flex-wrap: wrap; justify-content: center; gap: 12px`
   - Renderiza a pílula "Currículo Atual" (sempre) + loop de botões com `mostrar_area_central=True` (excluindo Currículo Atual para não duplicar)
   - Botões secundários ganham classe `.area-card-central` com `opacity: 0.94` (visualmente distintos do principal)
   - Quebra automática se não couber (flex-wrap)

4. **Admin de Categoria** (`conteudo/admin.py`):
   - Fieldset "📍 Onde este botão aparece" agora inclui 3 checkboxes: `mostrar_menu_superior`, `mostrar_navegue_area`, `mostrar_area_central`
   - Field `mostrar_area_central` ativo apenas para categorias raiz (validação manual possível futura)

5. **Context e view**:
   - `conteudo/views.py` `home()`: query `botoes_area_central` busca raiz com `mostrar_area_central=True`, exclui 'curriculo-atual'
   - Passa ao template em contexto

- **Versão de cache**: CSS `?v=20260717-1` (mudança de layout flex-wrap para central), JS mantém `?v=20260711-1`
- **Migração**: `conteudo/0024_mostrar_area_central.py` (adiciona field `mostrar_area_central` a Categoria)
- **Arquivos modificados**: `conteudo/models.py` (novo field), `conteudo/migrations/0024_mostrar_area_central.py` (migração), `conteudo/views.py` (botoes_area_central), `conteudo/admin_views.py` (dual checkboxes POST), `templates/home.html` (loop botoes_area_central, flex-wrap), `templates/admin/barra_superior.html` (checkbox na_central), `static/css/style.css` (.curriculo-atual-topo flex-wrap, .area-card-central opacity), `templates/base.html` (cache-busting), `conteudo/admin.py` (fieldset).
- **Testado fim-a-ponta**: Home 200 OK, Currículo Atual como raiz em todas as árvores, POST Barra Superior salvando checkbox (302 redirect), Programas marcado = aparece na área central da home, remover marca = desaparece, "Documentos Curriculares" não duplica Currículo Atual, pílula principal sempre visível.
- **Compatibilidade 100%**: zero mudanças quebradas — todos os outros sistemas funcionam normalmente.

### 2026-07-17 — Subáreas vs Botões: campo `mostrar_como_card` (parte 14)

**Problema identificado**: função "Criar subárea nos botões marcados" criava subcategorias que apareciam duplicadas — como chip no topo E como card grande no meio da página do pai, causando informação redundante. Solução: novo campo de modelo para diferenciar "botões estruturais" (aparecem nos dois lugares) de "subáreas rápidas" (aparecem só como chip).

1. **Novo field: `Categoria.mostrar_como_card`** (BooleanField, default=True, migração `conteudo/0025`):
   - Vale apenas para subcategorias (botões dentro de outro botão)
   - `True` (padrão): aparece como chip no topo E como card grande clicável no meio
   - `False`: aparece SOMENTE como chip no topo (sem duplicar)
   - Editável no Django Admin na seção colapsável "🗂️ Como aparece na página do botão pai"

2. **"Criar subárea nos botões marcados"** agora cria com `mostrar_como_card=False`:
   - Subáreas rápidas criadas via esta função aparecem só como chip (não duplicam)
   - Funcionava assim conceitualmente desde a Parte 12, mas agora tem controle explícito

3. **"Criar novo botão"** (tanto Painel Central quanto Estrutura de Árvores) cria com `mostrar_como_card=True`:
   - Botões estruturais (pensados como subbotões de verdade) aparecem como chip + card
   - Comportamento padrão = máxima visibilidade

4. **Compatibilidade com banco antigo**:
   - Categorias existentes herdam `mostrar_como_card=True` (comportamento que já tinham)
   - Possível corrigir retroativamente no admin caso necessário

- **Versão de cache**: CSS sem mudança (`?v=20260717-1`), JS sem mudança (`?v=20260711-1`)
- **Migração**: `conteudo/0025_mostrar_como_card.py` (adiciona field `mostrar_como_card` a Categoria, default=True)
- **Arquivos modificados**: `conteudo/models.py` (novo field), `conteudo/migrations/0025_mostrar_como_card.py` (migração), `conteudo/admin.py` (novo fieldset colapsável), `painel/views.py` (`_criar_subareas()` com `mostrar_como_card=False`), `templates/categoria.html` (condicional `{% if sub.mostrar_como_card %}` ao renderizar cards).
- **Testado fim-a-ponta**: Subárea criada via "Criar subárea" → nasce com `mostrar_como_card=False` → aparece só como chip ✓. Botão criado via "Criar novo botão" → nasce com `mostrar_como_card=True` → aparece como chip + card ✓. Categoria existente pode ser ajustada no admin ✓.
- **Compatibilidade 100%**: nenhuma mudança quebrada — todos os sistemas funcionam normalmente.

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
