# Site Currículos SEDU — Contexto do Projeto (v30 — atualizado em 2026-07-22 — Parte 34)

## O que é este projeto

Site da **Gerência de Currículo da Educação Básica (GECEB)**, da Secretaria de Estado da Educação do Espírito Santo (SEDU). Migração do site WordPress/Elementor em `curriculo.sedu.es.gov.br/curriculo/` para Django moderno.

O dono do projeto (**Dan**) não é programador — ele trabalha na SEDU e precisa de instruções claras, em português, para qualquer operação no terminal. Sempre explique comandos passo a passo e forneça comandos prontos para copiar e colar.

## 🚦 Estado atual (por onde começar uma conversa nova)

- O site está **completo e funcional localmente**, com 132 categorias e 588 conteúdos migrados, e **9 painéis administrativos** (Organizador, Adicionar Arquivos, Painel Central Tela 1, Tela 2, Barra Superior, Estrutura de Árvores, Área do Site, Editor do Rodapé, Central de Inteligência) — agora com **acesso delegável por usuário/grupo** via Autenticação e Autorização.
- **Deploy**: o PythonAnywhere foi **abandonado** (decisão de 2026-07-10). O destino final é o servidor da SEDU em `curriculo.sedu.es.gov.br`. Enquanto isso, demonstrações são feitas localmente via ngrok, e a **infraestrutura Docker (Postgres) + Backup/Restore já está pronta** para entregar à SEDU.
- **Leva mais recente (2026-07-22 — "parte 34")**: **4 correções de UX e bugs** — (1) **Selects cortando texto**: altura fixa 38px aplicada em 4 painéis (Editor do Rodapé, Área do Site, Organizador, Estrutura de Árvores) — texto em caixas de seleção agora visível por completo, sem truncamento. (2) **Títulos de colunas extras com formatação rich text**: campo `ColunaExtra.titulo` mudou de `CharField` para `TextField`, editor `RichTextWidget` injetado diretamente na view `area_do_site_view` — suporta negrito/itálico/alinhamento/listas; (3) **Resposta em massa para comentários**: nova ação `responder_em_massa` no `ComentarioAdmin` (além de aprovar/recusar/excluir em massa já existentes) — redireciona para tela intermediária (`templates/admin/comentario_responder_massa.html`), textarea de resposta, aplicada simultaneamente a todos os comentários selecionados via `queryset.update(resposta=..., data_resposta=timezone.now())`; (4) **Vídeo sem iframe (elimina erro 153 do YouTube)**: removido `<iframe srcdoc>` que quebrava quando dono do vídeo desabilitava embedding — agora SEMPRE renderiza botão `<a target="_blank" href=...>Assistir vídeo</a>` que abre URL em nova aba, elimina o erro de vez para qualquer vídeo (YouTube com/sem embedding bloqueado, Vimeo, ou link genérico); property `video_embed_valido` e método `get_video_embed_url()` continuam existindo no models.py (regex robusto mantido, inofensivo, base se precisar reativar embed no futuro). Migração `conteudo/0036` (CharField→TextField em ColunaExtra). **Zero breaking changes** — apenas melhorias de UX e resolução de bugs reportados pelo Dan. Testado ponta a ponta: 4 painéis carregando 200, editor rich text renderizando, respostas aplicadas a múltiplos comentários, vídeo sem iframe funcionando para YouTube/genérico. Detalhes no histórico item 47.
- **Leva anterior (2026-07-21 — "parte 33")**: **Comentários também em todos os botões (categorias) do site** — o Dan pediu que todo botão com conteúdo (ou criado no futuro) tenha, no rodapé da página, a mesma seção de comentários que já existia só nos conteúdos. Solução: campo `Comentario.categoria` (FK opcional, migração `conteudo/0035`) ao lado do `conteudo` já existente (agora também opcional) — mesmo padrão de FK dual mutuamente exclusiva já usado em `Anexo` (Conteudo OU Categoria, nunca os dois). A view `categoria_detalhe` ganhou a mesma lógica de busca/POST/moderação que `conteudo_detalhe` já tinha (comentários publicados, respostas aninhadas via `parent`, votos 👍/👎), e o template `categoria.html` ganhou a MESMA seção de comentários (HTML, CSS e JS idênticos ao de `conteudo_detalhe.html` — copy-paste proposital para manter consistência visual). **Como é resolvido pela própria view/template da página de categoria, vale automaticamente para QUALQUER botão do site — inclusive os criados depois, por qualquer painel (Painel Central, Organizador, Estrutura de Árvores, Área do Site)** — não foi preciso (nem faria sentido) marcar um por um; é uma regra estrutural, não uma configuração por botão. Vale também na página "Documentos Curriculares" (índice geral). Admin (`ComentarioAdmin`) atualizado: coluna "Conteúdo / Botão" mostra o link certo para qualquer um dos dois, "Local" mostra "página do botão" quando for comentário de categoria, "Ver no site" aponta para `/categoria/<slug>/#comentarios` (corrigido também `id="comentarios"` que faltava nas duas páginas — antes o link "Ver no site" não pulava para a seção). Testado ponta a ponta via Django test client: comentário criado numa categoria (pendente → aprovado → aparece no site), voto AJAX, resposta aninhada, página de índice geral também com comentários, E regressão confirmada de que comentários em Conteúdo continuam funcionando exatamente como antes (campo `categoria=None` nesse caso). Zero breaking changes. Detalhes no histórico item 46.
- **Leva anterior (2026-07-21 — "parte 32")**: implementado o documento `implementar.md` enviado pelo Dan — 9 pedidos: (1) **Estrutura de Árvores**: galeria de "Ícones personalizados enviados" agora funciona de verdade — clicar num ícone da galeria + "Salvar ícone" aplica aquele arquivo já existente ao botão selecionado (sem precisar reenviar), e novo botão dedicado "Excluir ícone" remove o ícone personalizado do botão em 1 clique (sem precisar marcar checkbox + salvar separadamente); (2) **"Aparecer em Conteúdos Recentes" para botões raiz**: o campo já existente `Categoria.mostrar_conteudos_recentes` agora também faz o BOTÃO aparecer como card na área "Conteúdos recentes" da home (antes só valia para os conteúdos de dentro dele) — como é o mesmo campo usado em todos os painéis (Django Admin, Estrutura de Árvores, Painel Central), a correção vale automaticamente em todos eles; (3-5) **Imagens do rodapé**: novo modelo `RodapeImagem` (imagem, largura, altura, alinhamento esquerda/centro/direita, URL opcional que vira link, ordem), gerenciado direto no painel "Editor do Rodapé" (nova seção "Imagens do rodapé", adicionar/excluir), renderizadas em uma faixa nova abaixo das 3 colunas — faixa de **altura fixa** (44px desktop/36px mobile), as imagens sempre se ajustam ao espaço via `object-fit:contain` e nunca aumentam a altura do rodapé, não importa quantas ou de que tamanho; (6) **Nome do botão "Currículo Atual" configurável**: novo campo `ConfiguracaoSite.nome_curriculo_atual`, editável em Django Admin → Configuração do site → "🎓 Botão Currículo Atual", usado na pílula central da home no lugar do texto fixo; (7) **Botões na área central**: já era possível via painel "Botões da Barra Superior" (`/admin/barra-superior/`, checkbox "Central?" + campo "Ordem" + link "Criar novo botão") desde a parte 13 — não foi criado um painel novo redundante, só confirmado/documentado que esse já atende ao pedido (marcar botões existentes, criar novos, reordenar); (8-9) **Identidade visual do cabeçalho**: novos campos em `ConfiguracaoSite` — brasão personalizado (`brasao_imagem` + alinhamento/largura/altura, opcional, com fallback para o brasão padrão do ES) e um segundo logotipo opcional (`logo2_imagem` + alinhamento/largura/altura, ex.: "Logo do Currículo"), editáveis em Django Admin → Configuração do site (2 novos fieldsets "🎖️ Identidade visual"). A barra superior mantém **altura fixa** (58px desktop, com os mesmos breakpoints responsivos já existentes) — os logotipos ficam dentro de um `.header-logo-slot` com `object-fit:contain`, nunca esticam a barra. Migração `conteudo/0034` (`RodapeImagem` + 9 campos novos em `ConfiguracaoSite`). Testado ponta a ponta via Django test client: aplicar/excluir ícone da galeria, categoria marcada aparecendo em Recentes, adicionar/renderizar/excluir imagem do rodapé, brasão personalizado no header, nome do Currículo Atual customizado — tudo confirmado funcionando, e a home/header/footer/admin continuam pixel-a-pixel iguais a antes quando nenhum campo novo é preenchido (compatibilidade 100%, nada removido). Detalhes no histórico item 45.
- **Leva anterior (2026-07-19 — "parte 31")**: **Organizador — "Mover selecionados para" mostra a árvore inteira de botões** — o Dan reportou que o select de destino no Organizador (`/admin/organizar/`) só mostrava alguns vizinhos (categoria pai + subcategorias), sem opção de escolher qualquer botão do site (diferente da Estrutura de Árvores, que já tinha isso desde a parte 10). Corrigido: o select agora lista TODOS os 133 botões ativos do site em formato de árvore indentada (novo helper `_arvore_flat_categorias()` em `conteudo/admin_views.py`, mesmo padrão do `_arvore_flat()` já usado no Painel Central), com caixa de busca instantânea sem acento (reaproveitado `filtro_select.js`, já usado no "Categoria pai" do Django Admin). Testado: conteúdo movido via o select da árvore completa para um botão fora dos vizinhos imediatos, confirmado no banco. Detalhes no histórico item 44.
- **Leva anterior (2026-07-18 — "parte 30")**: **Backup e Restauração Completa do Docker** — 2 novos `.bat` para fazer backup íntegro (banco Postgres + mídia + código) e restaurar em outro Windows/servidor. Fluxo: rodar **BACKUP DOCKER COMPLETO.bat** → copia pasta gerada para outro PC → roda **RESTAURAR ESTE BACKUP.bat** → site Docker com todos os dados está pronto. Testado ponta a ponta: gerou `banco_postgres.sql` (931 KB), `media_data.tar.gz` (265 MB, 259 arquivos), `codigo_projeto.zip` — tudo íntegro e restaurado com sucesso. Detalhes no histórico item 43.
- **Leva anterior (2026-07-18 — "parte 29")**: **Infraestrutura Docker com PostgreSQL pronta para produção** — o projeto agora suporta rodar em containers Docker com PostgreSQL, mantendo SQLite como padrão local. Novo arquivo `docker-compose.yml` com 2 serviços (db: Postgres 16, web: Django), variáveis de ambiente condicionais (`DOCKER_POSTGRES=1`), e novo `.bat` "ATUALIZAR BANCO DOCKER.bat" que sincroniza os dados do SQLite local para o Postgres do Docker com um clique (dumpdata → docker up → migrate → flush → loaddata). Ambiente local totalmente **intacto** — sem a variável de ambiente, o Django continua usando SQLite exatamente como antes. Adicionado `psycopg2-binary` às dependências. Testado ponta a ponta: 3674 registros (132 categorias, 588 conteúdos) importados com sucesso do banco local para o Postgres do Docker. Detalhes no histórico item 42.
- **Leva anterior (2026-07-18 — "parte 28")**: **Banner da home vira faixa fina + imagem recortada em formato faixa** — o Dan achou o banner (ajuste automático da parte 27) "muito alto" e pediu "a mais fina possível, bem fina e discreta". Duas coisas: (1) a imagem do skyline do ES (1376×768, quase quadrada) foi recortada via Pillow em **formato faixa** (`media/banners/hero-faixa.png`, 1376×420, proporção 3.28:1) removendo só o excesso de céu/chão vazios — desenho inteiro mantido; (2) o modo de **altura fixa** (`altura_personalizada`/classe `--fixo`) foi trocado de `contain`+blur (parte 26/27) para **`object-fit:cover`** — o banner fica com a altura exata escolhida e a imagem PREENCHE a faixa (sem barras, sem desfoque, recorta um pouco pra caber). O banner da home foi setado para **130px** (`altura_personalizada=130`) = faixa fina e discreta. O ajuste automático (parte 27, imagem inteira sem cortar) continua sendo o padrão quando `altura_personalizada` está vazio. Migração `conteudo/0033` (só help_text). Detalhes no histórico item 41.
- **Leva anterior (2026-07-18 — "parte 27")**: **Banner com AJUSTE AUTOMÁTICO à imagem (largura total, sem cortar, sem barras)** — a parte 26 tinha corrigido o corte trocando `cover` por `contain`, mas o Dan reprovou o resultado (a imagem ficava pequena no centro com barras desfocadas nas laterais dentro de uma faixa de altura fixa). Agora o banner (home + categoria) usa **ajuste automático**: a imagem ocupa **100% da largura** da página e a **altura acompanha a proporção da imagem** (`width:100%; height:auto`) — enche de ponta a ponta, mostra a imagem INTEIRA (nunca corta) e sem faixas vazias/desfocadas. Funciona sozinho para QUALQUER imagem enviada. ⚠️ Consequência geométrica inevitável: a altura do banner passa a depender da proporção da imagem (imagem quase quadrada → banner alto; imagem larga-e-baixa tipo faixa → banner baixo). Para um banner baixo, o Dan sobe uma imagem já no formato faixa. O campo "Altura fixa em pixels" (ex-"Altura personalizada", parte 26) virou **opcional e secundário**: se preenchido, força uma faixa de altura fixa com a imagem inteira dentro (contain) + fundo desfocado (classe `.hero-slide--fixo`/`.cat-banner-item--fixo`); vazio (padrão/recomendado) = ajuste automático. O campo `tamanho` (Pequeno/Médio/Grande) virou legado (não afeta mais o render — o ajuste automático ignora). Migração `conteudo/0032` (só help_text/verbose_name). Detalhes no histórico item 40.
- **Leva anterior (2026-07-17 — "parte 26")**: **Banner da home nunca mais corta a imagem + altura personalizável** — o banner central (hero) e os banners de categoria usavam `object-fit:cover`, que cortava topo/base de imagens com proporção diferente do espaço (bug real, reportado pelo Dan: "veja agora ela está cortada"). Corrigido para a mesma técnica já usada no carrossel/cartazes/destaques: imagem INTEIRA (`object-fit:contain`) sobre um fundo desfocado da própria imagem preenchendo as sobras (`::before` com blur+scale). Além disso, novo campo **"Altura personalizada (px)"** no admin de Banner. Migração `conteudo/0031`. **Substituído/refinado pela parte 27** (o `contain` numa faixa fixa deixava barras — parte 27 troca para ajuste automático). Detalhes no histórico item 39.
- **Leva anterior (2026-07-17 — "parte 25")**: **"Vários links de uma vez" expandido para os outros painéis** — depois da parte 24 (só Estrutura de Árvores), o mesmo recurso (linhas dinâmicas Nome + URL, botão "+ Adicionar outro link") chegou a: **Painel Central** (3 pontos: Criar novo botão, Criar subárea nos botões marcados, Editar botão selecionado), **Organizador** (2 pontos: Criar novo botão dentro de X, Adicionar novo arquivo ou URL a X) e **Área do Site** (1 ponto: "URL dentro do botão" da seção "Criar como botão completo do site"). Todos os campos de URL única já existentes foram mantidos intactos — o recurso novo é sempre um acréscimo ao lado deles. Backend: novo helper `_criar_links_extra()` duplicado em `painel/views.py` e `conteudo/admin_views.py` (mesma lógica da `_api_associar_links` da Estrutura, adaptada a cada arquivo) — lê listas paralelas `{prefixo}_link_nome`/`{prefixo}_link_url` e cria 1 `Conteudo(tipo='link')` por linha preenchida. A validação de "Adicionar novo arquivo ou URL" no Organizador foi ajustada para não bloquear quando só os links extras (sem URL única/arquivo) forem preenchidos. Detalhes no histórico item 38.
- **Leva anterior (2026-07-17 — "parte 24")**: **Vários links de URL de uma vez, dentro de botões/subbotões/subáreas (Estrutura de Árvores)** — aproveitando a base do arrastar-e-soltar (parte 23), agora dá pra anexar VÁRIOS links (não arquivos) de uma vez, em 2 pontos: (1) modal "Criar novo botão/subbotão" — abaixo do campo único "URL / Link" já existente (que continua funcionando igual), nova seção "Mais links / URLs" com linhas dinâmicas (Nome + URL) e botão "+ Adicionar outro link"; (2) painel de detalhes de qualquer botão/subbotão/subárea já existente → seção "Conteúdos" → nova subseção "Adicionar vários links de uma vez", mesmo padrão de linhas dinâmicas. Cada linha vira um `Conteudo(tipo='link')` na categoria; se o nome ficar em branco, usa o nome do próprio botão como título (mesmo comportamento do campo único antigo). Nova action AJAX `associar_links` em `conteudo/arvore_views.py` (`_api_associar_links`) + `_api_criar` passou a aceitar `link_nome`/`link_url` (getlist) na criação. Helper JS `EA._novaLinhaLink()`/`EA._coletarLinks()` reutilizável. Zero mudança de banco (migração não foi necessária — usa o model `Conteudo` já existente). Detalhes no histórico item 37.
- **Leva anterior (2026-07-17 — "parte 23")**: **Arrastar-e-soltar (drag-and-drop) expandido para TODOS os painéis com seções de anexar arquivos** — depois da parte 22 (só Estrutura de Árvores), agora Painel Central (4 pontos: Criar novo botão, Criar subárea, Editar botão selecionado, Anexos do conteúdo), Organizador (2 pontos: Criar novo botão, Adicionar novo arquivo/URL) e Área do Site (Anexos rápidos do botão completo) também ganharam zonas de arrastar-e-soltar. O Adicionar Arquivos (tabela de linhas) também ganhou dropzone que preenche as linhas automaticamente. Novo arquivo `static/js/dropzone.js` (helper genérico reutilizável, `attachDropzone()`, ativado via `data-dropzone-input`/`data-dropzone-texto`). Únicos 2 ajustes de backend: `_api_upload_anexo` (Estrutura de Árvores, campo novo `arquivos`) e `_editar_botao` (Painel Central, `editar_anexo` virou `getlist` — antes só aceitava 1 arquivo). Todos os outros pontos JÁ aceitavam múltiplos arquivos no backend (via `getlist` ou loop `arquivo_0..49`), então só precisaram de interface visual nova, zero mudança de backend. Ícones/imagens únicas (não são "anexar") ficaram de fora de propósito. Detalhes no histórico item 36.
- **Leva anterior (2026-07-17 — "parte 22")**: **Arrastar-e-soltar (drag-and-drop) de múltiplos arquivos na Estrutura de Árvores** — a seção "Anexos" de qualquer botão/subbotão/subárea (ao abrir seu painel de detalhes) e o modal "Criar novo botão/subbotão" agora têm uma zona de arrastar-e-soltar (`.ea-dropzone`) além do clique tradicional — dá pra soltar vários arquivos de uma vez, ou clicar para abrir o seletor normal. Backend (`_api_upload_anexo`) passou a aceitar múltiplos arquivos num campo novo (`arquivos`, via `getlist`), mantendo o campo antigo (`arquivo`, singular) 100% funcional para compatibilidade. Helper JS reutilizável `EA._attachDropzone()`. Zero mudança visual/funcional fora dessas duas zonas. Detalhes no histórico item 35.
- **Leva anterior (2026-07-17 — "parte 21")**: **Delegação de acesso aos painéis administrativos** — cada um dos 8 painéis personalizados (Organizador, Adicionar Arquivos, Painel Central, Barra Superior, Estrutura de Árvores, Editor do Rodapé, Área do Site, Central de Inteligência) ganhou uma permissão própria do Django (`Meta.permissions` em `ConfiguracaoSite`/`Vinculo`/`AlertaInteligencia`), controlável nativamente em **Admin → Autenticação e Autorização → Usuários/Grupos**, sem UI nova. Antes, qualquer usuário "membro da equipe" (`is_staff`) acessava todos os painéis igualmente; agora o Dan pode marcar exatamente quais painéis cada usuário (ou grupo) enxerga e acessa. Superusuário sempre tem acesso total; os 3 usuários atuais (`ridan`, `rabalista`, `kayode`) são todos superusuários, então **nada mudou para quem já usa o sistema** — o controle só passa a valer para novos usuários staff não-superusuário que o Dan criar. Dashboard esconde o banner de painéis sem permissão; acessar a URL direto sem permissão retorna 403. Ver seção dedicada "Delegação de acesso aos painéis administrativos" e histórico item 34.
- **Leva anterior (2026-07-17 — "parte 20")**: **Botões da "Área do Site" podem virar botões completos do site** — no formulário "Adicionar botão" de cada coluna extra, novo checkbox "Criar como botão completo do site (aparece nas árvores de botões)": quando marcado (e sem escolher uma categoria já existente), cria de fato uma `Categoria` nova, aninhada em "Botões novos criados" (mesmo bucket oculto já usado pelo Painel Central/Estrutura de Árvores quando nenhum pai é escolhido) — a partir daí o botão aparece em TODAS as árvores (Estrutura de Árvores, Painel Central, Organizador, Barra Superior) e aceita tudo que os outros botões aceitam (conteúdos, subbotões, anexos). Também ganhou campos de **URL rápida** e **anexos rápidos** para preencher o botão (novo ou existente) sem precisar abrir a árvore separadamente — mesmo padrão já usado em "Criar subcategoria" do Organizador. Comportamento padrão (checkbox desmarcado) continua **idêntico a antes** — zero mudanças no fluxo existente. Detalhes no histórico item 33.
- **Leva anterior (2026-07-17 — "parte 19")**: **Ícone também nas colunas extras** — a criação/edição de coluna extra (painel "Área do Site") ganhou o mesmo seletor de ícone das 3 seções fixas (Font Awesome via IconPicker OU upload de imagem, sempre com fundo transparente). Novos campos `ColunaExtra.icone`/`icone_imagem` (migração 0029). O ícone aparece antes do título de cada coluna extra na home. Detalhes no histórico item 32.
- **Leva anterior (2026-07-17 — "parte 18")**: **Ícones das 3 seções da home** — painel "Área do Site" ganhou seletor de ícone para "Destaques", "Conteúdos recentes" e "Navegue por área": escolha entre os ícones padrão do site (IconPicker, mesma grade usada em Conteúdo/Categoria) OU envie uma imagem em qualquer formato — a imagem sempre é exibida com **fundo transparente** (classe `.title-icon.sem-fundo` + `object-fit:contain`), sem prejudicar a estética do site. Novos campos em `ConfiguracaoSite`: `icone_destaques/icone_recentes/icone_areas` (Font Awesome) + `icone_destaques_imagem/icone_recentes_imagem/icone_areas_imagem` (upload, prioridade sobre o FA). Migração 0028. Detalhes no histórico item 31.
- **Leva anterior (2026-07-17 — "parte 17")**: **Novo painel "Área do Site"** — gerencia (1) o texto/formatação (negrito, itálico, sublinhado, alinhamento, lista) dos títulos das 3 seções da home ("Destaques", "Conteúdos recentes", "Navegue por área") via `ConfiguracaoSite.titulo_destaques/titulo_recentes/titulo_areas` (TextField HTML, RichTextWidget, migração 0027); (2) colunas extras opcionais à esquerda/direita da faixa "Recentes + Navegue por área" (novos modelos `ColunaExtra` e `ColunaExtraBotao`), cada uma com título e botões próprios (nome + categoria do site OU link externo + ícone FA/imagem). View `area_do_site_view` em `conteudo/admin_views.py`, template `templates/admin/area_do_site.html`, URL `/admin/area-do-site/`, banner ciano no dashboard. `home.html` envolve `.home-split` num `.home-split-wrap` flex para acomodar as colunas extras nas laterais. Detalhes no histórico item 30.
- **Leva anterior (2026-07-17 — "parte 16")**: **Gerenciamento de Destaques: campo `destaque_gerenciado` para controlar visibilidade** — (1) novo campo `Conteudo.destaque_gerenciado` (BooleanField, migração 0026) marca "este item pertence à área de Destaques do Organizador"; (2) lista de destaques agora mostra TODOS com `destaque_gerenciado=True`, ocultos ou não (usando campo separado `destaque` para visibilidade na home); (3) checkbox "Ocultar" continua funcionando (liga/desliga `destaque`), mas **item permanece na lista de gerenciamento** para reativação posterior; (4) conteúdos criados via "Criar Destaque" nascem com `destaque_gerenciado=True`; (5) 3 destaques existentes marcados retroativamente. Detalhes no histórico item 29.
- **Leva anterior (2026-07-17 — "parte 15")**: **Botões excluir no Organizador** — (1) coluna "Excluir" 🗑️ na tabela "Conteúdos em [botão]" com confirmação; (2) nova tabela "Arquivos anexados" mostrando todos os Anexo ligados à categoria com botão excluir; (3) ações `excluir_conteudo` e `excluir_anexo` no backend com validação de segurança. Detalhes no histórico item 28.
- **Leva anterior (2026-07-17 — "parte 14")**: **Subáreas vs Botões: campo `mostrar_como_card` para controlar duplicação** — (1) novo campo `Categoria.mostrar_como_card` (BooleanField, padrão True) distingue botões/subbotões estruturais (aparecem como chip + card grande) de subáreas rápidas (aparecem só como chip, sem duplicar); (2) função "Criar subárea nos botões marcados" agora cria com `mostrar_como_card=False` automaticamente; (3) "Criar novo botão" cria com `mostrar_como_card=True` (padrão); (4) campo editável no Django Admin de Categoria para ajuste manual. Detalhes no histórico item 27.
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
- **Migrações aplicadas**: `conteudo/0012-0036` + `painel/0002-0003` + `inteligencia/0002`. Migração **`conteudo/0036`** (`ColunaExtra.titulo` CharField→TextField, parte 34, 2026-07-22) é a mais recente. Anterior a ela: **`conteudo/0035`** (`Comentario.categoria` opcional, parte 33, 2026-07-21).
- **Arquivos Docker novos**: `Dockerfile` (Python 3.12 slim + dependências de sistema), `docker-compose.yml` (db: Postgres 16 + volumes, web: Django com migrations automáticas), `BAT SEDU/ATUALIZAR BANCO DOCKER.bat` (sincronização local→Docker em um clique).
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
- `titulo`, `subtitulo`, `imagem` (**opcional desde a 0012**), **`url_imagem`** (URL externa; tem prioridade sobre o arquivo), `link`, `tamanho` (**legado desde a parte 27** — não afeta mais o render; o ajuste automático ignora), **`altura_personalizada`** (px, opcional, migração 0031 — força faixa de altura fixa quando preenchida; vazio = ajuste automático), `ordem`, `ativo`, `categoria`
- Property **`imagem_src`** — devolve `url_imagem` ou `imagem.url`; os templates SEMPRE usam `imagem_src`
- **Ajuste automático (padrão, parte 27)**: a imagem ocupa 100% da largura e a altura acompanha a proporção (`.hero-slide img`/`.cat-banner-item img` com `width:100%;height:auto`) — enche tudo, NUNCA corta, sem barras. A altura do banner passa a depender da proporção da imagem enviada (para banner baixo, subir imagem em formato faixa).
- **Altura fixa (opcional, parte 28)**: preencher `altura_personalizada` liga a classe `.hero-slide--fixo`/`.cat-banner-item--fixo` → o banner fica com essa altura exata e a imagem **PREENCHE** a faixa (`object-fit:cover`, sem barras/desfoque, recorta um pouco pra caber). Serve para uma **faixa fina e discreta** (ex.: 120-150px). Quanto menor o número, mais fina. (Antes da parte 28 era `contain`+blur — trocado para `cover` a pedido do Dan que queria faixa fina cheia.)
- Largura sempre 100% da tela — sem campo de largura, é assim que banners funcionam
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
Comentários moderados (3 estados, migração 0019 — 2026-07-13). Desde a migração **0035** (parte 33, 2026-07-21), aceita comentários tanto em Conteúdo quanto em Categoria (botão) — FK dual mutuamente exclusiva, mesmo padrão do `Anexo`.
- **`conteudo`** (FK CASCADE, **opcional** desde 0035) e **`categoria`** (FK CASCADE, opcional, novo em 0035) — um comentário pertence a UM dos dois, nunca aos dois; property `origem` devolve `self.conteudo or self.categoria`
- `nome`, `email` (opcional), `texto`, `data_criacao` (auto_now_add)
- **`status`** (CharField, choices: `pendente`/`publicado`/`recusado`, default=`pendente`) — controla visibilidade: só `publicado` aparece no site
- **`resposta`** (TextField, blank) — resposta do administrador, exibida abaixo do comentário no site com ícone de escudo e data
- **`data_resposta`** (DateTimeField, null/blank) — preenchida automaticamente pelo `save_model` do admin ao inserir resposta
- **`aprovado`** (BooleanField, `editable=False`, default=False) — campo legado mantido para compatibilidade; não sincroniza com `status`
- Property `publicado` → `self.status == 'publicado'`
- **Comentários de Conteúdo NÃO aparecem** em conteúdos com `tipo='link'` — verificado na view com `exibir_comentarios = conteudo.tipo != 'link'`. **Comentários de Categoria (botão) aparecem em TODOS os botões**, sem exceção — regra estrutural resolvida pela própria view `categoria_detalhe`, não uma configuração por botão; vale automaticamente para botões criados no futuro por qualquer painel
- Admin: `ComentarioAdmin` com badges coloridos ⏳/✅/❌, ações em lote "Aprovar"/"Recusar", campos do visitante readonly, seção colapsável de resposta; coluna "Conteúdo / Botão" mostra o link certo para qualquer um dos dois; "Ver no site" aponta para `/conteudo/<slug>/#comentarios` ou `/categoria/<slug>/#comentarios` conforme o caso

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
6. **Editor do Rodapé** (`/admin/editor-rodape/`, cartão cinza no dashboard) — edita textos, links, ícones e imagens das 3 colunas do rodapé + copyright + contato/endereço.
7. **Estrutura de Árvores** (`/admin/estrutura-arvores/`, banner âmbar) — ver seção dedicada acima (histórico item 24).
8. **Área do Site** (`/admin/area-do-site/`, banner ciano no dashboard, partes 17-18 — 2026-07-17) — (a) formata (negrito/itálico/sublinhado/alinhamento/lista) os títulos das seções "Destaques", "Conteúdos recentes" e "Navegue por área" da home via `RichTextWidget`; (b) escolhe o ÍCONE de cada uma dessas 3 seções — padrão do site (IconPicker) OU imagem enviada em qualquer formato, sempre com fundo transparente; (c) cria colunas extras (`ColunaExtra`) à esquerda ou direita da faixa "Recentes + Navegue por área", cada uma com botões próprios (`ColunaExtraBotao` — nome + categoria do site OU link externo + ícone).
9. **Central de Inteligência do Portal** (`/admin/inteligencia/`, banner vermelho no dashboard, app `inteligencia`) — estatísticas de uso do portal: acessos, downloads, buscas, rankings de botões/subbotões/documentos, dispositivos/navegadores/referrer, alertas (documento sem acesso, link quebrado, pico de acesso), exportação Excel/PDF. Não documentado em detalhe neste arquivo (fora do escopo das "partes" numeradas) — ver `inteligencia/models.py`, `inteligencia/services.py`, `inteligencia/views.py` para detalhes de implementação.

