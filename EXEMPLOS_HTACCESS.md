# Exemplos de `.htaccess` — Prontos para Copiar e Colar

**Data:** 2026-07-07  
**Versão:** 1.0  

---

## 📝 Opção 1: Subdomínio WordPress (RECOMENDADA)

Quando o WordPress estiver em `wordpress.curriculo.sedu.es.gov.br`

**Arquivo:** `.htaccess` na raiz de `curriculo.sedu.es.gov.br`

**Copie e cole tudo abaixo:**

```apache
# ============================================================
# SITE CURRÍCULOS SEDU - REDIRECIONAMENTO DE /wp-content/
# ============================================================
# Reescreve requisições para /wp-content/ para o subdomínio WordPress
# Data: 2026-07-07
# ============================================================

<IfModule mod_rewrite.c>
    RewriteEngine On
    
    # Base do rewrite (importante para Django)
    RewriteBase /
    
    # ─────────────────────────────────────────────────────────
    # REDIRECIONAMENTOS DE /wp-content/ → SUBDOMÍNIO WORDPRESS
    # ─────────────────────────────────────────────────────────
    
    # Redirecionar /curriculo/wp-content/ para subdomínio
    RewriteCond %{REQUEST_URI} ^/curriculo/wp-content/
    RewriteRule ^curriculo/wp-content/(.*)$ https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-content/$1 [L,R=301,QSA]
    
    # Redirecionar /curriculo/wp-includes/ também (opcional, por segurança)
    RewriteCond %{REQUEST_URI} ^/curriculo/wp-includes/
    RewriteRule ^curriculo/wp-includes/(.*)$ https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-includes/$1 [L,R=301,QSA]
    
    # Redirecionar /curriculo/wp-admin/ também (opcional, por segurança)
    RewriteCond %{REQUEST_URI} ^/curriculo/wp-admin/
    RewriteRule ^curriculo/wp-admin/(.*)$ https://wordpress.curriculo.sedu.es.gov.br/curriculo/wp-admin/$1 [L,R=301,QSA]
    
    # ─────────────────────────────────────────────────────────
    # PASSTHROUGH: Deixa Django lidar com o resto
    # ─────────────────────────────────────────────────────────
    
    # Se o arquivo/diretório NÃO existir, deixar Django processar
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    
    # Redirecionar tudo para Django (WSGI)
    RewriteRule ^(.*)$ /index.wsgi/$1 [QSA,PT,L]
</IfModule>

# ─────────────────────────────────────────────────────────
# SEGURANÇA ADICIONAL (opcional)
# ─────────────────────────────────────────────────────────

<IfModule mod_headers.c>
    # Bloquear acesso direto ao .htaccess
    Header always append X-Frame-Options "SAMEORIGIN"
    Header always append X-Content-Type-Options "nosniff"
</IfModule>

# ─────────────────────────────────────────────────────────
# FIM DA CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────
```

---

## 📝 Opção 2: WordPress em Pasta Separada (Plano B)

Se não conseguir subdomínio, usar `/wp-backup/`

**Arquivo:** `.htaccess` na raiz de `curriculo.sedu.es.gov.br`

**Copie e cole tudo abaixo:**

```apache
# ============================================================
# SITE CURRÍCULOS SEDU - /wp-content/ EM PASTA LOCAL
# ============================================================
# Reescreve requisições para /wp-content/ para pasta /wp-backup/
# Usar APENAS se subdomínio não for possível
# ============================================================

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    
    # ─────────────────────────────────────────────────────────
    # REDIRECIONAR /wp-content/ PARA /wp-backup/
    # ─────────────────────────────────────────────────────────
    
    # Redirecionar /curriculo/wp-content/ para /wp-backup/curriculo/wp-content/
    RewriteCond %{REQUEST_URI} ^/curriculo/wp-content/
    RewriteRule ^curriculo/wp-content/(.*)$ /wp-backup/curriculo/wp-content/$1 [L,QSA]
    
    # Redirecionar /curriculo/wp-includes/ para /wp-backup/curriculo/wp-includes/
    RewriteCond %{REQUEST_URI} ^/curriculo/wp-includes/
    RewriteRule ^curriculo/wp-includes/(.*)$ /wp-backup/curriculo/wp-includes/$1 [L,QSA]
    
    # ─────────────────────────────────────────────────────────
    # PASSTHROUGH: Deixa Django lidar com o resto
    # ─────────────────────────────────────────────────────────
    
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ /index.wsgi/$1 [QSA,PT,L]
</IfModule>
```

---

## 🔍 Notas Importantes

### ✅ O que cada linha faz:

| Linha | Significado |
|---|---|
| `RewriteEngine On` | Ativa o módulo de reescrita |
| `RewriteBase /` | Define a base para URLs relativas |
| `RewriteCond` | Condição (se a URL atender) |
| `RewriteRule` | Regra (o que fazer) |
| `^/curriculo/wp-content/` | Começa com `/curriculo/wp-content/` |
| `(.*)$` | Captura o resto da URL |
| `$1` | Usa o que foi capturado |
| `[L,R=301]` | `L` = Last (para reescrita), `R=301` = Redirecionamento permanente |
| `[QSA]` | Preservar parâmetros de query string (ex: `?v=1`) |
| `[PT]` | Pass Through (deixar passar como arquivo real) |

---

## 🧪 Como Testar o `.htaccess`

### Passo 1: Upload do Arquivo

1. Acesse seu painel de controle (cPanel / Plesk)
2. Abra **File Manager**
3. Navegue para `/public_html/`
4. Crie arquivo novo chamado `.htaccess` (note o ponto no início)
5. Cole o conteúdo acima
6. Salve

**⚠️ Importante:** se um `.htaccess` já existe, ADICIONE as novas linhas de reescrita, não substitua tudo!

### Passo 2: Testar com `curl` (ver seção abaixo)

### Passo 3: Se Não Funcionar

Verifique:

1. **Módulo Apache `mod_rewrite` ativado?**
   ```bash
   a2enmod rewrite
   ```

2. **AllowOverride configurado?**
   ```apache
   <Directory /var/www/html>
       AllowOverride All
   </Directory>
   ```

3. **Erro no log?**
   ```bash
   tail -f /var/log/apache2/error.log
   ```

---

## ⚠️ Síntese: Use Qual?

| Situação | Usar |
|---|---|
| Tem acesso a criar subdomínio | **Opção 1** (subdomínio) — melhor |
| Não tem como criar subdomínio | **Opção 2** (pasta local) — funciona mas menos elegante |
| Não sabe qual usar | Pergunte à TI — eles saberão qual é possível no servidor |

---

**Documento criado por:** Claude Code  
**Última atualização:** 2026-07-07
