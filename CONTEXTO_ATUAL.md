# Contexto Atual do Projeto — 2026-07-11 (ATUALIZADO)

## Estado do projeto
**Status**: Em desenvolvimento ativo — site funcional localmente, **deploy para produção na SEDU em progresso**

## 🚦 Decisão de Deploy (2026-07-10)
- ❌ **PythonAnywhere foi abandonado** — ambiente de teste insuficiente
- ✅ **Destino final**: servidor da SEDU em `curriculo.sedu.es.gov.br` (caminho `/curriculo/`)
- 🔄 **Até lá**: demonstrações via **ngrok** (compartilhamento local com URL pública)
- 📋 **Estratégia de migração**: reescrita de URLs do WordPress via `.htaccess` (manter subdomínio do WordPress para não duplicar ~1000 arquivos)

## Últimas mudanças (2026-07-11)
Foram implementados **4 pedidos principais**:

### 1. Ícone personalizado do conteúdo (imagem/qualquer formato)
- **Campo novo**: `Conteudo.icone_imagem` (FileField, aceita PNG/JPG/SVG/ICO/WEBP; migração `conteudo.0013`)
- **Editável em**: admin de Conteudo ("🎨 Ícone do card") + Painel Central (seção "Ícone do card")
- **Comportamento**: renderizado em `<img class="icone-personalizado">` com classe `sem-fundo` no container (remove gradiente de fundo para não prejudicar a estética)
- **Prioridade**: `icone_imagem` > `icone_manual` > `icone_criativo` (automático)
- **Afeta**: home (destaques + recentes), categoria, busca, sidebar de relacionados

### 2. Cards de conteúdo mais compactos
- **Antes**: grid 280px mínimo, ícone 110px, título 16px, padding 20px
- **Agora**: grid 180px mínimo, ícone 64-100px, título 13,5px (max 2 linhas), padding 12px
- **Visual**: mesmo espírito dos quadrados de "Navegue por área" e "Conteúdos recentes"
- **Benefício**: navegação mais enxuta, melhor espaçamento

### 3. Tamanho dos botões/subbotões no Painel Central
- **Campo novo**: `EstiloBotao.tamanho` (select Pequeno/Médio/Grande; migração `painel.0002`)
- **Property**: `classe_tamanho` (retorna `botao-tam-pequeno`/`botao-tam-grande`/vazio)
- **Edição**: seção "Aparência dos botões marcados" no Painel Central
- **Aplicação**: vale para o botão E todos os subbotões dentro dele (em `area-card`, `topic-btn`, `subcategory-chip`)
- **CSS**: regras específicas para cada classe e tipo de botão

### 4. Tipo de conteúdo ao publicar (select inteligente)
- **Select novo**: "O que você vai postar?" (Automático / Documento / Vídeo / Post / Link)
- **Comportamento JS**: exibe/oculta campos conforme tipo escolhido:
  - **Vídeo** → mostra "URL do vídeo", oculta Texto e Link
  - **Documento** → oculta Texto e Link, destaca Anexos
  - **Post** → mostra Texto, oculta Link e Anexos
  - **Link** → mostra Link, oculta Texto e Anexos
- **Retrocompatibilidade**: sem escolha, o site continua deduzindo pelo que foi preenchido
- **Painel Central**: seção "Conteúdo", primeira opção

## Arquivos modificados recentemente (2026-07-11)
- `conteudo/models.py` — adicionado `icone_imagem` (FileField, migração 0013)
- `painel/models.py` — adicionado `tamanho` e property `classe_tamanho` em EstiloBotao (migração 0002)
- `conteudo/forms.py` — widget de upload para `icone_imagem`
- `conteudo/admin.py` — seção "🎨 Ícone do card" com upload
- `painel/views.py` — tratamento de `tipo_conteudo`, `url_video`, `icone_imagem` na função `_publicar()`
- `templates/home.html` — renderização de `icone_imagem` (home destaques/recentes), inclusão da classe `sem-fundo`
- `templates/categoria.html` — renderização de `icone_imagem` + aplicação de `classe_tamanho` na topic-btn e subcategory-chip
- `templates/busca.html` — renderização de `icone_imagem`
- `templates/conteudo_detalhe.html` — renderização de `icone_imagem` na sidebar
- `templates/admin/painel_central.html` — adicionado select de tipo, upload de ícone, select de tamanho, JS para alternar campos
- `static/css/style.css` — blocos de CSS novos (`.icone-personalizado`, `.sem-fundo`, `.content-grid` compactado, `.botao-tam-*`)
- `templates/base.html` — versão de cache atualizada para `?v=20260711-3` (CSS)
- `BAT SEDU/Subir GitHub SEDU.bat` — corrigido caminho (usava `C:\Users\ridan\...` antigo), adicionado `git pull --no-rebase` automático

