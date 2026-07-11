=== TEXTO 1 ===

# PAINEL CENTRAL ADMINISTRATIVO DO SITE

> Documento Mestre da Nova Arquitetura Administrativa

\---

## Projeto

Site Currículos SEDU

\---

## Versão

1.0

\---

## Objetivo deste documento

Este documento representa a especificação oficial da nova arquitetura administrativa do Site Currículos SEDU.

Este documento deverá servir como referência principal durante toda a implementação do novo painel administrativo.

Toda decisão técnica deverá seguir prioritariamente este documento.

Caso exista conflito entre este documento e qualquer interpretação do Claude Code, deverá prevalecer sempre o que está definido neste documento.

\---

# IMPORTANTE

Este documento NÃO é apenas um prompt.

Este documento representa uma especificação técnica completa da arquitetura do novo sistema administrativo.

Todo o desenvolvimento deverá seguir exatamente esta especificação.

Caso exista qualquer dúvida durante qualquer etapa da implementação, o desenvolvimento deverá ser interrompido até que a dúvida seja esclarecida.

O sistema nunca deverá assumir comportamentos não especificados.

Nunca implementar funcionalidades utilizando interpretação própria.

Sempre perguntar.

\---

# FILOSOFIA DO PROJETO

O Site Currículos SEDU já possui um painel administrativo funcional.

Este projeto NÃO pretende substituir o painel existente.

Também NÃO pretende alterar seu funcionamento.

O objetivo é transformar o painel atual em uma plataforma administrativa muito mais poderosa, capaz de administrar praticamente todo o conteúdo do site através de novos módulos independentes.

O novo sistema deverá coexistir com o sistema atual.

Todo código existente deverá permanecer preservado.

A evolução do projeto deverá ocorrer sempre por expansão da arquitetura existente e nunca por substituição.

\---

# PRINCÍPIO MAIS IMPORTANTE

## O PAINEL ADMINISTRATIVO ATUAL É INTOCÁVEL.

Isso significa:

* não remover telas
* não remover menus
* não remover funcionalidades
* não alterar URLs existentes
* não alterar rotinas existentes
* não alterar permissões existentes
* não modificar fluxos existentes
* não alterar templates existentes sem necessidade

Todo novo recurso deverá ser criado através de novos componentes.

Sempre adicionar.

Nunca substituir.

\---

# OBJETIVO GERAL

Criar um novo módulo administrativo capaz de controlar completamente:

* botões
* subbotões
* subáreas
* categorias
* conteúdos
* anexos
* imagens
* links
* páginas
* destaques
* conteúdos recentes
* ordem de exibição
* publicação
* agendamento

Tudo isso através de um único painel centralizado.

\---

# \# VISÃO DO PAINEL CENTRAL ADMINISTRATIVO

# 

# O Painel Central Administrativo será concebido desde sua primeira implementação como a plataforma central de gerenciamento de conteúdo do site.

# 

# Embora o desenvolvimento ocorra de forma incremental, a arquitetura deverá contemplar, desde já, os módulos responsáveis por administrar:

# 

# \- notícias

# \- eventos

# \- comunicados

# \- banners

# \- galerias

# \- vídeos

# \- formulários

# \- páginas completas

# \- menus

# \- rodapé

# \- áreas institucionais

# \- documentos

# \- legislação

# \- currículo

# \- downloads

# \- links rápidos

# 

# Esses módulos deverão fazer parte da arquitetura oficial do Painel Central Administrativo e compartilhar os mesmos princípios de modularidade, reutilização de conteúdo, permissões, versionamento, auditoria e gerenciamento centralizado.

# 

# A implementação poderá ocorrer em fases, porém a arquitetura deverá ser planejada para suportar todos esses módulos desde o início, evitando retrabalho e garantindo consistência entre eles.

# 

# Todo o sistema deverá ser modular, desacoplado e preparado para crescimento contínuo.



Todo o sistema deverá ser modular.

\---

# REGRAS ABSOLUTAS

Estas regras possuem prioridade máxima.

## REGRA 01

Nunca remover funcionalidades existentes.

\---

## REGRA 02

Nunca alterar comportamento existente sem autorização.

\---

## REGRA 03

Sempre criar novos módulos independentes.

\---

## REGRA 04

Todo código novo deverá seguir exatamente o padrão arquitetural já utilizado no projeto.

\---

## REGRA 05

Caso exista necessidade de modificar alguma estrutura existente, primeiro apresentar a justificativa e aguardar aprovação.

\---

## REGRA 06

Antes de iniciar qualquer implementação deverá ser apresentado um plano completo contendo:

* arquivos novos
* arquivos modificados
* migrations
* models
* views
* templates
* urls
* javascript
* css
* impacto esperado

Somente após aprovação iniciar a implementação.

\---

## REGRA 07

A implementação deverá ocorrer em pequenas etapas.

Cada etapa deverá ser concluída.

Testada.

Validada.

Somente depois iniciar a próxima.

\---

## REGRA 08

Nunca implementar duas grandes funcionalidades simultaneamente.

Cada funcionalidade deverá possuir começo, meio e fim.

\---

# ESTADO ATUAL DO PROJETO

Antes de iniciar qualquer desenvolvimento o Claude Code deverá realizar uma leitura completa do projeto.

A leitura deverá incluir:

* CLAUDE.md
* README.md
* documentação existente
* estrutura de pastas
* models
* migrations
* templates
* views
* javascript
* css
* urls
* configuração
* banco de dados
* estrutura administrativa

O objetivo é compreender completamente a arquitetura atual.

Nenhuma implementação deverá ser iniciada antes dessa leitura.

\---

# MISSÃO DO NOVO PAINEL

O novo painel administrativo deverá tornar possível que praticamente qualquer conteúdo do site possa ser administrado sem necessidade de alterar código.

O administrador deverá conseguir:

criar

editar

publicar

agendar

remover

organizar

mover

duplicar

reutilizar

qualquer conteúdo.

O sistema deverá ser intuitivo.

Organizado.

Escalável.

E preparado para muitos anos de evolução.

\---

# NOVO MÓDULO ADMINISTRATIVO

Será criado um novo módulo administrativo chamado:

# \# PAINEL CENTRAL ADMINISTRATIVO

# 

# Dentro deste módulo existirão diversos gerenciadores independentes.

# 

# O primeiro gerenciador será:

# 

# \## GERENCIADOR DE BOTÕES E CONTEÚDOS

# 

# A arquitetura do Painel Central Administrativo deverá ser modular, permitindo a criação e integração de novos gerenciadores conforme a evolução das necessidades do sistema, sem impacto na estrutura existente.

\---

# CONCEITO DO GERENCIADOR

O Gerenciador de Botões e Conteúdos será responsável por controlar todos os locais onde conteúdos podem ser publicados.

Ele funcionará como um grande distribuidor de conteúdos.

O administrador primeiro escolhe ONDE deseja publicar.

Depois escolhe O QUE deseja publicar.

Depois define COMO será publicado.

Por fim salva.

Todo o restante deverá ocorrer automaticamente.

\---

# FLUXO GERAL

O funcionamento sempre seguirá esta sequência.

PASSO 1

Selecionar categoria.

↓

PASSO 2

Selecionar botão.

↓

PASSO 3

Selecionar subbotão.

↓

PASSO 4

Selecionar subárea.

↓

PASSO 5

Adicionar conteúdo.

↓

PASSO 6

Adicionar anexos.

↓

PASSO 7

Definir aparência.

↓

PASSO 8

Definir publicação.

↓

PASSO 9

Salvar.

↓

PASSO 10

Sistema publica automaticamente nos locais selecionados.

\---

# \# PRINCÍPIO DE FUNCIONAMENTO

# 

# O conteúdo nunca deverá conhecer onde será publicado.

# 

# A responsabilidade pela publicação será exclusivamente do vínculo criado entre o conteúdo e os nós da árvore hierárquica durante a seleção dos elementos da interface administrativa.

# 

# Essa arquitetura deverá permitir que um mesmo conteúdo seja reutilizado simultaneamente em diferentes locais do site, sem duplicação de informações.

# 

# A separação entre conteúdo e publicação constitui um princípio fundamental do Painel Central Administrativo e deverá ser implementada desde esta versão do sistema, servindo como base para todos os módulos administrativos e funcionalidades da plataforma.

# 

# Toda nova funcionalidade deverá reutilizar esse modelo arquitetural, preservando a independência entre conteúdo, navegação e publicação.

\---

# FIM DA PARTE 1

Na Parte 2 será definida toda a arquitetura do novo módulo:

* categorias
* botões
* subbotões
* subáreas
* árvore hierárquica
* relacionamentos
* regras de criação
* organização automática
* estrutura visual do painel
* comportamento dos checkboxes
* sincronização entre interface e banco de dados
=== TEXTO 2 ===

# PARTE 2 — ARQUITETURA DO NOVO PAINEL ADMINISTRATIVO

\---

# OBJETIVO DESTA ETAPA

Esta etapa define toda a arquitetura funcional do novo Painel Central Administrativo.

O objetivo é permitir que qualquer conteúdo do site possa ser administrado através de uma única interface administrativa moderna, organizada e escalável.

Este painel será totalmente independente do painel existente.

Nenhuma funcionalidade atualmente utilizada pelos administradores poderá ser removida.

Todo o novo sistema deverá coexistir com o sistema atual.

\---

# NOVO MENU ADMINISTRATIVO

Criar um novo botão no menu administrativo.

Nome:

**PAINEL CENTRAL ADMINISTRATIVO**

Este botão deverá aparecer abaixo do botão:

Adicionar Arquivos

Ao acessar este novo módulo o usuário visualizará uma página inicial contendo todos os gerenciadores existentes.

Inicialmente existirão dois módulos.

## Módulo 1

GERENCIADOR DE BOTÕES E CONTEÚDOS

Responsável por criar, organizar e distribuir conteúdos dentro do site.

## Módulo 2

\# GERENCIADOR DE CONTEÚDOS



Responsável por visualizar e administrar todos os conteúdos cadastrados no sistema, independentemente do local onde estejam publicados.



A arquitetura deverá permitir a inclusão de novos módulos e funcionalidades de forma independente, sem necessidade de alteração dos módulos existentes.



\---

# PRINCÍPIO DA ARQUITETURA

Toda a arquitetura deverá seguir um modelo hierárquico.

A hierarquia será composta por quatro níveis.

Categoria

↓

Botão Principal

↓

Subbotão

↓

Subárea

Esta estrutura deverá ser ilimitada.



Uma categoria poderá possuir qualquer quantidade de botões.

Um botão poderá possuir qualquer quantidade de subbotões.

Um subbotão poderá possuir qualquer quantidade de subáreas.



A arquitetura deverá permitir a criação de novos níveis hierárquicos sem necessidade de alteração na estrutura de dados existente.

\---

# DEFINIÇÃO DOS ELEMENTOS

## Categoria

Representa um agrupador lógico.

Ela organiza visualmente os botões.

Exemplos:

* Home
* Conteúdos Recentes
* Navegue por Área
* Currículo Atual
* Rodapé

