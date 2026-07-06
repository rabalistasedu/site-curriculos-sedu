# Planejamento — Novo Site Currículo SEDU/ES

## 1. Diagnóstico do site atual

Após análise do site `curriculo.sedu.es.gov.br/curriculo/`, os seguintes problemas foram identificados:

**Navegação caótica**: a página "Documentos Curriculares" exibe mais de 35 botões em formato de imagem, sem categorização, sem hierarquia visual e sem agrupamento lógico. Não existe menu textual — toda a navegação é feita clicando em banners gráficos, o que torna impossível para o usuário encontrar rapidamente o que precisa.

**Design inconsistente**: cada seção do site usa um layout diferente. Algumas páginas têm header e footer, outras não. Banners são de tamanhos variados, cores e estilos visuais distintos. Não há identidade visual unificada.

**Impossibilidade de gestão sem código**: o WordPress com Elementor exige que alguém edite visualmente cada página para adicionar conteúdo. Não há painel administrativo estruturado onde se possa postar um PDF, vídeo ou texto formatado sem mexer no layout das páginas. Para um time não-técnico da GECEB, isso é inviável.

**Problemas de acessibilidade e SEO**: o `<title>` da home contém o texto completo da descrição (300+ caracteres). Não há metatags adequadas na maioria das páginas. As imagens de navegação não possuem atributos `alt`, prejudicando leitores de tela.

**Performance**: Elementor adiciona CSS e JavaScript pesados. Páginas compostas por dezenas de imagens grandes carregam lentamente, especialmente em conexões móveis das escolas.

---

## 2. A pergunta central: trocar de tecnologia?

### Resposta curta: sim, a troca é recomendada

O WordPress/Elementor atende bem para sites simples e blogs, mas o que a GECEB precisa é um **sistema de gestão de conteúdo institucional** com painel administrativo estruturado — algo que o Elementor não oferece nativamente.

### Opções de tecnologia avaliadas

| Critério | WordPress (atual) | Django (Python) | Laravel (PHP) | Strapi (Node.js) |
|---|---|---|---|---|
| Painel admin pronto | Genérico (posts/páginas) | Excelente (Django Admin) | Requer construção | Bom (headless CMS) |
| Curva de aprendizagem para devs | Baixa | Média | Média | Média |
| Gestão sem código pelo admin | Limitada (precisa Elementor) | Nativa e customizável | Requer desenvolvimento | Boa via interface |
| Hospedagem gov.br | Fácil (PHP nativo) | Requer container/servidor | Fácil (PHP nativo) | Requer container |
| Upload de múltiplos tipos de arquivo | Via plugins | Nativo | Nativo | Nativo |
| Editor de texto rico (WYSIWYG) | Gutenberg | CKEditor/TinyMCE | CKEditor/TinyMCE | Editor próprio |
| Formatação ABNT | Via plugins instáveis | Customizável no editor | Customizável | Limitada |
| Segurança institucional | Alvo frequente de ataques | Sólida | Boa | Boa |
| Comunidade e documentação em PT-BR | Extensa | Boa | Boa | Moderada |

### Recomendação: Django (Python)

O Django é a melhor escolha por três razões fundamentais:

1. **Django Admin**: vem com um painel administrativo pronto, que pode ser customizado para permitir que a equipe da GECEB gerencie documentos, programas, olimpíadas e todo o conteúdo do site sem tocar em código. É possível criar formulários específicos para cada tipo de conteúdo.

2. **Python é a linguagem do futuro na educação**: a SEDU pode formar equipe interna com competência em Python, linguagem que também é usada em ciência de dados, automação e IA — trazendo ganho institucional além do site.

3. **Segurança e robustez**: Django é usado pelo Instagram, Mozilla, NASA e pelo próprio governo americano. Possui proteções contra SQL injection, XSS e CSRF integradas.

---

## 3. Arquitetura proposta

