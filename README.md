# ðŸŽ“ Site CurrÃ­culo SEDU

**MigraÃ§Ã£o WordPress â†’ Django 5.2** para a GerÃªncia de CurrÃ­culo da EducaÃ§Ã£o BÃ¡sica (GECEB), Secretaria de Estado da EducaÃ§Ã£o (SEDU) â€” EspÃ­rito Santo.

## âš¡ Status Atual (2026-07-13)

âœ… **Site funcional e responsivo** â€” 365+ conteÃºdos migrados, 10 categorias, 42+ subcategorias  
âœ… **Admin completo** â€” Django Admin + 5 painÃ©is customizados (Organizador, Painel de Arquivos, Painel Central, Painel de BotÃµes da Barra)  
âœ… **Sistema de comentÃ¡rios moderados** â€” 3 estados, resposta do admin, visual moderno  
âœ… **Deploy em progresso** â€” ngrok (demo) â†’ `curriculo.sedu.es.gov.br/curriculo/` (produÃ§Ã£o final)

## ðŸš€ Quick Start

```bash
# Clone do GitHub
git clone https://github.com/rabalistasedu/site-curriculos-sedu.git
cd "Site Curriculos SEDU"

# Ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# DependÃªncias
pip install -r requirements.txt

# MigraÃ§Ãµes (se novo ambiente)
python manage.py migrate

# Rodar local
python manage.py runserver 8001
```

Acesse: **http://127.0.0.1:8001** (site) | **http://127.0.0.1:8001/admin/** (admin)

## ðŸ“‹ MudanÃ§as Recentes (2026-07-12 a 2026-07-13)

### 7 Partes de ImplementaÃ§Ã£o (18 features/bugs total)
1. âœ… **Bugs de layout** â€” navegaÃ§Ã£o mobile, carrossel dividido, rodapÃ© flutuante, anexos invisÃ­veis
2. âœ… **EdiÃ§Ã£o inline** â€” "Editar botÃ£o selecionado" com AJAX + criaÃ§Ã£o de subÃ¡reas em lote
3. âœ… **Carrossel admin** â€” mostra arquivo atual + checkbox "Limpar" + opÃ§Ã£o "Modificar"
4. âœ… **Campo URL no painel** â€” cria links automÃ¡ticos dentro de botÃµes
5. âœ… **Sistema de comentÃ¡rios** â€” 3 estados (pendente/publicado/recusado), resposta do admin, nÃ£o aparece em links
6. âœ… **Bugfixes UX** â€” busca Ã¡rvore 3+ nÃ­veis, rodapÃ© sticky, CategoriaPicker dinÃ¢mico

**MigraÃ§Ãµes novas**: `conteudo.0012-0019`, `painel.0002`

â†’ Veja **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** para detalhes completos

## ðŸ“ Estrutura

```
conteudo/               â†’ App principal (models, views, admin, forms, widgets)
painel/                 â†’ Painel Central Administrativo (Telas 1 e 2)
templates/              â†’ HTML5 (base, home, categoria, conteudo, busca, admin)
static/
  â”œâ”€ css/style.css      â†’ Design system (atualizado ?v=20260713-1)
  â”œâ”€ js/main.js         â†’ InteraÃ§Ãµes (slider, menu, carrossel)
  â””â”€ img/               â†’ BrasÃ£o, logos, Ã­cones
db.sqlite3              â†’ Banco SQLite (365+ docs)
CLAUDE.md               â†’ DocumentaÃ§Ã£o tÃ©cnica completa (v5 â€” 2026-07-13)
```

## ðŸŽ¯ Modelos Principais

- **Categoria** â€” hierarquia ilimitada, Ã­cone, descricÃ£o, orden, visibilidade por seÃ§Ã£o
- **Conteudo** â€” tipos (documento/video/post/link/pagina), `icone_imagem` novo, agendamento
- **Anexo** â€” FK dual (conteudo OU categoria), mÃºltiplos arquivos
- **Banner**, **Cartaz**, **Carrossel** â€” com URL de imagem opcional
- **EstiloBotao** â€” cores, fonte, `tamanho` novo, pulsante
- **Vinculo** â€” publicaÃ§Ã£o multi-destino sem duplicaÃ§Ã£o

## ðŸ“– URLs Principais

