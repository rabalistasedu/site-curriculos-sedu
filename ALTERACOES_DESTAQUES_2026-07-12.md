# Alterações na Seção de Destaques — 2026-07-12

## Resumo

Implementação completa da seção de **Destaques** (destaque=True em Conteudo) com suporte a múltiplos tipos de conteúdo, layout responsivo, e abertura automática de links externos em nova aba. O problema-chave resolvido: **URLs sem `https://` prefix não abriam** — era navegador interpretando como caminho interno.

---

## 1️⃣ Requisito Original (do Dan)

> "perfeito mas ficou cortado precia tudo ficar adequado a essa area sem cortar e outra coisa posso colocar varias coisas em destaques e uma precisa ficar ao lado da outra sem cortes trabalhe nesta area para suportar varios distaques, botoes, videos, e outros arquivos sem cortar e ficar se houver mais de um destaque alinhar todos nestes campos um ao lado do outro adequando ao espaco da area"

> "perfeito mas preciso tambem em tudo que eu marcar destaque e se eu escolher o campo no painel conteudo arquivo.midia link e adicionar uma url ao clicar no que esta em destaque abrir a url ou se for botao a mesma coisa se eu preencher o campo url"

**Exigências:**
- ✅ Múltiplos destaques lado a lado sem cortar conteúdo
- ✅ Suportar vários tipos: imagem, vídeo, documento, botão, link
- ✅ URLs externas abrem em nova aba (`target="_blank"`)
- ✅ Layout responsivo (quebra para 1 coluna em mobile)

---

## 2️⃣ Arquivos Alterados

### `conteudo/models.py`

#### ✨ Nova propriedade: `link_externo`
```python
@property
def link_externo(self):
    """URL externa pronta para uso no href. Garante que sempre tenha
    um schema (http:// ou https://) na frente — sem isso o navegador
    interpreta 'uol.com.br' como caminho interno do próprio site
    (=> tenta abrir /uol.com.br dentro do site atual, o que dá o erro
    'recusou a se conectar'). Aceita URLs coladas sem o https://."""
    url = (self.url_externa or '').strip()
    if not url:
        return ''
    # Já tem schema (http://, https://, mailto:, tel:, ftp://, //, #, /)?
    if '://' in url or url.startswith(('mailto:', 'tel:', '//', '#', '/')):
        return url
    # Sem schema: assume https:// (mais seguro e mais comum hoje)
    return 'https://' + url
```

**Problemas que resolve:**
- `uol.com.br` → `https://uol.com.br` ✅
- `www.sedu.es.gov.br` → `https://www.sedu.es.gov.br` ✅
- `https://uol.com.br` → mantém como está ✅
- `  uol.com.br  ` (com espaços) → `https://uol.com.br` ✅
- Vazio → `''` (sem link) ✅

### `templates/home.html`

#### 🎯 Destaques (linhas 47-78)
```django
<a href="{% if item.link_externo %}{{ item.link_externo }}{% else %}{% url 'conteudo:conteudo_detalhe' item.slug %}{% endif %}"
   class="content-card"
   {% if item.link_externo %}target="_blank" rel="noopener"{% endif %}>
```

**Mudanças:**
- Trocou `item.url_externa` por `item.link_externo` (propriedade que garante schema)
- Condicional: se tem URL externa, usa ela + abre em nova aba; senão, abre página interna
- Classes: `.content-grid` + `.destaques-grid` (layout responsivo)

#### 📋 Conteúdos Recentes (linhas 144-160)
```django
<a href="{% if item.link_externo %}{{ item.link_externo }}{% else %}{% url 'conteudo:conteudo_detalhe' item.slug %}{% endif %}"
   class="list-item"
   {% if item.link_externo %}target="_blank" rel="noopener"{% endif %}>
```

**Mudanças:** mesmo padrão dos destaques (URL com schema garantido + target="_blank")

### `templates/categoria.html`