A categoria não publica conteúdo.

Ela apenas organiza.

\---

## Botão Principal

É o primeiro elemento clicável do site.

Pode conter:

* conteúdos
* anexos
* imagens
* links
* textos
* posts
* arquivos
* subbotões

Um botão principal poderá existir sozinho.

Ou poderá possuir diversos subbotões.

\---

## Subbotão

Representa um botão localizado dentro do botão principal.

Seu comportamento será exatamente igual ao botão principal.

Também poderá possuir:

* conteúdos
* anexos
* imagens
* links
* arquivos
* subáreas

Não existirão limitações artificiais.

\---

## Subárea

Representa o último nível da estrutura.

Também poderá conter exatamente os mesmos recursos disponíveis para os botões.

O objetivo é manter consistência em toda a arquitetura.

\---

# PRINCÍPIO DA HERANÇA

Todos os níveis deverão compartilhar os mesmos recursos.

Ou seja:

Categoria

não recebe conteúdo.

Botão Principal

recebe tudo.

Subbotão

recebe exatamente tudo.

Subárea

recebe exatamente tudo.

Isso evita regras diferentes para cada nível.

\---

# IDENTIFICAÇÃO AUTOMÁTICA

Ao abrir o Gerenciador de Botões e Conteúdos o sistema deverá realizar uma leitura automática da estrutura existente.

O objetivo é localizar todos os botões atualmente cadastrados.

Esses botões deverão ser organizados automaticamente dentro de suas respectivas categorias.

Nenhum cadastro manual será necessário para os botões já existentes.

O administrador visualizará imediatamente toda a estrutura atual do site.

\---

# ÁRVORE DE NAVEGAÇÃO

Todos os botões deverão ser exibidos em formato hierárquico.

Exemplo:

📂 Home

☐ Documentos Curriculares

☐ Olimpíadas

☐ Avaliações

☐ Projetos

📂 Conteúdos Recentes

☐ Notícias

☐ Comunicados

☐ Eventos

📂 Currículo Atual

☐ Ensino Fundamental

☐ Ensino Médio

📂 Rodapé

☐ Contato

☐ Downloads

Quando um botão possuir subbotões deverá existir um ícone de expansão.

Exemplo:

▶ Ensino Fundamental

Ao expandir:

▼ Ensino Fundamental

☐ Matemática

☐ Ciências

☐ História

Caso algum subbotão possua subáreas:

▶ Matemática

↓

▼ Matemática

☐ Material do Professor

☐ Material do Estudante

☐ Avaliações

Toda a estrutura deverá ser navegável.

\---

# SISTEMA DE CHECKBOXES

Cada elemento deverá possuir um checkbox.

Ao selecionar um checkbox significa que aquele elemento será um destino para publicação.

Exemplo.

☐ Ensino Fundamental

↓

Selecionado

☑ Ensino Fundamental

Agora todo conteúdo configurado do lado direito será aplicado neste botão.

Caso vários checkboxes estejam selecionados o conteúdo será publicado em todos eles simultaneamente.

\---

# COMPORTAMENTO DOS CHECKBOXES

Os checkboxes deverão funcionar de forma inteligente.

Caso o administrador selecione uma Categoria inteira:

Todos os botões pertencentes à categoria deverão ser automaticamente selecionados.

Caso desmarque a categoria:

Todos deverão ser desmarcados.

Caso selecione apenas alguns botões:

A categoria deverá indicar estado parcial.

Este comportamento deverá seguir o padrão utilizado em exploradores de arquivos.

\---

# CRIAÇÃO DE NOVOS ELEMENTOS

Dentro de cada categoria deverá existir um botão:

➕

Adicionar Botão

Ao clicar será possível criar um novo botão principal.

Dentro de cada botão deverá existir:

➕

Adicionar Subbotão

Dentro de cada subbotão:

➕

Adicionar Subárea

Todo o processo deverá ocorrer sem necessidade de alterar código.

\---

# NOVA CATEGORIA

Também deverá existir um botão global.

Nova Categoria

Ao criar uma categoria será possível definir:

Nome

Descrição

Página onde será exibida

Posição

Ícone

Cor

Status

Visibilidade

Permissões

Após criada a categoria poderá receber novos botões.

\---

# REGRAS DE ORDENAÇÃO

Toda a estrutura deverá possuir ordenação manual.

A ordem deverá ser respeitada rigorosamente.

Sempre:

esquerda → direita

cima → baixo

Sempre que um novo botão for criado ele será colocado ao final da lista.

Posteriormente o administrador poderá reorganizar.

\---

# DRAG AND DROP

Sempre que possível utilizar arrastar e soltar.

O administrador poderá reorganizar:

Categorias

Botões

Subbotões

Subáreas

A nova posição deverá ser salva automaticamente após confirmação.

Caso o navegador não suporte drag and drop deverá existir ordenação numérica manual.

\---

# PESQUISA

Acima da árvore deverá existir uma pesquisa rápida.

Ela deverá localizar instantaneamente:

Categorias

Botões

Subbotões

Subáreas

Conteúdos associados

Sem necessidade de recarregar a página.

\---

# FILTROS

Também deverão existir filtros.

Exemplos:

Mostrar somente publicados

Mostrar somente rascunhos

Mostrar somente agendados

Mostrar ocultos

Mostrar sem conteúdo

Mostrar com anexos

Mostrar por categoria

Mostrar por página

Mostrar por responsável

\---

# \# EVOLUÇÃO DA ESTRUTURA

# 

# Toda esta estrutura deverá ser projetada para permitir novos níveis hierárquicos e novos tipos de elementos sem alteração da arquitetura existente.

# 

# Nenhuma decisão arquitetural deverá limitar a evolução, manutenção ou expansão do sistema.

# 

# O objetivo é que este módulo possua capacidade de crescimento contínuo, mantendo estabilidade, organização e compatibilidade ao longo de todo o ciclo de vida do projeto.

\---

# CRITÉRIOS DE ACEITAÇÃO DA ETAPA

Esta etapa será considerada concluída quando:

* O novo menu administrativo estiver criado.
* A árvore hierárquica estiver funcional.
* As categorias forem identificadas automaticamente.
* Os botões forem organizados corretamente.
* Os subbotões puderem ser expandidos.
* As subáreas puderem ser exibidas.
* Os checkboxes funcionarem corretamente.
* A pesquisa localizar elementos.
* Os filtros funcionarem.
* A ordenação estiver operacional.
* A criação de novos elementos estiver disponível.

\---

# FIM DA PARTE 2

Na Parte 3 será especificado todo o sistema de conteúdos, anexos, publicações, URLs amigáveis, imagens, arquivos, posts, agendamento e distribuição automática de conteúdos para os botões selecionados.
=== TEXTO 3 ===

# PARTE 3 — GERENCIADOR DE CONTEÚDOS

\---

# OBJETIVO

Esta etapa define todo o funcionamento do sistema de gerenciamento de conteúdos.

O objetivo é permitir que qualquer informação publicada no site possa ser criada, editada, organizada, reutilizada e distribuída através de um único painel administrativo.

Este módulo deverá ser totalmente independente da estrutura onde o conteúdo será exibido.

O conteúdo será uma entidade própria.

A publicação será realizada através de vínculos.

\---

# \# PRINCÍPIO FUNDAMENTAL

# 

# O conteúdo nunca deverá pertencer diretamente a um botão, subbotão, subárea ou qualquer outro elemento da navegação.

# 

# O conteúdo deverá existir como uma entidade independente dentro do sistema.

# 

# Sua publicação será realizada exclusivamente por meio de vínculos com os nós da árvore hierárquica.

# 

# Nesta implementação, um conteúdo poderá ser vinculado a:

# 

# \* Botões;

# \* Subbotões;

# \* Subáreas;

# \* Categorias, quando permitido pelas regras de negócio definidas para o módulo.

# 

# Esse modelo deverá ser implementado desde a primeira versão do Painel Central Administrativo e constituirá a base arquitetural para todo o gerenciamento de conteúdos.

# 

# Essa arquitetura permitirá a reutilização de um mesmo conteúdo em múltiplos locais do site, sem duplicação física de dados.

# 

# Exemplo:

# 

# O mesmo PDF poderá ser publicado simultaneamente em:

# 

# \* Ensino Fundamental;

# \* Formação de Professores;

# \* Página Inicial;

# \* Downloads;

# \* Biblioteca de Documentos.

# 

# Todos esses locais compartilharão o mesmo conteúdo original, preservando uma única fonte de dados e garantindo consistência, reutilização e facilidade de manutenção.

\---

# NOVO MENU

Dentro do Painel Central Administrativo deverá existir um novo módulo.

Nome:

GERENCIADOR DE CONTEÚDOS

Este módulo será responsável por administrar todos os conteúdos existentes no sistema.

Independentemente de onde estejam publicados.

\---

# TELA PRINCIPAL

Ao abrir o Gerenciador de Conteúdos deverá ser exibida uma tabela contendo todos os conteúdos cadastrados.

Cada linha representará um conteúdo.

Exemplo de colunas:

☐

Título

Tipo

Categoria

Quantidade de vínculos

Status

Autor

Última atualização

Data de criação

Ações

\---

# OPERAÇÕES DISPONÍVEIS

Cada conteúdo poderá possuir:

Visualizar

Editar

Duplicar

Mover

Publicar

Despublicar

Arquivar

Excluir

Remover vínculos

Criar vínculo

Histórico

Versões

Pré-visualizar

\---

# SELEÇÃO MÚLTIPLA

A listagem deverá permitir:

Selecionar individualmente.

Selecionar todos.

Selecionar por filtro.

Selecionar página atual.

Selecionar todos os resultados encontrados.

Após selecionar deverão aparecer ações em lote.

\---

# AÇÕES EM LOTE

Publicar

Despublicar

Arquivar

Excluir

Mover

Duplicar

Adicionar vínculo

Remover vínculo

Alterar categoria

Alterar autor

Alterar ordem

Exportar

\---

# CADASTRO DE CONTEÚDO

Ao clicar em:

Novo Conteúdo

Será aberta uma tela contendo todos os recursos disponíveis.

Todos os campos deverão ser opcionais.

\---

# CAMPOS BÁSICOS

Título

Subtítulo

Resumo

Descrição

Texto completo

Observações internas

Palavras-chave

Tags

Código interno

Slug

\---

# CAMPOS DE APRESENTAÇÃO

Imagem Principal

Imagem Secundária

Galeria

Miniatura

Ícone

Cor

Fonte

Tamanho da fonte

Alinhamento

Tema visual

Aparência automática

Aparência personalizada

\---

# LINKS

Cada conteúdo poderá possuir:

URL

URL amigável

Nome amigável

Link externo

Abrir em nova janela

Link interno

Link para download

Link para outro conteúdo

Não haverá limite para quantidade de links associados.

\---

# SISTEMA DE ANEXOS

Cada conteúdo poderá possuir quantidade ilimitada de anexos.

Cada anexo será independente.

O administrador poderá:

Adicionar

Editar

Remover

Duplicar

Mover

Reordenar

Renomear