## Delegação de acesso aos painéis administrativos (parte 21 — 2026-07-17)

Cada um dos 8 painéis acima (1-9, exceto o Django Admin nativo) agora tem uma **permissão própria do Django**, controlável na tela nativa **Autenticação e Autorização** (`/admin/auth/`), sem precisar de código novo para delegar acesso.

**Como usar** (Admin → Autenticação e Autorização):
- **Usuários → (escolher usuário) → seção "Permissões do usuário"**: marcar as permissões desejadas, com o rótulo `Pode acessar: <nome do painel>` (aparecem junto às permissões padrão dos models `Configuração do site`, `Vínculo de publicação` e `Alerta`).
- **Recomendado**: criar **Grupos** (ex.: "Editor de Conteúdo") com um conjunto de permissões marcadas, e depois só atribuir usuários ao grupo — mais rápido que marcar caixinha por usuário toda vez.
- O usuário também precisa ter **"Membro da equipe" (`is_staff`) marcado**, senão nem entra no `/admin/` (requisito que já existia, não mudou).
- **Superusuário sempre vê e acessa todos os painéis**, independente de qualquer permissão marcada ou não.
- **Usuários novos começam sem nenhum dos 8 acessos** (seguro por padrão) até alguém marcar explicitamente.

**As 8 permissões e para onde apontam:**

