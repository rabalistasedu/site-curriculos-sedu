# 🎓 SITE CURRÍCULO SEDU — Resumo de Contexto

## Estado atual: PRATICAMENTE COMPLETO ✅

Projeto de migração de site WordPress → Django 5.2 para SEDU (Secretaria Educação ES).  
**Status do banco**: 231+ conteúdos migrados, 10 categorias principais, 42+ subcategorias.

---

## ⚡ Para entender onde estamos

### Categorias principais (menu "Navegue por área")
1. **Documentos Curriculares** — Currículo Atual (5 sub-etapas) + Material de Apoio + 7 subcategorias  
2. **Orientações Curriculares** — 129 docs + 16 subcategorias  
3. **Itinerários Formativos de Aprofundamento (IFA)** — 10 subcategorias, 14 docs  
4. **Projetos Integradores** — 5 subcategorias, texto introdutório  
5. **Rotinas Pedagógicas Escolares (RPE)** — 8 subcategorias, **42 apostilas** (LP/Mat × EF/EM × Estudante/Prof × Trimestres)  
6. **Programas**, **Livro Didático**, **Modalidades e Diversidade**  
7. **Olimpíadas** — 9 subcategorias (OBF, OBFEP, OLITEF, Meninas Olímpiadas, Empreendedorismo, Biologia Sintética, Prêmio Jovem Cientista, Bem Público, Jovem Senador) + texto introdutório  
8. **Institucional**

### Dados no banco
- **SQLite** (`db.sqlite3`) — já com todos os dados migrados
- **231+ conteúdos** de tipos: documento, video, post, link, página
- **Sistema de comentários** com moderação (substitui Disqus do WordPress)
- **Agendamento de publicação** por data/hora futura
- **Banners rotativos** por área, tamanho configurável
- **Cartazes de eventos** na home (desktop: laterais presos à área branca; mobile: botão flutuante)

### Deploy em produção
- **URL**: https://rabalista.pythonanywhere.com  
- **Servidor**: PythonAnywhere (`rabalista`, Python 3.11)  
- **Sincronização**: git pull → migrate → collectstatic → Reload

---

## 🚀 Para levar no pendrive e clonar no trabalho

### Opção 1: Git (recomendado — pega tudo sincronizado)
```bash
cd seu\caminho\local
git clone https://github.com/DanBalista/site-curriculos-sedu.git
cd site-curriculos-sedu
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```
Acesse: http://127.0.0.1:8000/  
Admin: http://127.0.0.1:8000/admin/

### Opção 2: Copiar pasta do pendrive (se não tiver Git no trabalho)
1. Copie a pasta inteira `Site Curriculos SEDU` para seu computador
2. Abra terminal ali e rode:
```bash
python -m venv venv
venv\Scripts\activate  (Windows)
pip install django=5.2 pillow python-dateutil
python manage.py runserver
```

---

## 📋 Comandos essenciais (já executados, mas úteis para entender)

**Populam o banco:**
```bash
python manage.py popular_categorias           # 10 categorias principais
python manage.py popular_descricoes           # Textos intro (HTML)
python manage.py migrar_conteudo              # 102 docs do WordPress
python manage.py migrar_orientacoes           # 129 docs
python manage.py migrar_ifa                   # IFA: 10 subcats, 14 docs
python manage.py organizar_curriculo_atual    # Sub-botões EI/EFI/EFF/EM
python manage.py migrar_material_apoio        # 5 docs
python manage.py migrar_projetos_integradores # 5 subcats
python manage.py migrar_rpe                   # 8 subcats, 42 apostilas
python manage.py migrar_olimpiadas            # 9 subcats de olimpíadas
python manage.py curar_recentes                # Marca a seleção oficial de "Conteúdos recentes"
```
**Todos são idempotentes** (rodar 2x = mesmo resultado).

---

## 🎯 O que foi feito recentemente

### Últimas migrações e ajustes visuais (commits no GitHub)
1. **`organizar_curriculo_atual`** — "Currículo Atual" agora tem 5 sub-botões (Educação Infantil, EF Anos Iniciais, EF Anos Finais, Ensino Médio, Material de Apoio)
2. **`migrar_material_apoio`** — 5 documentos de apoio (MEC, OMEP, Porvir, PAEBES matrizes)
3. **`migrar_projetos_integradores`** — Nova categoria "Projetos Integradores" com 5 subcategorias
4. **`migrar_rpe`** — Nova categoria "Rotinas Pedagógicas Escolares" com **42 apostilas** em 8 subcategorias
5. **`migrar_olimpiadas`** — Categoria "Olimpíadas" reorganizada com 9 subcategorias oficiais + texto introdutório
6. **Ajustes visuais**: barra inferior do rodapé reduzida (18px, azul médio, texto branco, tudo inline); scrollbar em "Conteúdos recentes" e "Navegue por área"; botão "Eventos" mobile agora só ≤900px
7. **"Conteúdos recentes" curado**: novo campo `recente` no modelo Conteudo. Checkbox no admin (abaixo de "Destaque"). Só itens marcados aparecem na seção da home. Migração `0009_conteudo_recente`
8. **Curadoria automatizada**: como `db.sqlite3` não vai pelo Git (cada ambiente tem seu banco), o comando `curar_recentes` marca automaticamente os mesmos 5 itens em qualquer ambiente — **rode esse comando sempre que configurar o site em um computador novo** (não precisa marcar manualmente no admin)