Substituir

Visualizar

Baixar

\---

# FORMATOS SUPORTADOS

O sistema deverá aceitar todos os formatos já suportados atualmente pelo site.

Exemplos:

PDF

DOC

DOCX

XLS

XLSX

PPT

PPTX

TXT

CSV

ZIP

RAR

7Z

PNG

JPG

JPEG

GIF

WEBP

SVG

MP4

MP3

WAV

ODT

ODS

ODP

e qualquer outro formato permitido pela configuração existente.

\---

# ORGANIZAÇÃO DOS ANEXOS

Cada anexo deverá possuir:

Nome amigável

Descrição

Tipo

Ordem

Data

Responsável

Versão

Status

\---

# ORDENAÇÃO

Os anexos poderão ser reorganizados.

Preferencialmente utilizando Drag and Drop.

Caso não seja possível deverá existir ordenação numérica.

\---

# VISUALIZAÇÃO

Cada anexo deverá possuir:

Visualizar

Baixar

Editar

Excluir

Substituir arquivo

Alterar nome

Alterar ordem

\---

# SISTEMA DE PUBLICAÇÃO

Cada conteúdo poderá possuir:

Rascunho

Publicado

Agendado

Arquivado

Expirado

\---

# PUBLICAÇÃO IMEDIATA

Caso o administrador escolha:

Status

Publicado

e

Data esteja vazia

A publicação ocorrerá imediatamente.

\---

# AGENDAMENTO

Caso exista:

Data

Hora

O conteúdo somente será publicado quando chegar o momento definido.

\---

# EXPIRAÇÃO

Opcionalmente o conteúdo poderá possuir:

Data Final

Hora Final

Ao atingir esta data o sistema deverá:

Despublicar automaticamente.

\---

# DESTAQUES

Cada conteúdo poderá receber:

Destaque Home

Conteúdo Recente

Em destaque

Fixado

Urgente

Botão Pulsante

Botão Vibrante

Novo

Atualizado

Cada opção deverá funcionar de forma independente.

\---

# PRÉ-VISUALIZAÇÃO

Antes de salvar o administrador poderá visualizar como o conteúdo ficará.

A pré-visualização deverá respeitar:

Imagens

Textos

Botões

Ícones

Arquivos

Links

Formatação

\---

# HISTÓRICO

Todo conteúdo deverá manter histórico completo.

Registrar:

Quem criou.

Quem editou.

Quando editou.

O que foi alterado.

Endereço IP (quando disponível).

\---

# VERSIONAMENTO

Toda alteração importante deverá gerar uma nova versão.

O administrador poderá:

Comparar versões.

Visualizar diferenças.

Restaurar versões anteriores.

Duplicar versões.

\---

# LIXEIRA

Conteúdos excluídos deverão ser enviados para uma lixeira.

Não deverão ser apagados imediatamente.

A exclusão definitiva somente ocorrerá após confirmação administrativa.

\---

# REMOÇÃO DE VÍNCULOS

Remover um vínculo nunca deverá excluir o conteúdo.

Apenas interromper sua exibição naquele local.

Os demais vínculos deverão permanecer funcionando.

\---

# DUPLICAÇÃO

Ao duplicar um conteúdo deverão ser copiados:

Texto

Imagens

Arquivos

Configurações

Links

Metadados

Não copiar:

Histórico

Logs

Datas de publicação anteriores

\---

# BUSCA

A pesquisa deverá localizar por:

Título

Resumo

Texto

Tags

Autor

Categoria

Nome do arquivo

Nome amigável

Palavras-chave

Código interno

\---

# FILTROS

Publicado

Rascunho

Arquivado

Agendado

Com anexos

Sem anexos

Com imagem

Sem imagem

Autor

Data

Categoria

Quantidade de vínculos

\---

# OBJETIVO FINAL

Este módulo deverá transformar o conteúdo em uma entidade independente.



Os locais onde ele será exibido deverão ser tratados apenas como vínculos de relacionamento.



Esta arquitetura permitirá:



\* Reutilização;

\* Versionamento;

\* Escalabilidade;

\* Maior organização;

\* Facilidade de manutenção;

\* Evolução e expansão contínua;

\* Sem duplicação de informações.

\---

# CRITÉRIOS DE ACEITAÇÃO

Esta etapa será considerada concluída quando:

✓ O Gerenciador de Conteúdos estiver funcional.

✓ O cadastro de conteúdos estiver completo.

✓ Os anexos puderem ser gerenciados.

✓ O sistema de publicação funcionar.

✓ O agendamento funcionar.

✓ O versionamento estiver operacional.

✓ A lixeira funcionar.

✓ Os vínculos puderem ser criados e removidos.

✓ O histórico registrar alterações.

✓ Os filtros funcionarem.

✓ A pesquisa localizar conteúdos.

\---

# FIM DA PARTE 3

Na Parte 4 será definida toda a arquitetura do banco de dados.



Em vez de limitar a estrutura aos níveis Categoria → Botão → Subbotão → Subárea, será adotado um modelo baseado em árvore hierárquica (Tree Structure), preparado para crescimento ilimitado, inclusão de novos níveis e evolução contínua da estrutura, preservando a interface administrativa especificada neste documento.



=== TEXTO 4 ===

# PARTE 4 — ARQUITETURA DO BANCO DE DADOS

\---

# OBJETIVO

Esta etapa define toda a arquitetura de dados do Painel Central Administrativo.

O objetivo desta arquitetura é permitir crescimento ilimitado do sistema sem necessidade de modificar sua estrutura.

Toda a modelagem deverá ser preparada para suportar novas funcionalidades durante muitos anos.

O princípio principal será:

"Nunca limitar o sistema pela estrutura do banco."

\---

# \# PRINCÍPIO DA MODELAGEM

# 

# Embora o administrador visualize a estrutura como:

# 

# Categoria

# ↓

# Botão

# ↓

# Subbotão

# ↓

# Subárea

# 

# internamente o sistema não deverá possuir tabelas separadas para cada um desses elementos.

# 

# Toda a hierarquia deverá ser representada por uma única estrutura em árvore, composta por nós hierárquicos.

# 

# Cada nó deverá conhecer apenas seu elemento pai, permitindo que a hierarquia seja construída de forma dinâmica e independente do nível em que o elemento esteja localizado.

# 

# Essa modelagem deverá ser implementada desde a primeira versão do Painel Central Administrativo e constituirá a base estrutural de toda a navegação administrativa.

# 

# A arquitetura deverá suportar qualquer quantidade de níveis hierárquicos, sem necessidade de alterações no banco de dados, na modelagem ou na lógica da aplicação.

# 

# Toda a interface administrativa deverá utilizar essa mesma estrutura hierárquica para criação, edição, organização, movimentação e publicação dos conteúdos.

\---

# MODELO CONCEITUAL

Estrutura lógica.

```text

ROOT
│
├── Home
│     ├── Documentos Curriculares
│     │        ├── Ensino Fundamental
│     │        │        ├── Matemática
│     │        │        ├── Ciências
│     │        │        └── História
│     │        │
│     │        └── Ensino Médio
│     │
│     └── Olimpíadas
│
├── Conteúdos Recentes
│
├── Currículo Atual
│
└── Rodapé

```

Observe que todos são apenas nós.

A diferença entre eles será apenas o tipo.

\---

# TABELA PRINCIPAL

Criar uma tabela responsável por representar toda a árvore.

Nome sugerido:

SiteNode

\---

Campos.

id

uuid

parent\_id

tipo

titulo

slug

descricao

icone

cor

ordem

status

visivel

publicado

pagina

created\_at

updated\_at

deleted\_at

\---

# SIGNIFICADO DOS CAMPOS

\### id



Identificador interno do registro.



\---



\### uuid



Identificador único global do registro.



Utilizado para referências externas, integrações, sincronizações e comunicação entre diferentes componentes do ecossistema do projeto.

\---

parent\_id

Define quem é o pai deste elemento.

Se for NULL significa que está na raiz.

\---

tipo

Determina qual elemento será exibido.

Valores iniciais.

Categoria

Botão

Subbotão

Subárea

Página

Banner

Galeria

Evento

Notícia

Sem necessidade de alterar estrutura.

\---

titulo

Nome apresentado ao usuário.

\---

slug

URL amigável.

\---

descricao

Descrição administrativa.

\---

icone

Ícone personalizado.

\---

cor

Cor personalizada.

\---

ordem

Posição de exibição.

\---

status

Rascunho

Publicado

Arquivado

Agendado

Oculto

\---

visivel

Boolean.

\---

pagina

Em qual página será exibido.

\---

# ÁRVORE

Cada registro conhece apenas seu pai.

Exemplo.

```text

id = 1

Home

parent = NULL

↓

id = 2

Documentos Curriculares

parent = 1

↓

id = 3

Ensino Fundamental

parent = 2

↓

id = 4

Matemática

parent = 3

```

O sistema reconstruirá automaticamente toda a árvore.

\---

# VANTAGENS

Não existe limite de níveis.

Não existe necessidade de novas tabelas.

Arquitetura extremamente simples.

Consultas rápidas.

Manutenção reduzida.

Escalabilidade praticamente ilimitada.

\---

# TABELA CONTENT

Todo conteúdo deverá existir independentemente.

Nome sugerido.

Content

Campos.

id

uuid

titulo

subtitulo

descricao

texto

slug

status

autor

created\_at

updated\_at

deleted\_at

\---

# IMPORTANTE

Content NÃO pertence a SiteNode.

Content existe sozinho.

\---

# RELACIONAMENTO

A publicação será feita através de uma terceira tabela.

\---

Tabela.

NodeContent

\---

Campos.

id

node\_id

content\_id

ordem

destaque\_home

conteudo\_recente

pulsante

vibrante

publicar\_em

expirar\_em

created\_at

\---

Esta tabela representa somente o vínculo.

\---

# VANTAGEM

O mesmo conteúdo poderá estar ligado a:

Home

Currículo

Rodapé

Página Inicial

Downloads

Tudo ao mesmo tempo.

Sem duplicação.

\---

# TABELA FILE

Arquivos também serão independentes.

Nome.

ContentFile

Campos.

id

content\_id

arquivo

nome

descricao

tipo

ordem

created\_at

\---

Cada conteúdo poderá possuir qualquer quantidade de arquivos.

\---

# TABELA IMAGE

Imagens serão independentes.

Campos.

id

content\_id

arquivo

titulo

descricao

miniatura

ordem

\---

# TABELA LINKS

Links externos.

Campos.

id

content\_id

titulo

url

nome\_amigavel

nova\_janela

ordem

\---

# TABELA TAGS

Permitir classificação.

Tag

id

nome

slug

cor

\---

# RELACIONAMENTO

ContentTag

content\_id

tag\_id

\---

# HISTÓRICO

Criar tabela.

ContentHistory

Registrar.

Quem alterou.

Quando.

Qual campo.

Valor antigo.

Valor novo.

IP.

Navegador.

\---

# VERSIONAMENTO

Tabela.

ContentVersion

Cada salvamento importante poderá gerar uma nova versão.

Permitindo restaurar.

