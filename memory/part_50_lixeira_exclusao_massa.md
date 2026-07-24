---
name: part_50_lixeira_exclusao_massa
description: Exclusão em massa de itens expirados na Lixeira com checkboxes e "Selecionar todos"
metadata:
  type: project
  date: 2026-07-24
  version: v50
---

# Parte 50: Exclusão em Massa na Lixeira (2026-07-24)

## Pedido do Dan
"Painel lixeira tem um recurso de **excluir em massa** quando desejar"

## O que foi implementado

Painel `/admin/lixeira/` ganhou recurso de **selecionar múltiplos botões/conteúdos e deletar todos de uma vez**, sem precisar clicar "Excluir já" um por um para cada item.

### UI Changes
- Cada tabela (Botões excluídos / Conteúdos excluídos) agora tem:
  - **Coluna de checkbox** (esquerda de cada linha)
  - **"Selecionar todos"** (checkbox no cabeçalho que marca/desmarca tudo)
  - **Botão "Excluir selecionados definitivamente"** (vermelho escuro, desabilitado até marcar 1+ item)
  - **Confirmação dupla** (JS confirm + backend validation)

### Backend Changes
- Nova action `excluir_definitivo_massa` em `lixeira_view()` (conteudo/admin_views.py)
- Recebe `ids` e `tipo` (categoria/conteudo) via POST
- Loops sobre cada ID e chama `.hard_delete()` (exclusão permanente, sem recuperação)
- Retorna mensagem: "N botão(ões) excluído(s) definitivamente..." OU "N conteúdo(s)..."
- Suporta ambos tipos (Categoria e Conteudo) com uma única view

### Frontend Changes
- `templates/admin/lixeira.html` ganhou:
  - CSS novo (`.lx-check-col`, `.lx-bulk-bar`, `.lx-btn-excluir-massa`)
  - `<form id="lx-bulk-categoria/conteudo">` para cada tabela (POST com `ids[]` e tipo)
  - JS helper `lxToggleTodos(tipo, checkbox)` — "Selecionar todos" marca/desmarca
  - JS helper `lxAtualizarBotaoMassa(tipo)` — habilita/desabilita botão conforme seleção

### Testes Confirmados
- ✅ Marcar 2+ itens com "Selecionar todos" → botão habilitado
- ✅ Clicar botão → confirm() bloqueia acidental
- ✅ Confirmar → DELETE recebe os IDs corretos, ambos deletados
- ✅ Mensagem sucesso: "2 botão(ões) excluído(s) definitivamente"
- ✅ Página recarrega (redirect) e lixeira vazia
- ✅ Botões individuais "Restaurar" e "Excluir já" continuam funcionando

## Arquivos Alterados
- `conteudo/admin_views.py` — ação `excluir_definitivo_massa` (22 linhas)
- `templates/admin/lixeira.html` — UI + JS helpers (60 linhas novas, só adições)

## Zero Breaking Changes
- Nenhuma migração de banco necessária (usa hard_delete já existente)
- Nenhuma mudança em outras telas
- Botões individuais funcionam igual
- Compatibilidade 100% com Parte 41 (Lixeira)

## Design Decisions
1. **Desabilitável**: botão só fica verde quando 1+ item marcado (feedback visual claro)
2. **Confirmação dupla**: JS confirm + backend já faz validation (defesa profunda)
3. **Mensagem clara**: reporta número de itens deletados (feedback ao Dan)
4. **Isolado por tipo**: tabelas separadas (Botões / Conteúdos), formulários independentes
5. **Reutilizável**: mesmo padrão de checkboxes que Django admin usa

## Onde Mexer Se Precisar Expandir
- `conteudo/admin_views.py` linha ~1215: action `excluir_definitivo_massa`
- `templates/admin/lixeira.html` linhas com `.lx-bulk-*`: UI e JS
- Para adicionar "restaurar em massa" ou "mover em massa": reutilizar mesmo padrão de helper JS

## Status
✅ **Implementado, testado, zero breaking changes**