| Permissão (`app.codename`) | Painel |
|---|---|
| `conteudo.pode_acessar_organizador` | Organizador de Conteúdo |
| `conteudo.pode_acessar_adicionar_arquivos` | Adicionar Arquivos |
| `painel.pode_acessar_painel_central` | Painel Administrativo Completo (Telas 1 e 2) |
| `conteudo.pode_acessar_barra_superior` | Botões da Barra Superior |
| `conteudo.pode_acessar_estrutura_arvores` | Estrutura de Árvores |
| `conteudo.pode_acessar_editor_rodape` | Editor do Rodapé |
| `conteudo.pode_acessar_area_do_site` | Área do Site |
| `inteligencia.pode_acessar_inteligencia` | Central de Inteligência do Portal |

**Implementação**: `Meta.permissions` em `ConfiguracaoSite` (conteudo, 6 permissões), `Vinculo` (painel, 1) e `AlertaInteligencia` (inteligencia, 1) — migrações `conteudo/0030`, `painel/0003`, `inteligencia/0002` (só `AlterModelOptions`, nenhuma coluna de tabela alterada). Decorator `exige_permissao_painel(codename)` em `conteudo/permissoes.py`, empilhado junto ao `@staff_member_required` já existente em cada view (sem substituir nada). Dashboard (`templates/admin/index.html`) esconde o banner de qualquer painel que o usuário logado não tenha permissão de acessar (`{% if perms.app.codename %}`), mas a segurança de verdade está nas views — acessar a URL direto sem permissão sempre retorna 403.

**Testado fim-a-ponta** (via Django test client): usuário staff sem superusuário e sem nenhuma permissão → dashboard sem nenhum dos 8 banners, todas as 8 URLs retornam 403; concedida 1 permissão (Organizador) → só aquele banner aparece, só aquela URL abre (200), as outras 7 continuam em 403; superusuário (`ridan`) → todos os 8 banners e todas as 8 URLs continuam funcionando normalmente (zero regressão para contas existentes, já que os 3 usuários atuais — `ridan`, `rabalista`, `kayode` — são todos superusuários).

## Comportamentos importantes do front-end

- **Barra superior com menu "3 pontinhos" (⋯)**: quando os botões de categoria não cabem na barra azul, os excedentes vão automaticamente para um dropdown ⋯ (elementos `#navMore`/`#navMoreMenu` em `base.html`, lógica em `main.js` — recalcula no `resize`, que também dispara com zoom do navegador; folga de 6px contra arredondamento). No celular (≤768px) vale o hamburger e o ⋯ é desativado.
- **"Navegue por área" E "Conteúdos recentes" com botões quadrados** (2026-07-11): ambos em grid de 3 colunas (2 em ≤480px), ícone em cima + texto embaixo (13px). Nos quadrados de áreas a descrição pequena é ocultada; nos de recentes aparecem categoria/data pequenas (10px) e o título é limitado a 3 linhas (`-webkit-line-clamp`). O botão **"Currículo Atual" é uma pílula compacta CENTRALIZADA ACIMA das duas colunas** (div `.curriculo-atual-topo`, antes do `.home-split`). Ele é **hardcoded** no `home.html` (slug `curriculo-atual`), não vem do loop de categorias.
- **Cartazes/carrosséis nunca somem com zoom**: ver tabela de breakpoints na seção do modelo Cartaz. Botão "Eventos" agora entra em ≤1000px (mesma faixa em que as laterais somem — sem "faixa morta").
- **Cache-busting**: `base.html` carrega `style.css` com `?v=AAAAMMDD-N` (hoje `20260718-2`) e `main.js` com `?v=20260711-1`. **Sempre incrementar ao mudar CSS/JS**, senão o navegador usa a versão cacheada. Ao testar: Ctrl+Shift+R.
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

### 2026-07-17 — Botões excluir no Organizador de Conteúdo (parte 15)

**Problema**: no painel **Organizador de Conteúdo**, o Dan podia ver os conteúdos/URLs dentro de um botão (com opção de editar), mas não havia jeito de EXCLUIR — só mover ou editar. Idem para arquivos enviados direto pelo formulário verde "Adicionar novo arquivo ou URL" — eles viravam `Anexo` (não `Conteudo`) e nunca apareciam em lista com opção de excluir.

**Solução**:

1. **Coluna "Excluir" na tabela de conteúdos** (o que já estava em "Conteúdos em [botão]"):
   - Nova coluna ao lado de "Editar" com ícone de lixeira vermelha 🗑️
   - Clique exibe confirmação: "Excluir permanentemente '[título]'? Esta ação não pode ser desfeita."
   - Confirmando, o conteúdo é **excluído permanentemente** (não reversível como "Mover")

2. **Nova tabela "Arquivos anexados"** (logo abaixo de conteúdos):
   - Lista TODOS os `Anexo` ligados à categoria (arquivos enviados pelo formulário verde)
   - Cada linha: nome do arquivo (link clicável) + extensão + botão excluir 🗑️
   - Botão excluir com confirmação igual à de conteúdos
   - Só aparece se houver anexos

3. **Backend** (`conteudo/admin_views.py`):
   - Nova action `excluir_conteudo` — exclui conteúdo do banco (permanente)
   - Nova action `excluir_anexo` — exclui anexo do banco (com validação de categoria para segurança)
   - Context da view passa `anexos_categoria` ao template

