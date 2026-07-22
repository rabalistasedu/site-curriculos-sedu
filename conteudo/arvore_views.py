# -*- coding: utf-8 -*-
"""
Views do módulo administrativo "Estrutura de Árvores".
Gerenciamento completo da hierarquia do site: CRUD, drag-and-drop,
associação de conteúdo, biblioteca de ícones.

Completamente independente dos demais módulos — nenhum código existente é alterado.
"""
import json
import os

from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .models import Categoria, Conteudo, Anexo
from .permissoes import exige_permissao_painel


def _slug_unico(modelo, base):
    slug = slugify(base) or 'item'
    original = slug
    n = 1
    while modelo.objects.filter(slug=slug).exists():
        slug = f'{original}-{n}'
        n += 1
    return slug


def _montar_arvore_completa():
    """Árvore completa de categorias com metadados completos.
    Uma consulta por tabela — sem N+1."""
    from django.db.models import Count
    cats = list(
        Categoria.objects.filter(ativa=True)
        .annotate(n_conteudos=Count('conteudos'), n_anexos=Count('anexos'))
        .order_by('ordem', 'nome')
    )
    filhos_map = {}
    for c in cats:
        filhos_map.setdefault(c.categoria_pai_id, []).append(c)

    def no(cat):
        filhos = [no(f) for f in filhos_map.get(cat.pk, [])]
        nivel = 0
        p = cat.categoria_pai_id
        visited = set()
        while p and p not in visited:
            visited.add(p)
            nivel += 1
            parent = next((c for c in cats if c.pk == p), None)
            p = parent.categoria_pai_id if parent else None
        return {
            'cat': cat,
            'n_conteudos': cat.n_conteudos,
            'n_anexos': cat.n_anexos,
            'filhos': filhos,
            'nivel': nivel,
            'tem_filhos': len(filhos) > 0,
        }

    return [no(c) for c in filhos_map.get(None, [])]


def _arvore_json(arvore):
    """Converte árvore em JSON para o JavaScript."""
    def serializar(no):
        cat = no['cat']
        return {
            'id': cat.pk,
            'nome': cat.nome,
            'slug': cat.slug,
            'icone': cat.icone or cat.icone_display,
            'icone_imagem': cat.icone_imagem.url if cat.icone_imagem else None,
            'ordem': cat.ordem,
            'ativa': cat.ativa,
            'pai_id': cat.categoria_pai_id,
            'n_conteudos': no['n_conteudos'],
            'n_anexos': no['n_anexos'],
            'nivel': no['nivel'],
            'descricao': (cat.descricao or '')[:100],
            'filhos': [serializar(f) for f in no['filhos']],
        }
    return [serializar(n) for n in arvore]


def _listar_icones_enviados():
    """Lista todos os ícones personalizados já enviados (pasta media/icones_categoria/)."""
    icones = []
    pasta = os.path.join(settings.MEDIA_ROOT, 'icones_categoria')
    if os.path.isdir(pasta):
        for f in sorted(os.listdir(pasta)):
            ext = os.path.splitext(f)[1].lower()
            if ext in ('.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.gif'):
                icones.append({
                    'nome': f,
                    'pasta': 'icones_categoria',
                    'url': f'{settings.MEDIA_URL}icones_categoria/{f}',
                })
    pasta2 = os.path.join(settings.MEDIA_ROOT, 'icones')
    if os.path.isdir(pasta2):
        for f in sorted(os.listdir(pasta2)):
            ext = os.path.splitext(f)[1].lower()
            if ext in ('.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.gif'):
                icones.append({
                    'nome': f,
                    'pasta': 'icones',
                    'url': f'{settings.MEDIA_URL}icones/{f}',
                })
    return icones


# ── View principal ──────────────────────────────────────────────────────

@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_estrutura_arvores')
def estrutura_arvores_view(request):
    """Tela principal do módulo Estrutura de Árvores."""
    arvore = _montar_arvore_completa()
    arvore_json = json.dumps(_arvore_json(arvore), ensure_ascii=False)
    icones_enviados = _listar_icones_enviados()

    context = {
        'title': 'Estrutura de Árvores',
        'arvore': arvore,
        'arvore_json': arvore_json,
        'icones_enviados': icones_enviados,
        'has_permission': True,
    }
    return render(request, 'admin/estrutura_arvores.html', context)