### Camada 1 — Frontend público (o que professores e alunos veem)

Tecnologia: **Next.js** (React) ou **templates Django** (mais simples de manter).

O site público será organizado com:

- Menu superior claro com categorias: Documentos Curriculares, Programas, Olimpíadas, Livro Didático, EJA, Educação Especial
- Subcategorias dentro de cada seção (ex.: Documentos → Ensino Fundamental, Ensino Médio, EJA)
- Busca textual com filtros por tipo de conteúdo (PDF, vídeo, orientação)
- Design responsivo (funciona em celulares e tablets)
- Cards visuais padronizados substituindo os banners de imagem atuais

### Camada 2 — Painel administrativo (o que a GECEB usa)

Tecnologia: **Django Admin** customizado.

O painel permitirá:

- Criar e editar seções/categorias do menu sem código
- Postar conteúdo com editor de texto rico (negrito, itálico, listas, tabelas — formatação ABNT)
- Fazer upload de PDFs, vídeos, planilhas Excel, documentos Word
- Incorporar vídeos do YouTube/Vimeo com campo simples de URL
- Gerenciar banners da página principal
- Controle de publicação (rascunho, publicado, arquivado)
- Prévia do conteúdo antes de publicar
- Gerenciar múltiplos usuários com permissões (editor, revisor, administrador)

### Camada 3 — Backend e banco de dados

- **Django** como framework web
- **PostgreSQL** como banco de dados (gratuito, robusto, usado pelo governo)
- **Amazon S3** ou **MinIO** para armazenamento de arquivos grandes (PDFs, vídeos)
- **Nginx** como servidor web
- **Docker** para facilitar a implantação

---

## 4. Estrutura de conteúdo proposta

Com base na análise do site atual, a seguinte reorganização é sugerida:

### Menu principal (6 itens, atualmente são ~40 botões soltos)

1. **Documentos curriculares**
   - Currículo atual (Ed. Infantil, Ens. Fundamental, Ens. Médio)
   - Currículo de Computação
   - Orientações curriculares
   - Guias de habilidades
   - Cadernos metodológicos
   - Mapas de progressão
   - Ementas curriculares
   - Histórico (Currículo 2018, Currículo 2009)

2. **Programas**
   - Matemática na Rede
   - Educar para a Paz
   - Música na Rede
   - Mais Leitores
   - Educação Ambiental
   - Sucesso Escolar
   - GEEPEI / PROETI / PIPAT

3. **Livro didático e materiais**
   - PNLD
   - Catálogo de livros
   - Práticas experimentais
   - Sequências didáticas
   - Materiais de apoio (Ensino Médio)

4. **Modalidades e diversidade**
   - EJA (documentos, orientações, cadernos de práticas, planos de curso)
   - Educação do campo
   - Educação escolar indígena
   - Educação escolar quilombola
   - Relações étnico-raciais
   - Socioeducação
   - Educação integral em tempo integral

5. **Olimpíadas e competições**
   - Lista de olimpíadas por área
   - Calendário de inscrições
   - Resultados e premiações

6. **Institucional**
   - Sobre a GECEB
   - Contato
   - Notícias e informes
   - Revista Diálogos

---

## 5. O que o painel administrativo permitirá fazer (sem código)

### Cenário 1 — Postar um novo PDF
O gestor acessa o painel → clica em "Novo documento" → seleciona a categoria (ex.: Guias de habilidades) → preenche título e descrição → faz upload do PDF → clica em "Publicar". O documento aparece automaticamente na seção correta do site.

### Cenário 2 — Adicionar um vídeo
O gestor acessa "Novo conteúdo" → seleciona tipo "Vídeo" → cola o link do YouTube → escreve título e descrição → seleciona a categoria → publica. O vídeo é embutido automaticamente com player responsivo.