4. **Template** (`templates/admin/organizar.html`):
   - Coluna "Excluir" adicionada à tabela de conteúdos (usando form inline com CSRF + confirmação JS)
   - Nova tabela "Arquivos anexados" renderizada condicionalmente se houver anexos

- **Versão de cache**: CSS/JS sem mudança (`?v=20260717-1` e `?v=20260711-1`)
- **Arquivos modificados**: `conteudo/admin_views.py` (2 actions + contexto), `templates/admin/organizar.html` (coluna excluir + tabela anexos)
- **Testado fim-a-ponta**: Conteúdo excluído via botão 🗑️ → permanentemente do banco ✓. Anexo subido via formulário verde → renderiza na tabela "Arquivos anexados" ✓. Anexo excluído via botão 🗑️ → permanentemente do banco ✓. Confirmação JS funciona.
- **Compatibilidade 100%**: nenhuma mudança quebrada — funcionalidades existentes (mover, editar) continuam normais.

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

### 2026-07-17 — Novo painel "Área do Site" (parte 17)

**Pedido do Dan**: gerenciar a área onde ficam escritos "Destaques", "Conteúdos recentes" e "Navegue por área" — formatar esses textos com todos os recursos de formatação, e poder criar uma nova coluna (esquerda ou direita das duas existentes) com botões personalizados dentro.

**1. Títulos das 3 seções com formatação rica** (migração `conteudo/0027`):
   - Novos campos em `ConfiguracaoSite`: `titulo_destaques`, `titulo_recentes`, `titulo_areas` (TextField, HTML, default = texto atual)
   - Editados via `RichTextWidget` já existente no projeto (mesmo editor usado em `home_texto`) — barra com negrito, itálico, sublinhado, alinhar esquerda/centro/direita, lista com marcadores, limpar formatação
   - Novo form `TituloSecoesForm` em `conteudo/forms.py`
   - `home.html` renderiza `{{ config.titulo_destaques|default:"Destaques"|safe }}` (e equivalentes) no lugar do texto fixo antigo

**2. Colunas extras com botões personalizados** (2 novos modelos):
   - `ColunaExtra`: `titulo`, `lado` (esquerda/direita), `ativa`, `ordem`
   - `ColunaExtraBotao`: `coluna` (FK), `nome`, `categoria` (FK opcional — abre categoria do site) OU `link_externo` (URL, tem prioridade), `icone` (Font Awesome), `icone_imagem` (upload), `ordem`
   - Quantas colunas o Dan quiser, em qualquer lado, cada uma com quantos botões quiser
   - Registrado também no Django Admin (`ColunaExtraAdmin` com inline de botões) como caminho alternativo

**3. Painel "Área do Site"** (`/admin/area-do-site/`, banner ciano no dashboard):
   - View `area_do_site_view` em `conteudo/admin_views.py` — actions: `salvar_titulos`, `criar_coluna`, `editar_coluna`, `excluir_coluna`, `criar_botao`, `excluir_botao`
   - Template `templates/admin/area_do_site.html` — seção 1 com os 3 editores ricos; seção 2 lista as colunas existentes (cada uma com seus botões, formulário para adicionar botão, formulário para editar/mover de lado/ativar-desativar, botão excluir) + formulário para criar nova coluna
   - URL registrada em `curriculo_sedu/urls.py`

**4. Home renderiza as colunas extras** (`templates/home.html` + `conteudo/views.py`):
   - `home()` busca `ColunaExtra.objects.filter(ativa=True)` e separa em `colunas_esquerda`/`colunas_direita`
   - `.home-split` (que já continha "Recentes" + "Navegue por área") foi envolvido por um novo `.home-split-wrap` (flex) — colunas da esquerda entram ANTES do `.home-split`, colunas da direita entram DEPOIS
   - Cada coluna extra renderiza como `.home-coluna-extra` com os botões em formato `.area-card` (mesmo visual dos cards de "Navegue por área")
   - CSS novo (`AJUSTES 2026-07-17 — Área do Site`): `.home-split-wrap` em flex com gap 32px; responsivo — empilha em coluna única abaixo de 1024px

- **Versão de cache**: CSS `?v=20260717-2` (incrementado de `-1`), JS sem mudança (`?v=20260711-1`)
- **Arquivos modificados**: `conteudo/models.py` (3 campos em ConfiguracaoSite + modelos ColunaExtra/ColunaExtraBotao), `conteudo/migrations/0027_colunaextra_configuracaosite_titulo_areas_and_more.py` (nova migração), `conteudo/forms.py` (TituloSecoesForm), `conteudo/admin_views.py` (area_do_site_view), `conteudo/admin.py` (ColunaExtraAdmin + inline), `conteudo/views.py` (home() busca colunas extras), `templates/admin/area_do_site.html` (novo), `templates/admin/index.html` (banner), `templates/home.html` (títulos via config + colunas extras), `static/css/style.css` (bloco novo), `templates/base.html` (cache-busting `-2`), `curriculo_sedu/urls.py` (rota nova)
- **Testado fim-a-ponta** (via Django test client E interface real no navegador): título com `<strong>` salvo e renderizado em negrito na home ✓; coluna criada aparece do lado escolhido ✓; botão apontando para categoria gera URL correta (`/categoria/<slug>/`) ✓; botão aparece na home dentro da coluna ✓; editar coluna (mudar de lado) funciona ✓; excluir botão e excluir coluna funcionam (cascade) ✓; layout flex sem sobreposição (`getBoundingClientRect` confirmado) ✓
- **Compatibilidade 100%**: nenhuma mudança quebrada — se nenhuma coluna extra existir, a home renderiza exatamente como antes (só o `.home-split-wrap` envolve o `.home-split`, sem efeito visual quando vazio)

### 2026-07-17 — Ícones das 3 seções da home (parte 18)

**Pedido do Dan**: escolher os ícones dos textos "Navegue por área", "Destaques" e "Conteúdo recente" entre os padrões do site, como também anexar qualquer formato de imagem, sempre com fundo transparente para não atrapalhar a estética.

**1. Novos campos em `ConfiguracaoSite`** (migração `conteudo/0028`):
   - `icone_destaques`, `icone_recentes` (default `fas fa-wand-magic-sparkles`), `icone_areas` (default `fas fa-compass`) — classe Font Awesome
   - `icone_destaques_imagem`, `icone_recentes_imagem`, `icone_areas_imagem` (FileField, `icones_secao/`, qualquer formato) — tem prioridade sobre o ícone Font Awesome quando preenchida

**2. Form `TituloSecoesForm`** (`conteudo/forms.py`): os 3 campos de ícone FA usam o `IconPicker` já existente no projeto (mesma grade de ícones usada em Conteúdo/Categoria). Os campos de imagem são tratados manualmente na view (fora do ModelForm), junto com checkboxes "Remover imagem" (`limpar_icone_X_imagem`).

**3. Painel "Área do Site"** (`templates/admin/area_do_site.html`): cada uma das 3 seções (Destaques/Recentes/Áreas) ganhou um bloco com: título (RichTextWidget), grade de ícones padrão (IconPicker), preview do ícone/imagem atual (com fundo quadriculado para visualizar transparência) + checkbox remover, e campo de upload de nova imagem. Form principal agora é `enctype="multipart/form-data"`.

**4. Renderização (`templates/home.html`)**: em cada uma das 3 seções, se há imagem enviada (`icone_X_imagem`), renderiza `<img class="icone-personalizado">` dentro de `<span class="title-icon sem-fundo">` (fundo removido); senão, renderiza o ícone Font Awesome escolhido (ou o padrão do site, se nenhum foi escolhido).

**5. CSS** (`static/css/style.css`, junto ao bloco `.title-icon`):
   ```css
   .title-icon.sem-fundo { background: none; }
   .title-icon .icone-personalizado { padding: 0; }
   ```
   Reutiliza a classe `.icone-personalizado` (já usada em botões/cards de conteúdo) que aplica `object-fit: contain` — a imagem nunca é cortada e nunca ganha fundo colorido atrás, mantendo a estética do site.

- **Versão de cache**: CSS `?v=20260717-3` (incrementado de `-2`), JS sem mudança
- **Arquivos modificados**: `conteudo/models.py` (6 campos novos em ConfiguracaoSite), `conteudo/migrations/0028_configuracaosite_icone_areas_and_more.py` (nova migração), `conteudo/forms.py` (TituloSecoesForm com IconPicker), `conteudo/admin_views.py` (area_do_site_view trata uploads/remoção de imagem), `templates/admin/area_do_site.html` (blocos de ícone por seção), `templates/home.html` (ícone dinâmico nas 3 seções), `static/css/style.css` (`.title-icon.sem-fundo`), `templates/base.html` (cache-busting `-3`)
- **Testado fim-a-ponta**: escolher ícone FA (fa-star) para Destaques → aparece na home ✓; enviar imagem PNG para Recentes → aparece com prioridade sobre o FA, classe `sem-fundo` aplicada ✓; remover a imagem enviada (checkbox) → volta ao ícone FA padrão (`fa-wand-magic-sparkles`) ✓
- **Compatibilidade 100%**: com os campos vazios (banco antigo), os ícones padrão (`fa-wand-magic-sparkles`/`fa-compass`) continuam aparecendo exatamente como antes; "Destaques" continua sem ícone até o Dan escolher um

### 2026-07-17 — Ícone também nas colunas extras (parte 19)

**Pedido do Dan**: ao criar uma nova coluna extra (painel "Área do Site"), também precisava da opção de escolher ícone padrão ou anexar arquivo — só existia isso para os botões dentro da coluna, não para o título da coluna em si.

**1. Novos campos em `ColunaExtra`** (migração `conteudo/0029`):
   - `icone` (CharField, Font Awesome)
   - `icone_imagem` (FileField, `icones_secao/`, qualquer formato) — prioridade sobre `icone`

**2. Formulário "Criar nova coluna"**: ganhou campo de texto para o ícone Font Awesome + campo de upload de imagem, lado a lado com título/lado.

**3. Formulário "Editar coluna" (rodapé de cada card de coluna)**: mesmos dois campos + checkbox "Remover imagem" (só aparece se já houver imagem enviada). Form ganhou `enctype="multipart/form-data"`.

**4. Cabeçalho de cada coluna no painel**: mostra o ícone atual (imagem ou Font Awesome) ao lado do título, antes dos badges de lado/ativa.

**5. `admin_views.py`** (`area_do_site_view`): `criar_coluna` agora lê `coluna_icone` do POST e trata `coluna_icone_imagem` de `request.FILES`; `editar_coluna` faz o mesmo + trata `limpar_coluna_icone_imagem` para remover.

**6. `home.html`**: cada coluna extra (`.home-coluna-extra`) agora renderiza o ícone antes do título, mesmo padrão das 3 seções fixas — `<span class="title-icon sem-fundo">` com imagem (`.icone-personalizado`, `object-fit:contain`) OU `<span class="title-icon">` com `<i>` Font Awesome, fundo transparente garantido pela mesma classe `.title-icon.sem-fundo` do CSS da Parte 18.

- **Versão de cache**: CSS `?v=20260717-4` (incrementado de `-3`), JS sem mudança
- **Arquivos modificados**: `conteudo/models.py` (2 campos novos em ColunaExtra), `conteudo/migrations/0029_colunaextra_icone_colunaextra_icone_imagem.py` (nova migração), `conteudo/admin_views.py` (criar_coluna/editar_coluna tratam ícone), `templates/admin/area_do_site.html` (campos de ícone nos 2 formulários + preview no cabeçalho), `templates/home.html` (ícone antes do título de cada coluna extra), `templates/base.html` (cache-busting `-4`)
- **Testado fim-a-ponta**: criar coluna com ícone FA (`fas fa-star`) → aparece na home ✓; editar coluna enviando imagem → tem prioridade sobre o FA, aparece com fundo transparente ✓; remover a imagem enviada → volta ao ícone FA ✓
- **Compatibilidade 100%**: colunas extras existentes sem ícone continuam renderizando só o título, sem nenhum ícone (comportamento anterior preservado)

### 2026-07-17 — Botões da Área do Site viram botões completos (parte 20)

**Pedido do Dan**: quando cria um botão dentro de uma coluna extra (painel "Área do Site"), precisava que ele aparecesse nas árvores de botões (Estrutura de Árvores, Painel Central, etc.), porque dentro dele vai colocar tudo que os outros botões suportam. Também pediu opção de anexar arquivo ou URL rápida na hora de criar, sem precisar ir até a árvore.

**Sem alterar nenhuma migração** — só lógica de view + template.

