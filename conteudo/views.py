from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Case, When, Value, IntegerField, F, Prefetch
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Categoria, Conteudo, Banner, Comentario, Cartaz, Anexo, Carrossel


def home(request):
    """Página principal do site"""
    categorias = Categoria.objects.filter(
        ativa=True, categoria_pai__isnull=True, mostrar_navegue_area=True
    )
    # Apenas banners sem categoria específica aparecem na home
    banners = Banner.objects.filter(ativo=True, categoria__isnull=True)
    destaques = Conteudo.objects.publicados().filter(destaque=True)[:6]
    # "Conteúdos recentes" mostra APENAS itens marcados como recente=True no admin
    recentes = Conteudo.objects.publicados().filter(recente=True)

    cartazes_esq = Cartaz.objects.filter(ativo=True, lado='esquerdo')
    cartazes_dir = Cartaz.objects.filter(ativo=True, lado='direito')

    # Carrosséis ativos — aparecem junto com os cartazes, no lado escolhido.
    # Carrossel sem NENHUMA imagem (e sem código HTML) não tem o que exibir:
    # é pulado para não renderizar uma moldura vazia — era isso que dava a
    # impressão de o checkbox "Ativar carrossel" não funcionar.
    carrosseis = list(Carrossel.objects.filter(ativo=True).prefetch_related('imagens'))
    for c in carrosseis:
        c.html_personalizado = _montar_carrossel_html(c)
    carrosseis = [
        c for c in carrosseis
        if c.html_personalizado or any(i.imagem_src for i in c.imagens.all())
    ]
    carrosseis_esq = [c for c in carrosseis if c.lado == 'esquerdo']
    carrosseis_dir = [c for c in carrosseis if c.lado == 'direito']

    return render(request, 'home.html', {
        'categorias': categorias,
        'banners': banners,
        'destaques': destaques,
        'recentes': recentes,
        'cartazes_esq': cartazes_esq,
        'cartazes_dir': cartazes_dir,
        'carrosseis_esq': carrosseis_esq,
        'carrosseis_dir': carrosseis_dir,
    })


def _montar_carrossel_html(carrossel):
    """Se o carrossel tem código HTML personalizado, substitui o marcador
    <!--IMAGENS--> (ou {{IMAGENS}}) pelas imagens cadastradas e devolve o
    HTML pronto para ser exibido em um iframe isolado. Sem código, devolve
    vazio e o site usa o visual padrão."""
    codigo = (carrossel.codigo_html or '').strip()
    if not codigo:
        return ''
    slides = []
    for img in carrossel.imagens.all():
        src = img.imagem_src
        if not src:
            continue
        if img.eh_video:
            tag = (f'<video src="{src}" autoplay muted loop playsinline '
                   f'style="width:100%;height:100%;object-fit:contain;display:block;background:#0f2033;"></video>')
        else:
            tag = (f'<img src="{src}" alt="" '
                   f'style="width:100%;height:100%;object-fit:contain;display:block;background:#0f2033;">')
        if img.link:
            tag = f'<a href="{img.link}" target="_blank" rel="noopener">{tag}</a>'
        slides.append(f'<div class="carousel-item" style="min-height:100%;width:100%;">{tag}</div>')
    imagens_html = ''.join(slides)
    for marcador in ('<!--IMAGENS-->', '{{IMAGENS}}'):
        if marcador in codigo:
            codigo = codigo.replace(marcador, imagens_html)
    return codigo


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

    # Conteúdos desta categoria e das subcategorias — inclui também os
    # publicados aqui por vínculo (Painel Central), sem duplicar.
    # ordem=0 significa "sem posição definida" → vai para o final (9999)
    # ordem=1,2,3... aparece primeiro, nessa sequência
    from painel.models import Vinculo
    cats = [categoria] + list(subcategorias)
    conteudos = Conteudo.objects.publicados().filter(
        Q(categoria__in=cats) | Q(vinculos__categoria__in=cats)
    ).distinct().order_by(
        Case(When(ordem=0, then=Value(9999)), default=F('ordem'), output_field=IntegerField()),
        '-data_publicacao'
    )
    # Conteúdos marcados como vibrantes/pulsantes nestes locais
    pulsantes = set(Vinculo.objects.filter(
        categoria__in=cats, pulsante=True
    ).values_list('conteudo_id', flat=True))

    # Filtro por tipo
    tipo = request.GET.get('tipo')
    if tipo:
        conteudos = conteudos.filter(tipo=tipo)

    # Banners específicos desta categoria
    banners_cat = Banner.objects.filter(ativo=True, categoria=categoria)

    anexos_categoria = categoria.anexos.all().order_by('ordem', 'nome')

    return render(request, 'categoria.html', {
        'categoria': categoria,
        'subcategorias': subcategorias,
        'conteudos': conteudos,
        'tipo_filtro': tipo,
        'banners': banners_cat,
        'anexos_categoria': anexos_categoria,
        'pulsantes': pulsantes,
    })


