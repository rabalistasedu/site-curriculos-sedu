# Como Sincronizar Dados Locais com Servidor SEDU

**Data:** 2026-07-07  
**Versão:** 1.0  
**Para:** Dan (SEDU)  

---

## 📌 O Problema

Quando você adiciona conteúdo, categoria ou banner via admin local:

```
Seu PC (local)                           Servidor SEDU
┌─────────────────────┐                 ┌─────────────────────┐
│ db.sqlite3          │                 │ db.sqlite3          │
│ ✅ Dados novos aqui │        ❌       │ Dados NÃO aparecem  │
│ (você salvou)       │      Banco      │ aqui               │
│                     │     NÃO vai     │                     │
│                     │    para Git     │ (banco separado)    │
└─────────────────────┘                 └─────────────────────┘
```

**Por quê?** O arquivo `db.sqlite3` está no `.gitignore` — não é versionado no GitHub.

---

## ✅ A Solução: Backup Manual + Upload

### **Passo 1: Trabalhe Localmente**

Adicione o que quiser no admin:
- http://127.0.0.1:8000/admin/

Adicione categorias, conteúdos, banners, comentários, tudo que precisar.

Tudo é salvo automaticamente em `db.sqlite3` no seu PC.

---

### **Passo 2: Faça Backup do Banco Local**

**Opção A: Manualmente (GUI)**

1. Abra a pasta do projeto:
   ```
   C:\Users\ridan\Claude\Projects\Site Curriculos SEDU\
   ```

2. Copie o arquivo `db.sqlite3`

3. Cole em uma pasta de backup com nome que inclua a data:
   ```
   C:\Backups\db_curriculo_2026_07_07.sqlite3
   ```

**Opção B: Linha de Comando (mais fácil)**

```bash
# No terminal, na pasta do projeto:
# Windows (Git Bash):
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# Mac/Linux:
cp db.sqlite3 ~/Backups/db_curriculo_$(date +%Y%m%d_%H%M%S).sqlite3
```

---

### **Passo 3: Subir Código para GitHub (Como Sempre)**

```bash
# Terminal na pasta do projeto:
git add -A
git commit -m "Adiciona nova categoria: [descrição]"
git push origin main
```

Ou clique 2x no `.bat` "Subir GitHub SEDU" (seu script atual).

---

### **Passo 4: Subir Banco para SEDU (Via cPanel)**

**Local:** `C:\Users\ridan\Claude\Projects\Site Curriculos SEDU\db.sqlite3`  
**Destino:** `/home/rabalista/site-curriculos-sedu/db.sqlite3` (em SEDU)

#### **Método 1: cPanel File Manager (Mais Fácil)**

1. **Acesse cPanel SEDU:**
   - URL: `https://cpanel.pythonanywhere.com/` (ou conforme instruído)
   - Login: seu usuário PythonAnywhere

2. **Abra File Manager**

3. **Navegue para:** `/home/rabalista/site-curriculos-sedu/`

4. **Delete o banco antigo:**
   - Clique com botão direito em `db.sqlite3`
   - Clique **Delete**

5. **Upload do novo banco:**
   - Clique em **Upload**
   - Selecione seu arquivo `db.sqlite3` local
   - Espere 100% de progresso

6. **Pronto!** Django automaticamente usa o novo banco

---

#### **Método 2: SFTP (Mais Seguro, Recomendado)**

Abra terminal/PowerShell e copie este código (altere o caminho se necessário):

```bash
# Conectar ao servidor
sftp rabalista@rabalista.pythonanywhere.com

# Entrar na pasta do projeto
cd site-curriculos-sedu

# Opcional: fazer backup do banco antigo (por segurança)
rename db.sqlite3 db.sqlite3.backup

# Enviar seu arquivo local
put C:\Users\ridan\Claude\Projects\Site Curriculos SEDU\db.sqlite3 db.sqlite3

# Sair
exit
```

**Se aparecer erro de permissão:** (Windows)
```bash
# Use aspas se o caminho tiver espaços:
put "C:\Users\ridan\Claude\Projects\Site Curriculos SEDU\db.sqlite3" db.sqlite3
```

---

### **Passo 5: Recarregar o Django em SEDU**

1. **Acesse PythonAnywhere:**
   - https://www.pythonanywhere.com/

2. **Abra aba Web:**
   - Clique em **Reload** (botão verde)

3. **Espere ~30 segundos**

---

### **Passo 6: Verificar se Funcionou**

**Método 1: Visualmente (Mais Fácil)**

1. Abra no navegador:
   - Local: http://127.0.0.1:8000/admin/
   - SEDU: https://rabalista.pythonanywhere.com/admin/

2. Compare os dados em ambos (devem ser iguais)

3. Se vir o conteúdo novo em SEDU, funcionou! ✅

**Método 2: Linha de Comando (Mais Preciso)**

```bash
# Local: contar quantos conteúdos existem
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM conteudo_conteudo;"
# Resultado: 150 (exemplo)

# SEDU: abra Bash do PythonAnywhere e execute:
cd ~/site-curriculos-sedu && sqlite3 db.sqlite3 "SELECT COUNT(*) FROM conteudo_conteudo;"
# Resultado deve ser igual: 150
```

Se os números forem iguais, sincronização bem-sucedida! ✅

---

## ⚠️ Cuidados Importantes

### **1. Sempre Fazer Backup do Banco SEDU Antes**

Se o servidor tem dados que não estão no seu backup local, eles vão desaparecer!

```bash
# No Bash do PythonAnywhere, antes de fazer upload:
cp ~/site-curriculos-sedu/db.sqlite3 ~/db.sqlite3.backup.sedu
```

### **2. Sincronizar Migrations Antes (Se Aplicável)**