**1. Formulário "Adicionar botão"** (`templates/admin/area_do_site.html`): novo checkbox **"Criar como botão completo do site (aparece nas árvores de botões)"**. Ao marcar, revela (JS simples, sem lib externa) dois campos extras: "URL dentro do botão" e "Anexos dentro do botão" (múltiplos arquivos).

**2. Lógica em `admin_views.py` (`area_do_site_view`, action `criar_botao`)**:
   - Se **nenhuma** categoria existente foi escolhida **e** o checkbox foi marcado → cria uma `Categoria` **RAIZ** de verdade (`categoria_pai=None`, exatamente como "Currículo Atual" e qualquer outro botão principal — corrigido em 2026-07-17 depois de o Dan reportar que a versão inicial aninhava em "Botões novos criados" e não aparecia como esperado nas árvores) — `mostrar_menu_superior=False`, `mostrar_navegue_area=False` (não duplica na barra/home, já que o botão já aparece via a própria coluna extra)
   - Ícone Font Awesome/imagem informado no formulário do botão é aplicado também à nova `Categoria`
   - Se preenchida, a "URL rápida" vira um `Conteudo(tipo='link')` dentro dessa categoria (mesmo padrão de `criar_subcategoria`)
   - Se enviados, os "anexos rápidos" viram `Anexo` ligados à categoria
   - `ColunaExtraBotao.categoria` passa a apontar para essa nova categoria (o botão na home usa a property `url` que já resolve para `/categoria/<slug>/`)
   - **Se o checkbox NÃO for marcado** (comportamento padrão): fluxo 100% idêntico ao anterior — `botao_link` vira link externo puro, sem criar Categoria nenhuma

**3. Reaproveitamento de arquivo enviado**: como o mesmo `icone_imagem` do POST pode ser usado tanto na `Categoria` nova quanto no `ColunaExtraBotao`, foi adicionado `.seek(0)` antes de cada `.save()` — mesma armadilha já documentada no item de armadilhas conhecidas (arquivo reaproveitado para múltiplos destinos fica vazio no segundo `.save()` sem isso).

- **Arquivos modificados**: `conteudo/admin_views.py` (`criar_botao` reescrito), `templates/admin/area_do_site.html` (checkbox + campos extras + CSS `.as-botao-arvore-toggle`/`.as-botao-arvore-extra`)
- **Testado fim-a-ponta**: (a) botão SEM marcar checkbox → `categoria=None`, `link_externo` preenchido, comportamento antigo intacto ✓; (b) botão COM checkbox marcado + URL rápida + anexo rápido → nova `Categoria` **raiz** (`categoria_pai=None`) ✓, `mostrar_menu_superior=False`/`mostrar_navegue_area=False` ✓, `Conteudo` tipo link criado dentro dela ✓, `Anexo` criado dentro dela ✓, categoria aparece **entre as raízes** da árvore JSON da Estrutura de Árvores (`/admin/estrutura-arvores/api/?action=arvore_json`) ✓, aparece entre os `principais` usados pela Barra Superior (`categoria_pai__isnull=True`) ✓, botão na home aponta para `/categoria/<slug>/` corretamente ✓
- **Compatibilidade 100%**: nenhuma mudança em fluxo já existente — checkbox desmarcado (padrão) preserva o comportamento anterior sem qualquer diferença

### 2026-07-17 — Gerenciamento de Destaques: campo `destaque_gerenciado` (parte 16)

**Problema resolvido**: ao ocultar um destaque (usando checkbox "Ocultar"), o item **desaparecia completamente da lista de gerenciamento** do Organizador, impedindo reativação posterior.

**Root cause**: a query de destaques filtrava por `destaque=True`, então ao desmarcar esse checkbox, o item saía da lista de gerenciamento.

**Solução**: novo campo **`destaque_gerenciado`** (migração `conteudo/0026`) que marca "pertence à área de Destaques" **independentemente** de estar visível (`destaque=True`) ou oculto (`destaque=False`) no momento:

1. **Campo `Conteudo.destaque_gerenciado`** (BooleanField, default=False):
   - Ligado automaticamente quando conteúdo é criado via "Criar Destaque" no Organizador
   - Não pode ser alterado manualmente pelo usuário (é controle interno)
   - Help text: "Marcado automaticamente para itens criados na área 'Destaques do Site' (Organizador). Mantém item visível na lista mesmo quando ocultado."

2. **Query de destaques no Organizador** (`conteudo/admin_views.py`):
   - Mudou de: `filter(destaque=True)` 
   - Para: `filter(destaque_gerenciado=True)`
   - Resultado: lista mostra **todos** os itens criados aqui, ocultos ou não

3. **Checkbox "Ocultar"** (template `templates/admin/organizar.html`):
   - Continua ligando/desligando `destaque` (controla visibilidade na home)
   - MAS item permanece na lista (porque `destaque_gerenciado=True` não muda)
   - Fluxo: marca "Ocultar" → desaparece da home, mas fica visível no Organizador para reativar depois

4. **Ação `criar_destaque`** (`conteudo/admin_views.py`):
   - Detecta arquivo: se é imagem, salva em `imagem_destaque`; senão em `arquivo`
   - Define `destaque_gerenciado=True` automaticamente
   - Cria com `destaque=True` (visível na home)

5. **Retroativo** (não quebra banco antigo):
   - Dados antigos: `destaque_gerenciado=False` (padrão da migração)
   - Comando executado na sessão: marcou 3 destaques existentes com `destaque_gerenciado=True` para não sumirem

**Comportamento fim-a-ponta testado**:
- ✅ Criar destaque → nasce com `destaque_gerenciado=True` e `destaque=True` → aparece na home E na lista
- ✅ Marcar "Ocultar" → `destaque` vira False → sumiu da home, MAS permanece na lista do Organizador
- ✅ Desmarcar "Ocultar" (reativar) → `destaque` vira True → reaparece na home
- ✅ Compatibilidade 100%: nenhuma quebra em outros sistemas

- **Versão de cache**: CSS `?v=20260717-1` (sem mudança), JS `?v=20260711-1` (sem mudança)
- **Arquivos modificados**: `conteudo/models.py` (novo field), `conteudo/migrations/0026_destaque_gerenciado.py` (nova migração), `conteudo/admin_views.py` (query + criar_destaque + toggle_destaque), `conteudo/views.py` (nenhuma alteração — home continua filtrando `destaque=True`)
- **Testado**: criar → ocultar → permanece na lista → reativar → reaparece; 3 destaques antigos não sumiram

### 2026-07-17 — Delegação de acesso aos painéis administrativos (parte 21)

**Pedido do Dan**: dentro do painel administrativo, na área nativa "Autenticação e Autorização", poder delegar para usuários existentes e novos usuários **quem pode acessar qual painel** — sem quebrar o que já funciona.

**Situação anterior**: todos os 8 painéis personalizados (Organizador, Adicionar Arquivos, Painel Central, Barra Superior, Estrutura de Árvores, Editor do Rodapé, Área do Site, Central de Inteligência) só checavam `@staff_member_required` — qualquer usuário "membro da equipe" acessava todos igualmente, sem granularidade nenhuma.

**Solução**: 8 novas permissões customizadas do Django (uma por painel), usando `Meta.permissions` — as mesmas que já aparecem nativamente na tela de Usuário/Grupo em Autenticação e Autorização, junto com add/change/delete/view padrão. Zero tabela nova, zero campo novo — só uma lista extra dentro do `Meta` de um model que já existia em cada app.

1. **Permissões registradas** (`Meta.permissions`):
   - `conteudo.ConfiguracaoSite` (singleton de config do site) ganhou 6: `pode_acessar_organizador`, `pode_acessar_adicionar_arquivos`, `pode_acessar_barra_superior`, `pode_acessar_editor_rodape`, `pode_acessar_area_do_site`, `pode_acessar_estrutura_arvores`
   - `painel.Vinculo` ganhou 1: `pode_acessar_painel_central`
   - `inteligencia.AlertaInteligencia` ganhou 1: `pode_acessar_inteligencia`
   - Migrações `conteudo/0030`, `painel/0003`, `inteligencia/0002` — só `AlterModelOptions`, nenhuma coluna de tabela alterada.

2. **Novo helper `conteudo/permissoes.py`**: decorator `exige_permissao_painel(codename)` que levanta `PermissionDenied` (→ 403 automático do Django) se `request.user.has_perm(codename)` for falso. Superusuário sempre passa (comportamento nativo do Django).

3. **12 views protegidas** (decorator empilhado junto ao `@staff_member_required` já existente, sem remover nada):
   - `conteudo/admin_views.py`: `organizar_view`, `api_subcategorias_itens` (API AJAX do Adicionar Arquivos), `adicionar_arquivos_view`, `barra_superior_view`, `editor_rodape_view`, `area_do_site_view`
   - `conteudo/arvore_views.py`: `estrutura_arvores_view`, `arvore_api`
   - `painel/views.py`: `painel_central_view` (Tela 1), `conteudos_view` (Tela 2) — mesma permissão para as duas telas
   - `inteligencia/views.py`: `dashboard_view`, `dashboard_api`, `exportar_excel_view`, `exportar_pdf_view`

4. **Dashboard** (`templates/admin/index.html`): cada um dos 8 banners agora está dentro de `{% if perms.app.codename %}...{% endif %}` — some da tela quem não tem a permissão (cosmético; a segurança de verdade está nas views, que sempre retornam 403 se a URL for acessada direto sem permissão).

**Como o Dan usa**: Admin → Autenticação e Autorização → Usuários → (escolher usuário) → seção "Permissões do usuário" → marcar as permissões com rótulo "Pode acessar: ...". Ou criar um Grupo com um conjunto de permissões e atribuir usuários a ele (mais prático para papéis recorrentes). O usuário também precisa ter "Membro da equipe" marcado (requisito que já existia).

- **Testado fim-a-ponta** (Django test client): usuário staff de teste sem superusuário e sem nenhuma permissão → dashboard com 0 dos 8 banners, as 8 URLs retornam 403 ✓; concedida a permissão do Organizador → só aquele banner aparece, `/admin/organizar/` abre (200), as outras 7 URLs continuam em 403 ✓; usuário de teste removido ao final ✓. Superusuário `ridan` (via `force_login`) → todos os 8 banners visíveis e todas as 8 URLs continuam em 200 — **zero regressão** ✓.
- **Compatibilidade 100%**: os 3 usuários existentes (`ridan`, `rabalista`, `kayode`) são todos superusuários, então **nenhum perde acesso** com esta mudança — o controle granular só passa a valer para novos usuários staff não-superusuário que o Dan criar a partir de agora (que nascem sem nenhum dos 8 acessos, seguro por padrão). Nenhuma URL, template (fora do `{% if %}` cosmético) ou lógica interna de view foi alterada.
- **Arquivos modificados**: `conteudo/models.py` (Meta.permissions em ConfiguracaoSite), `painel/models.py` (Meta.permissions em Vinculo), `inteligencia/models.py` (Meta.permissions em AlertaInteligencia), `conteudo/migrations/0030_alter_configuracaosite_options.py`, `painel/migrations/0003_alter_vinculo_options.py`, `inteligencia/migrations/0002_alter_alertainteligencia_options.py` (novas migrações), `conteudo/permissoes.py` (novo arquivo — decorator), `conteudo/admin_views.py` + `conteudo/arvore_views.py` + `painel/views.py` + `inteligencia/views.py` (decorator aplicado, 12 views), `templates/admin/index.html` (8 banners com `{% if perms %}`).

### 2026-07-17 — Arrastar-e-soltar de múltiplos arquivos na Estrutura de Árvores (parte 22)

**Pedido do Dan**: ao criar ou abrir qualquer botão/subbotão/subárea na Estrutura de Árvores, poder arrastar e soltar vários arquivos de uma vez em vez de escolher um por vez.

**Escopo confirmado com o Dan**: só dentro do admin (painel Estrutura de Árvores), não no site público — visitantes continuam só vendo/baixando arquivos, sem poder enviar nada.

**Onde foi aplicado** (2 pontos, ambos dentro de `templates/admin/estrutura_arvores.html`):
1. **Seção "Anexos"** do painel de detalhes — ao clicar em qualquer nó da árvore e abrir a seção Anexos, o campo de upload agora é uma zona arrastar-e-soltar (`.ea-dropzone`), com fallback de clique (abre o seletor de arquivos normal). Aceita vários arquivos de uma vez.
2. **Modal "Criar novo botão/subbotão"** — o campo de anexos (que já aceitava múltiplos arquivos via clique) ganhou a mesma zona de arrastar-e-soltar.

