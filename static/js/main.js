// ── Banner slider automático ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('heroSlider');
    if (!slider) return;

    const slides = slider.querySelectorAll('.hero-slide');
    if (slides.length <= 1) return;

    let current = 0;

    setInterval(function() {
        slides[current].classList.remove('active');
        current = (current + 1) % slides.length;
        slides[current].classList.add('active');
    }, 5000);
});

// ── Barra superior: menu de "3 pontinhos" (⋯) para botões que não cabem ──
// Quando a barra azul fica cheia (muitas categorias, zoom, tela menor),
// os botões excedentes são movidos para um menu suspenso em vez de cortados.
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('.nav');
    const moreBtn = document.getElementById('navMore');
    const moreMenu = document.getElementById('navMoreMenu');
    if (!nav || !moreBtn || !moreMenu) return;

    // Guarda a lista original de links (sem o botão ⋯)
    const links = Array.prototype.slice.call(nav.querySelectorAll(':scope > .nav-link'));

    function reorganizar() {
        // No celular (≤768px) o menu vira hamburger — devolve tudo e sai
        const mobile = window.matchMedia('(max-width: 768px)').matches;
        // Devolve todos os links para a barra, na ordem original
        links.forEach(function(l) { nav.insertBefore(l, moreBtn); l.style.display = ''; });
        moreMenu.innerHTML = '';
        moreBtn.classList.remove('visivel');
        moreMenu.classList.remove('aberto');
        if (mobile) return;

        // Verifica se está estourando; se sim, move os últimos para o menu
        // (folga de 6px evita sobras de 1-2px por arredondamento do navegador)
        if (nav.scrollWidth <= nav.clientWidth + 1) return;
        moreBtn.classList.add('visivel');
        for (let i = links.length - 1; i >= 0; i--) {
            if (nav.scrollWidth <= nav.clientWidth - 6) break;
            moreMenu.insertBefore(links[i], moreMenu.firstChild);
        }
    }

    moreBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        moreMenu.classList.toggle('aberto');
    });
    document.addEventListener('click', function() {
        moreMenu.classList.remove('aberto');
    });

    let timer = null;
    window.addEventListener('resize', function() {
        clearTimeout(timer);
        timer = setTimeout(reorganizar, 120);
    });
    reorganizar();
});

// ── Carrossel de imagens (área dos cartazes da home) ──────────────
// Passa as imagens automaticamente e atualiza os indicadores laterais.
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.carrossel-widget').forEach(function(widget) {
        const slides = widget.querySelector('.carrossel-slides');
        const itens = widget.querySelectorAll('.carrossel-slide');
        const inds = widget.querySelectorAll('.carrossel-ind');
        if (!slides || itens.length === 0) return;

        const intervalo = (parseInt(widget.dataset.intervalo, 10) || 5) * 1000;

        function irPara(direcao) {
            const h = slides.offsetHeight;
            if (direcao > 0 && slides.scrollTop + h >= slides.scrollHeight - 2) {
                slides.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                slides.scrollBy({ top: direcao * h, behavior: 'smooth' });
            }
        }

        slides.addEventListener('scroll', function() {
            const i = Math.round(slides.scrollTop / slides.offsetHeight);
            inds.forEach(function(ind, n) {
                ind.classList.toggle('ativo', n === i);
            });
        });

        const btnCima = widget.querySelector('.carrossel-nav-cima');
        const btnBaixo = widget.querySelector('.carrossel-nav-baixo');
        if (btnCima) btnCima.addEventListener('click', function() { irPara(-1); });
        if (btnBaixo) btnBaixo.addEventListener('click', function() { irPara(1); });

        if (itens.length > 1) {
            setInterval(function() { irPara(1); }, intervalo);
        }
    });
});
