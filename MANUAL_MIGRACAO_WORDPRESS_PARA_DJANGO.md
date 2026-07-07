# Manual: Migração de WordPress para Django — Solução de Links `/wp-content/`

**Data:** 2026-07-07  
**Versão:** 1.0  
**Preparado para:** Dan (SEDU)  

---

## 📋 O Problema

Quando o novo site Django (Python) ficar **ativo** em `curriculo.sedu.es.gov.br`, o WordPress será **removido ou desligado**. Porém:

- Todos os 1000+ arquivos migrados têm links como:  
  `https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento...pdf`

- Desses arquivos, apenas uma pequena parte foi **copiada** para o novo site (`/media/anexos/`)
- A maioria continua no WordPress original
- **Se o WordPress sumir, todos esses links quebram** ❌

---

## ✅ A Solução Recomendada

**Manter o WordPress rodando em um SUBDOMÍNIO** (`wordpress.curriculo.sedu.es.gov.br`) e deixar um **redirecionador automático** no domínio principal que manda as requisições `/wp-content/` de volta para o WordPress.

**Benefícios:**
- ✅ Todos os links antigos continuam funcionando
- ✅ Sem duplicar 1000+ arquivos
- ✅ Sem modificar nenhum link no banco de dados do Django
- ✅ Arquivos servidos do servidor original (WordPress + Apache)
- ✅ Fácil de remover o WordPress depois se não for mais necessário
- ✅ Sem custo de espaço em disco

**Diagrama:**

```
┌─────────────────────────────────────────────────────────────┐
│ Usuário clica em link: /curriculo/wp-content/uploads/file.pdf
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴────────────────────┐
        │                                        │
   Novo Django                          Redirecionador Apache
   (Python + SQLite)                    (reescreve /wp-content/)
   em curriculo.sedu.es.gov.br          ↓
                                 WordPress continua rodando
                                 em wordpress.curriculo.sedu.es.gov.br
                                 (servidor antigo ou mesmo servidor)
                                        ↓
                                   Arquivo PDF entregue ✅
```

---

## 🔧 Implementação Técnica

### **Opção 1: WordPress em Subdomínio** (RECOMENDADA — mais simples)

#### Passo 1️⃣: Configurar Novo Subdomínio no Painel de Controle

**No cPanel/Plesk/seu provedor de hosting:**

1. Acesse **Addon Domains** ou **Subdomínios**
2. Crie novo subdomínio:
   - **Nome:** `wordpress` (ficará `wordpress.curriculo.sedu.es.gov.br`)
   - **Apontar para pasta:** `/public_html/wordpress/` (ou pasta onde o WordPress original está)

3. Teste acesso: `https://wordpress.curriculo.sedu.es.gov.br/`
   - Se ver o WordPress funcionando, ótimo! ✅

#### Passo 2️⃣: Reescrever URLs `/wp-content/` no Django

**No servidor do Django (PythonAnywhere ou seu servidor):**

Edite o arquivo de configuração do Apache (ou crie um `.htaccess` se estiver no root do domínio principal):

**Arquivo:** `/var/www/rabalista_pythonanywhere_com_wsgi.py` (PythonAnywhere) ou `.htaccess` (cPanel)

Se o seu servidor for **Apache**, adicione estas regras:

```apache
# .htaccess (raiz de curriculo.sedu.es.gov.br)

<IfModule mod_rewrite.c>
    RewriteEngine On
    
    # Redirecionar /wp-content/ para o subdomínio WordPress
    RewriteRule ^curriculo/wp-content/(.*)$ https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/$1 [L,R=301]
    
    # Redirecionar /wp-includes/ também (por segurança, em caso de links antigos)
    RewriteRule ^curriculo/wp-includes/(.*)$ https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-includes/$1 [L,R=301]
</IfModule>
```

**Se estiver no PythonAnywhere**, a reescrita será feita via **URL mapeamento na aba Web**:

1. Acesse o painel PythonAnywhere → aba **Web**
2. Em **URL mappings**, adicione:

