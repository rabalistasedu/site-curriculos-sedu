---
name: comece_aqui
description: Ponto de partida rápido (30 seg) para novas conversas
metadata:
  type: reference
  version: v50
  date: 2026-07-24
---

# Comece Aqui (30 segundos)

## O Projeto
Site da SEDU (Educação ES) migrado de WordPress para Django. **Completo, 50 partes, pronto para entrega.**

## Estado Agora
- ✅ 10 painéis admin funcionais
- ✅ 132 botões + 588 conteúdos
- ✅ Comentários + Lixeira (30 dias)
- ✅ Docker pronto (Postgres 16)
- ✅ Último: Parte 50 — exclusão em massa na Lixeira

## 3 Coisas Urgentes

1. **Leia PRIMEIRO**: [`known_pitfalls.md`](known_pitfalls.md) (37 armadilhas)
2. **Contexto Técnico**: [`../CLAUDE.md`](../CLAUDE.md) (v50, todas as 50 partes)
3. **Status Consolidado**: [`STATUS_FINAL_V50_2026_07_24.md`](STATUS_FINAL_V50_2026_07_24.md)

## Estrutura de Memory

```
MEMORY.md ← Você está aqui (índice geral)
├─ README_COMECE_AQUI_AGORA.md ← 2 min resumo
├─ known_pitfalls.md ← CRÍTICO (37 armadilhas)
├─ STATUS_FINAL_V50_2026_07_24.md ← Estado consolidado
├─ part_50_lixeira_exclusao_massa.md ← Última feature
├─ part_49_anexo_imagem_galeria.md
├─ ... (part_48, part_47, ..., part_1)
└─ Temas Especiais (docker, teams, css, etc.)
```

## Quick Links para Próxima Conversa

```markdown
# Conversa Nova

Projeto: Site Curriculos SEDU  
Versão: v50 (2026-07-24)  
Estado: Funcional, 50 partes, 10 painéis admin  
Última feature: Exclusão em massa na Lixeira (Part 50)  

Ver: memory/known_pitfalls.md → memory/CLAUDE.md
```

## Ambiente

- **Local**: Windows 11, SQLite, venv Python 3.13
- **Docker**: Postgres 16, sincroniza via .bat
- **Deploy**: Destino = `curriculo.sedu.es.gov.br` (SEDU)

## Próximas Ideias

- [ ] Deploy SEDU com SSL/TLS
- [ ] Paginação listas públicas
- [ ] 2FA admin, webhooks genéricos, auditoria
- [ ] Dark mode, mais idiomas

---

👉 **Agora leia** [`known_pitfalls.md`](known_pitfalls.md) para evitar os top 3 problemas:
1. CSS/JS cache (incrementar ?v= + Ctrl+Shift+R)
2. dumpdata sem --all (quebra FK no Docker)
3. Campos URLField com links >200 chars