#### 📌 Conteúdos da Categoria (linhas 131-153)
```django
<a href="{% if item.link_externo %}{{ item.link_externo }}{% else %}{% url 'conteudo:conteudo_detalhe' item.slug %}{% endif %}"
   class="content-card{% if item.pk in pulsantes %} btn-pulse{% endif %}"
   {% if item.link_externo %}target="_blank" rel="noopener"{% endif %}>
```

**Mudanças:** aplicado mesmo padrão de URL segura

### `templates/busca.html`

#### 🔍 Resultados de Busca (linhas 40-55)
```django
<a href="{% if item.link_externo %}{{ item.link_externo }}{% else %}{% url 'conteudo:conteudo_detalhe' item.slug %}{% endif %}"
   class="list-item"
   {% if item.link_externo %}target="_blank" rel="noopener"{% endif %}>
```

**Mudanças:** mesmo padrão (4 templates, 1 padrão — consistente)

### `static/css/style.css`

#### 🎨 Destaques Grid (bloco "AJUSTES 2026-07-11")
```css
.destaques-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}
```

**Mudanças anteriores (já existentes, mas relevantes):**
- Mudou de `grid-template-columns: 1fr` (1 coluna) para `repeat(auto-fit, minmax(300px, 1fr))`
- Resultado: múltiplos cards lado a lado, quebram automaticamente em mobile
- Cards têm 300px de mínimo, mas crescem para preencher espaço

#### 🖼️ Cards com Imagem
```css
.card-image img {
    object-fit: contain;  /* não corta, apenas ajusta */
}

.card-image::before {
    filter: blur(20px) brightness(0.6);
    transform: scale(1.15);
}
```

**Efeito:** imagem inteira visível + fundo desfocado (não corta conteúdo)

---

## 3️⃣ O Problema Identificado

### Sintoma: "sedu.es.gov.br se recusou a se conectar"

Quando o usuário colava uma URL no campo `url_externa` **sem o `https://` na frente**:
- Campo: `uol.com.br` ou `sedu.es.gov.br`
- Href gerado: `href="/uol.com.br"` (navegador acha que é caminho relativo)
- Resultado: tenta abrir `http://localhost:8001/uol.com.br` → **erro "recusou"**

### Raiz do Problema

O template Django tinha:
```django
<a href="{{ item.url_externa }}">
```

E o banco guardava:
```
url_externa = 'uol.com.br'  # sem schema
```

Resultado:
```html
<a href="uol.com.br">  <!-- navegador interpreta como caminho relativo! -->
```

### Solução Implementada

Adicionada propriedade Python `link_externo` que **sempre garante um schema**:
- Se `url_externa` tiver `://`, usa como está
- Senão, adiciona `https://` na frente

Template agora usa:
```django
<a href="{{ item.link_externo }}">  <!-- sempre tem schema -->
```

---

## 4️⃣ Testes Realizados

### ✅ Teste de Propriedade (shell)
```bash
from conteudo.models import Conteudo

c = Conteudo(url_externa='uol.com.br'); print(c.link_externo)
# Output: https://uol.com.br

c = Conteudo(url_externa='https://uol.com.br'); print(c.link_externo)
# Output: https://uol.com.br

c = Conteudo(url_externa='http://uol.com.br'); print(c.link_externo)
# Output: http://uol.com.br

c = Conteudo(url_externa='  uol.com.br  '); print(c.link_externo)
# Output: https://uol.com.br

c = Conteudo(url_externa=''); print(c.link_externo)
# Output: ''
```

### ✅ Teste End-to-End (com imagem)
```bash
# Criou destaque com URL incompleta
c = Conteudo.objects.create(
    titulo='', tipo='documento', categoria=cat, 
    destaque=True, status='publicado', 
    imagem_destaque=img, url_externa='uol.com.br'
)

# Verificou no banco
print(c.url_externa)  # 'uol.com.br' (salvo como colado)
print(c.link_externo)  # 'https://uol.com.br' (renderizado com schema)
```

### ✅ Teste no Navegador (JavaScript)
```javascript
// Verificou o href gerado no HTML
const cards = [...document.querySelectorAll('.destaques-grid .content-card')];
cards.map(c => ({href: c.href, target: c.getAttribute('target')}))

// Output: href é 'https://uol.com.br/' completo ✅
```

