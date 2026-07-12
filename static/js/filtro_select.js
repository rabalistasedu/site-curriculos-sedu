/* Pesquisa em selects longos (pedido 2026-07-11).
   Qualquer <select data-pesquisavel="placeholder"> ganha uma caixinha de
   pesquisa logo acima: digitar filtra as opções na hora, ignorando
   acentos e maiúsculas ("matematica" acha "Matemática").
   Usado no "Categoria pai" do Django Admin e no "Criar novo botão"
   do Painel Central. */
(function () {
    'use strict';

    function normalizar(t) {
        return (t || '')
            .normalize('NFD')
            .replace(/[̀-ͯ]/g, '')
            .toLowerCase();
    }

    function ativar(select) {
        if (select.dataset.filtroAtivo) return;
        select.dataset.filtroAtivo = '1';

        var input = document.createElement('input');
        input.type = 'text';
        input.placeholder = select.getAttribute('data-pesquisavel') || '🔍 Pesquisar...';
        input.autocomplete = 'off';
        input.setAttribute('aria-label', 'Pesquisar opções da lista abaixo');
        input.style.cssText =
            'display:block;width:100%;max-width:520px;margin-bottom:5px;' +
            'padding:6px 10px;border:1px solid #cbd5e1;border-radius:5px;' +
            'font-size:13px;box-sizing:border-box;';
        select.parentNode.insertBefore(input, select);

        // Guarda TODAS as opções originais (a primeira é o "— Nenhuma —")
        var originais = Array.prototype.slice.call(select.options).map(function (o) {
            return { value: o.value, text: o.text };
        });

        input.addEventListener('input', function () {
            var alvo = normalizar(input.value);
            var valorAtual = select.value;
            while (select.options.length) select.remove(0);
            originais.forEach(function (o, i) {
                if (i === 0 || !alvo || normalizar(o.text).indexOf(alvo) !== -1) {
                    select.add(new Option(o.text, o.value));
                }
            });
            // mantém o que estava escolhido, se ainda estiver visível
            select.value = valorAtual;
            if (select.selectedIndex === -1 && select.options.length) {
                select.selectedIndex = 0;
            }
            // com poucos resultados, abre a lista "expandida" para facilitar
            select.size = (alvo && select.options.length > 1 && select.options.length <= 12)
                ? select.options.length : 0;
        });

        // Ao escolher com a lista expandida, volta ao formato fechado
        select.addEventListener('change', function () { select.size = 0; });
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll('select[data-pesquisavel]'), ativar);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
