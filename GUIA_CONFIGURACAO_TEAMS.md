# Guia: Configurar a integração de Comentários com o Microsoft Teams (GECEB)

Este guia explica, passo a passo, o que fazer no Teams e no site para ligar a integração. O código já está pronto e funciona **sem quebrar nada** mesmo antes de qualquer configuração — enquanto nada estiver preenchido, o site funciona exatamente como sempre funcionou.

A integração tem 2 partes independentes:
- **Parte A — Enviar comentário para o Teams**: você pode configurar HOJE, sem depender da TI.
- **Parte B — Trazer a resposta do Teams de volta pro site automaticamente**: depende de um cadastro que só a TI da SEDU pode fazer (Azure AD). Enquanto isso, você mesmo cola a resposta no admin (funciona igual, é o mesmo campo de sempre).

---

## Parte A — Enviar comentário para o Teams (disponível agora)

### Passo 1 — Confirmar o canal do GECEB
No Teams, entre no Team (grupo) **GECEB** → escolha (ou crie) o canal onde os comentários vão aparecer (ex.: "Comentários do Site" ou o canal "Geral").

### Passo 2 — Criar o fluxo no app Workflows
1. No canal escolhido, clique nos **três pontinhos (⋯)** no topo → **Workflows**.
2. Procure o modelo pronto: **"Publicar em um canal quando um webhook for recebido"** (em inglês: *"Post to a channel when a webhook request is received"*).
3. Clique em **Avançar/Next**, escolha o **Team** (GECEB) e o **Canal** certos.
4. Finalize a criação. O Teams vai gerar uma **URL de webhook** — copie essa URL (você só consegue ver ela uma vez, então copie com cuidado).

### Passo 3 — Ajustar o cartão (Adaptive Card) que aparece no Teams
Dentro do fluxo criado (edite-o no Power Automate), a ação final ("Publicar cartão em um canal") já vem com um cartão padrão. Edite esse cartão para mostrar os campos que o site vai mandar. O site envia este JSON para a URL do webhook:

```json
{
  "comentario_id": 5482,
  "titulo": "Material de Apoio para Nivelamento",
  "nome": "Ana",
  "email": "ana@email.com",
  "data": "23/07/2026 14:32",
  "texto": "Poderiam verificar o Material de Apoio...",
  "url": "https://curriculo.sedu.es.gov.br/categoria/material-de-apoio/"
}
```

No editor do cartão, monte algo assim usando os campos acima (arraste o "conteúdo dinâmico" de cada um):

| No cartão, mostre... | Usando o campo |
|---|---|
| Título "💬 Novo comentário recebido" | (texto fixo) |
| Título: | `titulo` |
| Nome: | `nome` |
| E-mail: | `email` |
| Data: | `data` |
| Comentário: | `texto` |
| (linha pequena/discreta no rodapé) | **`ID do comentário: ` + `comentario_id`** |

⚠️ **Muito importante**: a linha "ID do comentário: N" no rodapé do cartão **precisa existir exatamente nesse formato** ("ID do comentário: " seguido do número, sem nada a mais colado) — é assim que o sistema, mais tarde, vai reconhecer automaticamente qual comentário é aquele quando for buscar a resposta. Pode deixar essa linha com letra pequena/cinza (estilo "subtle" no editor de cartão), já que ela é só para uso interno.

### Passo 4 — Colar a URL no site
Cole a URL do webhook copiada no Passo 2 na variável de ambiente `TEAMS_WEBHOOK_URL`:

- **Rodando local (fora do Docker)**: crie/edite um arquivo `.env` na pasta do projeto (ou defina a variável de ambiente do Windows) com `TEAMS_WEBHOOK_URL=https://...`. Se preferir mais simples, me avise que eu ajusto o `.bat` de início para perguntar/ler de um arquivo de configuração.
- **Rodando no Docker**: crie um arquivo `.env` ao lado do `docker-compose.yml` com `TEAMS_WEBHOOK_URL=https://...` (o Docker Compose lê esse arquivo automaticamente).

### Passo 5 — Testar
Faça um comentário de teste no site → em poucos segundos deve aparecer um cartão novo no canal do GECEB, com os dados certos e a linha "ID do comentário: N" no rodapé.

---

## Parte B — Resposta automática do Teams voltar pro site (depende da TI)

