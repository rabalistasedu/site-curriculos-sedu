# Teste Manual — Validar Links `/wp-content/` Após Migração

**Data:** 2026-07-07  
**Versão:** 1.0  

---

## 📝 Como Usar Este Documento

Quando o novo Django estiver publicado e o WordPress em subdomínio, copie e cole **cada comando abaixo** no terminal (Bash/PowerShell) do seu computador para validar que os links funcionam.

**Não precisa estar logado no servidor** — os testes são feitos remotamente via `curl`.

---

## 🔧 Teste 1: Link Antigo Redireciona Corretamente

Verifica se um link `/wp-content/` do banco de dados redireciona para o subdomínio.

**Comando:**

```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf
```

**Esperado:**

```
HTTP/1.1 301 Moved Permanently
Location: https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf
```

✅ Se ver `301`, funcionou! O navegador vai seguir para o subdomínio automaticamente.

❌ Se ver `404 Not Found`, o arquivo não está no subdomínio WordPress.

---

## 🔧 Teste 2: Arquivo Existe no Subdomínio WordPress

Verifica se o arquivo realmente está no subdomínio após redirecionamento.

**Comando:**

```bash
curl -I https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf
```

**Esperado:**

```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Length: 1234567
```

✅ Se ver `200 OK`, arquivo existe e pode ser baixado.

❌ Se ver `404`, arquivo não foi copiado para o subdomínio.

---

## 🔧 Teste 3: Cadeia Completa (Redirecionamento + Entrega)

Teste simulando um navegador (segue redirecionamentos automaticamente).

**Comando:**

```bash
curl -L -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf
```

**Esperado:**

```
HTTP/1.1 301 Moved Permanently
Location: https://wordpress.curriculo.sedu.es.gov.br/curriculo/...

HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Length: 1234567
```

✅ Duas respostas: primeiro `301` (redirecionamento), depois `200` (arquivo).

❌ Se terminar em `404`, arquivo não existe no subdomínio.

---

## 🔧 Teste 4: Vários Tipos de Arquivo

Teste diferentes extensões (PDF, Word, Excel, vídeo, imagem).

### PDF:
```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/arquivo.pdf
```

### Word (.docx):
```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/10/documento.docx
```

### Excel (.xlsx):
```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/11/planilha.xlsx
```

### PowerPoint (.pptx):
```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/12/apresentacao.pptx
```

### Vídeo (.mp4):
```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2026/01/video.mp4
```

### Imagem (.jpg):
```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/08/imagem.jpg
```

**Esperado para todos:** `301` ou `200` (sem `404`)

---

## 🔧 Teste 5: Parâmetros de Query String

Alguns links antigos podem ter parâmetros (ex: `?v=123`). Testa se são preservados.

**Comando:**

```bash
curl -I "https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/arquivo.pdf?v=1&download=true"
```

**Esperado:**

```
HTTP/1.1 301 Moved Permanently
Location: https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/arquivo.pdf?v=1&download=true
```

✅ Parâmetros aparecem no redirecionamento (por isso o `[QSA]` no `.htaccess`).

---

## 🔧 Teste 6: Links 404 (Arquivo Não Existe)

Testa se erros são tratados corretamente.

**Comando:**

```bash
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/99/arquivo-inexistente.pdf
```

**Esperado:**

```
HTTP/1.1 301 Moved Permanently
Location: https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/99/arquivo-inexistente.pdf

HTTP/1.1 404 Not Found
```

✅ Redirecionamento acontece, mas subdomínio retorna `404` (normal).

❌ Se receber `404` já no domínio principal **sem redirecionar**, há problema na reescrita.

---

## 🔧 Teste 7: HTTPS Funciona

Garante que certificado SSL é válido em ambos os domínios.

**Comando:**

```bash
curl -v https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/arquivo.pdf 2>&1 | grep -E "SSL|certificate|subject"
```

**Esperado:**

```
* subject: CN=curriculo.sedu.es.gov.br
* issuer: C=...; O=Let's Encrypt; CN=...
* SSL certificate verify ok
```

✅ Certificado válido.

❌ Se ver `certificate verify failed`, certificado está expirado ou inválido.

---

## 🔧 Teste 8: Ambos os Domínios Respondendo

