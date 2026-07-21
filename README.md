# Site Currículos SEDU

**Migração WordPress → Django 5.2** para a Gerência de Currículo da Educação Básica (GECEB), Secretaria de Estado da Educação (SEDU) – Espírito Santo.

## Status Atual (2026-07-21 — Parte 32 + 9 Implementações do implementar.md)

✅ **Site funcional e responsivo** – 588 conteúdos, 132 categorias, organização hierárquica ilimitada  
✅ **9 painéis administrativos** – Organizador, Adicionar Arquivos, Painel Central (Telas 1+2), Barra Superior, Estrutura de Árvores, Área do Site, Editor do Rodapé, Central de Inteligência  
✅ **Sistema de comentários** – 3 estados (pendente/publicado/recusado), respostas aninhadas, votos 👍/👎  
✅ **Infraestrutura Docker** – PostgreSQL 16 + Postgres pronto para produção, SQLite local intacto  
✅ **Backup/Restore automático** – `.bat` para sincronizar dados locais ↔ Docker em 1 clique  
✅ **Deploy** – ngrok (demo) + próximo: `curriculo.sedu.es.gov.br/curriculo/` (SEDU)

## Quick Start

```bash
# Clone do GitHub
git clone https://github.com/rabalistasedu/site-curriculos-sedu.git
cd "Site Curriculos SEDU"

# Ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Dependências
pip install -r requirements.txt

# Migrações (se novo ambiente)
python manage.py migrate

# Rodar local
python manage.py runserver 8001
```

Acesse: **http://127.0.0.1:8001** (site) | **http://127.0.0.1:8001/admin/** (admin)

## Últimas Implementações (2026-07-11 a 2026-07-21)

### 32 Partes de Implementação (60+ features/bugs total)
- **Partes 1-10**: 6 bugs de layout/UX + 8 features (edição inline, carrossel admin, comentários, respostas, votos)
- **Partes 11-21**: 6 correções + 8 features (duplicação, Estrutura de Árvores, Currículo Atual central, subáreas, Área do Site, ícones, delegação de acesso)
- **Partes 22-28**: arrastar-e-soltar (anexos + todos painéis), vários links (URL), banner automático + faixa fina
- **Partes 29-31**: **Docker/PostgreSQL**, **Backup/Restore**, **Organizador com árvore completa no "Mover para"**
- **Parte 32**: **9 Implementações** — ícone galeria (Estrutura), categorias recentes (home), imagens rodapé, nome Currículo Atual, identidade visual cabeçalho

**Migrações novas**: `conteudo.0012-0034` + `painel.0002-0003` + `inteligencia.0002`

→ Veja **[CLAUDE.md](CLAUDE.md)** para detalhes completos

## Estrutura

```
conteudo/               → App principal (models, views, admin, forms, widgets, arvore_views, permissoes)
painel/                 → Painel Central Administrativo (Telas 1 + 2, Vinculo, EstiloBotao)
inteligencia/           → Central de Inteligência (estatísticas, alertas, exports)
templates/
  ├─ base.html          → Layout base (header, nav, footer com flexbox sticky)
  ├─ home.html          → Hero (faixa 130px), destaques, recentes, áreas, colunas extras
  ├─ categoria.html     → Conteúdos com filtros, subbotões como cards, anexos
  ├─ conteudo_detalhe.html → Detalhe + comentários moderados + votos
  └─ admin/             → 9 painéis: organizar, adicionar-arquivos, painel-central,
                         painel-conteudos, barra-superior, estrutura-arvores,
                         area-do-site, editor-rodape, inteligencia
static/
  ├─ css/style.css      → Design system (atualizado ?v=20260718-2)
  ├─ js/                → main.js, dropzone.js, filtro_select.js
  └─ img/               → Brasão (50px), GECEB logo, ícones
db.sqlite3              → Banco SQLite (588 conteúdos, 132 categorias)
docker-compose.yml      → Orquestração: db (Postgres 16) + web (Django)
Dockerfile              → Build da imagem Django com Python 3.12
CLAUDE.md               → Documentação técnica completa (v27 – 2026-07-19, Parte 31)
```