\---

# LIXEIRA

Nunca excluir imediatamente.

Utilizar Soft Delete.

deleted\_at

Toda exclusão será reversível.

\---

# AUDITORIA

Criar tabela.

AuditLog

Registrar.

Usuário.

Ação.

Data.

Objeto.

IP.

Resultado.

\---

# FAVORITOS

Preparar arquitetura para permitir favoritos administrativos

\---

# PERMISSÕES

Preparar estrutura para permissões específicas por módulo.

\---

# ÍNDICES

Criar índices para.

slug

status

tipo

parent\_id

ordem

created\_at

titulo

uuid

\---

# PERFORMANCE

Sempre utilizar:

Lazy Loading

Paginação

Cache

Consultas indexadas

Evitar consultas N+1.

\---

# MIGRATIONS

Todas as novas tabelas deverão ser criadas por migrations.

Jamais modificar migrations antigas.

\---

# MODELS

Criar novos Models independentes.

Não alterar Models existentes sem necessidade.

\---

# COMPATIBILIDADE

Toda a nova estrutura deverá coexistir com o banco atual.

Nenhuma tabela antiga deverá ser removida.

Nenhum relacionamento existente deverá ser quebrado.

Caso algum dado antigo precise ser utilizado, criar camada de integração.

Jamais alterar a lógica já utilizada pelo site.

\---

# DIAGRAMA GERAL

```text

SiteNode
│
├──── NodeContent ───── Content
│                           │
│                           ├──── ContentFile
│                           │
│                           ├──── ContentImage
│                           │
│                           ├──── ContentLink
│                           │
│                           ├──── ContentHistory
│                           │
│                           ├──── ContentVersion
│                           │
│                           └──── ContentTag
│
└──── AuditLog

```

\---

# RESULTADO ESPERADO

Ao concluir esta etapa, o sistema possuirá uma arquitetura preparada para evolução contínua, permitindo crescimento e expansão sem necessidade de remodelagem da estrutura do banco de dados.



A evolução do sistema ocorrerá através da criação de novos tipos de nós, novos módulos e novas funcionalidades, mantendo a mesma estrutura central e os princípios arquiteturais definidos.

\---

# FIM DA PARTE 4

Na Parte 5 será especificada toda a interface administrativa (UX/UI), incluindo a disposição dos painéis esquerdo e direito, o comportamento dos formulários, drag and drop, pré-visualização, seleção por árvore, edição em massa, responsividade e a integração com as telas de referência fornecidas para este projeto.
=== TEXTO 5 ===

# PARTE 5 — INTERFACE ADMINISTRATIVA (UX / UI)

\---

# OBJETIVO

Esta etapa define completamente a experiência de uso do novo Painel Central Administrativo.

O objetivo principal é reduzir drasticamente a quantidade de telas administrativas existentes.

Ao invés de diversos formulários espalhados pelo sistema, todas as operações deverão ocorrer dentro de uma única interface inteligente.

O administrador deverá conseguir visualizar toda a estrutura do site, selecionar qualquer elemento e modificar seu conteúdo sem sair da mesma tela.

O fluxo deverá ser intuitivo, rápido e preparado para administrar milhares de conteúdos.

\---

# FILOSOFIA DA INTERFACE

A interface deverá seguir alguns princípios fundamentais.

## Simplicidade

Nunca apresentar opções desnecessárias.

Mostrar apenas aquilo que faz sentido para o item atualmente selecionado.

\---

## Contexto

Toda alteração deverá acontecer baseada no elemento selecionado.

Ao clicar em um botão diferente, o painel deverá adaptar automaticamente todas as propriedades disponíveis.

\---

## Não perder contexto

O administrador nunca deverá sair da tela principal para realizar tarefas simples.

Sempre que possível utilizar:

Painéis

Modais

Menus laterais

Abas

Diálogos

\---

## Interface Viva

A interface deverá atualizar automaticamente seus componentes.

Sempre que possível evitar recarregar toda a página.

\---

# ESTRUTURA GERAL

O Painel Central Administrativo será dividido em quatro regiões principais.

```text

+--------------------------------------------------------------+
| Barra Superior                                                |
+--------------------------------------------------------------+

| Árvore | Área Central | Painel Inteligente |
|         |              |                    |
|         |              |                    |

+--------------------------------------------------------------+

| Barra Inferior (status do sistema)                           |
+--------------------------------------------------------------+

```

\---

# BARRA SUPERIOR

A barra superior será fixa.

Ela deverá conter.

Logo

Nome do módulo atual

Pesquisa global

Adicionar novo

Notificações

Ajuda

Perfil do usuário

Configurações

\---

# ÁRVORE DE NAVEGAÇÃO

Toda a estrutura do site ficará localizada na lateral esquerda.

Ela representará exatamente a estrutura lógica do sistema.

Exemplo.

```text

HOME

▼ Documentos Curriculares

▼ Ensino Fundamental

□ Matemática

□ Ciências

□ História

► Ensino Médio

CONTEÚDOS RECENTES

▼ Notícias

▼ Eventos

RODAPÉ

▼ Downloads

▼ Contato

```

Cada item poderá possuir.

Ícone

Cor

Quantidade de conteúdos

Indicadores de publicação

Status

\---

# COMPORTAMENTO DA ÁRVORE

A árvore deverá permanecer aberta.

O administrador poderá expandir ou recolher qualquer nível.

A posição deverá ser lembrada durante a navegação.

Ao retornar para o painel, a árvore continuará exatamente como foi deixada.

\---

# MENU DE CONTEXTO

Ao clicar com o botão direito sobre qualquer elemento deverá aparecer um menu.

Exemplo.

Editar

Duplicar

Criar filho

Mover

Renomear

Ocultar

Publicar

Despublicar

Excluir

Histórico

Permissões

\---

# PAINEL CENTRAL

Esta será a área de trabalho principal.

Ela exibirá informações diferentes dependendo do elemento selecionado.

Nenhum formulário ficará fixo.

Tudo será carregado dinamicamente.

\---

# PAINEL INTELIGENTE

A lateral direita será completamente dinâmica.

Ela substituirá dezenas de telas administrativas.

Quando um item for selecionado, este painel carregará automaticamente suas propriedades.

\---

# EXEMPLO

Selecionou um botão.

Mostrar.

Título

Ícone

Cor

Conteúdos

Anexos

Publicação

Permissões

\---

Selecionou um conteúdo.

Mostrar.

Texto

Imagens

Arquivos

Tags

Categorias

Links

Histórico

Versões

\---

Selecionou um arquivo.

Mostrar.

Nome

Descrição

Download

Substituir

Excluir

Versões

\---

# ABAS

O painel inteligente será dividido em abas.

Geral

Conteúdo

Arquivos

Links

Imagens

Publicação

Permissões

Histórico

Configurações

\---

# ABA GERAL

Campos.

Título

Descrição

Slug

Status

Tipo

Ícone

Cor

Página

Responsável

\---

# ABA CONTEÚDO

Editor de texto.

Pré-visualização.

Resumo.

Observações.

\---

# ABA ARQUIVOS

Lista completa de anexos.

Adicionar.

Remover.

Reordenar.

Visualizar.

Duplicar.

\---

# ABA LINKS

Links internos.

Links externos.

Nome amigável.

Abrir em nova aba.

Ordem.

\---

# ABA IMAGENS

Imagem principal.

Galeria.

Miniaturas.

Legenda.

Texto alternativo.

\---

# ABA PUBLICAÇÃO

Status.

Data.

Hora.

Agendamento.

Expiração.

Conteúdo recente.

Destaque.

Botão pulsante.

Botão vibrante.

\---

# ABA PERMISSÕES

Quem pode visualizar.

Quem pode editar.

Quem pode publicar.

Quem pode excluir.

\---

# ABA HISTÓRICO

Linha do tempo.

Versões.

Alterações.

Usuário responsável.

Data.

\---

# PAINEL DE PROPRIEDADES

Todas as propriedades deverão possuir salvamento automático opcional.

Caso o administrador prefira, poderá utilizar um botão:

Salvar Alterações.

\---

# SISTEMA DE DRAG AND DROP

Toda movimentação deverá ocorrer por arrastar.

Categorias.

Botões.

Subbotões.

Conteúdos.

Arquivos.

Imagens.

Links.

Sempre que possível.

\---

# EDIÇÃO EM MASSA

Ao selecionar diversos elementos deverão aparecer ações coletivas.

Publicar.

Arquivar.

Mover.

Excluir.

Adicionar vínculo.

Remover vínculo.

Alterar categoria.

Alterar página.

Alterar ordem.

\---

# PRÉ-VISUALIZAÇÃO

Toda alteração poderá ser visualizada antes da publicação.

O sistema deverá gerar uma visualização semelhante ao site real.

Sem publicar.

\---

# RESPONSIVIDADE

O painel deverá funcionar.

Desktop.

Notebook.

Tablet.

Dispositivos móveis (operações básicas).

\---

# ACESSIBILIDADE

Todos os componentes deverão possuir.

Navegação por teclado.

Contraste adequado.

Textos alternativos.

Ícones identificáveis.

Mensagens claras.

\---

# MENSAGENS DO SISTEMA

Sempre utilizar mensagens amigáveis.

Exemplos.

Conteúdo salvo com sucesso.

Arquivo enviado.

Publicação agendada.

Alterações descartadas.

Erro ao salvar.

\---

# BARRA DE STATUS

Na parte inferior deverá existir uma barra discreta contendo.

Usuário atual.

Ambiente.

Versão.

Quantidade de itens selecionados.

Última sincronização.

\---

# \# PLATAFORMA ADMINISTRATIVA CENTRAL

# 

# O Painel Central Administrativo deverá ser implementado desde esta primeira versão como a plataforma administrativa oficial do site.

# 

# Sua arquitetura, interface e estrutura de dados deverão contemplar todos os módulos administrativos previstos para o projeto, permitindo que sejam implementados de forma incremental sem necessidade de reestruturação da plataforma.

# 

# A interface deverá ser preparada para administrar, através de módulos integrados, funcionalidades como:

# 

# \* Notícias

# \* Eventos

# \* Comunicados

# \* Banners

# \* Galerias

# \* Vídeos

# \* Formulários

# \* Páginas

# \* Menus

# \* Rodapé

# \* Áreas Institucionais

# \* Documentos

# \* Legislação

# \* Currículo

# \* Downloads

# \* Links Rápidos

# \* Demais módulos previstos na evolução do sistema.

# 

# Sempre que um novo módulo fizer parte do escopo da implementação, ele deverá ser integrado ao Painel Central Administrativo utilizando a arquitetura já estabelecida, preservando a consistência visual, funcional e técnica da plataforma.

# 

# Nenhuma decisão de arquitetura, interface ou banco de dados deverá restringir a implementação desses módulos durante o desenvolvimento do projeto.

# 

# O Painel Central Administrativo deverá funcionar como uma plataforma única, modular, escalável e integrada para o gerenciamento de todo o conteúdo e recursos administrativos do site.

\---

# CRITÉRIOS DE ACEITAÇÃO