### Cenário 3 — Publicar um texto com formatação ABNT
O gestor acessa "Novo post" → usa o editor WYSIWYG que já possui estilos ABNT configurados (fonte Times New Roman 12pt, espaçamento 1.5, recuo de parágrafo, referências formatadas) → pode colar texto do Word mantendo a formatação → publica.

### Cenário 4 — Reorganizar o menu
O gestor acessa "Menus" → arrasta os itens para reordenar → cria novas subcategorias → salva. O menu do site atualiza automaticamente.

### Cenário 5 — Subir planilha Excel ou documento Word
O gestor acessa "Novo arquivo" → faz upload do .xlsx ou .docx → o sistema gera automaticamente um link de download e uma pré-visualização inline no site.

---

## 6. Cronograma sugerido

### Fase 1 — Fundação (4-6 semanas)
- Configurar ambiente Django + PostgreSQL
- Modelar banco de dados (categorias, documentos, programas, olimpíadas)
- Implementar Django Admin customizado com upload de arquivos
- Criar editor WYSIWYG com template ABNT

### Fase 2 — Frontend (4-6 semanas)
- Desenvolver design system (cores, tipografia, componentes)
- Implementar páginas: home, documentos, programas, olimpíadas
- Busca textual com filtros
- Design responsivo (mobile-first)

### Fase 3 — Migração (2-3 semanas)
- Migrar todo o conteúdo do WordPress atual
- Importar PDFs, imagens e links existentes
- Configurar redirecionamentos de URLs antigas

### Fase 4 — Testes e ajustes (2 semanas)
- Testes com usuários da GECEB (usabilidade do painel)
- Testes com professores (navegação do site público)
- Ajustes de acessibilidade (WCAG 2.1)
- Otimização de performance

### Fase 5 — Lançamento (1 semana)
- Deploy no servidor da SEDU
- Treinamento da equipe GECEB no painel admin
- Documentação de uso
- Monitoramento pós-lançamento

**Prazo total estimado: 13-18 semanas** (3-4 meses)

---

## 7. Alternativa mais simples: WordPress refeito

Se a equipe não dispuser de desenvolvedores Python, uma alternativa intermediária seria:

- Manter WordPress, mas substituir o Elementor por um tema profissional com ACF (Advanced Custom Fields)
- Criar Custom Post Types para cada tipo de conteúdo (documentos, programas, olimpíadas)
- Instalar plugin de upload de arquivos e organização por categorias
- Redesenhar a navegação com menu hierárquico textual

Essa opção é mais rápida (4-6 semanas), mas tem limitações: menos flexibilidade no painel admin, dependência de plugins de terceiros, e os problemas de segurança e performance do WordPress permanecem.

---

## 8. Custos estimados

| Item | Django | WordPress refeito |
|---|---|---|
| Desenvolvimento | R$ 30.000 - 50.000 | R$ 15.000 - 25.000 |
| Servidor (anual) | R$ 2.400 - 4.800 | R$ 1.200 - 2.400 |
| Manutenção mensal | R$ 1.500 - 3.000 | R$ 800 - 1.500 |
| Treinamento equipe | R$ 2.000 - 5.000 | R$ 1.000 - 2.000 |

Valores aproximados para o mercado brasileiro em 2026. Se a SEDU possui equipe de TI interna, os custos de desenvolvimento podem ser significativamente menores.

---

## 9. Próximos passos recomendados

1. **Decisão de tecnologia**: Django (recomendado) ou WordPress refeito?
2. **Levantamento de infraestrutura**: qual servidor a SEDU possui? Suporta Docker/Python?
3. **Definição de equipe**: a SEDU tem desenvolvedores Python ou precisará contratar?
4. **Priorização de conteúdo**: quais seções são mais acessadas e devem ser migradas primeiro?
5. **Prototipação**: criar wireframes do novo design para aprovação antes de codificar

---

*Documento elaborado em 04/07/2026 — Planejamento para análise da GECEB/SEDU-ES*