## Modelos Principais

- **Categoria** – hierarquia ilimitada, ícone, descrição, ordem, visibilidade por seção
- **Conteudo** – tipos (documento/video/post/link/pagina), icone_imagem novo, agendamento
- **Comentario** – 3 estados (pendente/publicado/recusado), respostas aninhadas, votos 👍/👎
- **Anexo** – FK dual (conteudo OU categoria), múltiplos arquivos
- **Banner**, **Cartaz**, **Carrossel** – com URL de imagem opcional
- **EstiloBotao** – cores, fonte, tamanho novo, pulsante
- **Vinculo** – publicação multi-destino sem duplicação

## URLs Principais

| Rota | Descrição |
|------|-----------|
| `/` | Home (hero faixa 130px, destaques, recentes, navegue por área, colunas extras) |
| `/categoria/<slug>/` | Conteúdos com filtros, subbotões, anexos, comentários |
| `/conteudo/<slug>/` | Detalhe + comentários moderados (3 estados) + votos AJAX |
| `/busca/?q=termo` | Busca sem acento em conteúdos e botões |
| `/admin/` | Django Admin (modelos principais) |
| `/admin/organizar/` | **Organizador** – gerenciar conteúdos e anexos por categoria |
| `/admin/adicionar-arquivos/` | **Adicionar Arquivos** – upload em lote + subcategorias |
| `/admin/painel-central/` | **Painel Central Tela 1** – árvore + publicação multi-destino |
| `/admin/painel-central/conteudos/` | **Painel Central Tela 2** – listagem geral de conteúdos |
| `/admin/barra-superior/` | **Barra Superior** – 5 botões fixos no topo |
| `/admin/estrutura-arvores/` | **Estrutura de Árvores** – 133 nós interativos, CRUD, drag-drop, biblioteca ícones |
| `/admin/area-do-site/` | **Área do Site** – títulos formatáveis + colunas extras personalizadas |
| `/admin/editor-rodape/` | **Editor do Rodapé** – 3 colunas de links + contato |
| `/admin/inteligencia/` | **Central de Inteligência** – estatísticas, alertas, exports Excel/PDF |

## Stack

- **Backend**: Django 5.2, Python 3.13 (local) / 3.12 (Docker)
- **DB Local**: SQLite (desenvolvimento, intacto)
- **DB Docker/Produção**: PostgreSQL 16
- **Frontend**: CSS puro, Font Awesome 6 (ícones), Google Fonts (Inter)
- **Versionamento**: GitHub (`rabalistasedu/site-curriculos-sedu`)
- **Demo**: ngrok (URL pública temporária com UTF-8)
- **Containerização**: Docker + Docker Compose (pronto para SEDU)
- **Produção**: `curriculo.sedu.es.gov.br/curriculo/` (em progresso)

## Deploy

### Desenvolvimento Local (SQLite — padrão)
```bash
# Clone + setup
git clone https://github.com/rabalistasedu/site-curriculos-sedu.git
cd "Site Curriculos SEDU"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Rodar (SQLite automaticamente)
python manage.py runserver 8001
# Acesse: http://127.0.0.1:8001/admin/ (superuser: ridan / Sedu@2026)
```

### Docker + PostgreSQL (Sincronização local → Docker)
```bash
# 1. Certifique-se de que Docker Desktop está aberto
# 2. Clique no ".bat" (mais fácil) ou rodeo comando:
"BAT SEDU\ATUALIZAR BANCO DOCKER.bat"

# Ou manualmente (5 passos automáticos no .bat):
python manage.py dumpdata -e contenttypes -e auth.permission -e admin.logentry -e sessions --indent 2 -o dump_local.json
docker compose up -d --build
docker compose exec -T web python manage.py migrate
docker compose exec -T web python manage.py flush --no-input
docker compose exec -T web python manage.py loaddata dump_local.json

# Site no Docker (PostgreSQL): http://localhost:8000
```

