# Contexto Atual do Projeto — 2026-07-21 (ATUALIZADO — parte 32)

## Estado do projeto
**Status**: ✅ Pronto para produção — site funcional com Docker + Backup/Restore, **9 implementações finalizadas**, **32 partes completadas, 60+ features/bugs**

## 🚦 Decisão de Deploy (2026-07-10)
- ❌ **PythonAnywhere foi abandonado** — ambiente de teste insuficiente
- ✅ **Destino final**: servidor da SEDU em `curriculo.sedu.es.gov.br` (caminho `/curriculo/`)
- 🔄 **Até lá**: demonstrações via **ngrok** (compartilhamento local com URL pública — **UTF-8 e vídeo AGORA funcionando**)
- 📋 **Estratégia de migração**: reescrita de URLs do WordPress via `.htaccess` (manter subdomínio do WordPress para não duplicar ~1000 arquivos)

## 🎯 Leva Mais Recente: Parte 32 (2026-07-21)

**9 implementações concluídas** do documento `implementar.md`:

1. ✅ **Ícone personalizado galeria** (Estrutura de Árvores) — clique em thumbnail da galeria + salvar aplica sem upload
2. ✅ **Categorias raiz em "Conteúdos Recentes"** — botões raiz marcados aparecem como cards na home
3. ✅ **Imagens do rodapé** — novo modelo `RodapeImagem` + painel em Editor do Rodapé (altura fixa 44px, 3 alinhamentos, quantas quiser)
4. ✅ **Nome customizável "Currículo Atual"** — novo campo `ConfiguracaoSite.nome_curriculo_atual`, editável no admin
5. ✅ **Botões em área central** — confirmado que já existia (parte 13), sem duplicação
6. ✅ **Brasão personalizado** — novo campo `ConfiguracaoSite.brasao_imagem` + alinhamento/tamanho, fallback para padrão
7. ✅ **Segundo logotipo** — novos campos `logo2_imagem/alinhamento/tamanho`, renderiza no cabeçalho se preenchido
8. ✅ **Tudo com zero breaking changes** — campos opcionais, fallback automático quando vazios
9. ✅ **Migração 0034** aplicada com sucesso (RodapeImagem + 10 campos ConfiguracaoSite)

**Arquivos alterados**: models.py, migrations/0034, views.py, admin_views.py, arvore_views.py, admin.py, context_processors.py, base.html, home.html, style.css, editor_rodape.html

**Testado**: ✅ django check, migrações, funcionalidade fim-a-ponta, navegador, backward compatibility

---

## Histórico de mudanças (2026-07-12 a 2026-07-13)
Foram implementadas **9 partes de correções + features (20 no total)**:

### Parte 1—4: Bugs de layout + funcionalidade (2026-07-12, morning-afternoon)
1. ✅ **Navegação embolada no mobile** — regra global de 2 colunas limitada a 861px+
2. ✅ **Carrossel dividido no painel Eventos** — agora entra como widget funcional
3. ✅ **Carrossel invadindo rodapé** — faltava `max-height: 100%`
4. ✅ **Anexos de conteúdo invisíveis** — seção de download adicionada à página de detalhe
5. ✅ **Subbotões invisíveis como cards** — agora aparecem no grid com borda azul
6. ✅ **Busca da árvore 3+ níveis** — ancestrais expandem automaticamente
7. ✅ **Rodapé flutuando** — flexbox sticky footer (body 100vh + flex:1 no main)

### Parte 5: Edição inline + features (2026-07-12, evening)
8. ✅ **Editar botão selecionado** — seção verde AJAX no Painel Central (nome, descrição, ícone, anexo)
9. ✅ **Botões sem pai → "Botões novos criados"** — categoria raiz oculta automática
10. ✅ **CategoriaPicker dinâmico** — categorias vazias agora aparecem no picker
11. ✅ **Criar subárea nos botões marcados** — nova seção azul para criar subáreas em lote

### Parte 6: Carrossel admin + URL (2026-07-12, evening)
12. ✅ **Carrossel admin** — `ClearableFileInput` mostra arquivo atual + "Limpar" + "Modificar"
13. ✅ **Campo URL no painel** — cria automaticamente Conteudo tipo "link"

### Parte 7: Sistema de Comentários Moderados (2026-07-13)
14. ✅ **Sistema de comentários** — 3 estados (pendente/publicado/recusado)
15. ✅ **Resposta do admin** — campo editável com data automática
16. ✅ **Exclusão de tipo "link"** — comentários não aparecem em links externos
17. ✅ **Visual moderno** — badge, botão gradiente, aviso de moderação, seção colapsável

