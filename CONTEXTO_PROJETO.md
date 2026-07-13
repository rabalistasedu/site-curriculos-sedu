# ðŸŽ“ SITE CURRÃCULO SEDU â€” Resumo de Contexto (2026-07-13 â€” parte 8)

## Estado atual: FUNCIONAL E COMPLETO âœ…âœ…âœ…

Projeto de migraÃ§Ã£o de site WordPress â†’ Django 5.2 para SEDU (Secretaria EducaÃ§Ã£o ES).  
**Status do banco**: 365+ conteÃºdos migrados, 10 categorias principais, 42+ subcategorias, **sistema de comentÃ¡rios moderado**.  
**Deploy**: âŒ PythonAnywhere abandonado | âœ… ngrok (demo) | ðŸŽ¯ `curriculo.sedu.es.gov.br/curriculo/` (produÃ§Ã£o)

---

## âš¡ Para entender onde estamos (2026-07-11)

### ðŸš¦ DecisÃ£o crÃ­tica de Deploy (2026-07-10)
- **PythonAnywhere nÃ£o Ã© mais usado** â€” ambiente de teste insuficiente para demonstraÃ§Ãµes
- **Novo destino**: servidor prÃ³prio da SEDU em `curriculo.sedu.es.gov.br/curriculo/` (subdomÃ­nio para nÃ£o quebrar WordPress existente)
- **AtÃ© lÃ¡**: demonstraÃ§Ãµes via **ngrok** (gera URL pÃºblica vÃ¡lida por 2h)
- **EstratÃ©gia**: reescrita de URLs via `.htaccess` Apache (manter WordPress em subdomÃ­nio, evitar duplicar ~1000 arquivos)

### Categorias principais (menu "Navegue por Ã¡rea")
1. **Documentos Curriculares** â€” CurrÃ­culo Atual (5 sub-etapas) + Material de Apoio + 7 subcategorias  
2. **OrientaÃ§Ãµes Curriculares** â€” 129 docs + 16 subcategorias  
3. **ItinerÃ¡rios Formativos de Aprofundamento (IFA)** â€” 10 subcategorias, 14 docs  
4. **Projetos Integradores** â€” 5 subcategorias  
5. **Rotinas PedagÃ³gicas Escolares (RPE)** â€” 8 subcategorias, **42 apostilas**  
6. **Programas** â€” Educar para a Paz, Mais Leitores, EducaÃ§Ã£o Ambiental, Sucesso Escolar
7. **Livro DidÃ¡tico**, **Modalidades e Diversidade**, **OlimpÃ­adas**, **Institucional**

### ðŸ“Š Dados no banco
- **SQLite** (`db.sqlite3`) â€” 365+ conteÃºdos (documento, video, post, link, pÃ¡gina)
- **Sistema de comentÃ¡rios MODERADO** â€” 3 estados (pendente/publicado/recusado), resposta do admin, nÃ£o aparece em links
- **Agendamento de publicaÃ§Ã£o** por data/hora futura
- **Banners rotativos** por Ã¡rea, tamanho configurÃ¡vel, URL de imagem opcional
- **Cartazes de eventos** (desktop sticky nas laterais, mobile botÃ£o flutuante)
- **CarrossÃ©is de imagens** com autoplay, aceita vÃ­deos (MP4/WebM/etc), cÃ³digo HTML customizÃ¡vel

---

## ðŸ†• O que mudou em 2026-07-12 a 2026-07-13

### ðŸŽ¯ 7 Partes de ImplementaÃ§Ã£o

**Parte 1â€“4 (2026-07-12, morning-afternoon): Bugs de layout + funcionalidade**
- âœ… NavegaÃ§Ã£o embolada em mobile â†’ limitada a 861px+
- âœ… Carrossel dividido em dois no painel Eventos â†’ widget funcional
- âœ… Carrossel invadindo rodapÃ© azul â†’ `max-height: 100%`
- âœ… Anexos de conteÃºdo invisÃ­veis â†’ seÃ§Ã£o de download adicionada
- âœ… SubbotÃµes invisÃ­veis â†’ aparecem como cards destacados com borda azul
- âœ… Busca da Ã¡rvore (3+ nÃ­veis) â†’ ancestrais expandem automaticamente
- âœ… RodapÃ© flutuando em pÃ¡ginas vazias â†’ flexbox sticky footer

**Parte 5 (2026-07-12, evening): EdiÃ§Ã£o inline + features novas**
- âœ… Editar botÃ£o selecionado â†’ seÃ§Ã£o verde AJAX (nome, descriÃ§Ã£o, Ã­cone, anexo)
- âœ… BotÃµes sem pai â†’ "BotÃµes novos criados" (categoria raiz automÃ¡tica)
- âœ… CategoriaPicker dinÃ¢mico â†’ categorias vazias agora aparecem
- âœ… Criar subÃ¡rea nos botÃµes marcados â†’ nova seÃ§Ã£o azul (criar subÃ¡reas em lote)

