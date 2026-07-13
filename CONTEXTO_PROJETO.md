# 🎓 SITE CURRÍCULO SEDU — Resumo de Contexto (2026-07-13)

## Estado atual: FUNCIONAL E COMPLETO ✅✅✅

Projeto de migração de site WordPress → Django 5.2 para SEDU (Secretaria Educação ES).  
**Status do banco**: 365+ conteúdos migrados, 10 categorias principais, 42+ subcategorias, **sistema de comentários moderado**.  
**Deploy**: ❌ PythonAnywhere abandonado | ✅ ngrok (demo) | 🎯 `curriculo.sedu.es.gov.br/curriculo/` (produção)

---

## ⚡ Para entender onde estamos (2026-07-11)

### 🚦 Decisão crítica de Deploy (2026-07-10)
- **PythonAnywhere não é mais usado** — ambiente de teste insuficiente para demonstrações
- **Novo destino**: servidor próprio da SEDU em `curriculo.sedu.es.gov.br/curriculo/` (subdomínio para não quebrar WordPress existente)
- **Até lá**: demonstrações via **ngrok** (gera URL pública válida por 2h)
- **Estratégia**: reescrita de URLs via `.htaccess` Apache (manter WordPress em subdomínio, evitar duplicar ~1000 arquivos)

### Categorias principais (menu "Navegue por área")
1. **Documentos Curriculares** — Currículo Atual (5 sub-etapas) + Material de Apoio + 7 subcategorias  
2. **Orientações Curriculares** — 129 docs + 16 subcategorias  
3. **Itinerários Formativos de Aprofundamento (IFA)** — 10 subcategorias, 14 docs  
4. **Projetos Integradores** — 5 subcategorias  
5. **Rotinas Pedagógicas Escolares (RPE)** — 8 subcategorias, **42 apostilas**  
6. **Programas** — Educar para a Paz, Mais Leitores, Educação Ambiental, Sucesso Escolar
7. **Livro Didático**, **Modalidades e Diversidade**, **Olimpíadas**, **Institucional**

### 📊 Dados no banco
- **SQLite** (`db.sqlite3`) — 365+ conteúdos (documento, video, post, link, página)
- **Sistema de comentários MODERADO** — 3 estados (pendente/publicado/recusado), resposta do admin, não aparece em links
- **Agendamento de publicação** por data/hora futura
- **Banners rotativos** por área, tamanho configurável, URL de imagem opcional
- **Cartazes de eventos** (desktop sticky nas laterais, mobile botão flutuante)
- **Carrosséis de imagens** com autoplay, aceita vídeos (MP4/WebM/etc), código HTML customizável

---

## 🆕 O que mudou em 2026-07-12 a 2026-07-13

### 🎯 7 Partes de Implementação

**Parte 1–4 (2026-07-12, morning-afternoon): Bugs de layout + funcionalidade**
- ✅ Navegação embolada em mobile → limitada a 861px+
- ✅ Carrossel dividido em dois no painel Eventos → widget funcional
- ✅ Carrossel invadindo rodapé azul → `max-height: 100%`
- ✅ Anexos de conteúdo invisíveis → seção de download adicionada
- ✅ Subbotões invisíveis → aparecem como cards destacados com borda azul
- ✅ Busca da árvore (3+ níveis) → ancestrais expandem automaticamente
- ✅ Rodapé flutuando em páginas vazias → flexbox sticky footer

**Parte 5 (2026-07-12, evening): Edição inline + features novas**
- ✅ Editar botão selecionado → seção verde AJAX (nome, descrição, ícone, anexo)
- ✅ Botões sem pai → "Botões novos criados" (categoria raiz automática)
- ✅ CategoriaPicker dinâmico → categorias vazias agora aparecem
- ✅ Criar subárea nos botões marcados → nova seção azul (criar subáreas em lote)

**Parte 6 (2026-07-12, evening): Carrossel admin + URL no painel**
- ✅ Carrossel admin melhorado → `ClearableFileInput` (mostra arquivo atual + Limpar + Modificar)
- ✅ Campo URL no painel → cria automaticamente Conteudo tipo "link"