* Esta etapa será considerada concluída quando:
* A árvore de navegação estiver funcional.
* O painel inteligente responder ao item selecionado.
* As abas forem carregadas dinamicamente.
* O administrador puder editar conteúdos sem sair da tela principal.
* O menu de contexto funcionar.
* O sistema suportar edição em massa.
* A interface permanecer organizada mesmo com milhares de registros.
* O layout estiver preparado para evolução contínua, inclusão de novos recursos e expansão da estrutura.



\---

# FIM DA PARTE 5

Na Parte 6 será especificado todo o mecanismo de segurança, permissões, auditoria, logs, versionamento avançado, recuperação de conteúdo, backup lógico, integrações com o sistema existente e regras para garantir que nenhuma funcionalidade atual seja comprometida durante a implementação.

=== TEXTO 6 ===

# PARTE 6 — SEGURANÇA, PERMISSÕES, AUDITORIA E GOVERNANÇA

\---

# OBJETIVO

Esta etapa define toda a arquitetura de segurança do Painel Central Administrativo.

O objetivo não é apenas controlar quem pode acessar determinadas funcionalidades.

O objetivo é garantir:

* integridade do sistema
* proteção dos conteúdos
* rastreabilidade das alterações
* recuperação de informações
* auditoria completa
* compatibilidade com o sistema atual

Todo o sistema deverá ser construído considerando que vários administradores poderão trabalhar simultaneamente.

Nenhuma alteração deverá comprometer a estabilidade do site.

\---

# PRINCÍPIO FUNDAMENTAL

Nenhum usuário poderá executar ações para as quais não possua autorização explícita.

Caso exista qualquer dúvida sobre uma permissão.

Negar acesso.

Nunca assumir permissão automaticamente.

\---

# COMPATIBILIDADE

Toda a estrutura de autenticação atualmente utilizada pelo projeto deverá permanecer funcionando.

Não substituir.

Não alterar.

Não remover.

O Painel Central Administrativo deverá utilizar exatamente o mesmo sistema de autenticação já existente.

\---

# CAMADA DE AUTORIZAÇÃO

O novo painel deverá criar apenas uma camada adicional de permissões.

Jamais alterar o mecanismo atual.

\---

# \## PERFIS

# 

# O sistema deverá possuir controle de acesso baseado em perfis de usuário.

# 

# Perfis iniciais suportados:

# 

# \* Administrador Geral

# \* Administrador de Conteúdo

# \* Editor

# \* Publicador

# \* Revisor

# \* Leitor

# 

# A estrutura de permissões deverá permitir a criação, alteração e expansão de perfis sem necessidade de alteração estrutural do sistema.



\---

# PERMISSÕES

Cada módulo poderá definir permissões específicas.

Exemplo.

Visualizar

Criar

Editar

Excluir

Publicar

Arquivar

Agendar

Mover

Duplicar

Importar

Exportar

Gerenciar usuários

Gerenciar categorias

Gerenciar árvore

Gerenciar configurações

\---

# PERMISSÕES POR MÓDULO

Cada módulo do Painel Central Administrativo poderá definir permissões independentes.

Exemplo.

Gerenciador de Conteúdo

✓ Editar

✓ Publicar

✗ Excluir

Gerenciador de Botões

✓ Editar

✗ Criar

✗ Excluir

\---

# PERMISSÕES POR NÓ

Opcionalmente um nó da árvore poderá possuir permissões próprias.

Exemplo.

Currículo Ensino Médio

Somente equipe pedagógica.

Documentos internos

Somente administradores.

\---

# HERANÇA

Permissões poderão ser herdadas.

Categoria

↓

Botão

↓

Subbotão

↓

Subárea

Caso um nível não possua configuração própria deverá herdar do nível superior.

\---

# AUDITORIA

Toda operação importante deverá ser registrada.

Nunca apagar histórico.

\---

# EVENTOS AUDITÁVEIS

Login.

Logout.

Criação.

Edição.

Publicação.

Despublicação.

Agendamento.

Exclusão.

Restauração.

Movimentação.

Alteração de permissões.

Alteração de ordem.

Importação.

Exportação.

\---

# DADOS REGISTRADOS

Cada registro deverá armazenar.

Usuário.

Data.

Hora.

Ação.

Objeto.

Tipo do objeto.

Valor anterior.

Valor novo.

IP.

Navegador.

Sistema operacional (quando disponível).

Resultado.

Mensagem.

\---

# HISTÓRICO

Cada conteúdo deverá possuir uma linha do tempo.

Exemplo.

09:30

Conteúdo criado.

↓

09:42

Imagem alterada.

↓

09:45

Arquivo anexado.

↓

10:15

Publicado.

↓

11:00

Agendamento alterado.

\---

# LOGS

O sistema deverá possuir dois níveis.

Log funcional.

Log técnico.

\---

# LOG FUNCIONAL

Destinado ao administrador.

Registrar ações compreensíveis.

Exemplo.

Maria publicou o conteúdo.

João removeu um anexo.

Pedro alterou a categoria.

\---

# LOG TÉCNICO

Destinado aos desenvolvedores.

Registrar.

Exceções.

Erros.

Consultas.

Falhas.

Timeouts.

Integrações.

\---

# VERSIONAMENTO

Toda alteração importante deverá gerar uma nova versão.

O administrador poderá.

Visualizar.

Comparar.

Restaurar.

Duplicar.

Exportar.

\---

# COMPARAÇÃO

O sistema deverá permitir comparar duas versões.

Mostrar.

Texto removido.

Texto adicionado.

Imagem alterada.

Arquivo alterado.

Links alterados.

\---

# RECUPERAÇÃO

Qualquer versão poderá ser restaurada.

A restauração nunca deverá apagar versões anteriores.

Sempre criar uma nova versão baseada na restauração.

\---

# LIXEIRA

Excluir não significa apagar.

Excluir significa mover para lixeira.

A lixeira deverá possuir.

Data.

Responsável.

Motivo.

Tempo restante para exclusão definitiva.

\---

# EXCLUSÃO DEFINITIVA

A exclusão definitiva somente poderá ocorrer.

Por administradores autorizados.

Após confirmação.

Após nova confirmação.

\---

# BACKUP LÓGICO

O sistema deverá permitir exportar.

Categorias.

Árvore.

Conteúdos.

Anexos.

Configurações.

Permissões.

Metadados.

Preferencialmente em JSON.

\---

# IMPORTAÇÃO

Também deverá ser possível importar.

Conteúdos.

Categorias.

Árvores.

Configurações.

Mantendo validações.

\---

# TRANSAÇÕES

Toda operação crítica deverá utilizar transações.

Exemplo.

Mover um conteúdo.

Criar vínculos.

Excluir árvore.

Publicar múltiplos registros.

Caso ocorra erro.

Executar rollback completo.

\---

# CONCORRÊNCIA

Caso dois usuários editem o mesmo conteúdo.

O sistema deverá avisar.

Exemplo.

"Este conteúdo também está sendo editado por outro usuário."

\---

# BLOQUEIO DE EDIÇÃO

Opcionalmente poderá existir bloqueio temporário.

Enquanto um usuário edita.

Outro poderá visualizar.

Mas não salvar alterações.

\---

# RECUPERAÇÃO AUTOMÁTICA

Sempre que possível salvar automaticamente rascunhos temporários.

Caso o navegador feche inesperadamente.

Permitir recuperar alterações.

\---

# PROTEÇÃO CONTRA EXCLUSÃO ACIDENTAL

Nunca excluir.

Categorias.

Árvores.

Conteúdos.

Anexos.

Sem confirmação.

Para exclusões críticas utilizar confirmação dupla.

\---

# VALIDAÇÕES

Todos os formulários deverão validar.

Campos obrigatórios.

Tipos.

Limites.

Datas.

Duplicidade.

Relacionamentos.

\---

# \# NOTIFICAÇÕES

# 

# O sistema deverá implementar um módulo de notificações integrado ao Painel Central Administrativo.

# 

# Nesta implementação, deverão estar disponíveis as seguintes notificações:

# 

# \* Conteúdo publicado.

# \* Conteúdo despublicado.

# \* Conteúdo agendado.

# \* Conteúdo expirado.

# \* Falha na publicação.

# \* Erro de upload.

# \* Alteração de permissões.

# \* Conteúdo arquivado.

# \* Falha em operações críticas.

# \* Conclusão de importação ou exportação.

# 

# O módulo de notificações deverá ser desenvolvido de forma modular e extensível, permitindo a adição de novos tipos de notificações sem necessidade de alterações estruturais.

# 

# \## EXTENSIBILIDADE DA ARQUITETURA

# 

# A arquitetura deverá permitir a evolução do sistema através da adição de novos recursos, mantendo a mesma estrutura de dados e os mesmos princípios de organização.

# 

# Recursos como:

# 

# \* Notificações relacionadas a comentários;

# \* Workflows de aprovação;

# \* Integrações externas;

# 

# deverão utilizar a mesma base arquitetural, sem necessidade de reconstrução da estrutura existente.

\---

# \# API ADMINISTRATIVA

# 

# O Painel Central Administrativo deverá implementar uma camada de API como parte desta implementação.

# 

# A API deverá ser considerada um componente oficial da arquitetura do sistema e deverá ser desenvolvida em conjunto com os módulos administrativos, evitando adaptações posteriores.

# 

# Inicialmente, a API deverá disponibilizar endpoints para os módulos implementados, respeitando as mesmas regras de autenticação, autorização, auditoria e versionamento do painel administrativo.

# 

# A arquitetura deverá suportar:

# 

# \* API REST;

# \* API GraphQL;

# \* ou ambas, conforme a arquitetura do projeto.

# 

# Todos os serviços do Painel Central Administrativo deverão ser desenvolvidos seguindo uma arquitetura orientada a serviços, com uma camada de negócio centralizada e independente da interface de consumo.

# 

# A mesma camada deverá atender a interface administrativa, integrações externas, APIs e demais aplicações que necessitem consumir as funcionalidades do sistema.

# 

# A implementação da API deverá reutilizar os serviços e regras de negócio existentes, evitando duplicação de código.

# 

# Nenhuma decisão de arquitetura, banco de dados ou organização do projeto deverá impedir a evolução e ampliação da API.

# 

# A API deverá ser documentada, versionada e desenvolvida seguindo princípios de extensibilidade, permitindo o consumo por aplicações web, dispositivos móveis, serviços externos e demais módulos do ecossistema do projeto, mantendo a mesma arquitetura e camada de negócio.

\---

# ESCALABILIDADE

O sistema deverá suportar crescimento contínuo.

Novos módulos.

Novos tipos de conteúdo.

Novas permissões.

Novas integrações.

Sem reestruturação.

\---

# GOVERNANÇA

Toda alteração estrutural deverá seguir esta ordem.

Planejamento.

Validação.

Implementação.

Testes.

Homologação.

Produção.

\---

# REGRAS PARA O CLAUDE CODE

Antes de modificar qualquer arquivo existente.

Apresentar.

Nome do arquivo.

Motivo.

Impacto.

Alternativas.