### Backup/Restore Completo (Parte 31)
```bash
# Fazer backup (banco + mídia + código)
"BAT SEDU\BACKUP DOCKER COMPLETO.bat"

# Restaurar em outro PC (copie a pasta gerada)
"BAT SEDU\RESTAURAR ESTE BACKUP.bat"
```

### Demonstração ao gerente (ngrok):
```bash
# Opção 1: Usar BAT (mais fácil)
"BAT SEDU\INICIAR COM NGROK.bat"

# Opção 2: Manualmente
python teste_ngrok.py         # testa tudo
python ngrok_compartilhar.py  # compartilha com ngrok
```

### Produção na SEDU:
- Servidor: `curriculo.sedu.es.gov.br/curriculo/`
- Estratégia: Docker (Postgres) + `.htaccess` para URLs do WordPress
- Detalhes: ver `MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md` e `CLAUDE.md` Parte 29-30

## Documentação

| Arquivo | Conteúdo |
|---------|----------|
| **[CLAUDE.md](CLAUDE.md)** | Documentação técnica completa (modelos, views, admin, decisões de design, troubleshooting) |
| **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** | Estado atual + mudanças de 2026-07-11 + quick start |
| **[Especificacao_Painel_Admin_Site_Curriculos.md](Especificacao_Painel_Admin_Site_Curriculos.md)** | Spec oficial do Painel Central (Partes 1–5) |
| **[MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md)** | Estratégia de migração e deploy final na SEDU |

## Notas Importantes

1. **Banco já populado** – `db.sqlite3` local tem tudo (588 conteúdos, 132 categorias). Não precisa migration manual (a menos que teste).
2. **Docker pronto** – use o `.bat` "ATUALIZAR BANCO DOCKER.bat" para sincronizar local → Docker em 1 clique. Sem Docker? SQLite local funciona 100% igual.
3. **Backup portável** – `.bat` "BACKUP DOCKER COMPLETO.bat" gera backup com tudo (banco + mídia + código). Leve para outro PC com ".bat" de restauração.
4. **Conteúdos em URLs externas** – PDFs estão no WordPress, Google Drive, SEDU (apenas links, não arquivos locais).
5. **Cache do navegador** – CSS atualizado? Force com **Ctrl+Shift+R** (Windows/Linux) ou **Cmd+Shift+R** (Mac).
6. **GitHub** – sempre use `.bat` "Subir GitHub SEDU" para enviar (faz pull automático, evita conflitos).
7. **Superusers padrão**: `ridan` / `Sedu@2026` e `rabalista`. Deletar testes com `django shell` antes de push.
8. **ngrok para demo** – teste com `python teste_ngrok.py` antes de compartilhar. UTF-8 já corrigido (2026-07-13).

## Usuário Principal

- **Dan** (não programador) – trabalha na SEDU
- Reforço: sempre ADICIONAR nunca quebrar o que já funciona
- Sempre fornecer comandos prontos em português

## Contribuindo

1. Clone do GitHub
2. Crie uma branch para sua feature (`git checkout -b feature/sua-coisa`)
3. Commit com mensagem clara em português
4. Push (`git push origin feature/sua-coisa`)
5. Abra um PR

## Suporte

- **Banco de dados**: se clonou do GitHub (banco vazio), rode `python manage.py migrate` + commands em `conteudo/management/commands/`
- **Deploy**: ver `MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md`
- **Admin local**: `python manage.py createsuperuser` → http://127.0.0.1:8001/admin/
- **ngrok não funciona**: teste com `python teste_ngrok.py`, certifique-se de que Django está rodando

---

**Última atualização**: 2026-07-19 (Parte 31)  
**Versão CSS**: `?v=20260718-2` | **Versão JS**: `?v=20260711-1`  
**Migrações aplicadas**: `conteudo/0012-0033` + `painel/0002-0003` + `inteligencia/0002`  
**Docker pronto para produção**: Dockerfile + docker-compose.yml com PostgreSQL 16  
**Documentação completa**: [CLAUDE.md](CLAUDE.md) (v27)
