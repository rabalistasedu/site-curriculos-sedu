# Contexto Atual do Projeto — 2026-07-07

## Estado do projeto
**Status**: Em desenvolvimento ativo — site funcional e publicado em PythonAnywhere

## Últimas alterações (2026-07-07)
1. **Logo pulsante** — Logo "Currículo Espírito Santo" tem efeito de ondulação em páginas internas (categoria, conteúdo, busca) para convidar retorno à home
   - Implementado em: `base.html`, `categoria.html`, `conteudo_detalhe.html`, `busca.html`
   - CSS: `.logo.logo-pulse` com animação `logoPulse` (2s) e hover effects

2. **Ícone em "Navegue por área"** — Adicionado ícone de bússola (`fas fa-compass`) antes do texto na home
   - Arquivo: `templates/home.html` (linha ~131)

3. **Botão "Currículo Atual" centralizado** — Ícone e texto perfeitamente centrados no botão azul
   - CSS: `.area-card-featured` + `.area-text` com flexbox `center`

## Arquivos principais modificados recentemente
- `static/css/style.css` — novo CSS para logo pulsante + botão centralizado
- `templates/base.html` — adicionado bloco `{% block logo_class %}`
- `templates/home.html` — adicionado ícone em "Navegue por área"
- `templates/categoria.html`, `conteudo_detalhe.html`, `busca.html` — adicionado `{% block logo_class %}logo-pulse{% endblock %}`
- `CLAUDE.md` — documentação completa atualizada

## Próximas sessões — como começar
1. Leia **CLAUDE.md** para entender a arquitetura completa do projeto
2. Para fazer alterações:
   - Edite os arquivos em `templates/` ou `static/css/`
   - Teste localmente: `python manage.py runserver` → http://127.0.0.1:8000
   - **Importante**: Aperte **Ctrl+Shift+R** ao testar CSS (força recarregamento sem cache)
3. Para enviar para GitHub:
   - Clique 2x em **"Subir GitHub SEDU.bat"** na área de trabalho
   - Digite a mensagem do commit e aperte Enter
4. Para publicar no PythonAnywhere:
   - Terminal bash PythonAnywhere: `cd ~/site-curriculos-sedu && git pull origin main && python manage.py migrate && python manage.py collectstatic --noinput`
   - Painel Web do PythonAnywhere: clique **Reload**

## Stack técnico
- Django 5.2 + Python 3.13 (local) / 3.11 (PythonAnywhere)
- SQLite (desenvolvimento e produção)
- CSS puro (sem frameworks), Font Awesome 6, Google Fonts Inter
- GitHub: https://github.com/DanBalista/site-curriculos-sedu.git
- PythonAnywhere: https://rabalista.pythonanywhere.com

## Estrutura rápida
```
conteudo/              → App principal (models, views, admin, forms, widgets)
templates/             → HTML (base, home, categoria, conteudo_detalhe, busca, admin/)
static/css/            → style.css (design system) + admin_picker.css
static/js/             → main.js (slider hero, menu mobile)
db.sqlite3             → Banco com 230+ conteúdos
```

## Modelos principais
- **Categoria** — hierarquia de 2 níveis (categoria_pai) com ícone, descrição, ordem
- **Conteudo** — tipos: documento, video, post, link, pagina. Agendamento por data_publicacao
- **Anexo** — FK dual (conteudo OU categoria), múltiplos arquivos com ordem editável
- **Banner**, **Comentario**, **Cartaz**, **ConfiguracaoSite** — já implementados

## URLs importantes
- `/` → home
- `/categoria/<slug>/` → lista de conteúdos com filtros
- `/conteudo/<slug>/` → detalhe com comentários
- `/admin/` → Django admin
- `/admin/organizar/` → Organizador visual de categorias e conteúdos
- `/busca/?q=termo` → busca textual

## Conhecimento do usuário (Dan)
- **Não é programador** — sempre forneça comandos prontos para copiar/colar
- **Trabalha na SEDU** — site para Gerência de Currículo da Educação Básica
- **Preferência**: instruções em português, passo a passo

## Dúvidas?
Consulte **CLAUDE.md** para:
- Estrutura completa do projeto
- Decisões de design já tomadas
- Como adicionar conteúdo (via admin)
- Management commands (migrar_conteudo, popular_categorias, etc.)
- Notas sobre anexos, cartazes, comentários, organizador