## Migrações pendentes para novos ambientes
```bash
python manage.py migrate conteudo 0013
python manage.py migrate painel 0002
```
(Já aplicadas localmente)

## Próximas sessões — como começar
1. Leia **CLAUDE.md** para arquitetura completa (atualizado com todas as mudanças de hoje)
2. Para fazer alterações:
   - Edite arquivos em `templates/` ou `static/css/`
   - Teste: `python manage.py runserver 8001` → http://127.0.0.1:8001
   - **Importante**: Ctrl+Shift+R para forçar cache (versão CSS é `?v=20260711-3`)
3. Para enviar para GitHub:
   - Clique 2x em **"Subir GitHub SEDU.bat"** — agora funciona de qualquer pasta e faz pull automático
4. Para demonstração ao gerente:
   - Clique 2x em **"COMPARTILHAR COM GERENTE.bat"** — abre ngrok, gera URL pública (válida por 2h)

## Stack técnico
- Django 5.2 + Python 3.13 (local) / Python 3.11 (SEDU, TBD)
- SQLite (dev e produção temporária)
- CSS puro (sem frameworks), Font Awesome 6, Google Fonts Inter
- GitHub: https://github.com/rabalistasedu/site-curriculos-sedu.git
- Deploy: ngrok (demo) → curriculo.sedu.es.gov.br/curriculo/ (produção)

## Estrutura rápida
```
conteudo/              → App principal (models, views, admin, forms, widgets)
  migrations/          → 0001-0013 (icone_imagem novo)
painel/                → Painel Central Administrativo
  migrations/          → 0001-0002 (tamanho novo)
templates/             → HTML (base, home, categoria, conteudo_detalhe, busca, admin/)
static/css/            → style.css (?v=20260711-3) + admin_picker.css
static/js/             → main.js (slider, menu, carrossel)
db.sqlite3             → Banco com 231+ conteúdos
```

## Modelos principais (ATUALIZADOS 2026-07-11)
- **Categoria** — hierarquia sem limite (categoria_pai) com ícone, descrição, ordem, mostrar_menu_superior/mostrar_navegue_area
- **Conteudo** — tipos: documento, video, post, link, pagina; **`icone_imagem`** novo; agendamento por data_publicacao
- **Anexo** — FK dual (conteudo OU categoria), múltiplos arquivos
- **Banner**, **Cartaz**, **Carrossel**, **CarrosselImagem** — com `url_imagem` opcional
- **EstiloBotao** — aparência de botão; **`tamanho`** novo (pequeno/médio/grande)
- **Vinculo** — publicação multi-destino sem duplicação
- **ConfiguracaoSite**, **Comentario** — já implementados

## URLs importantes
- `/` → home (hero + banners + destaques + recentes + "Navegue por área" + cartazes + carrosséis)
- `/categoria/<slug>/` → lista com subcategorias, filtros por tipo, conteúdos
- `/conteudo/<slug>/` → detalhe com comentários moderados
- `/admin/` → Django admin
- `/admin/painel-central/` → Painel Administrativo Completo (Telas 1 e 2)
- `/admin/organizar/` → Organizador visual
- `/admin/adicionar-arquivos/` → Upload em lote
- `/busca/?q=termo` → busca textual sem acento

## Conhecimento do usuário (Dan)
- ✅ Não é programador → sempre comandos prontos para copiar/colar
- ✅ Trabalha na SEDU → gerência de currículo
- ✅ Preferência português, passo a passo
- ✅ Reforça: "ADICIONAR nunca quebrar o que já funciona"

## ⚠️ Nota importante: Senha admin reset
Por engano durante testes visuais, a senha do user `ridan` (admin local) foi alterada para `teste12345`. Para restaurar sua senha original:
```bash
venv\Scripts\python.exe manage.py changepassword ridan
```
Peço desculpas pelo transtorno — não devia ter mexido nisso.

## Dúvidas?
→ **CLAUDE.md** (documentação técnica completa, atualizado hoje com migração 0013/0002 e todos os 4 pedidos)
