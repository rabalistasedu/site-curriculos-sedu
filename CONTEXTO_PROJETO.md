# 🎓 SITE CURRÍCULO SEDU — Resumo de Contexto (2026-07-11)

## Estado atual: FUNCIONAL E EM TRANSIÇÃO ✅➡️🚀

Projeto de migração de site WordPress → Django 5.2 para SEDU (Secretaria Educação ES).  
**Status do banco**: 231+ conteúdos migrados, 10 categorias principais, 42+ subcategorias.  
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
- **SQLite** (`db.sqlite3`) — 231+ conteúdos (documento, video, post, link, página)
- **Sistema de comentários** com moderação (substitui Disqus)
- **Agendamento de publicação** por data/hora futura
- **Banners rotativos** por área, tamanho configurável
- **Cartazes de eventos** (desktop sticky nas laterais, mobile botão flutuante)
- **Carrosséis de imagens** (novo 2026-07-11) com autoplay e código HTML customizável

---

## 🆕 O que mudou em 2026-07-11

### ✨ 4 Pedidos Implementados

#### 1. Ícone personalizado (imagem/qualquer formato)
- Campo novo: `Conteudo.icone_imagem` (FileField, aceita PNG/JPG/SVG/ICO/WEBP)
- Migração: `conteudo.0013`
- Editável em: admin de Conteudo + Painel Central
- Renderização: `<img class="icone-personalizado">` com classe `sem-fundo` (remove gradiente de fundo)
- Prioridade: `icone_imagem` > `icone_manual` > automático
- Afeta: home (destaques + recentes), categoria, busca, sidebar

#### 2. Cards de conteúdo mais compactos
- **Grid**: 280px → 180px mínimo
- **Ícone**: 110px → 64-100px
- **Título**: 16px → 13,5px (max 2 linhas)
- **Padding**: 20px → 12px
- **Visual**: mesmo espírito do "Navegue por área" e "Conteúdos recentes" quadrados

#### 3. Tamanho dos botões/subbotões no Painel Central
- Campo novo: `EstiloBotao.tamanho` (select Pequeno/Médio/Grande)
- Migração: `painel.0002`
- Property: `classe_tamanho` (retorna `botao-tam-pequeno`/`botao-tam-grande`/vazio)
- Edição: seção "Aparência dos botões marcados" do Painel Central
- Aplicação: vale para o botão E todos os subbotões de dentro dele
- CSS: regras específicas em `area-card`, `topic-btn`, `subcategory-chip`

#### 4. Tipo de conteúdo ao publicar (select inteligente)
- Select "O que você vai postar?" (Automático / Documento / Vídeo / Post / Link)
- JS mostra/oculta campos:
  - **Vídeo** → "URL do vídeo" (novo campo `url_video`)
  - **Documento** → Anexos visíveis
  - **Post** → Texto visível
  - **Link** → URL externa visível
- Retrocompatibilidade: sem escolha, site deduz pelo conteúdo preenchido (comportamento antigo)
- Painel Central: seção "Conteúdo", primeira opção

### 📝 Arquivos modificados
- `conteudo/models.py` — `icone_imagem` + url_video atualizado
- `painel/models.py` — `tamanho` em EstiloBotao + property `classe_tamanho`
- `conteudo/forms.py` — widget para `icone_imagem`
- `painel/views.py` — tratamento de `tipo_conteudo`, `url_video`, `icone_imagem`
- `templates/` (5 arquivos) — renderização de `icone_imagem` + `classe_tamanho`
- `templates/admin/painel_central.html` — select de tipo, upload ícone, select tamanho, JS dinâmico
- `static/css/style.css` — CSS novo, cache `?v=20260711-3`
- `BAT SEDU/Subir GitHub SEDU.bat` — corrigido caminho (era `C:\Users\ridan\...` antigo), adicionado `git pull --no-rebase`

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
  └─ migrations/            # 0001-0013 (icone_imagem novo)
painel/                      # Painel Central Administrativo
  ├─ models.py              # Vinculo, EstiloBotao (+ tamanho)
  ├─ views.py               # painel_central_view, conteudos_view (Telas 1 e 2)
  └─ migrations/            # 0001-0002 (tamanho novo)
templates/
  ├─ base.html              # Header, nav, footer
  ├─ home.html              # Hero, banners, destaques, recentes, áreas, cartazes, carrosséis
  ├─ categoria.html         # Subcategorias, filtros, conteúdos
  ├─ conteudo_detalhe.html  # Detalhe + comentários
  ├─ busca.html             # Resultados de busca
  └─ admin/                 # Templates customizados do admin (painel central, organizar)
static/
  ├─ css/style.css          # Design system (?v=20260711-3)
  ├─ css/admin_picker.css   # Estilos dos widgets visuais
  ├─ js/main.js             # Slider, menu, carrossel (?v=20260711-1)
  └─ img/                   # Logos, brasão, ícones
db.sqlite3                   # Banco SQLite (231+ conteúdos)
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
5. **Migrações novas** — `conteudo.0013` (icone_imagem) + `painel.0002` (tamanho).
6. **Senha admin** — foi alterada para `teste12345` durante testes. Para restaurar:
   ```bash
   venv\Scripts\python.exe manage.py changepassword ridan
   ```

---

## 📞 Documentação

- **[CLAUDE.md](CLAUDE.md)** — Documentação técnica completa (modelos, views, admin, decisões, troubleshooting)
- **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** — Estado atual + mudanças de 2026-07-11
- **[README.md](README.md)** — Overview do projeto
- **[Especificacao_Painel_Admin_Site_Curriculos.md](Especificacao_Painel_Admin_Site_Curriculos.md)** — Spec oficial do Painel Central
- **[MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md)** — Deploy final na SEDU

---

**Última atualização**: 2026-07-11  
**Versão CSS**: `?v=20260711-3` | **Versão JS**: `?v=20260711-1`  
**GitHub**: https://github.com/rabalistasedu/site-curriculos-sedu.git
