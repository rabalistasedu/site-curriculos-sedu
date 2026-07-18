/* Zona de arrastar-e-soltar para uploads de arquivos (pedido 2026-07-17, parte 23).
   Qualquer <div class="dropzone" data-dropzone-input="idDoInput" data-dropzone-texto="idDoTexto">
   vira uma zona de arrastar-e-soltar ligada ao <input type="file"> indicado — clique abre o
   seletor normal, arrastar solta os arquivos no mesmo input (populado via DataTransfer).
   Funciona com ou sem o atributo "multiple" no input.
   Usado em: Painel Central, Organizador, Área do Site (uploads simples, 1 input só). A
   Estrutura de Árvores e o Adicionar Arquivos usam variações próprias (linhas dinâmicas de
   vários inputs), com script inline em cada template. */
(function () {
    'use strict';

    function atualizarTexto(input, textoEl, textoPadrao) {
        if (!textoEl) return;
        var n = input.files.length;
        if (n === 0) textoEl.textContent = textoPadrao;
        else if (n === 1) textoEl.textContent = '1 arquivo selecionado: ' + input.files[0].name;
        else textoEl.textContent = n + ' arquivos selecionados';
    }

    function ativar(zona) {
        if (zona.dataset.dropzoneAtivo) return;
        zona.dataset.dropzoneAtivo = '1';

        var input = document.getElementById(zona.dataset.dropzoneInput);
        var textoEl = document.getElementById(zona.dataset.dropzoneTexto);
        if (!input) return;
        var textoPadrao = textoEl ? textoEl.textContent : '';

        zona.addEventListener('click', function () { input.click(); });
        input.addEventListener('change', function () { atualizarTexto(input, textoEl, textoPadrao); });

        zona.addEventListener('dragover', function (e) {
            e.preventDefault();
            zona.classList.add('dropzone-ativa');
        });
        zona.addEventListener('dragleave', function () {
            zona.classList.remove('dropzone-ativa');
        });
        zona.addEventListener('drop', function (e) {
            e.preventDefault();
            zona.classList.remove('dropzone-ativa');
            var soltos = e.dataTransfer.files;
            if (!soltos || !soltos.length) return;
            var dt = new DataTransfer();
            if (input.multiple) {
                for (var i = 0; i < input.files.length; i++) dt.items.add(input.files[i]);
                for (var j = 0; j < soltos.length; j++) dt.items.add(soltos[j]);
            } else {
                dt.items.add(soltos[0]);
            }
            input.files = dt.files;
            atualizarTexto(input, textoEl, textoPadrao);
        });
    }

    function init() {
        Array.prototype.forEach.call(document.querySelectorAll('.dropzone[data-dropzone-input]'), ativar);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Exposto globalmente para telas que possam precisar reativar após
    // recriar o formulário dinamicamente.
    window.ativarDropzone = ativar;
})();