Se você mudou a estrutura do banco (adicionou campo novo, removeu coluna, etc.):

```bash
# Bash PythonAnywhere:
cd ~/site-curriculos-sedu
source venv/bin/activate
python manage.py migrate
```

Depois sim, faz upload do `db.sqlite3`.

### **3. Permissões do Arquivo**

Após upload, garanta que o arquivo tem permissões certas:

```bash
# Bash PythonAnywhere:
chmod 644 ~/site-curriculos-sedu/db.sqlite3
```

### **4. Horário do Servidor**

Se conteúdos têm `data_publicacao` (agendamento) no futuro, verifique se a hora está certa:

```bash
# Bash PythonAnywhere, ver hora do servidor:
date

# Esperado: algo como: Mon Jul  7 14:30:15 UTC 2026
```

### **5. Tamanho do Banco**

SQLite funciona bem até ~500MB. Ver tamanho:

```bash
# Bash PythonAnywhere:
ls -lh ~/site-curriculos-sedu/db.sqlite3
# Resultado: -rw-r--r-- 1 rabalista rabalista 25M Jul  7 14:30 db.sqlite3
```

Se ficar > 300MB, considerar migrar para PostgreSQL.

---

## 📅 Frequência Recomendada

| Frequência | Recomendação |
|---|---|
| **Semanal** | Sincronize 1x por semana ou quando adicionar conteúdo importante |
| **Backup Local** | Sempre mantenha backup local em pasta segura (ex: `C:\Backups\`) |
| **Histórico** | Guarde backups por pelo menos 1 mês (para poder reverter se necessário) |
| **Documentação** | Anote a data de cada backup em uma lista (Excel, Notepad, etc.) |

---

## 🔄 Fluxo Visual Completo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. TRABALHE LOCALMENTE (seu PC)                                  │
│    - Abra http://127.0.0.1:8000/admin/                         │
│    - Adicione categorias, conteúdos, banners                   │
│    - Tudo salva em db.sqlite3 automaticamente                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. FAÇA BACKUP DO BANCO LOCAL                                   │
│    - Copie db.sqlite3 para pasta de backup                     │
│    - Coloque data no nome: db_2026_07_07.sqlite3             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. SUBA CÓDIGO PARA GITHUB (como sempre)                       │
│    - git add -A                                                  │
│    - git commit -m "descrição"                                 │
│    - git push origin main                                      │
│    (ou clique 2x no .bat "Subir GitHub SEDU")                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. SUBA BANCO PARA SEDU (nova etapa!)                         │
│    - Via cPanel: Upload do db.sqlite3 para /home/rabalista/   │
│    - Via SFTP: sftp + put comando                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. RELOAD NO PYTHONANYWHERE                                     │
│    - Acesse https://www.pythonanywhere.com/                    │
│    - Clique em "Reload" (aba Web)                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ ✅ PRONTO! Site em SEDU com dados novos                        │
│    - Verifique em https://rabalista.pythonanywhere.com/admin/  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🆘 Se Algo der Errado

### **Problema: Após reload, dados não aparecem em SEDU**

**Verificar:**

1. Arquivo foi realmente uploadado?
   ```bash
   # Bash PythonAnywhere:
   ls -lh ~/site-curriculos-sedu/db.sqlite3
   ```

2. Tamanho do arquivo é similar ao local?
   ```bash
   # Local: Abra File Manager e veja tamanho
   # SEDU: Use comando ls acima
   ```

3. Clicar Reload novamente (às vezes precisa 2x)

4. Limpar cache do navegador (Ctrl+Shift+R)

### **Problema: Dados em SEDU desapareceram**

Você provavelmente fez upload de um banco antigo. **Reverter:**

```bash
# Bash PythonAnywhere:
cd ~/site-curriculos-sedu

# Ver backups disponíveis:
ls db.sqlite3*

# Restaurar o backup:
mv db.sqlite3.backup db.sqlite3

# Reload novamente
```

### **Problema: Erro de permissão ao fazer upload**

```bash
# Bash PythonAnywhere, dar permissão ao arquivo:
chmod 644 ~/site-curriculos-sedu/db.sqlite3
chmod 755 ~/site-curriculos-sedu/
```

---

## 📊 Resumo: Banco de Dados em Cada Lugar

| Onde | O que tem | Sincronizado? |
|---|---|---|
| **PC Local** | db.sqlite3 + seus dados | ✅ Você controla |
| **GitHub** | ❌ Não vai (gitignore) | ❌ Não |
| **SEDU** | db.sqlite3 (antigo/novo) | ✅ Você decide quando |

**Fluxo:**
- Código (Python) → GitHub → SEDU (automático via git pull/push)
- Dados (banco) → Manual via SFTP/cPanel (você controla)

---

## ✅ Checklist de Segurança

- [ ] Backup local do db.sqlite3 feito
- [ ] Backup local armazenado em pasta segura com data
- [ ] Backup do banco SEDU feito antes de fazer upload
- [ ] Migrations sincronizadas (se aplicável)
- [ ] Código pushado para GitHub
- [ ] Banco uploadado via SFTP/cPanel
- [ ] Reload clicado no PythonAnywhere
- [ ] Verificação visual: dados aparecem em SEDU
- [ ] Contagem de conteúdos conferida (local = SEDU)

---

## 📞 Dúvidas?

Consulte:
- Este documento: **SINCRONIZAR_BANCO_LOCAL_SEDU.md**
- CLAUDE.md → seção "Sincronização de Dados"
- MANUAL_MIGRACAO_WORDPRESS_PARA_DJANGO.md

---

**Documento criado por:** Claude Code  
**Última atualização:** 2026-07-07  
**Status:** Pronto para usar