| URL | Directory/Redirecionador |
|---|---|
| `/curriculo/wp-content/` | Redirecionar para `https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/` |
| `/curriculo/wp-includes/` | Redirecionar para `https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-includes/` |

#### Passo 3️⃣: Testar os Links

Copie e cole no navegador um dos links antigos:

```
https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf
```

**Esperado:**
- ✅ Navegador redireciona automaticamente para `wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/...`
- ✅ PDF abre ou baixa normalmente
- ✅ No inspector do navegador (F12 → Network), ver status `301` (redirecionamento permanente)

---

### **Opção 2: WordPress no Mesmo Servidor (Caminho Diferente)**

Se não for possível criar subdomínio, criar uma pasta separada:

```
/public_html/curriculo/          ← Django (novo site)
/public_html/wp-backup/          ← WordPress (cópia do original)
```

Reescrever no `.htaccess`:

```apache
RewriteRule ^curriculo/wp-content/(.*)$ /wp-backup/curriculo/wp-content/$1 [L]
```

**Menos elegante** que subdomínio, mas funciona se não houver opção.

---

## 🚀 Cronograma de Migração

| Data | Ação | Responsável |
|---|---|---|
| **Semana 1** | Criar subdomínio `wordpress.curriculo.sedu.es.gov.br` + testar acesso | TI SEDU |
| **Semana 2** | Copiar WordPress completo (código + banco) para subdomínio | TI SEDU |
| **Semana 3** | Configurar reescrita de URLs no servidor principal | TI SEDU / Dan |
| **Semana 4** | Publicar novo Django em `curriculo.sedu.es.gov.br` (substituir WordPress) | Dan + TI |
| **Após 1 mês** | Testar todos os links `/wp-content/` com relatório | Dan |
| **Após 3 meses** | Se tudo OK, remover subdomínio WordPress (opcional) | TI SEDU |

---

## 🧪 Checklist de Testes (Antes de Publicar)

- [ ] Subdomínio criado e acessível
- [ ] WordPress rodando em subdomínio sem erros
- [ ] Django rodando em domínio principal sem erros
- [ ] Reescrita de URLs configurada
- [ ] Teste manual: clicar em 5 links `/wp-content/` diferentes → redirecionam corretamente
- [ ] Inspector F12 → Network → status `301` em todos os testes
- [ ] PDFs abrem/baixam normalmente
- [ ] Imagens carregam normalmente
- [ ] Vídeos (se houver em `/wp-content/`) reproduzem
- [ ] Teste em navegador diferente (Firefox, Chrome, Safari)
- [ ] Teste em celular (HTTP Request manda User-Agent mobile)
- [ ] Verificar Google Search Console → não há erros de redirecionamento
- [ ] Teste de 404: acessar link `wp-content` que não existe → erro 404 legível

---

## ⚠️ Cuidados Importantes

### 1. **Protocolo HTTPS vs HTTP**
Certifique-se de que **ambos os domínios têm certificado SSL válido**:
- `https://curriculo.sedu.es.gov.br` ✅ (Django)
- `https://wordpress.curriculo.sedu.es.gov.br` ✅ (WordPress)

Se um dos dois tiver apenas HTTP, navegadores modernos vão bloquear ou gerar avisos.

### 2. **CORS (Cross-Origin)**
Se imagens/CSS/JS do WordPress forem carregadas pelo Django (em outro domínio), pode haver erro CORS. Se isso acontecer, adicione ao `.htaccess` do WordPress:

```apache
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
</IfModule>
```

### 3. **Cache do Navegador**
Usuários que acessavam `/curriculo/wp-content/file.pdf` antes da migração podem ter a versão antiga em cache. O redirecionamento `301` (permanente) instrui navegadores a **nunca mais pedir o URL antigo**, então após uns dias tudo fica limpo. Se quiser forçar agora:

```
Ctrl+Shift+R  (Windows/Linux)
Cmd+Shift+R   (Mac)
```

### 4. **Logs e Monitoramento**
Depois da migração, monitore:

