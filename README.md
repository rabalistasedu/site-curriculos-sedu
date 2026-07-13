# Site Currículos SEDU

**Migração WordPress → Django 5.2** para a Gerência de Currículo da Educação Básica (GECEB), Secretaria de Estado da Educação (SEDU) – Espírito Santo.

## Status Atual (2026-07-13 — Parte 8 + ngrok corrigido)

✅ **Site funcional e responsivo** – 365+ conteúdos migrados, 10 categorias, 42+ subcategorias  
✅ **Admin completo** – Django Admin + 5 painéis customizados (Organizador, Painel de Arquivos, Painel Central, Painel de Botões da Barra)  
✅ **Sistema de comentários moderados** – 3 estados, respostas aninhadas com votação 👍/👎, visual moderno  
✅ **ngrok corrigido** – UTF-8 funcionando, vídeo do carrossel agora acessível via compartilhamento  
✅ **Deploy em progresso** – ngrok (demo) → `curriculo.sedu.es.gov.br/curriculo/` (produção final)

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

## Mudanças Recentes (2026-07-12 a 2026-07-13)

### 8 Partes de Implementação (19 features/bugs total)
1. ✅ **Bugs de layout** – navegação mobile, carrossel dividido, rodapé flutuante, anexos invisíveis
2. ✅ **Edição inline** – "Editar botão selecionado" com AJAX + criação de subáreas em lote
3. ✅ **Carrossel admin** – mostra arquivo atual + checkbox "Limpar" + opção "Modificar"
4. ✅ **Campo URL no painel** – cria links automáticos dentro de botões
5. ✅ **Sistema de comentários** – 3 estados (pendente/publicado/recusado), resposta do admin, não aparece em links
6. ✅ **Bugfixes UX** – busca árvore 3+ níveis, rodapé sticky, CategoriaPicker dinâmico
7. ✅ **Respostas + Votos** – comentários aninhados com votação 👍/👎 AJAX, migração 0020
8. ✅ **ngrok corrigido** – UTF-8 funcionando, vídeo renomeado para ASCII-only

**Migrações novas**: `conteudo.0012-0020`, `painel.0002`

→ Veja **[CLAUDE.md](CLAUDE.md)** para detalhes completos

## Estrutura

```
conteudo/               → App principal (models, views, admin, forms, widgets)
painel/                 → Painel Central Administrativo (Telas 1 e 2)
templates/              → HTML5 (base, home, categoria, conteudo, busca, admin)
static/
  ├─ css/style.css      → Design system (atualizado ?v=20260713-2)
  ├─ js/main.js         → Interações (slider, menu, carrossel, votos AJAX)
  └─ img/               → Brasão, logos, ícones
db.sqlite3              → Banco SQLite (365+ docs)
CLAUDE.md               → Documentação técnica completa (v6 – 2026-07-13)
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
| `/` | Home (hero, banners, destaques, recentes, áreas, cartazes, carrosséis) |
| `/categoria/<slug>/` | Conteúdos da categoria com filtros |
| `/conteudo/<slug>/` | Detalhe do conteúdo + comentários + votos |
| `/busca/?q=termo` | Busca textual sem acento |
| `/admin/` | Django Admin |
| `/admin/painel-central/` | **Painel Administrativo Completo** (Telas 1 e 2) |
| `/admin/organizar/` | Organizador visual de hierarquia |
| `/admin/adicionar-arquivos/` | Upload em lote de arquivos |

## Stack

- **Backend**: Django 5.2, Python 3.13 (local) / 3.11 (SEDU)
- **DB**: SQLite
- **Frontend**: CSS puro, Font Awesome 6 (ícones), Google Fonts (Inter)
- **Versionamento**: GitHub (`rabalistasedu/site-curriculos-sedu`)
- **Demo**: ngrok (URL pública temporária – UTF-8 corrigido)
- **Produção**: `curriculo.sedu.es.gov.br/curriculo/` (em progresso)

## Deploy

### Demonstração ao gerente (ngrok — AGORA CORRIGIDO):
```bash
# Opção 1: Usar BAT (mais fácil)
"BAT SEDU\INICIAR COM NGROK.bat"

# Opção 2: Manualmente (Python com UTF-8)
python ngrok_compartilhar.py

# Opção 3: Teste primeiro, depois compartilhe
python teste_ngrok.py         # testa tudo
python ngrok_compartilhar.py  # compartilha com ngrok
```

### Produção na SEDU:
- Servidor: `curriculo.sedu.es.gov.br/curriculo/`
- Estratégia: reescrita via `.htaccess` de URLs do WordPress (evita duplicar ~1000 arquivos)
- Detalhes: ver `MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md`

## Fixes Recentes do ngrok (2026-07-13)

1. **UTF-8 corrigido** – BAT agora usa Python script com `# -*- coding: utf-8 -*-` em vez de ngrok direto
2. **Vídeo do carrossel renomeado** – `AFINAL_PARA_QUÊ_...mp4` → `AFINAL_PARA_QUE_...mp4` (ASCII-only para ngrok)
3. **Teste automatizado** – novo script `teste_ngrok.py` valida tudo antes de compartilhar
4. **BAT melhorado** – `COMPARTILHAR COM GERENTE.bat` agora tenta Python script primeiro (fallback para ngrok direto)

Resultado: caracteres especiais (ç, á, é) agora aparecem corretamente quando gerente acessa via ngrok, e vídeos carregam normalmente.

## Documentação

| Arquivo | Conteúdo |
|---------|----------|
| **[CLAUDE.md](CLAUDE.md)** | Documentação técnica completa (modelos, views, admin, decisões de design, troubleshooting) |
| **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** | Estado atual + mudanças de 2026-07-11 + quick start |
| **[Especificacao_Painel_Admin_Site_Curriculos.md](Especificacao_Painel_Admin_Site_Curriculos.md)** | Spec oficial do Painel Central (Partes 1–5) |
| **[MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md)** | Estratégia de migração e deploy final na SEDU |

## Notas Importantes

1. **Banco já populado** – `db.sqlite3` tem tudo. Não precisa rodar migration commands (a menos que teste).
2. **Conteúdos apontam para URLs externas** – PDFs estão no WordPress, Google Drive, SEDU.
3. **Cache do navegador** – ao mudar CSS, força recarregamento: **Ctrl+Shift+R** (Windows/Linux) ou **Cmd+Shift+R** (Mac).
4. **GitHub** – sempre use o `.bat` "Subir GitHub SEDU" para enviar (ele faz pull automático).
5. **Migrações aplicadas** – todas de 0012 a 0020; superusers: `ridan` (Sedu@2026) e `rabalista`.
6. **ngrok funcionando** – teste com `python teste_ngrok.py` antes de compartilhar.

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

**Última atualização**: 2026-07-13  
**Versão CSS**: `?v=20260713-2` | **Versão JS**: `?v=20260711-1`
