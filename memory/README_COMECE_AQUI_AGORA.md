# 🚀 Comece Aqui (v50, 2026-07-24)

**Status**: Site funcional, 50 partes completas, 10 painéis admin, zero breaking changes.

## Em 2 Minutos

- **Site**: Django 5.2 + PostgreSQL (Docker) + SQLite (local)
- **Dados**: 132 botões (categorias), 588 conteúdos, comentários, anexos
- **Admin**: 10 painéis personalizados + acesso delegável (permissões)
- **Deploy**: Docker pronto para SEDU (`curriculo.sedu.es.gov.br`)
- **Última feature**: Parte 50 — exclusão em massa na Lixeira (checkboxes + botão)

## 3 Arquivos Essenciais

1. **[known_pitfalls.md](known_pitfalls.md)** ⚠️ — 37+ armadilhas críticas (LER PRIMEIRO)
2. **[MEMORY.md](MEMORY.md)** — índice de toda a documentação
3. **[../CLAUDE.md](../CLAUDE.md)** — contexto técnico completo (43 KB)

## Para Começar uma Conversa Nova

```
Projeto Site Curriculos SEDU, v50 (2026-07-24).
50 partes completadas. Estado: funcional.
Última feature: exclusão em massa na Lixeira.
Leia: memory/known_pitfalls.md primeiro.
```

## As 10 Ideias Principais

| # | Painel | Descrição |
|---|--------|-----------|
| 1 | **Lixeira** | Recupera até 30 dias + exclusão em massa (Part 50) |
| 2 | **Estrutura de Árvores** | 121 nós, CRUD, ícones, drag-drop |
| 3 | **Painel Central** | Tela 1 (árvore+publicar) + Tela 2 (conteúdo) |
| 4 | **Organizador** | Move conteúdo, cria subáreas |
| 5 | **Adicionar Arquivos** | 3 passos: categoria→subárea→upload |
| 6 | **Barra Superior** | Botões do header + ordem |
| 7 | **Área do Site** | Títulos seções + colunas extras |
| 8 | **Editor Rodapé** | Rodapé customizável (imagens, links) |
| 9 | **Central de Inteligência** | Analytics, rankings, downloads |
| 10 | **Django Admin** | CRUD completo + ações em massa |

## Banco & Infra

- **Local**: SQLite (`db.sqlite3`, 6.6 MB)
- **Docker**: Postgres 16 (`docker-compose.yml`, sincronização automática via `.bat`)
- **Backup**: Completo em 3 arquivos (banco + mídia + código)
- **Ambiente**: Windows 11, venv Python 3.13

## Próximos Passos (Ideias)

- [ ] Deploy em `curriculo.sedu.es.gov.br` (SEDU)
- [ ] SSL/TLS, ALLOWED_HOSTS restringido, DEBUG=False
- [ ] Paginação em listagens públicas
- [ ] Mais integrações (ex.: Slack, webhook genérico)
- [ ] UI refinamentos conforme feedback do Dan

## Armadilhas Top 3

1. **CSS/JS não atualiza** → incrementar `?v=` em `base.html` + Ctrl+Shift+R
2. **Campos URLField com links >200 chars quebram no Docker** → max_length=1000 (migração 0038, já aplicada)
3. **dumpdata sem --all exclui Lixeira** → usar `dumpdata --all` (ou `.bat` já faz)

👉 Ver [known_pitfalls.md](known_pitfalls.md) para os 34 restantes.

---

**Próxima conversa?** Comece com este arquivo + `known_pitfalls.md`, depois CLAUDE.md conforme precisar.