**Implementação**:
- `conteudo/arvore_views.py` (`_api_upload_anexo`): passou a aceitar um campo novo `arquivos` (lista, via `request.FILES.getlist`) além do campo antigo `arquivo` (singular) — os dois continuam funcionando, o antigo sem nenhuma mudança de comportamento. Quando mais de 1 arquivo é enviado, o campo "Nome" é ignorado (cada arquivo usa seu próprio nome de arquivo); com exatamente 1, o nome customizado continua valendo como antes.
- `templates/admin/estrutura_arvores.html`: novo helper JS reutilizável `EA._attachDropzone(dropzoneId, inputId, textoId, textoPadrao)` — liga os eventos `dragover`/`dragleave`/`drop` a uma zona, populando o `<input type="file">` correspondente via `DataTransfer` (funciona com `multiple` ou não). O `<input>` real fica oculto (`display:none`); a zona visível dispara o clique nele. Nova classe CSS `.ea-dropzone` (borda tracejada, destaque ao arrastar por cima — `.ea-dropzone-ativa`) usando as variáveis de cor já existentes do painel (`--ea-primary`, âmbar).
- `uploadAnexo(catId)` (JS) reescrita para ler a `FileList` inteira do input (antes só pegava `files[0]`) e enviar cada arquivo sob o campo `arquivos`.

**Testado fim-a-ponta**: upload de 2 arquivos de uma vez via campo novo `arquivos` → 2 `Anexo` criados numa única requisição, mensagem "2 anexos adicionados" ✓; upload de 1 arquivo pelo campo antigo `arquivo` com nome customizado → continua funcionando exatamente como antes ✓; dropzone renderiza corretamente nos dois locais (seção Anexos e modal Criar botão), sem erros no console do navegador ✓; fechar o modal (`fecharModal()`) continua restaurando o HTML original sem corrupção (mesma proteção da parte 11) ✓.

**Compatibilidade 100%**: nenhuma mudança em outros painéis, nenhuma migração de banco necessária (o campo `arquivos` é só um nome de campo do formulário, não uma coluna). Não expandido a outros pontos de upload do sistema (Adicionar Arquivos, Organizador, Painel Central) — só à Estrutura de Árvores, conforme escopo confirmado.

### 2026-07-17 — Arrastar-e-soltar em todos os painéis com anexos (parte 23)

**Pedido do Dan**: "faça isso em todos os painéis que possuem partes para anexar" — expandir o recurso de arrastar-e-soltar (implementado na parte 22 só na Estrutura de Árvores) para os demais painéis administrativos.

**Levantamento feito antes de implementar**: mapeados todos os `<input type="file">` do admin, separando **seções de anexar** (listas de arquivos, aceitam vários) de **campos de ícone/imagem única** (um só arquivo, ex.: ícone de categoria, imagem de destaque, logo do rodapé — esses ficaram de fora, não são "anexar"). A maioria dos campos de anexar **já aceitava múltiplos arquivos no backend** (via `request.FILES.getlist(...)` ou loop `arquivo_0..49`), então só precisou de interface nova — só 2 pontos exigiram mudança de backend.

**Novo arquivo `static/js/dropzone.js`** (helper genérico, reutilizável por qualquer template):
```html
<div class="dropzone" data-dropzone-input="idDoInput" data-dropzone-texto="idDoTexto">...</div>
<input type="file" id="idDoInput" multiple style="display:none">
```
Auto-inicializa em todo `.dropzone[data-dropzone-input]` da página no carregamento — liga clique (abre seletor normal) e os eventos `dragover`/`dragleave`/`drop` (popula o input via `DataTransfer`). Funciona com ou sem `multiple`. Incluído via `<script src="{% static 'js/dropzone.js' %}">` nos templates que usam o padrão simples.

**Onde foi aplicado**:
1. **Painel Central** (`templates/admin/painel_central.html`):
   - "Criar novo botão" → `novo_arquivos` (já multi no backend, só UI nova)
   - "Criar subárea nos botões marcados" → `subarea_arquivos` (idem)
   - "Editar botão selecionado" → `editar_anexo` **virou múltiplo** (antes só 1 arquivo) — backend `painel/views.py` `_editar_botao`: `request.FILES.get('editar_anexo')` → `for anexo_file in request.FILES.getlist('editar_anexo')`
   - "Anexos" (seção do formulário de publicar conteúdo, linhas dinâmicas `arquivo_0..49`) → dropzone **customizada** (não usa o helper genérico, já que preenche várias linhas de uma vez): a função `criarLinhaAnexo(arquivo)` foi extraída do handler de clique existente e reaproveitada pelo `drop`, criando 1 linha nova por arquivo solto (ou preenchendo a 1ª linha vazia, se existir)
2. **Organizador** (`templates/admin/organizar.html`, ganhou `{% load static %}`):
   - "Criar novo botão dentro de X" → `arquivos` (já multi no backend)
   - "Adicionar novo arquivo ou URL a X" → `novo_arquivos` (já multi no backend)
3. **Adicionar Arquivos** (`templates/admin/adicionar_arquivos.html`): dropzone customizada acima da tabela de linhas (`arquivo_0/1/2...`) — reaproveita a função `addRow()` já existente (agora aceita um arquivo opcional como parâmetro), preenchendo primeiro linhas vazias antes de criar novas
4. **Área do Site** (`templates/admin/area_do_site.html`, ganhou `{% load static %}`): "Anexos dentro do botão" (seção que só aparece com o checkbox "Criar como botão completo do site" marcado, dentro do loop de colunas extras) → `botao_anexos_rapidos`, com IDs únicos por coluna (`{{ coluna.pk }}`) já que o formulário se repete por coluna

**Testado fim-a-ponta**: `editar_anexo` com 2 arquivos → 2 Anexo criados numa função só (antes só aceitava 1) ✓; todas as 8 dropzones novas renderizam o texto correto e sem erros de console (Painel Central: 4, Organizador: 2, Adicionar Arquivos: 1, Área do Site: 1 — testada criando e depois excluindo uma `ColunaExtra` temporária) ✓; `dropzone.js` carrega 200 OK em todos os templates que o incluem ✓; nenhuma migração de banco necessária ✓.

**Compatibilidade 100%**: campos de ícone único (categoria, conteúdo, seções da home, colunas, rodapé) e de imagem única (destaque, capa de destaque) **não foram alterados** — continuam exatamente como antes, só 1 arquivo, sem dropzone (não são "anexar" no sentido de lista de anexos). Nenhuma URL, nenhuma view renomeada, nenhum campo de formulário removido.

### 2026-07-17 — Vários links de URL de uma vez na Estrutura de Árvores (parte 24)

**Pedido do Dan**: depois do arrastar-e-soltar de arquivos (parte 23), poder anexar **vários links de URL** de uma vez dentro de botões, subbotões e subáreas — não só arquivos.

**Decisão de UX** (confirmada com o Dan antes de implementar): como não existe "arrastar" de um link (não é um arquivo), a experiência escolhida foi **linhas dinâmicas com Nome + URL** (campo de nome opcional ao lado da URL, botão "+ Adicionar outro link" para ir criando quantas linhas quiser) — em vez de uma caixa de texto com 1 link por linha. Escopo: **Estrutura de Árvores** (onde já existe o campo de URL único ao criar/editar botão).

**Onde foi aplicado** (2 pontos em `templates/admin/estrutura_arvores.html`):
1. **Modal "Criar novo botão/subbotão"** — abaixo do campo único "URL / Link (opcional)" já existente (mantido intacto, comportamento 100% igual a antes), nova seção "Mais links / URLs (opcional, quantos quiser)" com linhas dinâmicas.
2. **Painel de detalhes de qualquer nó já existente** → seção "Conteúdos" → nova subseção "Adicionar vários links de uma vez", abaixo do formulário "Associar novo conteúdo" já existente (também mantido intacto).

**Implementação**:
- `conteudo/arvore_views.py`:
  - Nova action `associar_links` → `_api_associar_links(request)`: recebe listas pareadas `link_nome`/`link_url` (via `request.POST.getlist`), cria 1 `Conteudo(tipo='link')` por linha com URL preenchida (nome em branco usa o nome da categoria, mesmo comportamento do campo único antigo). Ignora linhas sem URL.
  - `_api_criar()`: passou a também ler `link_nome`/`link_url` (getlist) na criação do botão, além do campo antigo `url_conteudo` (mantido, ambos funcionam juntos).
- `templates/admin/estrutura_arvores.html`:
  - Helper JS reutilizável `EA._novaLinhaLink(containerId)` — cria uma linha com 2 inputs (nome + URL) e botão "×" para remover a linha; `EA._coletarLinks(containerId)` — varre as linhas e devolve arrays paralelos de nomes/URLs, ignorando linhas com URL vazia.
  - `EA.associarLinks(catId)` — usado no painel de detalhes, chama a action `associar_links` e recarrega os detalhes do nó.
  - `confirmarCriar()` — passou a também coletar as linhas de `criarLinksContainer` e enviá-las junto com o restante do formulário de criação.
  - Cada local (`criarLinksContainer` no modal, `acLinksContainer_<id>` no painel) nasce com 1 linha vazia já pronta para preencher.

**Testado fim-a-ponta** (via navegador real + chamadas diretas à API): criar botão com 2 links (1 nomeado "Link A", 1 sem nome) → 2 `Conteudo` tipo link criados, o sem nome herdou o nome do botão ✓; adicionar mais 2 links a um botão já existente via `associar_links` → 2 novos `Conteudo` criados, mensagem "2 link(s) adicionado(s)" ✓; campo único antigo "URL / Link" continua funcionando normalmente em paralelo ✓; nó de teste e os 4 conteúdos de teste excluídos ao final (limpeza).

**Compatibilidade 100%**: nenhuma migração de banco necessária (usa o model `Conteudo` já existente, só um novo formato de formulário). Campo único "URL / Link" do modal de criar e o formulário "Associar novo conteúdo" do painel de detalhes continuam exatamente como antes — o recurso novo é só um **acréscimo** ao lado deles. Não expandido a outros painéis (Painel Central, Organizador, Área do Site) nesta leva — só à Estrutura de Árvores, conforme escopo confirmado com o Dan.

### 2026-07-17 — Vários links de URL em todos os painéis (parte 25)

**Pedido do Dan**: levar o recurso de "vários links de uma vez" da parte 24 (só Estrutura de Árvores) para os outros painéis administrativos.

**Onde foi aplicado** (3 painéis, 6 pontos no total):

1. **Painel Central** (`templates/admin/painel_central.html` + `painel/views.py`):
   - "Criar novo botão" — abaixo do campo `novo_url_externa` já existente, novo bloco "Mais links / URLs" com linhas dinâmicas (`novo_link_nome`/`novo_link_url`).
   - "Criar subárea nos botões marcados" — mesmo padrão (`subarea_link_nome`/`subarea_link_url`), aplicado a CADA subárea criada (uma por botão marcado).
   - "Editar botão selecionado" — mesmo padrão (`editar_link_nome`/`editar_link_url`), abaixo do campo único "URL / Link" já existente; o container é limpo e resemeado toda vez que a seção carrega os dados de um botão diferente (AJAX `atualizarEditar()`).
   - Novo helper `_criar_links_extra(post, prefix, categoria, nome_padrao)` em `painel/views.py`, chamado a partir de `_criar_no`, `_criar_subareas` e `_editar_botao`.
   - JS: `window.pcNovaLinhaLink(containerId, prefix)` global, seeded automaticamente para os containers "novo"/"subárea" no carregamento da página.

2. **Organizador** (`templates/admin/organizar.html` + `conteudo/admin_views.py`):
   - "Criar novo botão dentro de X" — abaixo do campo `url_externa`, novo bloco com `nova_link_nome`/`nova_link_url`.
   - "Adicionar novo arquivo ou URL a X" — abaixo do campo `novo_url`, novo bloco com `aqui_link_nome`/`aqui_link_url`. A validação que antes exigia "arquivo ou URL" foi ajustada para também aceitar "só links extras preenchidos" (`tem_links_extra` checa `aqui_link_url` antes de recusar o formulário).
   - Mesmo helper `_criar_links_extra()` duplicado em `conteudo/admin_views.py` (arquivo diferente do painel, sem import cruzado) — usado nas actions `criar_subcategoria` (prefixo `nova`) e `criar_conteudo_aqui` (prefixo `aqui`).
   - JS: função `orgNovaLinhaLink(containerId, prefix)` global no `<script>` da página, seeded no `DOMContentLoaded`.

3. **Área do Site** (`templates/admin/area_do_site.html` + `conteudo/admin_views.py`):
   - Dentro do checkbox "Criar como botão completo do site" (por coluna extra), abaixo do campo único "URL dentro do botão", novo bloco `botao_link_nome`/`botao_link_url` — como o formulário se repete por `ColunaExtra`, o container usa ID único por coluna (`botaoLinksContainer{{ coluna.pk }}`, mesmo padrão já usado para `botao_anexos_rapidos` desde a parte 23).
   - `_criar_links_extra()` chamado dentro da action `criar_botao`, logo após os anexos rápidos, usando a MESMA `categoria` (nova ou já existente) que recebe a URL única e os anexos rápidos.
   - JS: função `asNovaLinhaLink(containerId, prefix)` global, seeded via `document.querySelectorAll('[id^="botaoLinksContainer"]')` no `DOMContentLoaded` (cobre quantas colunas existirem, sem precisar de um loop Django).

