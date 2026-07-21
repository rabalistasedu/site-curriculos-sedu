# 🎓 SITE CURRÍCULO SEDU — Resumo de Contexto (2026-07-21 — Parte 33)

## Estado atual: FUNCIONAL E COMPLETO ✅✅✅

Projeto de migração de site WordPress → Django 5.2 para SEDU (Secretaria Educação ES).  
**Status do banco**: 588 conteúdos migrados, 132 categorias principais, 42+ subcategorias, **sistema de comentários em botões e conteúdos, votos AJAX, respostas aninhadas**.  
**Deploy**: ❌ PythonAnywhere abandonado | ✅ ngrok (demo) | 🎯 `curriculo.sedu.es.gov.br/curriculo/` (produção)

---

## ⚡ Para entender onde estamos (2026-07-21 — Parte 33)

### 🚦 Decisão crítica de Deploy (2026-07-10)
- **PythonAnywhere não é mais usado** — ambiente de teste insuficiente para demonstrações
- **Novo destino**: servidor próprio da SEDU em `curriculo.sedu.es.gov.br/curriculo/` (subdomínio para não quebrar WordPress existente)
- **Até lá**: demonstrações via **ngrok** (gera URL pública válida por 2h, UTF-8 corrigido parte 9, vídeo streaming parte 9)
- **Estratégia**: reescrita de URLs via `.htaccess` Apache (manter WordPress em subdomínio, evitar duplicar ~1000 arquivos)

### 📋 Leva Mais Recente: Parte 33 (2026-07-21)
**Comentários em botões (categorias)** — pedido do Dan: toda página de botão precisa da mesma seção de comentários que já existia só em conteúdos individuais.
- ✅ Novo campo `Comentario.categoria` (FK opcional) → FK dual com `conteudo` (agora também opcional)
- ✅ View `categoria_detalhe` ganhou moderação/respostas/votos idêntica a `conteudo_detalhe`
- ✅ Página de índice geral ("Documentos Curriculares") também tem comentários
- ✅ Regra automática vale para **qualquer botão futuro** (sem configuração por botão)
- ✅ Migração `conteudo/0035` aplicada
- ✅ Testado: criar/aprovar/votar/responder em categoria, regressão confirmada (conteúdos OK)

### Leva Anterior: Parte 32 (2026-07-21)
**9 implementações concluídas** do documento `implementar.md`:
1. ✅ Ícone personalizado galeria (Estrutura de Árvores) — clique em thumbnail + salvar aplica
2. ✅ Categorias raiz em "Conteúdos Recentes" — botões raiz marcados como cards na home
3. ✅ Imagens do rodapé — novo modelo `RodapeImagem`, painel Editor do Rodapé (altura fixa 44px)
4. ✅ Nome customizável "Currículo Atual" — novo campo `ConfiguracaoSite.nome_curriculo_atual`
5. ✅ Botões em área central — confirmado que já existia (parte 13), sem duplicação
6. ✅ Brasão personalizado — novo campo `ConfiguracaoSite.brasao_imagem` + alinhamento/tamanho
7. ✅ Segundo logotipo — novos campos `logo2_imagem/alinhamento/tamanho`
8. ✅ Tudo com zero breaking changes — campos opcionais, fallback automático
9. ✅ Migração 0034 aplicada com sucesso

### Categorias principais (menu "Navegue por área")
1. **Documentos Curriculares** — Currículo Atual (5 sub-etapas) + Material de Apoio + 7 subcategorias  
2. **Orientações Curriculares** — 129 docs + 16 subcategorias  
3. **Itinerários Formativos de Aprofundamento (IFA)** — 10 subcategorias, 14+ docs  
4. **Projetos Integradores** — 5 subcategorias  
5. **Rotinas Pedagógicas Escolares (RPE)** — 8 subcategorias, **42 apostilas**  
6. **Programas** — Educar para a Paz, Mais Leitores, Educação Ambiental, Sucesso Escolar
7. **Livro Didático**, **Modalidades e Diversidade**, **Olimpíadas**, **Institucional**

### 📊 Dados no banco
- **SQLite** (`db.sqlite3`) — 588 conteúdos (documento, video, post, link, página)
- **Sistema de comentários MODERADO** — 3 estados (pendente/publicado/recusado), resposta do admin, votos 👍/👎, respostas aninhadas
- **Docker + PostgreSQL pronto** — sincronização local→Docker em .bat, backup/restore automático
- **Migrações aplicadas**: conteudo/0012-0035 + painel/0002-0003 + inteligencia/0002 (total 40+ migrações)