Pesquisei a fundo e confirmei que o Microsoft Teams/Power Automate **não tem um jeito de baixo código de "avisar" quando alguém responde dentro de uma conversa** (só avisa para mensagem nova, não para resposta em thread — é uma limitação conhecida da própria Microsoft). O jeito certo e confiável é o **próprio site consultar a Microsoft Graph API de tempos em tempos** perguntando "chegou resposta nova?". Isso é mais robusto, mas exige um cadastro de aplicativo no Azure AD, que só a equipe de TI da SEDU consegue fazer (é uma permissão administrativa do tenant/organização).

### O que pedir para a TI da SEDU
Peça o cadastro de um **App Registration no Azure AD** com:
- **Tipo de permissão**: *Application* (não "delegada")
- **Permissão necessária**: `ChannelMessage.Read.All` (Microsoft Graph) — **só leitura**, o site não precisa de permissão para apagar nem alterar nada no Teams
- Também precisa: `Team.ReadBasic.All` e `Channel.ReadBasic.All` (para o site conseguir listar mensagens do canal)
- Peça que a TI aplique o **consentimento de administrador** (admin consent) para essas permissões
- Peça de volta: **Client ID**, **Client Secret** (valor, não o ID do secret) e **Tenant ID**

### O que você (Dan) faz depois de receber isso da TI
1. Preencha no `.env` (local ou Docker):
   ```
   TEAMS_CLIENT_ID=...
   TEAMS_CLIENT_SECRET=...
   TEAMS_TENANT_ID=...
   TEAMS_TEAM_ID=...      (ID do Team GECEB — veja como pegar abaixo)
   TEAMS_CHANNEL_ID=...   (ID do canal — veja como pegar abaixo)
   ```
2. **Como pegar o Team ID e o Channel ID**: no Teams, clique nos três pontinhos (⋯) ao lado do nome do canal → **Obter link para o canal**. O link gerado tem esse formato, com os dois IDs dentro:
   ```
   https://teams.microsoft.com/l/channel/{CHANNEL_ID}/nome-do-canal?groupId={TEAM_ID}&tenantId=...
   ```
   Copie a parte `{CHANNEL_ID}` (depois de `/channel/`) e a parte `{TEAM_ID}` (depois de `groupId=`).
3. (Opcional, mas recomendado) Preencha `TEAMS_MEMBROS_AUTORIZADOS` com os e-mails da equipe GECEB que pode responder, separados por vírgula — funciona como uma segunda trava de segurança além do próprio canal do Teams já ser restrito.
4. Rode `BAT SEDU\SINCRONIZAR TEAMS.bat` uma vez para testar (deve dizer "sincronização concluída").
5. Para deixar automático: registre esse `.bat` no **Agendador de Tarefas do Windows** (local) repetindo a cada 3-5 minutos, ou — se estiver no Docker — não precisa fazer nada, o serviço `teams_sync` do `docker-compose.yml` já roda sozinho em loop.

A partir daí, quando a equipe responder dentro da conversa no Teams, em até alguns minutos a resposta aparece sozinha no site, embaixo do comentário — sem precisar abrir o admin.

---

## Os 3 domínios do projeto

O código já reconhece os 3 domínios (não precisa editar nada na troca de ambiente):
- Oficial: `curriculo.sedu.es.gov.br`
- Homologação: `curriculohm.sedu.es.gov.br`
- Homologação: `curriculodev.sedu.es.gov.br`

Isso está em `curriculo_sedu/settings.py` (`DOMINIOS_CONHECIDOS`). Qualquer um dos 3 já funciona no admin/CSRF sem precisar mexer em nada. Links que o sistema gera (por exemplo, um link "ver no site" dentro do cartão do Teams) se ajustam sozinhos ao domínio de onde o site está rodando no momento — não é preciso configurar qual domínio usar.

---

## Enquanto isso — solução provisória (recomendado por você)

Até a TI liberar o Azure AD: quando a equipe GECEB responder no Teams, é só copiar a resposta e colar no campo **"Resposta do administrador"** do comentário, em `/admin/conteudo/comentario/` (o mesmo recurso que já existe hoje, sem nenhum código novo). Aparece no site exatamente igual a uma resposta automática apareceria. Quando a automação da Parte B for ligada, isso deixa de ser necessário, mas continua funcionando do mesmo jeito.