**Testado fim-a-ponta** (via navegador real, preenchendo e submetendo os formulários de verdade — não só chamadas diretas à API): Painel Central "Criar novo botão" com 2 links extras → botão criado com 2 `Conteudo` tipo link dentro (mensagem "+ 2 link(s) extra(s)") ✓; Organizador "Criar novo botão dentro de X" com 2 links → subcategoria com 2 conteúdos ✓; Organizador "Adicionar novo arquivo ou URL" preenchendo SÓ os links extras (sem URL única, sem arquivo) → aceito normalmente, "2 item(ns) adicionado(s)" (confirma a correção da validação) ✓; Área do Site, botão completo do site com 2 links extras → categoria raiz criada com 2 conteúdos tipo link (1 nomeado, 1 com nome automático = nome do botão) ✓. Todos os dados de teste foram excluídos ao final.

**Compatibilidade 100%**: nenhuma migração de banco necessária. Todos os campos de URL única (`novo_url_externa`, `subarea_url_externa`, `editar_url`, `url_externa` do Organizador, `novo_url`, `botao_url_rapida`) continuam funcionando exatamente como antes — o recurso novo é sempre um acréscimo ao lado deles, nunca uma substituição. Nenhuma view renomeada, nenhum campo removido.

### 2026-07-17 — Banner sem corte + altura personalizada (parte 26)

**Pedido do Dan**: a imagem central do banner da home estava aparecendo cortada; pediu ajuste automático (nunca cortar) + poder controlar altura/largura no admin do Banner.

**Diagnóstico**: `.hero-slide img` (banner da home) e `.cat-banner-item img` (banners de categoria) usavam `object-fit:cover` — corta a imagem para preencher a caixa quando a proporção não bate. Verificado ao vivo: imagem 1376×768 exibida numa caixa 1265×240 (proporção bem mais larga) perdia boa parte do topo/base. O resto do site (carrossel, cartazes, "Destaques") já usava a técnica correta desde antes — só o Banner ficou de fora nessa vez.

**Correção do corte** (`static/css/style.css`):
- `.hero-slide` e `.cat-banner-item`: a imagem passa a usar `object-fit:contain` (nunca corta), com um `::before` absoluto usando o mesmo `background-image` (já vinha inline no HTML) desfocado (`blur(20px) brightness(0.6)` + `scale(1.15)`) preenchendo o espaço ao redor — mesma técnica já usada em `.carrossel-slide-fundo` e `.destaques-grid .card-image::before`.
- Ajustado `z-index` (`img`: 1, `.hero-overlay`/`.cat-banner-overlay`: 2) para o texto sobreposto continuar legível por cima da imagem.
- Funciona automaticamente para qualquer imagem daqui pra frente — não precisa de nenhuma ação no admin.

**Altura personalizada** (opcional, pedido do Dan para controle fino além dos 3 tamanhos prontos):
- Novo campo `Banner.altura_personalizada` (`PositiveIntegerField`, null/blank, migração `conteudo/0031`) — mesmo espírito dos campos `largura`/`altura` (px) que o Carrossel já tinha.
- Admin (`BannerAdmin`): campo exposto no fieldset "🖼️ Imagem", ao lado de "Tamanho", com texto explicando que ele tem prioridade sobre Pequeno/Médio/Grande quando preenchido.
- Templates (`home.html`, `categoria.html`): quando preenchido, define `min-height`/`height` inline em pixels (sobrepõe as classes `tamanho-pequeno/medio/grande`); quando vazio, comportamento 100% igual a antes (usa as classes CSS de tamanho).
- **Trade-off avisado no help text**: a altura personalizada vale em qualquer tela (não diminui sozinha no celular, diferente dos 3 tamanhos prontos que têm breakpoints responsivos). Decisão consciente para manter simples — se o Dan digitar um valor pensado pra desktop, vale também no celular.
- Largura NÃO ganhou controle — banner continua sempre 100% da largura da tela (confirmado com o Dan; é assim que banners funcionam na maioria dos sites).

**Testado fim-a-ponta**: banner real da home com imagem 1376×768 → antes cortava boa parte do topo/base, depois aparece inteira com fundo desfocado nas sobras (`object-fit` confirmado via `getComputedStyle`) ✓; altura personalizada de 550px aplicada temporariamente no banner real → `min-height`/`height` inline de 550px confirmados, sem corte ✓; revertido para vazio → volta a 240px (tamanho "médio") automaticamente ✓; campo aparece corretamente no Django Admin do Banner com o texto de ajuda certo ✓.

**Compatibilidade 100%**: nenhuma alteração em outros componentes (carrossel, cartazes, destaques, cards de conteúdo) — só `.hero-slide`/`.cat-banner-item` foram tocados. Banners sem altura personalizada preenchida continuam com comportamento idêntico a antes (só sem o corte, que era o bug).

### 2026-07-18 — Banner com ajuste automático à imagem (parte 27)

**Pedido do Dan**: a correção da parte 26 (`object-fit:contain` numa faixa de altura fixa) não agradou — a imagem ficava pequena no centro, com barras desfocadas nas laterais. Ele mandou um print e pediu: "tem que ficar do tamanho total da área e sem cortar... implemente uma IA de toda imagem que subir se adequar ao tamanho total desta área sem cortar".

**Explicação geométrica dada ao Dan**: preencher 100% de uma área de altura FIXA sem cortar só é possível se a imagem tiver exatamente a proporção da área (quase nunca). As únicas saídas eram: (a) cortar [parte pré-26]; (b) barras desfocadas [parte 26]; (c) a área se adaptar à imagem [parte 27, escolhida]. Não é "IA" de verdade — é ajuste automático de proporção via CSS, mas resolve exatamente o que ele quer.

**Solução (ajuste automático)**:
- `static/css/style.css`: `.hero-slide img` e `.cat-banner-item img` passaram a usar `display:block; width:100%; height:auto` — a imagem ocupa a largura toda e a altura acompanha a proporção. Removida a altura fixa do `.hero-slide`/`.cat-banner-item` e o `::before` desfocado do modo padrão. Neutralizadas TODAS as regras que forçavam altura fixa espalhadas pelo arquivo (bloco base, bloco "AJUSTES 2026-07-11 parte 2" ~linha 1917, media queries mobile ~1152 e ~1929, presets `tamanho-*`).
- Novo modo opcional `.hero-slide--fixo` / `.cat-banner-item--fixo` (ligado só quando `altura_personalizada` está preenchida): faixa de altura fixa com `object-fit:contain` + `::before` desfocado (é o comportamento da parte 26, agora opt-in).
- `templates/home.html` e `templates/categoria.html`: `{% if banner.altura_personalizada %}` escolhe entre a `<div>` de altura fixa (com classe `--fixo`, `background-image` p/ o blur e `height`/`min-height` inline) e a `<div>` de ajuste automático (sem classe de tamanho, sem inline, sem background). Auto-fit NÃO recebe mais a classe `tamanho-{{...}}` (senão os presets voltariam a forçar altura por especificidade maior).
- `conteudo/models.py`: `help_text`/`verbose_name` de `tamanho` (agora "campo legado") e `altura_personalizada` (agora "Altura fixa em pixels (opcional)") reescritos explicando o ajuste automático como padrão/recomendado. `conteudo/admin.py`: descrição do fieldset "🖼️ Imagem" reescrita. Migração `conteudo/0032` (só metadados de campo, nenhuma coluna alterada).

**Trade-off documentado (importante para o Dan entender)**: com ajuste automático, a ALTURA do banner é ditada pela proporção da imagem. Imagem quase quadrada (ex.: a atual 1376×768) → banner ~706px de altura a 1265px de largura. Imagem em formato faixa (ex.: 1920×500) → banner baixo e largo. Para um banner baixo, subir imagem já cortada no formato faixa (ou usar "Altura fixa em pixels", aceitando as barras). Não dá para ter, ao mesmo tempo, altura fixa baixa + largura total + zero corte com uma imagem quase quadrada — é geometria.

**Testado fim-a-ponta** (via `getComputedStyle`/`getBoundingClientRect`, screenshots estavam travando na ferramenta nesta sessão): modo automático → `slideRect` == `imgRect` (1265×706), `width:100%`, `height:auto`, sem `::before`, sem corte, sem barra ✓; modo altura fixa (300px de teste) → classe `hero-slide--fixo`, slide 300px, img `object-fit:contain` dentro dos 300px, `::before` blur ativo ✓; revertido para automático ao final ✓; CSS carregando `?v=20260718-1` ✓; `manage.py check` limpo ✓.

### 2026-07-18 — Banner faixa fina + imagem recortada em faixa (parte 28)

**Pedido do Dan**: o banner da parte 27 (ajuste automático) ficou "enorme"/"muito alto" com a imagem quase quadrada (1376×768 → 706px). Ele pediu primeiro pra recortar a imagem em "formato faixa"; depois, mesmo com a faixa (386px), pediu "a mais fina possível, bem fina e discreta".

**Escolha do Dan (via pergunta)**: entre cortar / barras / subir imagem faixa, ele escolheu **subir imagem em formato faixa**. Como a imagem que ele quer é o skyline do ES já existente, eu mesmo recortei ela.

**1. Imagem recortada em faixa** (via Pillow, sem numpy): `media/banners/hero-faixa.png`. Método: `Image.convert('L').point(lambda p: 255 if p<150 else 0).getbbox()` achou o bounding box do desenho (linhas escuras sobre gradiente claro) = y 222..550 (altura 328px, largura cheia). Recortei mantendo largura total e y 176..596 (margem de 46px em cima/embaixo) → **1376×420** (proporção 3.28:1), desenho inteiro preservado (Buda, beija-flor, prédios, montanha, igreja, árvore), só removeu o céu/chão vazios. Arquivo original (`hero-ilustracao_zeSTcbw.png`) mantido intacto. Banner pk=3 repontado para o novo arquivo (via `b.imagem.name = 'banners/hero-faixa.png'`).

**2. Modo altura fixa virou `cover`** (era `contain`+blur nas partes 26/27): `.hero-slide--fixo img` e `.cat-banner-item--fixo img` agora usam `width:100%; height:100%; object-fit:cover; object-position:center` (removido o `::before` blur e o `background` do slide). Assim, preencher `altura_personalizada` = banner com aquela altura EXATA, imagem preenchendo (sem barras, sem desfoque, recorta um pouco pra caber). Ideal para faixa fina.

**3. Banner da home = 130px** (`altura_personalizada=130`): faixa fina e discreta. Antes de setar, gerei prévias com Pillow (cover a 110/150/190px, salvos no scratchpad e lidos com a ferramenta Read de imagem) pra escolher — 130px mostra o skyline como faixa decorativa reconhecível. O Dan pode ajustar o número no admin (Banners → "Altura fixa em pixels"; menor = mais fina).

**4. help_text** de `altura_personalizada` reescrito (agora explica: vazio = ajuste automático; número = faixa fina que preenche). Migração `conteudo/0033` (só metadados).

**Testado**: banner 130px, classe `hero-slide--fixo`, `object-fit:cover`, `hero-faixa.png` carregando, sem scroll horizontal, `heroBottom`=188px (58 header + 130 faixa), CSS `?v=20260718-2`, sem erro de console, `manage.py check` limpo ✓.

**Nota**: o ajuste automático (parte 27) continua sendo o padrão quando `altura_personalizada` está vazio — imagem inteira, sem cortar, altura pela proporção. Os dois modos coexistem.

### 2026-07-18 — Infraestrutura Docker com PostgreSQL (parte 29)

**Pedido do Dan**: manter o ambiente local SQLite intacto, mas também ter o projeto pronto em Docker com PostgreSQL para entregar/demonstrar à SEDU a qualquer momento.

**Decisão arquitetural**: banco condicional por variável de ambiente. Sem `DOCKER_POSTGRES=1` (ambiente local), Django usa SQLite exatamente como sempre foi — zero mudanças. Dentro do Docker (que seta `DOCKER_POSTGRES=1`), usa Postgres, lendo credenciais de outras variáveis de ambiente.

**1. Modificações em `curriculo_sedu/settings.py` (condicional, não quebra local)**:
   - Bloco `if os.environ.get('DOCKER_POSTGRES') == '1':` → usa Postgres (host, port, user, password, db do ambiente)
   - `else:` → continua SQLite (comportamento 100% igual a antes)
   - Testado: `python manage.py check` local passou sem erro nenhum — nenhum impacto no SQLite local