| Rota | DescriÃ§Ã£o |
|------|-----------|
| `/` | Home (hero, banners, destaques, recentes, Ã¡reas, cartazes, carrossÃ©is) |
| `/categoria/<slug>/` | ConteÃºdos da categoria com filtros |
| `/conteudo/<slug>/` | Detalhe do conteÃºdo + comentÃ¡rios |
| `/busca/?q=termo` | Busca textual sem acento |
| `/admin/` | Django Admin |
| `/admin/painel-central/` | **Painel Administrativo Completo** (Telas 1 e 2) |
| `/admin/organizar/` | Organizador visual de hierarquia |
| `/admin/adicionar-arquivos/` | Upload em lote de arquivos |

## ðŸ”§ Stack

- **Backend**: Django 5.2, Python 3.13 (local) / 3.11 (SEDU)
- **DB**: SQLite
- **Frontend**: CSS puro, Font Awesome 6 (Ã­cones), Google Fonts (Inter)
- **Versionamento**: GitHub (`rabalistasedu/site-curriculos-sedu`)
- **Demo**: ngrok (URL pÃºblica temporÃ¡ria)
- **ProduÃ§Ã£o**: `curriculo.sedu.es.gov.br/curriculo/` (em progresso)

## ðŸš¦ Deploy

**DemonstraÃ§Ã£o ao gerente:**
```bash
# Abra o .bat "COMPARTILHAR COM GERENTE" (Desktop)
# Ou manualmente:
cd "Site Curriculos SEDU"
venv\Scripts\python.exe ngrok_compartilhar.py
```

**ProduÃ§Ã£o na SEDU:**
- Servidor: `curriculo.sedu.es.gov.br/curriculo/`
- EstratÃ©gia: reescrita via `.htaccess` de URLs do WordPress (evita duplicar ~1000 arquivos)
- Detalhes: ver `MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md`

## ðŸ“š DocumentaÃ§Ã£o

| Arquivo | ConteÃºdo |
|---------|----------|
| **[CLAUDE.md](CLAUDE.md)** | ðŸ“˜ DocumentaÃ§Ã£o tÃ©cnica completa (modelos, views, admin, decisÃµes de design, troubleshooting) |
| **[CONTEXTO_ATUAL.md](CONTEXTO_ATUAL.md)** | ðŸ“‹ Estado atual + mudanÃ§as de 2026-07-11 + quick start |
| **[Especificacao_Painel_Admin_Site_Curriculos.md](Especificacao_Painel_Admin_Site_Curriculos.md)** | ðŸŽ¨ Spec oficial do Painel Central (Partes 1â€“5) |
| **[MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md](MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md)** | ðŸš€ EstratÃ©gia de migraÃ§Ã£o e deploy final na SEDU |
| **[SINCRONIZAR_BANCO_LOCAL_SEDU.md](SINCRONIZAR_BANCO_LOCAL_SEDU.md)** | ðŸ”„ Como sincronizar banco entre ambientes |

## âš ï¸ Notas Importantes

1. **Banco jÃ¡ populado** â€” `db.sqlite3` tem tudo. NÃ£o precisa rodar migration commands (a menos que teste).
2. **ConteÃºdos apontam para URLs externas** â€” PDFs estÃ£o no WordPress, Google Drive, SEDU.
3. **Cache do navegador** â€” ao mudar CSS, forÃ§a recarregamento: **Ctrl+Shift+R** (Windows/Linux) ou **Cmd+Shift+R** (Mac).
4. **GitHub** â€” sempre use o `.bat` "Subir GitHub SEDU" para enviar (ele faz pull automÃ¡tico).
5. **MigraÃ§Ãµes aplicadas** â€” todas de 0012 a 0019; superusers: `ridan` (Sedu@2026) e `rabalista`.

## ðŸ‘¤ UsuÃ¡rio Principal

- **Dan** (nÃ£o programador) â€” trabalha na SEDU
- ReforÃ§o: sempre ADICIONAR nunca quebrar o que jÃ¡ funciona
- Sempre fornecer comandos prontos em portuguÃªs

## ðŸ¤ Contribuindo

1. Clone do GitHub
2. Crie uma branch para sua feature (`git checkout -b feature/sua-coisa`)
3. Commit com mensagem clara em portuguÃªs
4. Push (`git push origin feature/sua-coisa`)
5. Abra um PR

## ðŸ“ž Suporte

- **Banco de dados**: se clonou do GitHub (banco vazio), rode `python manage.py migrate` + commands em `conteudo/management/commands/`
- **Deploy**: ver `MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md` e `SINCRONIZAR_BANCO_LOCAL_SEDU.md`
- **Admin local**: `python manage.py createsuperuser` â†’ http://127.0.0.1:8001/admin/

---

**Ãšltima atualizaÃ§Ã£o**: 2026-07-13  
**VersÃ£o CSS**: `?v=20260713-1` | **VersÃ£o JS**: `?v=20260711-1`