### 🎨 Infraestrutura
- **Frontend**: CSS puro, Font Awesome 6, Google Fonts (Inter)
- **Backend**: Django 5.2 + Python 3.13 (local) / Python 3.12 (Docker)
- **Banco Local**: SQLite (intacto)
- **Banco Docker/Produção**: PostgreSQL 16
- **Deploy Demo**: ngrok com UTF-8 correto
- **Containerização**: Docker + docker-compose.yml pronto para SEDU
- **GitHub**: https://github.com/rabalistasedu/site-curriculos-sedu.git

---

## 🛠️ 9 Painéis Administrativos (Delegação de acesso via permissões Django)

Cada painel tem uma permissão nativa em "Autenticação e Autorização":

| Painel | URL | Permissão |
|--------|-----|-----------|
| **Organizador** | `/admin/organizar/` | `conteudo.pode_acessar_organizador` |
| **Adicionar Arquivos** | `/admin/adicionar-arquivos/` | `conteudo.pode_acessar_adicionar_arquivos` |
| **Painel Central** (Telas 1+2) | `/admin/painel-central/` | `painel.pode_acessar_painel_central` |
| **Barra Superior** | `/admin/barra-superior/` | `conteudo.pode_acessar_barra_superior` |
| **Estrutura de Árvores** | `/admin/estrutura-arvores/` | `conteudo.pode_acessar_estrutura_arvores` |
| **Área do Site** | `/admin/area-do-site/` | `conteudo.pode_acessar_area_do_site` |
| **Editor do Rodapé** | `/admin/editor-rodape/` | `conteudo.pode_acessar_editor_rodape` |
| **Central de Inteligência** | `/admin/inteligencia/` | `inteligencia.pode_acessar_inteligencia` |

---

## 🚀 Quick Start (3 minutos)

```bash
# Clone + setup
git clone https://github.com/rabalistasedu/site-curriculos-sedu.git
cd "Site Curriculos SEDU"
python -m venv venv
venv\Scripts\activate  # Windows: ativação
pip install -r requirements.txt

# Banco (primeira vez apenas)
python manage.py migrate

# Rodar
python manage.py runserver 8001
```

**Acesse**: 
- 🌐 Site: http://127.0.0.1:8001
- 🔐 Admin: http://127.0.0.1:8001/admin/ (superuser: `ridan` / `Sedu@2026`)

## 🐳 Docker + PostgreSQL (Sincronização local→Docker)

```bash
# 1. Certifique-se de que Docker Desktop está aberto
# 2. Clique em: "BAT SEDU\ATUALIZAR BANCO DOCKER.bat"

# Resultado: site PostgreSQL em http://localhost:8000
```

## 📦 Backup/Restore (Portable)

```bash
# Fazer backup (banco + mídia + código)
"BAT SEDU\BACKUP DOCKER COMPLETO.bat"

# Restaurar em outro PC (copie a pasta gerada)
"BAT SEDU\RESTAURAR ESTE BACKUP.bat"
```

---

## 📚 Documentação Completa

| Arquivo | Conteúdo |
|---------|----------|
| **[CLAUDE.md](CLAUDE.md)** | Documentação técnica completa (modelos, views, admin, decisões de design, 33 partes, troubleshooting) |
| **[README.md](README.md)** | Quick start + status + stack |
| **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** | Estado atual + mudanças recentes + como começar próximas sessões |
| **[Especificacao_Painel_Admin_Site_Curriculos.md](Especificacao_Painel_Admin_Site_Curriculos.md)** | Spec oficial do Painel Central (histórico) |
| **[MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md)** | Estratégia de migração + deploy final na SEDU |

---

## ⚠️ Notas Importantes

1. **Banco já populado** — `db.sqlite3` tem tudo (588 conteúdos, 132 categorias). Não precisa importação manual.
2. **Superusers padrão**: `ridan` (`Sedu@2026`) e `rabalista` (senha trocada na parte 12 para `Sedu@2026` e depois variou conforme as sessões).
3. **Cache do navegador** — CSS atualizado? Force com **Ctrl+Shift+R** (Windows/Linux) ou **Cmd+Shift+R** (Mac).
4. **GitHub** — sempre use `.bat` "Subir GitHub SEDU" para enviar (faz pull automático, evita conflitos).
5. **ngrok para demo** — teste com `python teste_ngrok.py` antes de compartilhar. UTF-8 e vídeo funcionando (parte 9).

---

**Última atualização**: 2026-07-21 (Parte 33 — Comentários em botões)  
**Versão CSS**: `?v=20260718-2` | **Versão JS**: `?v=20260711-1`  
**Migrações aplicadas**: `conteudo/0012-0035` + `painel/0002-0003` + `inteligencia/0002` (total 40+)  
**Docker pronto para produção**: Dockerfile + docker-compose.yml com PostgreSQL 16