**Parte 6 (2026-07-12, evening): Carrossel admin + URL no painel**
- âœ… Carrossel admin melhorado â†’ `ClearableFileInput` (mostra arquivo atual + Limpar + Modificar)
- âœ… Campo URL no painel â†’ cria automaticamente Conteudo tipo "link"

**Parte 7 (2026-07-13): Sistema de ComentÃ¡rios Moderados**
- âœ… 3 estados (pendente/publicado/recusado) â€” migraÃ§Ã£o `conteudo.0019`
- âœ… Resposta do admin â€” campo editÃ¡vel com data automÃ¡tica
- âœ… ExclusÃ£o em tipo "link" â€” comentÃ¡rios nÃ£o aparecem em links externos
- âœ… Visual moderno â€” badge de contagem, botÃ£o gradiente, aviso de moderaÃ§Ã£o, seÃ§Ã£o colapsÃ¡vel

**Parte 8 (2026-07-13): Respostas + Votos em comentÃ¡rios**
- âœ… Respostas aninhadas â€” `Comentario.parent` (FK self), threads de atÃ© 2 nÃ­veis
- âœ… FormulÃ¡rio inline "Responder" â€” abre/fecha animado, placeholder dinÃ¢mico ("...a Maria")
- âœ… VotaÃ§Ã£o ðŸ‘/ðŸ‘Ž AJAX â€” `/comentario/<pk>/votar/`, sem reload, desabilita apÃ³s 1 voto
- âœ… Respostas recuadas â€” margin-left 40px, borda azul, label "â†© resposta" roxo

### ðŸ“ Arquivos modificados (2026-07-12 a 2026-07-13)
- `conteudo/models.py` â€” Comentario expandido (status, resposta, data_resposta)
- `conteudo/migrations/` â€” 0012â€“0019 (carrossel, Ã­cones, comentÃ¡rios)
- `conteudo/admin.py` â€” ComentarioAdmin reescrito (3 estados, aÃ§Ãµes em lote, badges)
- `conteudo/views.py` â€” conteudo_detalhe com `exibir_comentarios` + comentÃ¡rios com status
- `painel/views.py` â€” _dados_botao, _editar_botao, _criar_subareas (AJAX)
- `templates/conteudo_detalhe.html` â€” seÃ§Ã£o de comentÃ¡rios redesenhada
- `templates/admin/painel_central.html` â€” "Editar botÃ£o selecionado" (AJAX) + "Criar subÃ¡rea"
- `static/css/style.css` â€” novos blocos CSS (comentÃ¡rios, layout fixes) â€” cache `?v=20260713-2`
- `templates/base.html` â€” cache-busting atualizado

### ðŸ”„ Merge de conflito (2026-07-11)
- Um commit remoto ("codigo ngrok") havia substituÃ­do `.gitignore` inteiro por erro
- Resolvido no merge `2faca8e` mantendo versÃ£o completa do `.gitignore`
- Regra: nunca perder o `.gitignore` ao fazer pull em outro computador

---

## ðŸš€ Para comeÃ§ar novo (em novo computador)

### OpÃ§Ã£o 1: Git (recomendado)
```bash
git clone https://github.com/rabalistasedu/site-curriculos-sedu.git
cd "Site Curriculos SEDU"
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate  # Aplica migraÃ§Ãµes 0013 e 0002
python manage.py runserver 8001
```
Acesse: http://127.0.0.1:8001/

### OpÃ§Ã£o 2: Copiar pasta (sem Git)
```bash
python -m venv venv
venv\Scripts\activate
pip install django==5.2 pillow python-dateutil
python manage.py migrate  # Essencial: 0013 e 0002
python manage.py runserver 8001
```

---

## ðŸ“‹ Management Commands (jÃ¡ executados; dados no banco)

```bash
python manage.py popular_categorias           # 10 categorias + subcategorias
python manage.py popular_descricoes           # Textos introdutÃ³rios (HTML)
python manage.py migrar_conteudo              # 102 docs do site antigo
python manage.py migrar_orientacoes           # 129 docs (OrientaÃ§Ãµes Curriculares)
python manage.py migrar_ifa                   # 10 subcats + 14 docs (IFA)
python manage.py organizar_curriculo_atual    # 5 sub-botÃµes (EI/EFI/EFF/EM/Material)
python manage.py migrar_material_apoio        # 5 docs de apoio
python manage.py migrar_projetos_integradores # 5 subcats (Projetos Integradores)
python manage.py migrar_rpe                   # 8 subcats + 42 apostilas (RPE)
python manage.py migrar_olimpiadas            # 9 subcats (OlimpÃ­adas)
python manage.py curar_recentes                # Marca itens de "ConteÃºdos recentes"
python manage.py resolver_pendencias          # Arquiva 3 conteÃºdos sem dados
```
**Todos sÃ£o idempotentes** (rodar 2x = mesmo resultado).

---

## ðŸ“ Estrutura do projeto (atual)