- **Erros 404** → indica links que não foram migrados
- **Redirects 301** → redirecionamentos funcionando
- **Erros 500** → problema no subdomínio WordPress

**No cPanel** → Metrics → HTTP Requests or Error Log  
**No PythonAnywhere** → Web → Error Log

---

## 🔄 Plano B: Se Algo der Errado

Se os links quebrarem ou o redirecionamento não funcionar:

1. **Investigar com `curl` no terminal:**
   ```bash
   curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/file.pdf
   ```
   - Deve retornar `HTTP 301` (redirecionamento) ou `HTTP 200` (sucesso)
   - Se retornar `404`, o arquivo não está no subdomínio WordPress

2. **Verificar arquivo no subdomínio:**
   ```bash
   curl -I https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/file.pdf
   ```
   - Se retornar `404`, arquivo não foi copiado → copiar manualmente

3. **Reverter para WordPress temporariamente:**
   - Desativar reescrita de URLs (comentar as linhas do `.htaccess`)
   - Retirar Django do ar (manutenção)
   - Publicar WordPress novamente no domínio principal
   - Investigar e tentar de novo

---

## 📊 Resumo da Solução

| Aspecto | Solução |
|---|---|
| **Onde fica o Django** | `curriculo.sedu.es.gov.br` (domínio principal) |
| **Onde fica WordPress** | `wordpress.curriculo.sedu.es.gov.br` (subdomínio) |
| **Links do banco** | Sem alteração — continuam apontando para `/curriculo/wp-content/...` |
| **Roteamento** | Reescrita Apache automaticamente redireciona `/wp-content/` → subdomínio |
| **Espaço em disco** | Sem duplicação — WordPress continua em um local só |
| **Manutenção** | Apenas ligar/desligar WordPress quando necessário |
| **Remover depois** | Fácil — basta deletar subdomínio quando arquivos forem todos transferidos |

---

## 🎯 Próximos Passos (Quando Chegar a Hora)

1. **Avise a TI SEDU:** que vai precisar criar subdomínio antes da migração
2. **Prepare banco Django:** garanta que todos os links estejam corretos em `conteudo.url_externa`
3. **Teste localmente:** use um arquivo local `/etc/hosts` para simular subdomínios antes de publicar
4. **Coordene com TI:** agenda data/hora para:
   - Criar subdomínio
   - Copiar WordPress
   - Ativar reescrita
   - Publicar Django
   - Monitorar por 24h

5. **Documente:** salve este manual no GitHub do projeto para referência futura

---

## ❓ Perguntas Frequentes

**P: Por quanto tempo o WordPress deve continuar rodando no subdomínio?**  
R: Pelo menos 3-6 meses. Depois, se todos os arquivos tiverem sido copiados para o novo site Django, pode remover.

**P: Posso migrar os arquivos gradualmente enquanto o WordPress continua lá?**  
R: Sim! A vantagem da solução de subdomínio é que permite migração gradual — você copia arquivos para `/media/anexos/` do Django sem pressa, e os links redirecionados continuam funcionando pelo WordPress.

**P: E se o WordPress ficar offline acidentalmente?**  
R: Links vão retornar `503 Service Unavailable`. Por isso é importante ter alertas configurados (monitoramento).

**P: Preciso avisar aos usuários sobre a mudança?**  
R: Não — para eles é transparente. Links continuam funcionando normalmente, redirecionamento é automático.

**P: Como faz pra testar isso localmente antes de publicar?**  
R: Edite seu arquivo `/etc/hosts` (local) ou use uma ferramenta como ngrok para simular subdomínios em desenvolvimento.

---

## 📞 Suporte

Se durante a implementação algo não funcionar:

1. Verifique os logs do servidor (cPanel → Error Log)
2. Teste manualmente com `curl` (comando acima)
3. Verifique certificado SSL de ambos os domínios
4. Verifique se reescrita Apache está ativada (`a2enmod rewrite`)
5. Contate TI SEDU para ajuda de infraestrutura

---

**Documento criado por:** Claude Code  
**Última atualização:** 2026-07-07  
**Status:** Pronto para implementação
