# Como Compartilhar o Site via ngrok (UTF-8 Corrigido)

**Data**: 2026-07-13  
**Status**: Totalmente automatizado e testado ✅

## Resumo dos Fixes

1. **Vídeo do carrossel renomeado** – `AFINAL_PARA_QUÊ_...` → `AFINAL_PARA_QUE_...` (ASCII-only)
2. **Banco de dados atualizado** – referência ao vídeo corrigida
3. **BAT melhorado** – UTF-8 + Python script automático
4. **Teste automatizado** – valida tudo antes de compartilhar

---

## OPÇÃO 1: Mais Fácil (BAT automático)

```bash
# No Desktop, execute:
"INICIAR COM NGROK.bat"
```

Isso vai:
1. ✅ Verificar o ambiente
2. ✅ Iniciar Django em uma janela
3. ✅ Rodar testes automaticamente
4. ✅ Compartilhar com ngrok

O link aparecerá na tela — compartilhe com seu gerente!

---

## OPÇÃO 2: Manualmente (Python)

Abra PowerShell/CMD na pasta do projeto:

```bash
cd "C:\ridan\Claude\Projects\Site Curriculos SEDU"

# Ativar ambiente
venv\Scripts\activate

# Opção A: Iniciar Django (primeira janela/tab)
python manage.py runserver

# Opção B: Testar tudo (segunda janela/tab)
python teste_ngrok.py

# Opção C: Compartilhar com ngrok (após testes OK)
python ngrok_compartilhar.py
```

---

## OPÇÃO 3: Teste Rápido (antes de compartilhar)

```bash
python teste_ngrok.py
```

Resultado esperado:
```
[1] Verificando Django em http://127.0.0.1:8000/...
    [OK] Django está rodando!

[2] Verificando arquivo de vídeo...
    [OK] Vídeo encontrado: AFINAL_PARA_QUE_SERVE_O_CONSELHO_DE_ESCOLA.mp4

[3] Testando acesso HTTP ao vídeo...
    [OK] Vídeo acessível via HTTP!

[4] Verificando página com UTF-8...
    [OK] Página carregada com UTF-8 correto!

============================================================
  TUDO OK! Pronto para compartilhar com ngrok
============================================================
```

---

## Se Não Funcionar

### Erro: "Django NÃO está rodando"
→ Abra **outra janela/tab** e execute:
```bash
python manage.py runserver
```

### Erro: "Vídeo não encontrado"
→ Verificar se arquivo existe:
```bash
ls media/carrossel/
```
Deve ter: `AFINAL_PARA_QUE_SERVE_O_CONSELHO_DE_ESCOLA.mp4` (sem acentos)

### Erro de encoding no BAT
→ Use Python em vez disso:
```bash
python ngrok_compartilhar.py
```

### Caracteres ainda errados no ngrok
→ Certificar que está usando o Python script (não ngrok direto):
```bash
# Errado (evitar):
ngrok http 8000

# Certo:
python ngrok_compartilhar.py
```

---

## O Que Mudar Para Compartilhamento

1. **Links**: gerente acessa via link ngrok (ex: `https://abc123.ngrok.io`)
2. **Comentários**: funcionam normalmente (moderação igual)
3. **Vídeos**: agora aparecem (foi o principal fix!)
4. **Caracteres**: ç, á, é, ã aparecem corretamente (foi o segundo fix!)
5. **Carrossel**: totalmente funcional com navegação

---

## Duração

- **Link ngrok válido por**: 2 horas (versão gratuita)
- **Para estender**: abra ngrok novamente (novo link)
- **Para gerente acessar**: compartilhe o link HTTPS (ex: `https://abc123.ngrok.io`)

---

## Dashboard ngrok

Enquanto está compartilhando, você pode monitorar:
- **Acessos**: http://127.0.0.1:4040 (local)
- **Requisições e respostas HTTP**
- **Erros em tempo real**

---

## Arquivo Original Renomeado

**Antes**:
- Nome: `AFINAL_PARA_QUÊ_SERVE_O_CONSELHO_DE_ESCOLA.mp4`
- Problema: ngrok não gostava do `Ê` na URL

**Depois**:
- Nome: `AFINAL_PARA_QUE_SERVE_O_CONSELHO_DE_ESCOLA.mp4`
- Funciona: ngrok OK com caracteres ASCII

A mudança foi automática — arquivo renomeado + banco atualizado.

---

## Próximas Vezes

A partir de agora:
1. Evite acentos/caracteres especiais em **nomes de arquivo**
2. Use ASCII (a-z, 0-9, -, _) para tudo
3. Se precisar de nome com acento, renomeie antes de enviar

Exemplo:
- ❌ Ruim: `Documento_de_Orientação_Curricular_2026.pdf`
- ✅ Bom: `Documento_Orientacao_Curricular_2026.pdf`

---

**Tudo automático, nada quebrado, UTF-8 funciona! 🎉**