# ── API AJAX ────────────────────────────────────────────────────────────

@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_estrutura_arvores')
def arvore_api(request):
    """Endpoint API para operações AJAX na árvore."""
    if request.method == 'GET':
        action = request.GET.get('action')
        if action == 'detalhes':
            return _api_detalhes(request)
        if action == 'conteudos':
            return _api_conteudos(request)
        if action == 'arvore_json':
            arvore = _montar_arvore_completa()
            return JsonResponse(_arvore_json(arvore), safe=False)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'criar':
            return _api_criar(request)
        if action == 'editar':
            return _api_editar(request)
        if action == 'excluir':
            return _api_excluir(request)
        if action == 'mover':
            return _api_mover(request)
        if action == 'reordenar':
            return _api_reordenar(request)
        if action == 'upload_icone':
            return _api_upload_icone(request)
        if action == 'associar_conteudo':
            return _api_associar_conteudo(request)
        if action == 'associar_links':
            return _api_associar_links(request)
        if action == 'associar_anexo_link':
            return _api_associar_anexo_link(request)
        if action == 'upload_anexo':
            return _api_upload_anexo(request)
        if action == 'remover_anexo':
            return _api_remover_anexo(request)
        if action == 'excluir_conteudo':
            return _api_excluir_conteudo(request)

    return JsonResponse({'error': 'Ação inválida'}, status=400)


def _api_detalhes(request):
    """Retorna detalhes completos de um nó."""
    cat_id = request.GET.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)
    anexos = list(cat.anexos.all().values('id', 'nome', 'arquivo', 'url', 'ordem'))
    conteudos = list(
        Conteudo.objects.filter(categoria=cat)
        .values('id', 'titulo', 'tipo', 'status', 'data_publicacao', 'url_externa')
        .order_by('ordem', '-data_publicacao')[:50]
    )
    for c in conteudos:
        if c.get('data_publicacao'):
            c['data_publicacao'] = c['data_publicacao'].isoformat()

    return JsonResponse({
        'id': cat.pk,
        'nome': cat.nome,
        'slug': cat.slug,
        'descricao': cat.descricao or '',
        'icone': cat.icone or '',
        'icone_imagem': cat.icone_imagem.url if cat.icone_imagem else None,
        'ordem': cat.ordem,
        'ativa': cat.ativa,
        'pai_id': cat.categoria_pai_id,
        'pai_nome': cat.categoria_pai.nome if cat.categoria_pai else None,
        'mostrar_menu_superior': cat.mostrar_menu_superior,
        'mostrar_navegue_area': cat.mostrar_navegue_area,
        'mostrar_conteudos_recentes': cat.mostrar_conteudos_recentes,
        'url_externa': cat.url_externa or '',
        'data_criacao': cat.pk,  # Categoria não tem data, usamos pk como proxy
        'anexos': anexos,
        'conteudos': conteudos,
        'n_filhos': cat.subcategorias.filter(ativa=True).count(),
    })


def _api_conteudos(request):
    """Lista conteúdos de uma categoria para associação."""
    cat_id = request.GET.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)
    conteudos = list(
        Conteudo.objects.filter(categoria=cat)
        .values('id', 'titulo', 'tipo', 'status', 'url_externa')
        .order_by('ordem', '-data_publicacao')
    )
    return JsonResponse({'conteudos': conteudos})