Aguardar aprovação.

\---

Nunca modificar.

CLAUDE.md

README

Configurações

Rotas

Models

Templates

Sem apresentar justificativa.

\---

Caso exista uma solução utilizando novos arquivos.

Sempre preferir criar novos arquivos.

\---

Nunca remover código legado.

Caso alguma rotina fique obsoleta.

Mantê-la funcionando.

Marcar apenas como legado.

\---

Toda implementação deverá ser incremental.

Nunca realizar grandes refatorações simultaneamente.

\---

Cada etapa deverá terminar com.

Relatório.

Arquivos criados.

Arquivos alterados.

Arquivos removidos (caso autorizado).

Banco alterado.

Pendências.

Riscos.

Próxima etapa.

\---

# CRITÉRIOS DE ACEITAÇÃO

Esta etapa será considerada concluída quando.

✓ Toda ação possuir auditoria.

✓ Versionamento estiver funcionando.

✓ Histórico estiver funcionando.

✓ Permissões forem independentes.

✓ Lixeira estiver operacional.

✓ Recuperação funcionar.

✓ Backup lógico estiver disponível.

✓ Transações forem utilizadas.

✓ Rollback estiver implementado.

✓ Logs estiverem funcionando.

✓ Compatibilidade com o sistema existente estiver preservada.

\---

# FIM DA PARTE 6

Na Parte 7 será especificado o Plano Mestre de Implementação.

Será definido exatamente em que ordem o Claude Code deverá construir o sistema, quais arquivos criar primeiro, quais migrations executar, quando parar para aprovação e quais testes deverão ser executados antes de prosseguir para a etapa seguinte.
=== TEXTO 7 ===

# PARTE 7 — PLANO MESTRE DE IMPLEMENTAÇÃO

\---

# OBJETIVO

Esta etapa define exatamente como o Claude Code deverá conduzir toda a implementação do Painel Central Administrativo.

O objetivo é eliminar riscos.

Evitar alterações inesperadas.

Garantir compatibilidade.

Garantir qualidade.

Garantir que cada etapa possa ser validada antes da próxima.

Nenhuma implementação poderá ocorrer fora deste plano.

\---

# PRINCÍPIO MAIS IMPORTANTE

O Claude Code nunca deverá implementar grandes funcionalidades de uma única vez.

Toda implementação deverá ser incremental.

Cada fase deverá possuir início, desenvolvimento, testes, validação e aprovação.

Somente depois iniciar a próxima fase.

\---

# FLUXO OFICIAL

Toda implementação seguirá obrigatoriamente esta sequência.

Leitura

↓

Planejamento

↓

Arquitetura

↓

Aprovação

↓

Implementação

↓

Testes

↓

Correções

↓

Nova aprovação

↓

Próxima etapa

\---

# FASE ZERO

## LEITURA COMPLETA DO PROJETO

Antes de escrever qualquer linha de código o Claude deverá realizar uma leitura completa do projeto.

Deverá compreender.

Estrutura de pastas.

Banco de dados.

Framework utilizado.

Arquitetura.

Padrões do projeto.

Templates.

Views.

Models.

Migrations.

Rotas.

Javascript.

CSS.

Sistema administrativo existente.

Autenticação.

Permissões.

Uploads.

Nenhuma implementação poderá ocorrer antes desta leitura.

\---

# RELATÓRIO DA LEITURA

Após finalizar a leitura deverá apresentar.

Resumo do projeto.

Arquitetura encontrada.

Tecnologias utilizadas.

Pontos fortes.

Possíveis riscos.

Arquivos importantes.

Arquivos críticos.

Dependências.

Pontos que precisam de esclarecimento.

\---

# FASE 1

## PLANEJAMENTO

O Claude deverá produzir um plano técnico completo.

Este plano deverá conter.

Arquitetura proposta.

Fluxo.

Modelos.

Migrations.

Novas tabelas.

Novos módulos.

Arquivos novos.

Arquivos alterados.

Integrações.

Impactos.

Riscos.

Alternativas.

Cronograma.

Estimativa de complexidade.

Nenhuma implementação deverá começar antes da aprovação deste plano.

\---

# FASE 2

## ESTRUTURA

Criar apenas.

Pastas.

Arquivos.

Namespaces.

Configurações.

Rotas iniciais.

Sem implementar lógica.

Objetivo.

Preparar a arquitetura.

\---

# FASE 3

## BANCO

Criar.

Migrations.

Models.

Relacionamentos.

Índices.

Validações.

Soft Delete.

Versionamento.

Auditoria.

Nenhuma interface deverá ser criada nesta fase.

\---

# FASE 4

## ÁRVORE

Implementar apenas a estrutura hierárquica.

Criar.

Nós.

Categorias.

Relacionamentos.

Expansão.

Ordenação.

Pesquisa.

Nada relacionado a conteúdo.

\---

# FASE 5

## GERENCIADOR DE CONTEÚDOS

Implementar.

Cadastro.

Edição.

Versionamento.

Anexos.

Links.

Histórico.

Publicação.

Sem interface avançada.

\---

# FASE 6

## INTERFACE

Construir.

Layout.

Painéis.

Abas.

Árvore.

Drag and Drop.

Pesquisa.

Filtros.

Menu de contexto.

Preview.

\---

# FASE 7

## PUBLICAÇÃO

Implementar.

Agendamento.

Expiração.

Conteúdo recente.

Home.

Botão pulsante.

Botão vibrante.

Distribuição automática.

\---

# FASE 8

## SEGURANÇA

Permissões.

Logs.

Auditoria.

Rollback.

Transações.

Backup.

Importação.

Exportação.

\---

# FASE 9

## OTIMIZAÇÃO

Cache.

Lazy Loading.

Consultas.

Paginação.

Performance.

Compressão.

\---

# FASE 10

## TESTES

Executar.

Testes unitários.

Testes funcionais.

Testes de integração.

Testes de interface.

Testes de regressão.

\---

# APROVAÇÃO OBRIGATÓRIA

Ao final de cada fase o Claude deverá parar.

Nunca iniciar automaticamente a próxima.

Deverá apresentar.

Resumo.

Arquivos criados.

Arquivos alterados.

Banco alterado.

Funcionalidades implementadas.

Problemas encontrados.

Pendências.

Próximos passos.

E aguardar aprovação.

\---

# RELATÓRIO TÉCNICO

Ao terminar cada etapa gerar relatório contendo.

## Arquivos criados

Lista completa.

\---

## Arquivos modificados

Lista completa.

\---

## Migrations

Executadas.

Pendentes.

\---

## Models

Criados.

Alterados.

\---

## Views

Criadas.

Alteradas.

\---

## Templates

Criados.

Alterados.

\---

## Banco

Novas tabelas.

Novos índices.

Novas relações.

\---

## Performance

Consultas novas.

Índices utilizados.

Cache.

\---

## Segurança

Permissões.

Logs.

Auditoria.

\---

## Compatibilidade

Confirmar que nenhuma funcionalidade existente foi quebrada.

\---

# REGRAS PARA ALTERAR ARQUIVOS

Antes de modificar qualquer arquivo existente deverá apresentar.

Nome.

Motivo.

Impacto.

Alternativa utilizando novo arquivo.

Caso exista alternativa sem modificar o arquivo.

Sempre preferir criar novo arquivo.

\---

# ARQUIVOS CRÍTICOS

Arquivos considerados críticos.

Nunca modificar sem aprovação.

Configurações.

Autenticação.

Permissões.

CLAUDE.md

README.

Rotas principais.

Templates principais.

Sistema administrativo atual.

\---

# COMMITS

Cada fase deverá terminar preparada para um commit independente.

Exemplo.

feat(admin): estrutura inicial do painel central

feat(tree): implementação da árvore hierárquica

feat(content): gerenciador de conteúdos

feat(ui): interface administrativa

feat(publish): sistema de publicação

Cada commit deverá representar uma funcionalidade completa.

\---

# DOCUMENTAÇÃO

Ao concluir cada fase atualizar automaticamente a documentação técnica do projeto.

Registrar.

Arquitetura.

Fluxos.

Novos módulos.

Relacionamentos.

Diagramas (quando necessário).

\---

# CRITÉRIOS DE QUALIDADE

Nenhuma etapa será considerada concluída se existir.

Erro conhecido.

TODO crítico.

Funcionalidade parcialmente implementada.

Código duplicado sem justificativa.

Quebra de compatibilidade.

\---

# CHECKLIST FINAL DE CADA FASE

☐ Código revisado.

☐ Testes executados.

☐ Logs funcionando.

☐ Auditoria funcionando.

☐ Performance validada.

☐ Compatibilidade preservada.

☐ Documentação atualizada.

☐ Relatório entregue.

☐ Aguardando aprovação.

\---

# REGRA ABSOLUTA

O Claude Code jamais deverá assumir que pode continuar implementando após concluir uma fase.

A implementação sempre deverá parar.

Somente continuará mediante autorização explícita do responsável pelo projeto.

\---

# RESULTADO ESPERADO

Ao seguir este Plano Mestre de Implementação, o desenvolvimento ocorrerá de forma incremental, segura, rastreável e compatível com a arquitetura existente.

Cada fase produzirá um conjunto coeso de funcionalidades, devidamente testadas, documentadas e aprovadas antes do avanço para a etapa seguinte.

\---

# FIM DA PARTE 7

Na Parte 8 serão definidos os requisitos não funcionais, padrões de código, convenções de nomenclatura, organização de diretórios, princípios de UX, estratégia de testes, critérios de desempenho, padrões de documentação e diretrizes técnicas que deverão orientar todas as implementações, evoluções e integrações do projeto.

=== TEXTO 8 ===

# PARTE 8 — REQUISITOS NÃO FUNCIONAIS

\---

# OBJETIVO

Esta etapa define todos os padrões técnicos que deverão ser seguidos durante a implementação.

Estes requisitos possuem o mesmo nível de importância dos requisitos funcionais.

O objetivo é garantir que o Painel Central Administrativo seja escalável, performático, seguro, consistente e fácil de manter durante muitos anos.

Nenhuma implementação deverá ignorar estes requisitos.

\---

# PRINCÍPIO GERAL

Todo código desenvolvido deverá priorizar:

Legibilidade.

Organização.

Baixo acoplamento.

Alta coesão.

Reutilização.

Escalabilidade.

Facilidade de manutenção.

Compatibilidade com a arquitetura existente.

\---

# PADRÕES DE NOMENCLATURA

Todos os nomes utilizados no projeto deverão seguir um padrão único.

Classes

PascalCase

Exemplo

ContentManager

TreeNode

ContentVersion

AuditLog

\---

Métodos

camelCase

Exemplo

createContent()

publishContent()

loadTree()

moveNode()

\---

Variáveis

camelCase

Exemplo

currentNode

selectedItems

publishDate

\---

Constantes

UPPER\_CASE

Exemplo

MAX\_UPLOAD\_SIZE

DEFAULT\_STATUS

\---

Slug

Sempre minúsculo.

Separado por hífen.

Nunca utilizar espaços.

\---

# PADRÃO DE ORGANIZAÇÃO

