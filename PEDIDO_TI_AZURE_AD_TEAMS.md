# Solicitação para a TI da SEDU — Cadastro de Aplicativo no Azure AD

**Pronto para copiar e enviar por e-mail, chamado/ticket, ou Teams para a equipe de TI da SEDU.**

---

## Assunto sugerido
Solicitação de cadastro de aplicativo no Azure AD (App Registration) — Site Currículo GECEB

---

## Texto para enviar

Olá,

Preciso de um cadastro de aplicativo (**App Registration**) no Azure AD do tenant da SEDU, para uma integração do site do Currículo (GECEB) com o Microsoft Teams. Essa integração já está funcionando na parte de **envio** (o site posta os comentários dos visitantes automaticamente em um canal do Teams); o que falta é a parte de **leitura**, para o site conseguir buscar as respostas que a equipe GECEB dá naquelas conversas do Teams e trazê-las de volta para o site automaticamente.

### O que preciso que seja cadastrado

Um **App Registration** no Azure AD, com:

- **Tipo de permissão**: **Application** (permissão de aplicativo — não é "delegada", já que não há um usuário logado interativamente; é um processo automático rodando em segundo plano).
- **Permissões da Microsoft Graph API necessárias**:
  - `ChannelMessage.Read.All` — ler mensagens de canais do Teams
  - `Team.ReadBasic.All` — listar informações básicas de Teams
  - `Channel.ReadBasic.All` — listar informações básicas de canais
- **Consentimento de administrador (admin consent)** aplicado a essas 3 permissões — sem isso, o aplicativo não consegue usá-las.

### Por que só leitura

O aplicativo **não precisa e não deve ter** nenhuma permissão de escrita, exclusão ou envio de mensagens via Graph API (o envio de comentários para o Teams já é feito por outro caminho, via Power Automate/webhook, que não depende desse cadastro). A única finalidade dessas 3 permissões é **consultar** mensagens já existentes num canal específico, para saber se a equipe respondeu a um comentário.

### O que preciso que me devolvam depois do cadastro

- **Application (client) ID**
- **Client secret** (o valor gerado, não o nome/ID do secret — e de preferência com validade longa, já que é um processo automático que roda continuamente)
- **Directory (tenant) ID**

Essas 3 informações serão guardadas em variável de ambiente no servidor do site (nunca em código-fonte versionado), e usadas apenas para autenticação do tipo *client credentials* (processo a processo, sem envolver login de nenhum usuário).

Fico à disposição para qualquer dúvida técnica ou para ajustar o escopo das permissões, se necessário.

Obrigado,
[seu nome]

---

## Depois que a TI responder

Quando vocês me devolverem o **Client ID**, o **Client Secret** e o **Tenant ID**, eu mesmo preencho essas informações no site — não precisa de nenhuma ação adicional da TI depois disso. O **Team ID** e o **Channel ID** eu já consigo pegar sozinho, direto no link do canal do Teams (não depende da TI).

## Se a TI perguntar "por que Graph API e não outra coisa"

Porque o Microsoft Teams **não tem um recurso de baixo código (Power Automate) que avise quando alguém responde dentro de uma conversa de um canal** — só avisa para mensagem nova na raiz do canal. A Microsoft Graph API é a forma oficial e documentada de consultar essas respostas. É uma limitação da própria plataforma Teams, não uma escolha técnica evitável.