def conteudo_detalhe(request, slug):
    """Página de detalhe de um conteúdo, com formulário de comentários."""
    conteudo = get_object_or_404(Conteudo.objects.publicados(), slug=slug)
    relacionados = Conteudo.objects.publicados().filter(
        categoria=conteudo.categoria
    ).exclude(pk=conteudo.pk)[:4]

    # Comentários só aparecem em conteúdos que não são links externos puros
    exibir_comentarios = conteudo.tipo != 'link'

    # Apenas comentários de nível raiz (sem parent); respostas vêm via prefetch
    respostas_qs = Comentario.objects.filter(status='publicado').order_by('data_criacao')
    comentarios = (
        conteudo.comentarios.filter(status='publicado', parent__isnull=True)
        .prefetch_related(Prefetch('respostas', queryset=respostas_qs))
        .order_by('data_criacao')
        if exibir_comentarios else []
    )

    if exibir_comentarios and request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        texto = request.POST.get('texto', '').strip()
        parent_id = request.POST.get('parent_id', '').strip()
        parent = None
        if parent_id:
            try:
                parent = Comentario.objects.get(pk=parent_id, conteudo=conteudo, status='publicado', parent__isnull=True)
            except Comentario.DoesNotExist:
                pass
        if nome and texto:
            Comentario.objects.create(
                conteudo=conteudo,
                nome=nome,
                email=email,
                texto=texto,
                status='pendente',
                parent=parent,
            )
            messages.success(
                request,
                'Comentário enviado! Ele será publicado após aprovação.'
            )
            return redirect('conteudo:conteudo_detalhe', slug=slug)
        else:
            messages.error(request, 'Preencha seu nome e o comentário.')

    anexos = conteudo.anexos.all().order_by('ordem', 'nome')

    return render(request, 'conteudo_detalhe.html', {
        'conteudo': conteudo,
        'relacionados': relacionados,
        'comentarios': comentarios,
        'exibir_comentarios': exibir_comentarios,
        'anexos': anexos,
    })


def busca(request):
    """Busca textual em TUDO que existe no site — conteúdos E botões/áreas
    (categorias) — ignorando acentos e maiúsculas/minúsculas
    ("matematica" encontra "Matemática")."""
    from .busca_utils import filtrar_por_texto
    query = request.GET.get('q', '').strip()
    resultados = []
    categorias_encontradas = []

    if query:
        resultados = filtrar_por_texto(
            Conteudo.objects.publicados(),
            query,
            ('titulo', 'resumo', 'corpo'),
        )
        # Botões/áreas do site também entram na busca (pelo nome e pelo
        # texto introdutório) — antes a busca só achava conteúdos
        categorias_encontradas = filtrar_por_texto(
            Categoria.objects.filter(ativa=True),
            query,
            ('nome', 'descricao'),
        )

    return render(request, 'busca.html', {
        'query': query,
        'resultados': resultados,
        'categorias_encontradas': categorias_encontradas,
    })


@require_POST
def votar_comentario(request, pk):
    """AJAX: registra voto 👍 ou 👎 em um comentário publicado."""
    try:
        c = Comentario.objects.get(pk=pk, status='publicado')
    except Comentario.DoesNotExist:
        return JsonResponse({'error': 'não encontrado'}, status=404)
    voto = request.POST.get('voto')
    if voto == 'positivo':
        c.votos_positivos += 1
        c.save(update_fields=['votos_positivos'])
    elif voto == 'negativo':
        c.votos_negativos += 1
        c.save(update_fields=['votos_negativos'])
    else:
        return JsonResponse({'error': 'voto inválido'}, status=400)
    return JsonResponse({
        'votos_positivos': c.votos_positivos,
        'votos_negativos': c.votos_negativos,
    })