### Problemas resolvidos recentemente
- ❌ Cartazes invadindo faixa azul do header/footer → ✅ CSS puro (position: sticky) agora prende ao branco
- ❌ Menu cortado em telas ~1200px → ✅ Ícones ocultados, textos reduzidos
- ❌ RPE vazio no PythonAnywhere → ✅ Comando `migrar_rpe` move docs existentes (não só cria)
- ❌ "Currículo Atual" com 18 docs sem organização → ✅ Agora dividido em 5 sub-botões por etapa
- ❌ Botão "Eventos" mobile aparecia atrás/sobreposto em desktop pequeno → ✅ Breakpoint mudado para 900px
- ❌ Barra inferior do rodapé muito grande e escura → ✅ Reduzida a 18px, cor azul médio, texto branco em linha única
- ❌ Seções "Conteúdos recentes" e "Navegue por área" cresciam indefinidamente → ✅ Scrollbar interna com max-height: 600px

---

## 📁 Estrutura do projeto

```
site-curriculos-sedu/
├── curriculo_sedu/          # Settings, URLs, WSGI
├── conteudo/
│   ├── models.py            # Categoria, Conteudo, Banner, Comentario, Cartaz, ConfiguracaoSite
│   ├── admin.py             # Admin customizado (badges, widgets, moderação)
│   ├── views.py             # home, categoria_detalhe, conteudo_detalhe, busca
│   ├── widgets.py           # IconPicker, CategoriaPicker, RichTextWidget
│   ├── forms.py             # Formulários do admin
│   ├── management/commands/ # 8 migration commands (popular_*, migrar_*)
│   └── migrations/          # Django migrations
├── templates/
│   ├── base.html            # Header (logos), nav dinâmica, footer
│   ├── home.html            # Hero + banners, "Conteúdos recentes" + "Navegue por área" + cartazes
│   ├── categoria.html       # Subcategorias, filtros por tipo, conteúdos
│   ├── conteudo_detalhe.html# Detalhe + comentários (moderação)
│   └── busca.html           # Resultados de busca
├── static/
│   ├── css/style.css        # Design system (vars cores, layout, componentes)
│   ├── css/admin_picker.css # Estilos widgets admin
│   ├── js/main.js           # Hero slider, menu mobile, cartazes
│   └── img/                 # Logos, banner
├── db.sqlite3               # Banco com 231+ conteúdos
├── requirements.txt         # Django 5.2, Pillow, python-dateutil
├── manage.py
└── CLAUDE.md                # Documentação técnica completa
```

---

## 🔧 Stack

- **Backend**: Django 5.2, Python 3.13 (local) / 3.11 (produção)
- **DB**: SQLite (dev e prod)
- **Frontend**: CSS puro, Font Awesome 6 (ícones), Google Fonts (Inter)
- **Deploy**: PythonAnywhere
- **Versionamento**: GitHub

---

## ⚠️ Notas importantes

1. **Banco já está populado** — db.sqlite3 tem tudo. Não precisa rodar commands novamente (a menos que queira testar/resetar).

2. **Conteúdos apontam para URLs externas** — PDFs estão no WordPress, Google Drive, SEDU; não armazenados localmente.

3. **No trabalho, Git é recomendado**:
   - Clonar: `git clone https://github.com/DanBalista/site-curriculos-sedu.git`
   - Depois de editar: `git add .` → `git commit -m "..."` → `git push origin main`
   - Sync com PythonAnywhere: `cd ~/site-curriculos-sedu && git pull origin main`

4. **Cache de browser** — Se mudar CSS e não ver no navegador, força recarregamento:
   - Windows/Linux: Ctrl+Shift+R
   - Mac: Cmd+Shift+R

5. **Para publicar no PythonAnywhere**:
   ```bash
   # Lá no PythonAnywhere (terminal Bash)
   cd ~/site-curriculos-sedu
   git pull origin main
   source venv/bin/activate
   python manage.py migrate
   python manage.py collectstatic --noinput
   # Depois: Web tab → Reload
   ```

---

## 📞 Contato / Debug

- **CLAUDE.md** — Documentação técnica completa (modelos, URLs, decisões de design, troubleshooting)
- **GitHub**: https://github.com/DanBalista/site-curriculos-sedu.git
- **Deploy**: https://rabalista.pythonanywhere.com (teste)
- **Admin local**: http://127.0.0.1:8000/admin/
  - Cria superuser: `python manage.py createsuperuser`

---

## ✅ Checklist ao chegar no trabalho

- [ ] Clonar do GitHub OU copiar pasta do pendrive
- [ ] Criar venv e instalar dependências (`pip install -r requirements.txt`)
- [ ] **Se clonou do GitHub (banco vazio)**: rodar todos os comandos da seção "Comandos essenciais" acima, na ordem, terminando com `curar_recentes` — isso popula o banco do zero e já deixa "Conteúdos recentes" com a curadoria certa, sem precisar clicar em nada no admin
- [ ] **Se copiou a pasta pelo pendrive** (banco já vem preenchido): não precisa rodar os comandos de novo, só `python manage.py migrate` para garantir que a estrutura está em dia
- [ ] Rodar `python manage.py runserver`
- [ ] Abrir http://127.0.0.1:8000 no navegador
- [ ] Testar admin em http://127.0.0.1:8000/admin/
- [ ] Ler CLAUDE.md para entender modelos e URLs
- [ ] Qualquer mudança → git add/commit/push (ou avisar para sincronizar)

**Boa sorte! 🚀**