Cada módulo deverá possuir estrutura própria.

Exemplo.

Models

Views

Templates

Services

Repositories

Validators

Permissions

Events

Jobs

DTOs

Helpers

Tests

\---

# CAMADAS

Sempre separar responsabilidades.

Nunca misturar.

Regra de negócio.

Interface.

Persistência.

Validação.

Integração.

\---

# PRINCÍPIO SOLID

Sempre que possível seguir.

Single Responsibility.

Open Closed.

Liskov.

Interface Segregation.

Dependency Inversion.

\---

# CÓDIGO LIMPO

Evitar.

Métodos gigantes.

Classes gigantes.

Duplicação.

Código morto.

Comentários desnecessários.

Variáveis sem significado.

\---

# DOCUMENTAÇÃO

Todo módulo deverá possuir documentação.

Objetivo.

Responsabilidade.

Dependências.

Fluxo.

Exemplos.

\---

# COMENTÁRIOS

Comentar apenas quando necessário.

O código deverá ser autoexplicativo.

\---

# PERFORMANCE

Toda consulta deverá ser analisada.

Evitar.

N+1.

Loops desnecessários.

Consultas duplicadas.

Consultas sem índices.

\---

Sempre utilizar.

Paginação.

Lazy Loading.

Cache.

Índices.

Pré-carregamento quando necessário.

\---

# \# CACHE

# 

# O Painel Central Administrativo deverá implementar uma camada de cache como parte desta implementação.

# 

# O sistema deverá utilizar cache para otimizar o desempenho das operações mais frequentes, reduzindo consultas desnecessárias ao banco de dados e melhorando o tempo de resposta.

# 

# Inicialmente, deverão ser implementadas estratégias de cache para:

# 

# \* Categorias;

# \* Árvore hierárquica;

# \* Conteúdos;

# \* Menus;

# \* Configurações do sistema.

# 

# A arquitetura de cache deverá ser modular e configurável, permitindo a expansão para novos módulos sem alterações estruturais.

# 

# Sempre que uma informação em cache for alterada, criada, removida ou atualizada, o sistema deverá invalidar ou atualizar automaticamente os dados armazenados, garantindo consistência entre o cache e o banco de dados.

# 

# A implementação deverá permitir a utilização de diferentes mecanismos de cache, conforme a infraestrutura do projeto, sem necessidade de alterações na lógica de negócio.

\---

# UPLOAD

Upload deverá suportar.

Múltiplos arquivos.

Arquivos grandes.

Retomada quando possível.

Validação.

Barra de progresso.

\---

# RESPONSIVIDADE

Interface preparada para.

Desktop.

Notebook.

Tablet.

Celular (operações administrativas básicas).

\---

# UX

Sempre reduzir quantidade de cliques.

Sempre manter contexto.

Nunca esconder ações importantes.

Priorizar produtividade.

\---

# ACESSIBILIDADE

Compatibilidade com teclado.

Leitores de tela.

Contraste.

Mensagens claras.

Ícones identificáveis.

\---

# MENSAGENS

Toda mensagem deverá ser compreensível.

Evitar erros técnicos.

Sempre informar ao usuário.

O que aconteceu.

O que fazer.

Como corrigir.

\---

# LOGS

Nunca registrar informações sensíveis.

Registrar apenas dados necessários para auditoria.

\---

# SEGURANÇA

Sanitizar entradas.

Validar uploads.

Escapar saídas.

Proteger contra:

SQL Injection.

XSS.

CSRF.

Upload malicioso.

Traversal.

\---

# IMPORTAÇÃO

Toda importação deverá validar.

Formato.

Estrutura.

Permissões.

Relacionamentos.

Duplicidade.

\---

# \# EXPORTAÇÃO

# 

# O Painel Central Administrativo deverá implementar um módulo de exportação como parte desta implementação.

# 

# O sistema deverá permitir a exportação de dados dos módulos administrativos, respeitando as permissões de acesso e os filtros aplicados pelo usuário.

# 

# Inicialmente, deverão ser suportados os seguintes formatos de exportação:

# 

# \* JSON;

# \* CSV;

# \* Excel (.xlsx);

# \* PDF.

# 

# O administrador poderá exportar, conforme o módulo utilizado:

# 

# \* Conteúdos;

# \* Categorias;

# \* Árvore hierárquica;

# \* Menus;

# \* Arquivos e anexos;

# \* Usuários (quando permitido);

# \* Logs de auditoria;

# \* Histórico de alterações;

# \* Configurações exportáveis.

# 

# As exportações deverão preservar a integridade dos dados, respeitar as permissões do usuário e gerar arquivos organizados, padronizados e compatíveis com aplicações externas.

# 

# A arquitetura deverá permitir a inclusão de novos formatos e novos tipos de exportação sem necessidade de alterações estruturais.

\---

# INTERNACIONALIZAÇÃO

Preparar arquitetura para múltiplos idiomas.

Mesmo que inicialmente utilize apenas Português.

\---

# TESTABILIDADE

Toda regra de negócio deverá ser facilmente testável.

Evitar lógica complexa dentro das Views.

\---

# OBSERVABILIDADE

Preparar o sistema para monitoramento.

Logs.

Métricas.

Tempo de resposta.

Erros.

Uso de memória.

\---

# ESCALABILIDADE

O sistema deverá suportar crescimento contínuo.

Novos módulos.

Novos tipos de conteúdo.

Novas integrações.

Novas APIs.

Sem necessidade de remodelagem.

\---

# MANUTENÇÃO

Sempre priorizar soluções simples.

Nunca criar complexidade desnecessária.

\---

# REVISÃO DE CÓDIGO

Antes de concluir qualquer fase.

Revisar.

Organizar.

Refatorar.

Documentar.

Testar.

\---

# CRITÉRIOS DE QUALIDADE

Uma implementação somente será considerada pronta quando atender simultaneamente:

✓ Requisitos funcionais.

✓ Requisitos não funcionais.

✓ Performance.

✓ Segurança.

✓ Compatibilidade.

✓ Documentação.

✓ Testes.

✓ Auditoria.

✓ Versionamento.

\---

# DEFINIÇÃO DE "CONCLUÍDO"

Uma funcionalidade somente poderá ser considerada concluída quando:

* estiver implementada;
* possuir testes;
* estiver documentada;
* não apresentar erros conhecidos;
* respeitar os padrões definidos neste documento;
* for aprovada pelo responsável pelo projeto.

Caso qualquer um desses itens não seja atendido, a funcionalidade deverá permanecer em desenvolvimento.

\---

# FIM DA PARTE 8

Na Parte 9 será definido o Plano Mestre de Testes, incluindo testes unitários, integração, regressão, performance, segurança, usabilidade e critérios objetivos para homologação antes da implantação em produção.

=== TEXTO 9 ===

# PARTE 9 — PLANO MESTRE DE TESTES, HOMOLOGAÇÃO E VALIDAÇÃO

\---

# OBJETIVO

Esta etapa define todos os procedimentos de validação do Painel Central Administrativo.

Nenhuma funcionalidade será considerada concluída apenas porque foi implementada.

Toda funcionalidade deverá passar por um conjunto de testes técnicos e funcionais antes de ser considerada apta para homologação.

O objetivo é garantir estabilidade, compatibilidade, desempenho e segurança.

\---

# PRINCÍPIO FUNDAMENTAL

Implementar não significa concluir.

Uma funcionalidade somente estará concluída quando:

* estiver implementada;
* estiver testada;
* estiver documentada;
* estiver homologada;
* tiver sido aprovada pelo responsável do projeto.

\---

# ESTRATÉGIA DE TESTES

O processo será dividido em sete níveis.

Nível 1

Testes Unitários

↓

Nível 2

Testes de Integração

↓

Nível 3

Testes Funcionais

↓

Nível 4

Testes de Interface

↓

Nível 5

Testes de Compatibilidade

↓

Nível 6

Testes de Performance

↓

Nível 7

Homologação

\---

# TESTES UNITÁRIOS

Cada componente deverá possuir testes próprios.

Exemplos.

Models.

Services.

Repositories.

Validators.

Permissions.

Helpers.

Eventos.

Versionamento.

\---

# TESTES DE INTEGRAÇÃO

Validar comunicação entre módulos.

Exemplos.

Tree ↔ Conteúdo

Conteúdo ↔ Arquivos

Conteúdo ↔ Publicação

Publicação ↔ Site

Permissões ↔ Usuários

Histórico ↔ Auditoria

\---

# TESTES FUNCIONAIS

Validar todos os fluxos administrativos.

Criar conteúdo.

Editar.

Duplicar.

Mover.

Excluir.

Restaurar.

Agendar.

Publicar.

Despublicar.

Criar vínculos.

Remover vínculos.

\---

# TESTES DA ÁRVORE

Criar nós.

Mover nós.

Excluir nós.

Reordenar.

Expandir.

Recolher.

Pesquisar.

Filtrar.

Duplicar estruturas.

\---

# TESTES DE PUBLICAÇÃO

Publicação imediata.

Agendamento.

Expiração.

Conteúdo recente.

Destaques.

Home.

Botões pulsantes.

Links.

Arquivos.

Imagens.

\---

# TESTES DE UPLOAD

Arquivos pequenos.

Arquivos grandes.

Múltiplos arquivos.

Arquivos inválidos.

Cancelamento.

Substituição.

Exclusão.

Download.

\---

# TESTES DE PERMISSÃO

Administrador.

Editor.

Revisor.

Leitor.

Cada perfil deverá ser validado.

Verificar.

Visualização.

Criação.

Alteração.

Publicação.

Exclusão.

Importação.

Exportação.

\---

# TESTES DE SEGURANÇA

Validar proteção contra.

SQL Injection.

XSS.

CSRF.

Upload malicioso.

Path Traversal.

Escalonamento de privilégios.

Sessões inválidas.

\---

# TESTES DE COMPATIBILIDADE

Confirmar que o sistema existente permanece íntegro.

Verificar.

Painel administrativo antigo.

Rotas existentes.

Templates existentes.

Uploads antigos.

Banco existente.

Usuários.

Permissões.

Nenhuma funcionalidade existente poderá deixar de funcionar.

\---

# TESTES DE INTERFACE

Verificar.

Responsividade.

Navegação.

Menus.

Abas.

Painel lateral.

Árvore.

Drag and Drop.

Filtros.

Pesquisa.

Pré-visualização.

\---

# TESTES DE ACESSIBILIDADE

Navegação por teclado.

Leitores de tela.

Contraste.

Mensagens.

Foco.

\---

# TESTES DE PERFORMANCE

Tempo de carregamento.

Consultas.

Cache.

Paginação.

Lazy Loading.

Consumo de memória.

\---

# TESTES DE CONCORRÊNCIA

Dois usuários editando simultaneamente.

Publicação simultânea.

Upload simultâneo.

Alterações concorrentes.

Rollback.

\---

# TESTES DE RECUPERAÇÃO

Restaurar versões.

Restaurar conteúdos.

Recuperar rascunhos.

Recuperar itens da lixeira.

\---

# TESTES DE AUDITORIA