Teste rápido para garantir que ambos estão online.

**Comando 1 — Django Principal:**
```bash
curl -s https://curriculo.sedu.es.gov.br/ | head -20
```

**Esperado:** Primeiras linhas do HTML da home do Django

**Comando 2 — Subdomínio WordPress:**
```bash
curl -s https://wordpress.curriculo.sedu.es.gov.br/ | head -20
```

**Esperado:** Primeiras linhas do HTML do WordPress

✅ Se ambos retornam HTML, estão online.

❌ Se algum retorna erro/timeout, servidor offline.

---

## 🧪 Teste Completo (Batch)

Copie e cole **todos de uma vez** para validar tudo rapidamente.

```bash
echo "=== TESTE 1: Redirecionamento 301 ==="
curl -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf

echo -e "\n=== TESTE 2: Arquivo no Subdomínio ==="
curl -I https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf

echo -e "\n=== TESTE 3: Cadeia Completa (com -L) ==="
curl -L -I https://curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/Curriculo-EM_Aprofundamento-da-area_-Matematica_-Alterado_15-09-23.pdf

echo -e "\n=== TESTE 4: Domínio Principal Online ==="
curl -s https://curriculo.sedu.es.gov.br/ | grep -i "<title>" | head -1

echo -e "\n=== TESTE 5: Subdomínio WordPress Online ==="
curl -s https://wordpress.curriculo.sedu.es.gov.br/ | grep -i "<title>" | head -1

echo -e "\n=== TESTES CONCLUÍDOS ==="
```

**Copie, execute, e envie o resultado para análise.**

---

## 🔍 Interpretar Resultados

### Status HTTP Codes:

| Código | Significado | É Problema? |
|---|---|---|
| `200` | OK — arquivo existe e pode ser baixado | ❌ Não |
| `301` | Redirecionamento permanente | ❌ Não (esperado) |
| `302` | Redirecionamento temporário | ⚠️ Possível (aceitar) |
| `304` | Não modificado (cache OK) | ❌ Não |
| `403` | Forbidden — acesso negado | ✅ Sim |
| `404` | Not Found — arquivo não existe | ✅ Sim (a menos que seja intencional) |
| `500` | Erro interno do servidor | ✅ Sim |
| `503` | Serviço indisponível | ✅ Sim |

---

## 📊 Tabela de Diagnóstico

Se algo não funcionar, use este fluxograma:

| Cenário | Causa Provável | Solução |
|---|---|---|
| Link retorna `404` do domínio principal | Reescrita `.htaccess` não ativa | Verificar se `RewriteEngine On` existe |
| Redireciona mas `404` no subdomínio | Arquivo não foi copiado | Copiar WordPress completo ou arquivo específico |
| `SSL certificate verify failed` | Certificado expirado/inválido | Renovar certificado Let's Encrypt |
| `Connection refused` | Subdomínio offline | Verificar se WordPress está rodando |
| `Timeout` | Servidor lento ou bloqueado | Verificar logs do servidor, firewall |

---

## 📝 Checklist Antes de Publicar

- [ ] Teste 1 retorna `301`? ✅
- [ ] Teste 2 retorna `200`? ✅
- [ ] Teste 3 retorna `301` + `200`? ✅
- [ ] Teste 4 funciona para PDF, Word, Excel, PPT, vídeo, imagem? ✅
- [ ] Teste 5 preserva parâmetros de query? ✅
- [ ] Teste 6 erros `404` são redirecionados? ✅
- [ ] Teste 7 certificados SSL válidos? ✅
- [ ] Teste 8 ambos domínios respondendo? ✅

Se todos forem ✅, **está pronto para publicar!**

---

## 📞 Suporte

Se algum teste falhar:

1. **Copie o resultado exato do comando**
2. **Envie o resultado + o comando usado**
3. **Indicar qual teste falhou** (1, 2, 3, etc.)

Exemplo de bug report:

```
Teste 2 falhou:

$ curl -I https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/uploads/2023/09/arquivo.pdf

curl: (7) Failed to connect to wordpress.curriculo.sedu.es.gov.br port 443: Connection refused
```

---

**Documento criado por:** Claude Code  
**Última atualização:** 2026-07-07  
**Status:** Pronto para usar