**2. `requirements.txt`** (aditivo):
   - Adicionado `psycopg2-binary==2.9.10` (driver Postgres)
   - Compatível com venv local — pip ignora se não quiser instalar

**3. `docker-compose.yml` (novo serviço Postgres)**:
   - `db`: imagem `postgres:16` com volume `postgres_data` para persistência
   - Healthcheck via `pg_isready` com retry de 10s
   - `web`: serviço Django existente, dependente do `db`, com variáveis `DOCKER_POSTGRES=1` + credenciais Postgres
   - Comando no `web` agora roda `python manage.py migrate` automaticamente antes do `runserver` (garante migrações aplicadas)
   - Removida versão do docker-compose (deprecated warning do Docker)

**4. Novo botão: `BAT SEDU/ATUALIZAR BANCO DOCKER.bat`** (sincronização local→Docker):
   - Etapa 1: exporta dados locais (SQLite) para JSON via `dumpdata` com `PYTHONUTF8=1` (força UTF-8, crítico no Windows com acentos em português)
   - Etapa 2: sobe containers Docker se não estiverem rodando (`docker compose up -d`)
   - Etapa 3: aplica migrações no Postgres do Docker
   - Etapa 4: limpa dados atuais (`flush --no-input`)
   - Etapa 5: importa dump JSON no Postgres
   - Resultado final: 100% dos dados do SQLite local (3674 registros, 132 categorias, 588 conteúdos) espelhados no Postgres do Docker
   - Bugs corrigidos durante testes: (a) parênteses literais dentro de blocos `if` precisam de escape `^(`/`^)` no cmd.exe, (b) quebra de linha deve ser CRLF, não LF, (c) caracteres UTF-8 multibyte descarrilham o parser do cmd.exe (armadilha #12 já documentada) — todos fixos

**5. `.gitignore`** (aditivo):
   - Ignora `dump_local.json` (arquivo temporário gerado e descartável, contém dados sensíveis/senhas)

**Testado ponta a ponta** (2026-07-18):
   - Docker Desktop iniciado, `docker compose up -d --build` rodou com sucesso
   - Postgres 16 container saudável, web container rodando
   - Migrações (40 ao total) aplicadas sem erro no Postgres do Docker
   - Fluxo de sincronização testado manualmente: SQLite local exportado (2MB) → Postgres do Docker
   - `loaddata dump_local.json` importou 3674 registros com sucesso
   - Site no Docker respondendo HTTP 200 em `http://localhost:8000/`
   - Verificado: 132 categorias e 588 conteúdos no banco Docker batem exatamente com o local

**Compatibilidade 100%**:
   - Ambiente local SQLite intacto — nenhuma mudança visível para o Dan no seu dia a dia
   - `.bat` existentes (INICIAR SISTEMA, ATUALIZAR BANCO) funcionam normalmente
   - Novo `.bat` é um atalho adicional, não obrigatório
   - Nenhuma migração de banco necessária (Docker é infraestrutura, não modelo)
   - Quando a SEDU pedir um ambiente pronto para produção: `docker-compose.yml` + `Dockerfile` já fazem tudo

**Próximos passos para produção**:
   - Gerar `.env` com credenciais Postgres reais (não hardcodadas)
   - Configurar SSL/TLS no domínio oficial `curriculo.sedu.es.gov.br`
   - Ajustar `ALLOWED_HOSTS` e `DEBUG=False` no deploy
   - Possível: usar Gunicorn em vez de `runserver` (já em requirements.txt)

### 2026-07-18 — Backup e Restauração Completa do Docker (parte 30)

**Pedido do Dan**: criar um fluxo para fazer backup do ambiente Docker (banco Postgres + arquivos de mídia + código) e poder restaurá-lo em outro Windows (incluindo o servidor da SEDU), levando todo o progresso/dados inseridos no site.

**Solução**: 2 novos `.bat` (autoexplicativos, sem exigir conhecimento de Docker/línux) + estrutura de backup portável.

**1. `BAT SEDU/BACKUP DOCKER COMPLETO.bat`** — gera backup íntegro e autocontido:
   - Verifica se Docker está rodando (se não, avisa e sai)
   - Valida que venv existe (pré-requisito)
   - Cria pasta `docker_backups/backup_AAAAMMDD_HHMMSS/` (nome único por data/hora, evita sobrescrita)
   - [1/5] Sobe containers Docker se não estiverem rodando
   - [2/5] Exporta banco Postgres via `pg_dump` (SQL puro, 931 KB de dados atuais, pronto para restaurar)
   - [3/5] Exporta mídia via `tar czf` dentro do container (265 MB, 259 arquivos, mantém permissões/paths)
   - [4/5] Empacota código do projeto via Powershell `Compress-Archive` — **exclui de propósito**: venv, staticfiles, docker_backups, .git, .claude, __pycache__, ngrok (ferramenta local desnecessária no Docker), BKPbat, dump_local.json (~295 MB zip comprimido)
   - [5/5] Copia o restaurador (ver ponto 2 abaixo) para dentro da pasta do backup
   - Exibe caminho da pasta gerada + instruções para levar outro PC

**2. `BAT SEDU/RESTAURAR ESTE BACKUP.bat`** — 6 etapas, restaura site completo:
   - Cópia automática dentro de cada pasta de backup pela etapa [5/5] do backup — cada backup é 100% autocontido
   - Pré-requisito único: Docker Desktop instalado e aberto no Windows de destino
   - [1/6] Extrai código via Powershell `Expand-Archive` (recria a pasta do projeto)
   - [2/6] Constrói imagem Docker (`docker compose build`) — pode demorar (Python 3.12 slim + dependências)
   - [3/6] Sobe Postgres vazio (`docker compose up -d db`) + espera healthcheck passar (10s)
   - [4/6] Restaura dump SQL via `pg_restore` (reconstrói schema + dados, 3674 registros)
   - [5/6] Sobe web Django (`docker compose up -d web`) + restaura mídia via `tar xzf` dentro do container
   - [6/6] Confere migrações (`migrate`) — caso houvesse migração nova depois do backup, roda aqui
   - Exibe URL local (`http://localhost:8000/`) pronto para usar

**3. Portabilidade garantida**:
   - User só copia a pasta `docker_backups/backup_...` (pendrive, email, nuvem, etc.)
   - Abre naquela pasta o arquivo `RESTAURAR ESTE BACKUP.bat`
   - Valida Docker (sai com mensagem clara se não estiver aberto)
   - Pergunta pasta de destino (padrão: `Site_Restaurado` na mesma pasta do .bat)
   - Valida que não existe site em `DESTINO` (evita sobrescrever acidentalmente)
   - Cria `DESTINO` e procede

**4. Testado ponta a ponta** (2026-07-18):
   - Backup gerou 3 arquivos: `banco_postgres.sql` (931 KB), `media_data.tar.gz` (265 MB, 259 arquivos confirmados íntegro), `codigo_projeto.zip` (manage.py, Dockerfile, docker-compose.yml, requirements.txt todos presentes)
   - Restaurador copiado automaticamente → presente dentro da pasta de backup
   - Zip extraído, imagem construída, containers subidos, dump restaurado com sucesso
   - Site respondendo HTTP 200 em `http://localhost:8000/` após restauração

**5. `.gitignore`** (aditivo):
   - Adicionado `docker_backups/` — backups contêm dados e não devem viajar pelo Git
   - Mantém `dump_local.json` já ignorado

**Fluxo de uso pelo Dan**:
   - Sempre que quer levar o progresso (dados inseridos no site) para outro PC: roda o **BACKUP**
   - Copia pasta gerada (pendrive/nuvem) para o outro PC
   - Abre a pasta lá e roda o **RESTAURAR**
   - Pronto — site Docker com todos os dados está rodando em `http://localhost:8000/`

**Compatibilidade 100%**:
   - Nenhuma mudança no código, nos painéis, na funcionalidade ou no ambiente local SQLite
   - Nenhuma migração de banco necessária
   - Os 2 `.bat` são puramente utilitários, não quebram nada existente
   - Site local SQLite intacto, roda normalmente

### 2026-07-19 — Organizador: árvore completa de botões no "Mover para" (parte 31)

**Pedido do Dan**: no painel Organizador de Conteúdo, a área "Conteúdos em [botão]" tem um select "Mover selecionados para" — mas ele só listava a categoria pai e as subcategorias diretas (vizinhos imediatos). O Dan queria escolher **qualquer botão da árvore inteira do site**, igual já funcionava na Estrutura de Árvores (botão "Mover" com modal listando toda a hierarquia).

**Investigação**: antes de implementar, testei ao vivo se o recurso "mover botão + conteúdo junto" já existia na Estrutura de Árvores (pedido de uma leva anterior) — confirmado que sim (drag-and-drop + botão "Mover" com modal). Mas o pedido desta vez era especificamente sobre o **Organizador**, que tem uma tela diferente: aqui não se move um BOTÃO inteiro, e sim CONTEÚDOS individuais (documentos/links/etc.) para dentro de outro botão. O select de destino dessa tela era limitado demais.

**Solução**:
1. Novo helper `_arvore_flat_categorias(excluir_pk=None)` em `conteudo/admin_views.py` — percorre TODAS as categorias ativas (todos os níveis) e devolve lista achatada com indentação por profundidade (mesmo padrão do `_arvore_flat()` já usado no Painel Central para o select "criar botão dentro de"). Aceita excluir uma categoria específica da lista (a atual, já que mover conteúdo para onde ele já está não faz sentido) mas **continua descendo nos filhos dela** — suas subcategorias continuam aparecendo normalmente como destinos válidos.
2. View `organizar_view`: novo contexto `arvore_destinos = _arvore_flat_categorias(excluir_pk=categoria.pk)`.
3. Template `organizar.html`: o select "Mover selecionados para" agora tem 2 grupos — "Atalho rápido" (categoria pai, se houver, para o caso comum de subir um nível) + "Toda a árvore de botões do site" (as 133 categorias ativas, indentadas com `└`). Removidos os grupos antigos "Subcategorias"/"Outras áreas" (redundantes — a árvore completa já inclui tudo).
4. Reaproveitado `data-pesquisavel` + `static/js/filtro_select.js` (já existente no projeto, usado no "Categoria pai" do Django Admin) — o select ganha automaticamente uma caixinha de busca instantânea sem acento acima dele, essencial com 133 opções.

**Testado fim-a-ponta** (via Django test client simulando clique real no navegador): select carregado com 133 opções + caixa de busca confirmada presente; conteúdo de teste movido da categoria "Icone teste" para "Botões novos criados" (fora dos vizinhos imediatos, só alcançável pela árvore completa) → confirmado no banco (`categoria_id` mudou corretamente) ✓; teste revertido, sem deixar dados de teste no banco ✓.

**Compatibilidade 100%**: nenhuma migração de banco (função só percorre dados existentes). Campo `destinos`/`todas_subcategorias` no contexto da view mantidos (não usados mais no template, mas não removidos — outros lugares podem depender). O atalho rápido "categoria pai" preservado para o caso mais comum (mover 1 nível acima). Nenhuma outra tela (Painel Central, Estrutura de Árvores, Área do Site) foi tocada.

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
13. **Usuário staff criado mas não consegue acessar NENHUM painel personalizado** (desde a parte 21) → não é bug, é o comportamento esperado: usuários novos (não-superusuário) nascem sem nenhuma das 8 permissões de painel. Marcar as permissões desejadas em Autenticação e Autorização → Usuários → (usuário) → "Permissões do usuário", ou colocar o usuário num Grupo que já tenha as permissões marcadas. Ver seção "Delegação de acesso aos painéis administrativos".
14. **Arquivo `.bat` criado mas não abre nada no cmd.exe** (desde a parte 29) → armadilha de sintaxe: (a) parênteses LITERAIS `(` `)`dentro de blocos `if (...)` precisam ser escapados com `^(` e `^)` no cmd.exe, senão o parser falha; (b) quebra de linha deve ser CRLF (`0d 0a`), não LF (`0a`); (c) **caracteres UTF-8 multibyte** (`—` travessão, `ç`, `ã`, `é`) descarrilham o parser do cmd.exe mesmo DENTRO DE COMENTÁRIOS `REM`, causando falha silenciosa — sempre usar ASCII puro em `.bat` (hífens simples `-` em vez de `—`, etc.). A janela abre e fecha quase instantaneamente sem mensagem visível. Solução: (1) verificar com `hexdump` ou `xxd` para confirmar LF vs CRLF; (2) procurar caracteres UTF-8 com `grep -P '[\x80-\xFF]'`; (3) testar rodando o `.bat` via Powershell com redireção de streams para capturar a mensagem de erro real do cmd.exe.
