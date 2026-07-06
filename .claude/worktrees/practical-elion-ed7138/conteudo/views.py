from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Categoria, Conteudo, Banner, Comentario, Cartaz


def home(request):
    """Página principal do site"""
    categorias = Categoria.objects.filter(ativa=True, categoria_pai__isnull=True)
    # Apenas banners sem categoria específica aparecem na home
    banners = Banner.objects.filter(ativo=True, categoria__isnull=True)
    destaques = Conteudo.objects.publicados().filter(destaque=True)[:6]
    recentes = Conteudo.objects.publicados()[:8]

    cartazes_esq = Cartaz.objects.filter(ativo=True, lado='esquerdo')
    cartazes_dir = Cartaz.objects.filter(ativo=True, lado='direito')

    return render(request, 'home.html', {
        'categorias': categorias,
        'banners': banners,
        'destaques': destaques,
        'recentes': recentes,
        'cartazes_esq': cartazes_esq,
        'cartazes_dir': cartazes_dir,
    })


# Página que funciona como "índice geral": reproduz a grade completa do
# site antigo, mostrando TODOS os temas (subcategorias) de todas as áreas.
SLUG_INDICE_GERAL = 'documentos-curriculares'


def categoria_detalhe(request, slug):
    """Página de uma categoria com seus conteúdos"""
    categoria = get_object_or_404(Categoria, slug=slug, ativa=True)
    subcategorias = categoria.subcategorias.filter(ativa=True).order_by('nome')

    # A página "Documentos Curriculares" é o índice geral: mostra todos os
    # temas do site (todas as subcategorias, de qualquer área), como no antigo.
    if slug == SLUG_INDICE_GERAL:
        botoes = Categoria.objects.filter(
            ativa=True, categoria_pai__isnull=False
        ).order_by('nome')
        banners_cat = Banner.objects.filter(ativo=True, categoria=categoria)
        return render(request, 'categoria.html', {
            'categoria': categoria,
            'botoes': botoes,
            'pagina_indice': True,
            'banners': banners_cat,
        })

    # Conteúdos desta categoria e das subcategorias
    conteudos = Conteudo.objects.publicados().filter(
        categoria__in=[categoria] + list(subcategorias)
    )

    # Filtro por tipo
    tipo = request.GET.get('tipo')
    if tipo:
        conteudos = conteudos.filter(tipo=tipo)

    # Banners específicos desta categoria
    banners_cat = Banner.objects.filter(ativo=True, categoria=categoria)

    return render(request, 'categoria.html', {
        'categoria': categoria,
        'subcategorias': subcategorias,
        'conteudos': conteudos,
        'tipo_filtro': tipo,
        'banners': banners_cat,
    })


def conteudo_detalhe(request, slug):
    """Página de detalhe de um conteúdo, com formulário de comentários."""
    conteudo = get_object_or_404(Conteudo.objects.publicados(), slug=slug)
    relacionados = Conteudo.objects.publicados().filter(
        categoria=conteudo.categoria
    ).exclude(pk=conteudo.pk)[:4]

    comentarios = conteudo.comentarios.filter(aprovado=True).order_by('data_criacao')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        texto = request.POST.get('texto', '').strip()
        if nome and texto:
            Comentario.objects.create(
                conteudo=conteudo,
                nome=nome,
                email=email,
                texto=texto,
                aprovado=False,
            )
            messages.success(
                request,
                'Comentário enviado! Ele será publicado após aprovação.'
            )
            return redirect('conteudo:conteudo_detalhe', slug=slug)
        else:
            messages.error(request, 'Preencha seu nome e o comentário.')

    return render(request, 'conteudo_detalhe.html', {
        'conteudo': conteudo,
        'relacionados': relacionados,
        'comentarios': comentarios,
    })


def busca(request):
    """Busca textual por conteúdos"""
    query = request.GET.get('q', '').strip()
    resultados = []

    if query:
        resultados = Conteudo.objects.publicados().filter(
            Q(titulo__icontains=query) |
            Q(resumo__icontains=query) |
            Q(corpo__icontains=query)
        )

    return render(request, 'busca.html', {
        'query': query,
        'resultados': resultados,
    })