def _api_criar(request):
    """Cria um novo nó na árvore, opcionalmente com conteúdo (URL ou arquivo)."""
    nome = request.POST.get('nome', '').strip()
    pai_id = request.POST.get('pai_id', '').strip()
    icone = request.POST.get('icone', '').strip()

    if not nome:
        return JsonResponse({'error': 'Nome é obrigatório'}, status=400)

    pai = None
    if pai_id:
        pai = get_object_or_404(Categoria, pk=pai_id)

    url_conteudo = request.POST.get('url_conteudo', '').strip()

    cat = Categoria.objects.create(
        nome=nome,
        slug=_slug_unico(Categoria, nome),
        categoria_pai=pai,
        icone=icone or 'fas fa-folder-open',
        ativa=True,
        url_externa=url_conteudo,
    )

    icone_img = request.FILES.get('icone_imagem')
    if icone_img:
        cat.icone_imagem.save(icone_img.name, icone_img, save=True)

    msg = f'"{nome}" criado com sucesso.'

    if url_conteudo:
        msg += ' Ao clicar no botão, abre o link direto.'

    link_nomes = request.POST.getlist('link_nome')
    link_urls = request.POST.getlist('link_url')
    n_links = 0
    for i, url in enumerate(link_urls):
        url = (url or '').strip()
        if not url:
            continue
        nome_link = (link_nomes[i] if i < len(link_nomes) else '').strip()
        Conteudo.objects.create(
            titulo=nome_link or nome,
            slug=_slug_unico(Conteudo, nome_link or nome),
            tipo='link',
            url_externa=url,
            categoria=cat,
            status='publicado',
            data_publicacao=timezone.now(),
        )
        n_links += 1
    if n_links:
        msg += f' {n_links} link(s) associado(s).'

    arquivos = request.FILES.getlist('arquivos_anexo')
    for arq in arquivos:
        Anexo.objects.create(
            categoria=cat,
            arquivo=arq,
            nome=arq.name,
        )
    if arquivos:
        msg += f' {len(arquivos)} anexo(s) adicionado(s).'

    anexolink_nomes = request.POST.getlist('anexolink_nome')
    anexolink_urls = request.POST.getlist('anexolink_url')
    n_anexolinks = 0
    for i, url in enumerate(anexolink_urls):
        url = (url or '').strip()
        if not url:
            continue
        nome_link = (anexolink_nomes[i] if i < len(anexolink_nomes) else '').strip()
        Anexo.objects.create(categoria=cat, url=url, nome=nome_link)
        n_anexolinks += 1
    if n_anexolinks:
        msg += f' {n_anexolinks} link(s) anexado(s).'

    return JsonResponse({
        'ok': True,
        'id': cat.pk,
        'nome': cat.nome,
        'slug': cat.slug,
        'msg': msg,
    })


def _api_editar(request):
    """Edita um nó existente."""
    cat_id = request.POST.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)

    nome = request.POST.get('nome', '').strip()
    if nome and nome != cat.nome:
        cat.nome = nome
        cat.slug = _slug_unico(Categoria, nome)

    descricao = request.POST.get('descricao')
    if descricao is not None:
        cat.descricao = descricao

    icone = request.POST.get('icone', '').strip()
    if icone:
        cat.icone = icone

    ordem = request.POST.get('ordem')
    if ordem is not None and ordem.strip().isdigit():
        cat.ordem = int(ordem)

    vis_menu = request.POST.get('mostrar_menu_superior')
    if vis_menu is not None:
        cat.mostrar_menu_superior = vis_menu == '1'

    vis_area = request.POST.get('mostrar_navegue_area')
    if vis_area is not None:
        cat.mostrar_navegue_area = vis_area == '1'

    vis_recentes = request.POST.get('mostrar_conteudos_recentes')
    if vis_recentes is not None:
        cat.mostrar_conteudos_recentes = vis_recentes == '1'

    url_ext = request.POST.get('url_externa_cat')
    if url_ext is not None:
        cat.url_externa = url_ext.strip()

    icone_img = request.FILES.get('icone_imagem')
    if icone_img:
        cat.icone_imagem.save(icone_img.name, icone_img, save=False)
    else:
        # Ícone escolhido na "biblioteca" (galeria de ícones já enviados) —
        # em vez de subir um arquivo novo, reaproveita um arquivo já existente
        # em media/icones_categoria/ ou media/icones/ e aplica ao botão.
        lib_pasta = request.POST.get('icone_imagem_biblioteca_pasta', '').strip()
        lib_nome = os.path.basename(request.POST.get('icone_imagem_biblioteca_nome', '').strip())
        if lib_pasta in ('icones_categoria', 'icones') and lib_nome:
            caminho_absoluto = os.path.join(settings.MEDIA_ROOT, lib_pasta, lib_nome)
            if os.path.isfile(caminho_absoluto):
                cat.icone_imagem.name = f'{lib_pasta}/{lib_nome}'

    limpar_icone = request.POST.get('limpar_icone_imagem')
    if limpar_icone == '1':
        cat.icone_imagem = None

    cat.save()
    return JsonResponse({
        'ok': True,
        'msg': f'"{cat.nome}" atualizado.',
    })