```
curriculo_sedu/              # Settings, URLs, WSGI
conteudo/
  â”œâ”€ models.py              # Categoria, Conteudo (+ icone_imagem), Anexo, 
  â”‚                         #   Banner, Cartaz, Carrossel, ConfiguracaoSite, Comentario
  â”œâ”€ admin.py               # Admin customizado (badges, widgets)
  â”œâ”€ views.py               # home, categoria, conteudo, busca
  â”œâ”€ widgets.py             # IconPicker, CategoriaPicker, RichTextWidget
  â”œâ”€ forms.py               # ConteudoAdminForm (+ icone_imagem)
  â”œâ”€ management/commands/   # 11 migration commands
  â””â”€ migrations/            # 0001-0019 (comentÃ¡rios novo)
painel/                      # Painel Central Administrativo (Telas 1 e 2)
  â”œâ”€ models.py              # Vinculo, EstiloBotao (+ tamanho)
  â”œâ”€ views.py               # painel_central_view, conteudos_view (Telas 1 e 2)
  â””â”€ migrations/            # 0001-0002 (tamanho novo)
templates/
  â”œâ”€ base.html              # Header, nav, footer
  â”œâ”€ home.html              # Hero, banners, destaques, recentes, Ã¡reas, cartazes, carrossÃ©is
  â”œâ”€ categoria.html         # Subcategorias, filtros, conteÃºdos
  â”œâ”€ conteudo_detalhe.html  # Detalhe + comentÃ¡rios moderados
  â”œâ”€ busca.html             # Resultados de busca
  â””â”€ admin/                 # Templates customizados do admin (painel central, organizar)
static/
  â”œâ”€ css/style.css          # Design system (?v=20260713-1)
  â”œâ”€ css/admin_picker.css   # Estilos dos widgets visuais
  â”œâ”€ js/main.js             # Slider, menu, carrossel (?v=20260711-1)
  â””â”€ img/                   # BrasÃ£o, logos, Ã­cones
db.sqlite3                   # Banco SQLite (365+ conteÃºdos)
requirements.txt
manage.py
CLAUDE.md                    # ðŸ“˜ DocumentaÃ§Ã£o tÃ©cnica completa
CONTEXTO_ATUAL.md            # ðŸ“‹ Estado atual + quick start
README.md                    # ðŸ“– Overview do projeto
```

---

## ðŸ”§ Stack

- **Backend**: Django 5.2, Python 3.13 (local) / 3.11 (SEDU)
- **DB**: SQLite (dev e produÃ§Ã£o)
- **Frontend**: CSS puro, Font Awesome 6, Google Fonts (Inter)
- **Versionamento**: GitHub (`rabalistasedu/site-curriculos-sedu`)
- **Demo**: ngrok (URL temporÃ¡ria)
- **ProduÃ§Ã£o**: `curriculo.sedu.es.gov.br/curriculo/` (2026)

---

## ðŸ“– URLs principais

| Rota | DescriÃ§Ã£o |
|------|-----------|
| `/` | Home |
| `/categoria/<slug>/` | ConteÃºdos da categoria |
| `/conteudo/<slug>/` | Detalhe + comentÃ¡rios |
| `/busca/?q=termo` | Busca textual |
| `/admin/` | Django Admin |
| `/admin/painel-central/` | Painel Central (Telas 1 e 2) |
| `/admin/organizar/` | Organizador visual |
| `/admin/adicionar-arquivos/` | Upload em lote |

---

## âš ï¸ Notas importantes

1. **Banco jÃ¡ populado** â€” db.sqlite3 tem tudo. NÃ£o precisa rodar commands (a menos que teste).
2. **ConteÃºdos apontam para URLs externas** â€” PDFs no WordPress/Google Drive/SEDU.
3. **Cache do navegador** â€” mudar CSS? Force: **Ctrl+Shift+R** (Windows/Linux) ou **Cmd+Shift+R** (Mac).
4. **GitHub** â€” use `.bat` "Subir GitHub SEDU" (faz pull automÃ¡tico agora).
5. **MigraÃ§Ãµes aplicadas** â€” `conteudo.0012-0019` + `painel.0002`. Para novo ambiente: `python manage.py migrate`.
6. **Superusers locais** â€” `ridan` (Sedu@2026), `rabalista`.

---

## ðŸ“ž DocumentaÃ§Ã£o

- **[CLAUDE.md](CLAUDE.md)** â€” DocumentaÃ§Ã£o tÃ©cnica completa (modelos, views, admin, decisÃµes, troubleshooting)
- **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** â€” Estado atual + mudanÃ§as de 2026-07-11
- **[README.md](README.md)** â€” Overview do projeto
- **[Especificacao_Painel_Admin_Site_Curriculos.md](Especificacao_Painel_Admin_Site_Curriculos.md)** â€” Spec oficial do Painel Central
- **[MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md)** â€” Deploy final na SEDU

---

**Ãšltima atualizaÃ§Ã£o**: 2026-07-13  
**VersÃ£o CSS**: `?v=20260713-1` | **VersÃ£o JS**: `?v=20260711-1`  
**GitHub**: https://github.com/rabalistasedu/site-curriculos-sedu.git
