# PLANO DE IMPLEMENTAÇÃO

# Biblioteca WordPress para Anexos

## Objetivo

Implementar uma nova funcionalidade no painel administrativo do sistema
Django que permita selecionar arquivos diretamente da Biblioteca de
Mídia do WordPress, sem necessidade de novo upload.

## Princípios

-   Manter 100% das funcionalidades atuais.
-   Não alterar o upload tradicional.
-   Adicionar uma nova opção chamada **📁 Biblioteca WordPress**.

## Interface

Na seção **Anexos**, manter:

-   Escolher arquivo
-   Nome (opcional)
-   Enviar

Adicionar abaixo:

-   **📁 Biblioteca WordPress**

## Funcionamento

Ao clicar no botão:

-   Abrir um modal.
-   Pesquisar arquivos pela API REST do WordPress.
-   Permitir filtrar por tipo.
-   Selecionar um arquivo.
-   Gravar apenas a URL do arquivo.
-   Não realizar upload.

## API REST

Endpoint:

`https://curriculo.sedu.es.gov.br/curriculo/wp-json/wp/v2/media`

Pesquisa:

`?search=nome`

Paginação:

`?per_page=100`

## Dados utilizados

-   ID
-   Nome
-   Título
-   MIME Type
-   Data
-   source_url

## Banco de dados

Suportar duas origens:

-   upload
-   wordpress

Quando a origem for WordPress, armazenar apenas a URL.

## Exibição

O visitante visualizará normalmente a lista de downloads, sem diferença
entre arquivos locais e arquivos do WordPress.

## Segurança

A integração será somente leitura.

Não permitir:

-   excluir arquivos
-   alterar arquivos
-   renomear arquivos
-   enviar arquivos para o WordPress

## Compatibilidade futura

Preparar a arquitetura para suportar:

-   URLs externas
-   Google Drive
-   OneDrive
-   SharePoint
-   AWS S3
-   Azure Blob
-   FTP

## Regra de Ouro

Nenhuma funcionalidade existente poderá ser alterada. O recurso
Biblioteca WordPress deverá ser totalmente independente e reutilizável
em todo o sistema.
