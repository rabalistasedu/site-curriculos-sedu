# Scripts da recuperação de 2026-07-23

Esta pasta guarda os scripts usados numa recuperação emergencial pontual —
não fazem parte do site, não são chamados por nenhum painel administrativo.
Mantidos aqui só como registro de auditoria.

**O que aconteceu**: o Dan excluiu por engano a categoria "Orientações
Curriculares" (raiz, 18 subcategorias, 127 conteúdos) no ambiente local,
antes do sistema de Lixeira existir.

**Como foi recuperada**: um backup do Postgres/Docker feito às 15:05 do
mesmo dia (`docker_backups/backup_20260723_150450/banco_postgres.sql`)
ainda tinha a árvore completa intacta. `extrair_orientacoes.py` extraiu a
categoria raiz + subárvore + conteúdos ligados a ela do dump SQL;
`restaurar_orientacoes.py` recriou as categorias com os mesmos IDs/dados
originais e reconectou os 127 conteúdos (que continuavam no banco local,
só órfãos — `categoria=None` — já que a exclusão de categoria nunca apaga
conteúdo, só desvincula).

**Depois disso**, foi implementado o sistema de Lixeira (ver seção
"Lixeira" no `CLAUDE.md`) — daqui pra frente, esse tipo de acidente se
resolve em 1 clique em `/admin/lixeira/`, sem precisar de recuperação
manual via backup.

`teste_lixeira.py` / `teste_lixeira_parte2.py` / `debug_dj.py` foram os
scripts de teste automatizado usados para validar o sistema de Lixeira
antes de entregá-lo (30 cenários testados, 0 problemas reais encontrados).
