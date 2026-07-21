# Documento de Implementações e Correções do Site

## Objetivo

Realizar as implementações e correções descritas neste documento **sem alterar o funcionamento das funcionalidades já existentes no sistema**.

Todos os recursos atuais do site devem permanecer operando exatamente como estão. As alterações deverão ser realizadas de forma isolada, preservando toda a compatibilidade com as funcionalidades existentes.

---

# Diretrizes Gerais

* Não remover funcionalidades existentes.
* Não alterar regras de negócio já implementadas.
* Não modificar layouts que já estejam funcionando corretamente, exceto nos pontos descritos neste documento.
* Toda nova funcionalidade deve ser integrada ao painel administrativo seguindo o padrão visual e estrutural já utilizado pelo sistema.
* Garantir compatibilidade com todo o restante do projeto.

---

# 1. Correção da Área de Ícones Personalizados

## Local

Painel Administrativo

**Estrutura de Árvore**

→ Área de Ícones

→ Ícones Personalizados

## Problema Atual

Atualmente é possível selecionar um ícone que já foi enviado para a biblioteca, porém, após selecioná-lo, ele não é aplicado ao botão correspondente, pois não existe uma ação de confirmação.

Também não existe uma forma de remover posteriormente esse ícone.

## Implementação

Adicionar os seguintes recursos:

### Botão Salvar

Após selecionar um ícone da biblioteca, deverá existir um botão **Salvar** que:

* grave o ícone selecionado;
* aplique imediatamente o ícone ao botão correspondente;
* mantenha o ícone salvo para futuras edições.

### Botão Excluir

Adicionar também um botão **Excluir** que deverá:

* remover o ícone personalizado;
* retirar o ícone do botão;
* retornar o botão ao estado anterior (sem ícone personalizado).

---

# 2. Correção do Recurso "Aparecer em Conteúdo Recente"

## Problema Atual

Todo botão raiz possui a opção:

**Aparecer em Conteúdo Recente**

Sim / Não

Mesmo selecionando **Sim** e salvando, o botão raiz não aparece na área de Conteúdo Recente do site.

## Correção

Corrigir esta funcionalidade para que:

* sempre que o usuário selecionar **Sim**;
* e clicar em **Salvar**;

o botão seja exibido corretamente na área **Conteúdo Recente**.

## Importante

Esta correção deverá ser aplicada em **todas as áreas do painel administrativo** que possuam esse recurso.

Não apenas em um módulo específico.

---

# 3. Implementação de Imagens no Rodapé

## Local

Painel Administrativo

**Editar Rodapé**

## Nova Funcionalidade

Adicionar uma área para gerenciamento de imagens do rodapé.

Cada imagem deverá possuir:

* upload da imagem;
* controle de largura;
* controle de altura;
* alinhamento.

## Opções de Alinhamento

* Esquerda
* Centralizado
* Direita

## Regras

Quando for escolhida a opção:

### Esquerda

A imagem deverá permanecer totalmente alinhada à margem esquerda do site.

Sem qualquer espaçamento adicional.

### Direita

A imagem deverá permanecer totalmente alinhada à margem direita do site.

Sem qualquer espaçamento adicional.

### Centralizado

A imagem ficará centralizada na faixa do rodapé.

---

# 4. Tamanho Fixo do Rodapé

Independentemente:

* da quantidade de imagens;
* do tamanho das imagens;
* da posição escolhida;

a faixa do rodapé **nunca poderá alterar sua altura atual**.

As imagens deverão adaptar-se ao espaço disponível.

O rodapé deve manter exatamente a mesma altura utilizada atualmente.

---

# 5. Campo Opcional para URL

Ainda na edição das imagens do rodapé, adicionar um campo opcional para informar uma URL.

Quando preenchido:

* a imagem deverá funcionar como um link.

Quando vazio:

* a imagem deverá ser exibida normalmente, sem hyperlink.

---

# 6. Configuração do Nome do Botão "Currículo Atual"

## Local

Painel Administrativo

Configuração do Site

## Implementação

Permitir alterar o texto do botão atualmente chamado:

**Currículo Atual**

O administrador poderá definir livremente outro nome para esse botão.

---

# 7. Inclusão de Novos Botões na Área Central

Ainda dentro de:

Configuração do Site

Na área onde atualmente existe o botão **Currículo Atual**, implementar uma funcionalidade que permita:

* criar novos botões;
* adicionar botões já existentes no sistema;
* reorganizar esses botões conforme necessário.

Essa funcionalidade deve oferecer flexibilidade para personalizar a página inicial sem necessidade de alterações no código.

---

# 8. Melhorias na Identidade Visual

## Local

Configuração do Site

→ Identidade Visual

Adicionar recursos para gerenciamento dos logotipos.

---

## Brasão Principal

Permitir configurar o brasão existente com as opções:

* esquerda;
* centro;
* direita.

Também permitir alterar:

* largura;
* altura.

---

## Segundo Logo

Adicionar suporte para um segundo logotipo.

Exemplo:

Logo do Currículo.

Este novo logotipo deverá possuir:

* upload;

* largura;

* altura;

* alinhamento:

* esquerda;

* centro;

* direita.

---

# 9. Barra Superior com Altura Fixa

Independentemente:

* da quantidade de logotipos;
* do tamanho configurado;
* da posição escolhida;

a barra superior onde ficam os brasões e logotipos **nunca poderá alterar sua altura atual**.

Os logotipos deverão adaptar-se ao espaço disponível sem modificar o layout existente.

---

# Requisitos Técnicos

Todas as implementações deverão obedecer aos seguintes critérios:

* preservar todas as funcionalidades atuais;
* manter compatibilidade com o restante do sistema;
* não alterar o banco de dados além do necessário para suportar as novas funcionalidades;
* seguir o padrão visual já existente;
* manter responsividade;
* manter compatibilidade com dispositivos móveis;
* evitar duplicação de código;
* utilizar componentes reutilizáveis sempre que possível.

---

# Resultado Esperado

Ao final das implementações:

* os ícones personalizados poderão ser salvos e removidos corretamente;
* o recurso **Conteúdo Recente** funcionará em todos os módulos do sistema;
* o rodapé permitirá adicionar imagens configuráveis e links opcionais;
* o rodapé manterá sua altura fixa;
* será possível alterar o nome do botão **Currículo Atual**;
* será possível adicionar novos botões ou reutilizar botões existentes na área central da página inicial;
* a identidade visual permitirá gerenciar um ou mais logotipos com posicionamento e tamanho configuráveis;
* a barra superior permanecerá com altura fixa independentemente da quantidade ou tamanho dos logotipos;
* todas as novas funcionalidades coexistirão com o sistema atual sem impactar os recursos já existentes.