def _api_excluir(request):
    """Exclui um nó (conteúdos ficam com categoria=None)."""
    cat_id = request.POST.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)
    nome = cat.nome
    n_filhos = cat.subcategorias.count()
    cat.delete()
    return JsonResponse({
        'ok': True,
        'msg': f'"{nome}" excluído.' + (f' ({n_filhos} subnível(is) removido(s) junto.)' if n_filhos else ''),
    })


def _api_mover(request):
    """Move um nó para outro pai (ou para raiz)."""
    cat_id = request.POST.get('id')
    novo_pai_id = request.POST.get('novo_pai_id', '').strip()
    cat = get_object_or_404(Categoria, pk=cat_id)

    if novo_pai_id:
        novo_pai = get_object_or_404(Categoria, pk=novo_pai_id)
        if _eh_descendente(cat, novo_pai):
            return JsonResponse({'error': 'Não pode mover para dentro de si mesmo.'}, status=400)
        cat.categoria_pai = novo_pai
    else:
        cat.categoria_pai = None

    cat.save()
    return JsonResponse({
        'ok': True,
        'msg': f'"{cat.nome}" movido com sucesso.',
    })


def _eh_descendente(ancestral, candidato):
    """Verifica se candidato é descendente de ancestral (evita ciclos)."""
    atual = candidato
    visited = set()
    while atual:
        if atual.pk == ancestral.pk:
            return True
        if atual.pk in visited:
            break
        visited.add(atual.pk)
        atual = atual.categoria_pai
    return False


def _api_reordenar(request):
    """Reordena nós irmãos."""
    try:
        ordem = json.loads(request.POST.get('ordem', '[]'))
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'error': 'Dados inválidos'}, status=400)

    for i, cat_id in enumerate(ordem):
        Categoria.objects.filter(pk=cat_id).update(ordem=i)

    return JsonResponse({'ok': True, 'msg': 'Ordem atualizada.'})


def _api_upload_icone(request):
    """Upload de ícone personalizado para a biblioteca."""
    arquivo = request.FILES.get('icone')
    if not arquivo:
        return JsonResponse({'error': 'Nenhum arquivo enviado'}, status=400)

    ext = os.path.splitext(arquivo.name)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.gif'):
        return JsonResponse({'error': f'Formato {ext} não suportado'}, status=400)

    pasta = os.path.join(settings.MEDIA_ROOT, 'icones_categoria')
    os.makedirs(pasta, exist_ok=True)

    nome_final = arquivo.name
    caminho = os.path.join(pasta, nome_final)
    counter = 1
    while os.path.exists(caminho):
        base, ext_orig = os.path.splitext(arquivo.name)
        nome_final = f'{base}_{counter}{ext_orig}'
        caminho = os.path.join(pasta, nome_final)
        counter += 1

    with open(caminho, 'wb') as f:
        for chunk in arquivo.chunks():
            f.write(chunk)

    return JsonResponse({
        'ok': True,
        'nome': nome_final,
        'pasta': 'icones_categoria',
        'url': f'{settings.MEDIA_URL}icones_categoria/{nome_final}',
        'msg': f'Ícone "{nome_final}" enviado para a biblioteca.',
    })


def _api_associar_conteudo(request):
    """Cria um conteúdo associado a uma categoria."""
    cat_id = request.POST.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)

    titulo = request.POST.get('titulo', '').strip()
    tipo = request.POST.get('tipo', 'post')
    url_ext = request.POST.get('url_externa', '').strip()

    if not titulo and not url_ext:
        return JsonResponse({'error': 'Título ou URL é obrigatório'}, status=400)

    conteudo = Conteudo.objects.create(
        titulo=titulo or cat.nome,
        slug=_slug_unico(Conteudo, titulo or cat.nome),
        tipo=tipo,
        url_externa=url_ext,
        categoria=cat,
        status='publicado',
        data_publicacao=timezone.now(),
    )

    arquivo = request.FILES.get('arquivo')
    if arquivo:
        conteudo.arquivo = arquivo
        if not tipo or tipo == 'post':
            conteudo.tipo = 'documento'
        conteudo.save()

    return JsonResponse({
        'ok': True,
        'id': conteudo.pk,
        'msg': f'Conteúdo "{conteudo.titulo}" associado a "{cat.nome}".',
    })