### Parte 8: Respostas + Votos em comentários (2026-07-13)
18. ✅ **Respostas de visitantes aninhadas** — `Comentario.parent` (FK self) para threads. Formulário inline "Responder" com comportamento show/hide animado. Respostas renderizadas recuadas com label "↩ resposta" em roxo.
19. ✅ **Votos 👍/👎 AJAX** — contador de `votos_positivos`/`votos_negativos`. Endpoint `/comentario/<pk>/votar/` (POST). Cada visitante vota 1x por sessão (desabilita botões após click). Atualiza contador sem reload.

### Parte 9: ngrok UTF-8 + Video Streaming (2026-07-13)
20. ✅ **Double-encoding UTF-8 corrigido** — templates restaurados do commit anterior; caracteres como "Currículos", "Educação" agora aparecem corretamente em localhost E via ngrok
21. ✅ **Vídeo do carrossel agora funciona via ngrok** — nova view Django `serve_media` com HTTP Range Requests (206 Partial Content) para streaming de vídeo 37MB. Testado com curl: funciona perfeitamente
22. ✅ **Automação completa** — scripts `teste_ngrok.py` (validação) + `INICIAR COM NGROK.bat` (launcher um-clique) + BAT melhorado com UTF-8
23. ✅ **Documentação nova** — `NGROK_COMPARTILHAR.md` (guia em português) + `RESUMO_FIXES_2026_07_13.md` (técnico) para futuras sessões

---

## Ícone personalizado do conteúdo (2026-07-11)
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

## Migrações aplicadas e pendentes
**Já aplicadas nesta máquina:**
- `conteudo.0012` — Carrossel, url_imagem, mostrar_menu_superior/mostrar_navegue_area
- `conteudo.0013` — icone_imagem em Conteudo
- `conteudo.0014` — icone_imagem em Categoria
- `conteudo.0015` — Carrossel aceita vídeo (FileField)
- `conteudo.0016` — Estilo de texto em Conteudo
- `painel.0002` — EstiloBotao.tamanho
- **`conteudo.0019`** — Comentario: status (3 estados) + resposta + data_resposta

**Para novos ambientes:**
```bash
python manage.py migrate  # Aplica TUDO de uma vez
```

## Próximas sessões — como começar
1. Leia **CLAUDE.md** para arquitetura completa (atualizado com todas as mudanças até 2026-07-13, parte 7)
2. Para fazer alterações:
   - Edite arquivos em `templates/` ou `static/css/`
   - Teste: `python manage.py runserver 8001` → http://127.0.0.1:8001
   - **Importante**: Ctrl+Shift+R para forçar cache (versão CSS é **`?v=20260713-1`**)
3. Para enviar para GitHub:
   - Clique 2x em **"Subir GitHub SEDU.bat"** — agora funciona de qualquer pasta e faz pull automático + migrate
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
  migrations/          → 0001-0019 (comentários moderados novo)
painel/                → Painel Central Administrativo
  migrations/          → 0001-0002 (tamanho novo)
templates/             → HTML (base, home, categoria, conteudo_detalhe, busca, admin/)
static/css/            → style.css (?v=20260713-1) + admin_picker.css
static/js/             → main.js (slider, menu, carrossel)
db.sqlite3             → Banco com 365+ conteúdos
```

## Modelos principais (ATUALIZADOS 2026-07-13)
- **Categoria** — hierarquia sem limite (categoria_pai) com ícone, descrição, ordem, mostrar_menu_superior/mostrar_navegue_area, **icone_imagem novo**
- **Conteudo** — tipos: documento, video, post, link, pagina; **`icone_imagem`**, estilo de texto; agendamento por data_publicacao
- **Anexo** — FK dual (conteudo OU categoria), múltiplos arquivos
- **Banner**, **Cartaz**, **Carrossel**, **CarrosselImagem** — com `url_imagem` opcional; carrossel aceita vídeos (FileField)
- **EstiloBotao** — aparência de botão; **`tamanho`** novo (pequeno/médio/grande)
- **Vinculo** — publicação multi-destino sem duplicação
- **ConfiguracaoSite** — singleton com dados do site
- **Comentario** — **3 estados (pendente/publicado/recusado)**, resposta do admin, data_resposta automática; não aparece em tipo='link'

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

## ⚠️ Nota importante: Credenciais de teste
**Superusers locais**: `ridan` (senha `Sedu@2026`) e `rabalista`

Para alterar senha:
```bash
venv\Scripts\python.exe manage.py changepassword <username>
```

## Dúvidas?
→ **CLAUDE.md** (documentação técnica completa, atualizado hoje com migração 0013/0002 e todos os 4 pedidos)