---

## 5️⃣ Estado Final

### ✨ Funcionalidades Implementadas

| Feature | Status | Onde |
|---------|--------|------|
| Múltiplos destaques lado a lado | ✅ | home.html / CSS grid |
| Sem cortar imagens/conteúdo | ✅ | object-fit: contain + blur fundo |
| Suporta: imagem, vídeo, ícone, documento | ✅ | Conteudo.imagem_destaque / video_thumbnail_url / icone_imagem |
| URLs aberem em nova aba | ✅ | target="_blank" rel="noopener" |
| URLs sem schema funcionam | ✅ | link_externo property |
| Responsivo (1 coluna mobile) | ✅ | media queries 768px |
| Destaques sem título aparecem | ✅ | \|\|default:get_tipo_display |

### 📝 Dados de Teste Criados (Limpos)

- Criado: `test_link_real` com `url_externa='https://sedu.es.gov.br'` → funcionou ✅
- Criado: `teste_uol` com `url_externa='uol.com.br'` → corrigido e testado ✅
- Ambos removidos do banco após testes

### 🔄 Fluxo de Uso (Para o Dan)

1. **No Painel Central** (`/admin/painel-central/`):
   - Preencher "O que você vai postar?" (Documento/Vídeo/Post/Link)
   - Preencher campos relevantes (Arquivo, URL, Texto, etc.)
   - **Importante:** se marcar "Destaque", o conteúdo aparece na seção "Destaques" da home
   - Se preencher "URL do arquivo/mídia/link" (campo `url_externa`), pode colar sem `https://` — site corrige automaticamente

2. **No Admin Clássico** (`/admin/conteudo/conteudo/`):
   - Campo "URL externa" (nome técnico: `url_externa`)
   - Pode colar `uol.com.br`, `www.google.com`, ou `https://github.com` — todos funcionam
   - Site garante que o link abre na URL correta, nunca como caminho interno

3. **Resultado no Site:**
   - Destaque aparece na home na seção "Destaques"
   - Clicando, abre a URL em **nova aba** (não sai do site)
   - Múltiplos destaques ficam lado a lado (até caber)
   - Nada é cortado

---

## 6️⃣ Cache-Busting

**CSS**: `base.html` linha 23
```html
<link rel="stylesheet" href="{% static 'css/style.css' %}?v=20260712-4">
```

**Não foi alterado neste commit** (CSS já estava ok), mas mantém versão anterior. Se alterar CSS futuramente, incrementar para `-5`.

---

## 7️⃣ Próximos Passos (Se Necessário)

- [ ] Adicionar imagem de destaque (preview) aos destaques no Django Admin
- [ ] Permitir ordem manual dos destaques
- [ ] Limite máximo de destaques exibidos (ex.: 6)
- [ ] Animação de hover nos cards
- [ ] Validação de URL no admin (avisar se não tem schema e for usar link_externo)

---

## 📚 Referência Rápida

### Comando para Criar Destaque com URL

```bash
python manage.py shell

from conteudo.models import Conteudo, Categoria

cat = Categoria.objects.filter(ativa=True).first()
Conteudo.objects.create(
    titulo='Meu Destaque Externo',
    slug='meu-destaque-externo',
    tipo='link',
    categoria=cat,
    url_externa='uol.com.br',  # sem https:// — site corrige
    destaque=True,
    status='publicado'
)
```

### Debug: Verificar link_externo

```bash
c = Conteudo.objects.get(slug='meu-destaque-externo')
print(f"Salvo: {c.url_externa}")
print(f"Renderizado: {c.link_externo}")
```

---

## 🎯 Conclusão

**Problema resolvido:** URLs sem schema agora funcionam perfeitamente. A propriedade `link_externo` garante que toda URL tem um schema válido antes de ser renderizada no HTML. Aplicado em 4 templates (home destaques/recentes, categoria, busca) com padrão consistente.

**Próxima conversa:** referir-se a este arquivo para contexto completo. Se precisar de mais destaques com URLs, o código já está pronto.