**Parte 7 (2026-07-13): Sistema de Comentários Moderados**
- ✅ 3 estados (pendente/publicado/recusado) — migração `conteudo.0019`
- ✅ Resposta do admin — campo editável com data automática
- ✅ Exclusão em tipo "link" — comentários não aparecem em links externos
- ✅ Visual moderno — badge de contagem, botão gradiente, aviso de moderação, seção colapsável

### 📝 Arquivos modificados (2026-07-12 a 2026-07-13)
- `conteudo/models.py` — Comentario expandido (status, resposta, data_resposta)
- `conteudo/migrations/` — 0012–0019 (carrossel, ícones, comentários)
- `conteudo/admin.py` — ComentarioAdmin reescrito (3 estados, ações em lote, badges)
- `conteudo/views.py` — conteudo_detalhe com `exibir_comentarios` + comentários com status
- `painel/views.py` — _dados_botao, _editar_botao, _criar_subareas (AJAX)
- `templates/conteudo_detalhe.html` — seção de comentários redesenhada
- `templates/admin/painel_central.html` — "Editar botão selecionado" (AJAX) + "Criar subárea"
- `static/css/style.css` — novos blocos CSS (comentários, layout fixes) — cache `?v=20260713-1`
- `templates/base.html` — cache-busting atualizado

### 🔄 Merge de conflito (2026-07-11)
- Um commit remoto ("codigo ngrok") havia substituído `.gitignore` inteiro por erro
- Resolvido no merge `2faca8e` mantendo versão completa do `.gitignore`
- Regra: nunca perder o `.gitignore` ao fazer pull em outro computador

---

## 🚀 Para começar novo (em novo computador)

### Opção 1: Git (recomendado)
```bash
git clone https://github.com/rabalistasedu/site-curriculos-sedu.git
cd "Site Curriculos SEDU"
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate  # Aplica migrações 0013 e 0002
python manage.py runserver 8001
```
Acesse: http://127.0.0.1:8001/

### Opção 2: Copiar pasta (sem Git)
```bash
python -m venv venv
venv\Scripts\activate
pip install django==5.2 pillow python-dateutil
python manage.py migrate  # Essencial: 0013 e 0002
python manage.py runserver 8001
```

---

## 📋 Management Commands (já executados; dados no banco)

```bash
python manage.py popular_categorias           # 10 categorias + subcategorias
python manage.py popular_descricoes           # Textos introdutórios (HTML)
python manage.py migrar_conteudo              # 102 docs do site antigo
python manage.py migrar_orientacoes           # 129 docs (Orientações Curriculares)
python manage.py migrar_ifa                   # 10 subcats + 14 docs (IFA)
python manage.py organizar_curriculo_atual    # 5 sub-botões (EI/EFI/EFF/EM/Material)
python manage.py migrar_material_apoio        # 5 docs de apoio
python manage.py migrar_projetos_integradores # 5 subcats (Projetos Integradores)
python manage.py migrar_rpe                   # 8 subcats + 42 apostilas (RPE)
python manage.py migrar_olimpiadas            # 9 subcats (Olimpíadas)
python manage.py curar_recentes                # Marca itens de "Conteúdos recentes"
python manage.py resolver_pendencias          # Arquiva 3 conteúdos sem dados
```
**Todos são idempotentes** (rodar 2x = mesmo resultado).

---

## 📁 Estrutura do projeto (atual)