def _api_associar_links(request):
    """Associa vários links (URL) de uma vez a uma categoria (botão/subbotão/subárea).
    Recebe listas pareadas 'link_nome' e 'link_url' (uma por linha do formulário)."""
    cat_id = request.POST.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)

    nomes = request.POST.getlist('link_nome')
    urls = request.POST.getlist('link_url')

    ids = []
    for i, url in enumerate(urls):
        url = (url or '').strip()
        if not url:
            continue
        nome_link = (nomes[i] if i < len(nomes) else '').strip()
        conteudo = Conteudo.objects.create(
            titulo=nome_link or cat.nome,
            slug=_slug_unico(Conteudo, nome_link or cat.nome),
            tipo='link',
            url_externa=url,
            categoria=cat,
            status='publicado',
            data_publicacao=timezone.now(),
        )
        ids.append(conteudo.pk)

    if not ids:
        return JsonResponse({'error': 'Nenhum link válido informado'}, status=400)

    return JsonResponse({
        'ok': True,
        'ids': ids,
        'msg': f'{len(ids)} link(s) adicionado(s) a "{cat.nome}".',
    })


def _api_associar_anexo_link(request):
    """Anexa vários links (URL) de uma vez a uma categoria — diferente de
    _api_associar_links (que cria um BOTÃO/card clicável), este cria Anexo(url=...),
    aparecendo na seção "Arquivos para download" junto dos PDFs, mas abrindo uma
    URL externa em vez de baixar um arquivo. Recebe listas pareadas
    'anexolink_nome' e 'anexolink_url' (uma por linha do formulário)."""
    cat_id = request.POST.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)

    nomes = request.POST.getlist('anexolink_nome')
    urls = request.POST.getlist('anexolink_url')

    ids = []
    for i, url in enumerate(urls):
        url = (url or '').strip()
        if not url:
            continue
        nome_link = (nomes[i] if i < len(nomes) else '').strip()
        anexo = Anexo.objects.create(categoria=cat, url=url, nome=nome_link)
        ids.append(anexo.pk)

    if not ids:
        return JsonResponse({'error': 'Nenhum link válido informado'}, status=400)

    return JsonResponse({
        'ok': True,
        'ids': ids,
        'msg': f'{len(ids)} link(s) anexado(s) a "{cat.nome}".',
    })


def _api_upload_anexo(request):
    """Upload de anexo(s) para uma categoria.
    Aceita 1 arquivo (campo 'arquivo', comportamento original) ou vários de
    uma vez (campo 'arquivos', usado pelo arrastar-e-soltar)."""
    cat_id = request.POST.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)

    arquivo_unico = request.FILES.get('arquivo')
    arquivos = ([arquivo_unico] if arquivo_unico else []) + request.FILES.getlist('arquivos')
    if not arquivos:
        return JsonResponse({'error': 'Nenhum arquivo enviado'}, status=400)

    nome_campo = request.POST.get('nome', '').strip()
    ids = []
    for arq in arquivos:
        nome = nome_campo if (nome_campo and len(arquivos) == 1) else arq.name
        anexo = Anexo.objects.create(categoria=cat, arquivo=arq, nome=nome)
        ids.append(anexo.pk)

    if len(ids) == 1:
        msg = f'Anexo "{nome_campo or arquivos[0].name}" adicionado a "{cat.nome}".'
    else:
        msg = f'{len(ids)} anexos adicionados a "{cat.nome}".'

    return JsonResponse({'ok': True, 'ids': ids, 'msg': msg})


def _api_remover_anexo(request):
    """Remove um anexo."""
    anexo_id = request.POST.get('anexo_id')
    anexo = get_object_or_404(Anexo, pk=anexo_id)
    nome = anexo.nome_exibicao
    anexo.delete()
    return JsonResponse({
        'ok': True,
        'msg': f'Anexo "{nome}" removido.',
    })


def _api_excluir_conteudo(request):
    """Exclui um conteúdo permanentemente."""
    conteudo_id = request.POST.get('conteudo_id')
    conteudo = get_object_or_404(Conteudo, pk=conteudo_id)
    titulo = conteudo.titulo
    conteudo.delete()
    return JsonResponse({
        'ok': True,
        'msg': f'Conteúdo "{titulo}" excluído.',
    })