Toda ação deverá gerar log.

Validar.

Criação.

Alteração.

Publicação.

Exclusão.

Permissões.

Importação.

Exportação.

\---

# TESTES DE VERSIONAMENTO

Criar versões.

Comparar versões.

Restaurar versões.

Duplicar versões.

\---

# TESTES AUTOMATIZADOS

Sempre que possível automatizar.

Testes Unitários.

Integração.

Regressão.

API.

Permissões.

\---

# TESTES MANUAIS

Também deverão existir testes conduzidos pelo responsável do projeto.

Fluxos administrativos.

Usabilidade.

Organização.

Experiência do usuário.

\---

# CRITÉRIOS DE HOMOLOGAÇÃO

Uma funcionalidade somente poderá seguir para produção quando:

✓ Todos os testes forem aprovados.

✓ Nenhum erro crítico permanecer aberto.

✓ A documentação estiver atualizada.

✓ A compatibilidade com o sistema legado estiver preservada.

✓ O responsável pelo projeto aprovar a entrega.

\---

# MATRIZ DE VALIDAÇÃO

Cada entrega deverá apresentar uma tabela semelhante à seguinte.

|Item|Status|Observações|
|-|-|-|
|Arquitetura|✓|Conforme especificação|
|Banco de Dados|✓|Migrations executadas|
|Interface|✓|Validada|
|Permissões|✓|Testadas|
|Auditoria|✓|Funcionando|
|Versionamento|✓|Funcionando|
|Compatibilidade|✓|Sem regressões|
|Performance|✓|Dentro dos limites|
|Documentação|✓|Atualizada|
|Testes|✓|Todos aprovados|

\---

# RELATÓRIO DE ENTREGA

Ao final de cada fase o Claude Code deverá gerar um relatório contendo.

Resumo da implementação.

Arquivos criados.

Arquivos alterados.

Migrations executadas.

Models criados.

Views criadas.

Templates criados.

Rotas adicionadas.

Testes executados.

Problemas encontrados.

Pendências.

Riscos.

Recomendações.

\---

# REGRA ABSOLUTA

Caso qualquer teste crítico falhe.

A implementação deverá ser interrompida.

O Claude Code deverá:

* explicar a causa;
* indicar os arquivos envolvidos;
* propor soluções;
* aguardar aprovação antes de prosseguir.

Jamais ignorar uma falha crítica.

\---

# DEFINIÇÃO DE PRONTO PARA PRODUÇÃO

Uma versão somente poderá ser considerada pronta quando:

* todos os testes estiverem aprovados;
* todos os critérios desta especificação forem atendidos;
* a documentação estiver sincronizada com o código;
* o responsável pelo projeto autorizar explicitamente a implantação.

\---

# FIM DA PARTE 9

Na Parte 10 será elaborado o Documento Mestre de Encerramento do Projeto, contendo o checklist definitivo de implantação, roteiro de atualização da documentação, estratégia de evolução contínua do CMS e as diretrizes finais que deverão orientar o Claude Code durante todo o ciclo de vida, manutenção e expansão do projeto.



=== TEXTO 10 ===

# PARTE 10 — CONSTITUIÇÃO DO PROJETO, DIRETRIZES PERMANENTES E ENCERRAMENTO

> Este documento estabelece os princípios permanentes que deverão orientar toda evolução do Painel Central Administrativo.

\---

# OBJETIVO

Esta etapa consolida todos os princípios arquiteturais, organizacionais e técnicos estabelecidos ao longo desta especificação.



Seu propósito é assegurar que todas as implementações, evoluções, integrações e manutenções do sistema preservem a coerência arquitetural, a estabilidade operacional e a compatibilidade com os objetivos originais do projeto.



Este documento deverá ser considerado a fonte de referência oficial para definição de padrões, decisões técnicas e evolução contínua do sistema.

\---

# A CONSTITUIÇÃO DO PROJETO

Os princípios abaixo possuem caráter permanente.

Nenhuma alteração estrutural deverá violá-los sem aprovação explícita do responsável pelo projeto.

\---

# PRINCÍPIO 1 — PRESERVAÇÃO DO SISTEMA LEGADO

O painel administrativo atualmente em produção constitui parte integrante do sistema.

Ele não deverá ser removido.

Ele não deverá ser substituído.

Ele não deverá ser reescrito apenas por motivos estéticos.

Toda evolução deverá ocorrer através da adição de novos módulos.

Sempre ampliar.

Nunca substituir.

\---

# PRINCÍPIO 2 — ARQUITETURA MODULAR

Toda nova funcionalidade deverá ser implementada como módulo independente.

Cada módulo deverá possuir responsabilidades claramente definidas.

Os módulos deverão comunicar-se através de interfaces bem definidas.

Evitar dependências diretas entre módulos.

\---

# PRINCÍPIO 3 — O CONTEÚDO É SOBERANO

O conteúdo nunca pertence à navegação.

A navegação apenas referencia conteúdos.

O conteúdo deverá existir independentemente.

Esta separação deverá ser preservada permanentemente.

\---

# PRINCÍPIO 4 — ÁRVORE HIERÁRQUICA

Toda a estrutura de navegação deverá utilizar uma árvore hierárquica baseada em nós.

Jamais criar tabelas específicas para cada nível da hierarquia.

A árvore deverá permanecer ilimitada.

\---

# PRINCÍPIO 5 — COMPATIBILIDADE

Nenhuma implementação poderá comprometer funcionalidades existentes.

Toda alteração deverá preservar:

* URLs existentes;
* rotinas administrativas;
* permissões atuais;
* dados existentes;
* estrutura de autenticação.

\---

# PRINCÍPIO 6 — EVOLUÇÃO INCREMENTAL

Grandes refatorações deverão ser evitadas.

O sistema deverá evoluir em pequenas entregas.

Cada entrega deverá ser testada, documentada e aprovada antes da próxima.

\---

# PRINCÍPIO 7 — DOCUMENTAÇÃO COMO FONTE OFICIAL

Toda decisão técnica deverá estar refletida na documentação.

Caso exista divergência entre código e documentação.

A implementação deverá ser interrompida.

A divergência deverá ser analisada.

Nunca assumir automaticamente que o código está correto.

\---

# PRINCÍPIO 8 — QUALIDADE ACIMA DA VELOCIDADE

O objetivo do projeto não é implementar rapidamente.

O objetivo é construir uma plataforma estável, segura e preparada para muitos anos de utilização.

Sempre priorizar qualidade.

\---

# PRINCÍPIO 9 — CÓDIGO COMO PATRIMÔNIO

Todo código produzido deverá ser considerado patrimônio do projeto.

Deverá ser:

* legível;
* documentado;
* organizado;
* reutilizável;
* testável.

Nunca produzir código descartável.

\---

# PRINCÍPIO 10 — DESENVOLVIMENTO ORIENTADO POR ESPECIFICAÇÃO

O Claude Code deverá considerar esta documentação como contrato de desenvolvimento.

Nenhuma funcionalidade deverá ser implementada por interpretação.

Sempre seguir esta especificação.

Caso exista qualquer ambiguidade.

Parar.

Explicar.

Solicitar orientação.

\---

# DIRETRIZES PARA O CLAUDE CODE

Antes de qualquer implementação:

1. Ler toda a documentação.
2. Compreender a arquitetura existente.
3. Apresentar plano técnico.
4. Identificar impactos.
5. Solicitar aprovação.
6. Implementar apenas a fase autorizada.
7. Executar testes.
8. Atualizar documentação.
9. Entregar relatório.
10. Aguardar nova autorização.

\---

# CHECKLIST FINAL DE ENTREGA

Antes de considerar qualquer versão concluída, verificar:

☐ Compatibilidade preservada.

☐ Painel antigo funcionando normalmente.

☐ Novo painel funcionando.

☐ Banco de dados consistente.

☐ Auditoria ativa.

☐ Versionamento operacional.

☐ Logs funcionando.

☐ Testes aprovados.

☐ Performance validada.

☐ Segurança validada.

☐ Documentação sincronizada.

☐ Aprovação do responsável registrada.

\---

# \# MÓDULOS OFICIAIS DA PLATAFORMA

# 

# O Painel Central Administrativo deverá ser implementado como uma plataforma única e integrada para o gerenciamento de todo o conteúdo e recursos administrativos do site.

# 

# A arquitetura do sistema deverá contemplar e suportar a implementação dos seguintes módulos oficiais:

# 

# \* Gerenciador de Notícias;

# \* Gerenciador de Eventos;

# \* Gerenciador de Comunicados;

# \* Gerenciador de Banners;

# \* Gerenciador de Galerias;

# \* Gerenciador de Vídeos;

# \* Gerenciador de Formulários;

# \* Workflow de Aprovação;

# \* Assinatura Eletrônica;

# \* API Pública;

# \* API Administrativa;

# \* Integração com Serviços Externos;

# \* Painéis Analíticos (Dashboard);

# \* Relatórios Gerenciais;

# \* Sistema de Notificações;

# \* Busca Avançada;

# \* Inteligência Artificial para Classificação de Conteúdos;

# \* Recomendação Automática de Conteúdos Relacionados.

# 

# A implementação deverá ocorrer de forma incremental, seguindo as fases definidas neste documento, porém todos esses módulos fazem parte do escopo oficial do projeto e deverão compartilhar a mesma arquitetura central, os mesmos padrões de desenvolvimento, segurança, permissões, auditoria, versionamento e integração.

# 

# Nenhuma decisão arquitetural deverá impedir ou dificultar a implementação desses módulos durante o desenvolvimento do projeto. Todos os módulos deverão reutilizar os serviços, componentes e infraestrutura já estabelecidos pelo Painel Central Administrativo, garantindo uma plataforma coesa, escalável e de fácil manutenção.



\---

# MANUTENÇÃO DA DOCUMENTAÇÃO

Sempre que houver alteração arquitetural:

* atualizar os documentos correspondentes;
* revisar diagramas;
* atualizar exemplos;
* revisar critérios de aceite;
* registrar a versão da documentação.

A documentação deverá evoluir junto com o código.

\---

# CONSIDERAÇÕES FINAIS

O Painel Central Administrativo não deverá ser tratado apenas como uma funcionalidade adicional do site.

Ele representa a base de uma plataforma institucional de gestão de conteúdos.

As decisões tomadas durante sua implementação deverão privilegiar estabilidade, simplicidade, escalabilidade e facilidade de manutenção.

A arquitetura deverá permanecer aberta para evolução contínua, preservando compatibilidade com o sistema existente e garantindo que novos módulos possam ser incorporados sem necessidade de reestruturações profundas.

\---

# ENCERRAMENTO

Este documento constitui a Especificação Oficial do Projeto.



Ele deverá orientar todas as implementações, evoluções, integrações e manutenções relacionadas ao Painel Central Administrativo.



Qualquer alteração nesta especificação deverá ser registrada, documentada e avaliada antes de sua implementação, garantindo a preservação dos princípios arquiteturais e técnicos definidos no projeto.



\---

**FIM DA ESPECIFICAÇÃO OFICIAL**