```
curriculo_sedu/              # Settings, URLs, WSGI
conteudo/
  ├─ models.py              # Categoria, Conteudo (+ icone_imagem), Anexo, 
  │                         #   Banner, Cartaz, Carrossel, ConfiguracaoSite, Comentario
  ├─ admin.py               # Admin customizado (badges, widgets)
  ├─ views.py               # home, categoria, conteudo, busca
  ├─ widgets.py             # IconPicker, CategoriaPicker, RichTextWidget
  ├─ forms.py               # ConteudoAdminForm (+ icone_imagem)
  ├─ management/commands/   # 11 migration commands
  └─ migrations/            # 0001-0019 (comentários novo)
painel/                      # Painel Central Administrativo (Telas 1 e 2)
  ├─ models.py              # Vinculo, EstiloBotao (+ tamanho)
  ├─ views.py               # painel_central_view, conteudos_view (Telas 1 e 2)
  └─ migrations/            # 0001-0002 (tamanho novo)
templates/
  ├─ base.html              # Header, nav, footer
  ├─ home.html              # Hero, banners, destaques, recentes, áreas, cartazes, carrosséis
  ├─ categoria.html         # Subcategorias, filtros, conteúdos
  ├─ conteudo_detalhe.html  # Detalhe + comentários moderados
  ├─ busca.html             # Resultados de busca
  └─ admin/                 # Templates customizados do admin (painel central, organizar)
static/
  ├─ css/style.css          # Design system (?v=20260713-1)
  ├─ css/admin_picker.css   # Estilos dos widgets visuais
  ├─ js/main.js             # Slider, menu, carrossel (?v=20260711-1)
  └─ img/                   # Brasão, logos, ícones
db.sqlite3                   # Banco SQLite (365+ conteúdos)
requirements.txt
manage.py
CLAUDE.md                    # 📘 Documentação técnica completa
CONTEXTO_ATUAL.md            # 📋 Estado atual + quick start
README.md                    # 📖 Overview do projeto
```

---

## 🔧 Stack

- **Backend**: Django 5.2, Python 3.13 (local) / 3.11 (SEDU)
- **DB**: SQLite (dev e produção)
- **Frontend**: CSS puro, Font Awesome 6, Google Fonts (Inter)
- **Versionamento**: GitHub (`rabalistasedu/site-curriculos-sedu`)
- **Demo**: ngrok (URL temporária)
- **Produção**: `curriculo.sedu.es.gov.br/curriculo/` (2026)

---

## 📖 URLs principais

| Rota | Descrição |
|------|-----------|
| `/` | Home |
| `/categoria/<slug>/` | Conteúdos da categoria |
| `/conteudo/<slug>/` | Detalhe + comentários |
| `/busca/?q=termo` | Busca textual |
| `/admin/` | Django Admin |
| `/admin/painel-central/` | Painel Central (Telas 1 e 2) |
| `/admin/organizar/` | Organizador visual |
| `/admin/adicionar-arquivos/` | Upload em lote |

---

## ⚠️ Notas importantes

1. **Banco já populado** — db.sqlite3 tem tudo. Não precisa rodar commands (a menos que teste).
2. **Conteúdos apontam para URLs externas** — PDFs no WordPress/Google Drive/SEDU.
3. **Cache do navegador** — mudar CSS? Force: **Ctrl+Shift+R** (Windows/Linux) ou **Cmd+Shift+R** (Mac).
4. **GitHub** — use `.bat` "Subir GitHub SEDU" (faz pull automático agora).
5. **Migrações aplicadas** — `conteudo.0012-0019` + `painel.0002`. Para novo ambiente: `python manage.py migrate`.
6. **Superusers locais** — `ridan` (Sedu@2026), `rabalista`.

---

## 📞 Documentação

- **[CLAUDE.md](CLAUDE.md)** — Documentação técnica completa (modelos, views, admin, decisões, troubleshooting)
- **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** — Estado atual + mudanças de 2026-07-11
- **[README.md](README.md)** — Overview do projeto
- **[Especificacao_Painel_Admin_Site_Curriculos.md](Especificacao_Painel_Admin_Site_Curriculos.md)** — Spec oficial do Painel Central
- **[MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md)** — Deploy final na SEDU

---

**Última atualização**: 2026-07-13  
**Versão CSS**: `?v=20260713-1` | **Versão JS**: `?v=20260711-1`  
**GitHub**: https://github.com/rabalistasedu/site-curriculos-sedu.git
