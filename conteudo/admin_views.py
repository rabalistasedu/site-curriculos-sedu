import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from .models import Categoria, Conteudo, Anexo, Banner, ConfiguracaoSite, ColunaExtra, ColunaExtraBotao, RodapeImagem
from .permissoes import exige_permissao_painel


def _arvore_flat_categorias(excluir_pk=None):
    """Lista achatada de TODAS as categorias ativas (todos os níveis, com
    recuo por profundidade) — usada nos selects "mover para" que precisam
    listar a árvore inteira de botões, não só os vizinhos."""
    cats = list(Categoria.objects.filter(ativa=True).order_by('ordem', 'nome'))
    filhos_map = {}
    for c in cats:
        filhos_map.setdefault(c.categoria_pai_id, []).append(c)

    itens = []

    def caminhar(pai_id, nivel):
        for c in filhos_map.get(pai_id, []):
            if c.pk != excluir_pk:
                itens.append({'cat': c, 'nivel': nivel, 'recuo': ' ' * (nivel * 4)})
            caminhar(c.pk, nivel + 1)

    caminhar(None, 0)
    return itens


def _criar_links_extra(post, prefix, categoria, nome_padrao):
    """Cria vários Conteudo(tipo='link') a partir de linhas dinâmicas de
    nome+URL (campos '{prefix}_link_nome'/'{prefix}_link_url', uma lista
    paralela por linha do formulário). Nome em branco usa nome_padrao."""
    nomes = post.getlist(f'{prefix}_link_nome')
    urls = post.getlist(f'{prefix}_link_url')
    n = 0
    for i, url in enumerate(urls):
        url = (url or '').strip()
        if not url:
            continue
        nome_link = (nomes[i] if i < len(nomes) else '').strip() or nome_padrao
        slug = slugify(nome_link)[:50] or 'link'
        original = slug
        c = 1
        while Conteudo.objects.filter(slug=slug).exists():
            slug = f'{original}-{c}'
            c += 1
        Conteudo.objects.create(
            titulo=nome_link,
            slug=slug,
            tipo='link',
            url_externa=url,
            categoria=categoria,
            status='publicado',
        )
        n += 1
    return n


def _criar_anexos_link(post, prefix, conteudo=None, categoria=None):
    """Cria vários Anexo(url=...) a partir de linhas dinâmicas de nome+URL
    (campos '{prefix}_anexolink_nome'/'{prefix}_anexolink_url'). Diferente
    de _criar_links_extra (que cria um BOTÃO/card clicável), este aparece
    na seção "Arquivos para download" junto dos PDFs/anexos, mas abre uma
    URL externa em vez de baixar um arquivo. Nome em branco usa a própria URL."""
    nomes = post.getlist(f'{prefix}_anexolink_nome')
    urls = post.getlist(f'{prefix}_anexolink_url')
    n = 0
    for i, url in enumerate(urls):
        url = (url or '').strip()
        if not url:
            continue
        nome_link = (nomes[i] if i < len(nomes) else '').strip()
        Anexo.objects.create(conteudo=conteudo, categoria=categoria, url=url, nome=nome_link)
        n += 1
    return n


@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_organizador')
def organizar_view(request):
    cat_id = request.GET.get('cat')
    busca = request.GET.get('busca', '').strip()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'criar_subcategoria':
            nome = request.POST.get('nome', '').strip()
            pai_id = request.POST.get('categoria_pai_id')
            icone = request.POST.get('icone', '').strip()
            icone_img = request.FILES.get('icone_imagem')
            url_externa = request.POST.get('url_externa', '').strip()
            arquivos = request.FILES.getlist('arquivos')
            if nome and pai_id:
                pai = get_object_or_404(Categoria, pk=pai_id)
                slug = slugify(nome)
                original_slug = slug
                counter = 1
                while Categoria.objects.filter(slug=slug).exists():
                    slug = f'{original_slug}-{counter}'
                    counter += 1
                nova = Categoria.objects.create(
                    nome=nome,
                    slug=slug,
                    categoria_pai=pai,
                    icone=icone or 'fas fa-folder',
                    ativa=True,
                    url_externa=url_externa,
                )
                if icone_img:
                    nova.icone_imagem.save(icone_img.name, icone_img, save=True)

                # URL preenchida também vira Conteudo tipo=link dentro do botão
                if url_externa:
                    slug_link = slugify(nome)[:50] or 'link'
                    original_link = slug_link
                    n = 1
                    while Conteudo.objects.filter(slug=slug_link).exists():
                        slug_link = f'{original_link}-{n}'
                        n += 1
                    Conteudo.objects.create(
                        titulo=nome,
                        slug=slug_link,
                        tipo='link',
                        url_externa=url_externa,
                        categoria=nova,
                        status='publicado',
                    )

                # Arquivos viram anexos da nova subcategoria
                for arq in arquivos:
                    Anexo.objects.create(categoria=nova, arquivo=arq, nome=arq.name)

                n_links = _criar_links_extra(request.POST, 'nova', nova, nome)
                n_anexolinks = _criar_anexos_link(request.POST, 'nova', categoria=nova)

                extras = []
                if icone_img:
                    extras.append('ícone imagem')
                if url_externa:
                    extras.append('URL')
                if arquivos:
                    extras.append(f'{len(arquivos)} arquivo(s)')
                if n_links:
                    extras.append(f'{n_links} link(s) extra(s)')
                if n_anexolinks:
                    extras.append(f'{n_anexolinks} link(s) anexado(s)')
                sufixo = f' (+ {", ".join(extras)})' if extras else ''
                messages.success(request, f'Subcategoria "{nome}" criada com sucesso{sufixo}!')
            return redirect(f'/admin/organizar/?cat={pai_id}')

        elif action == 'mover':
            conteudo_ids = request.POST.getlist('conteudo_ids')
            destino_id = request.POST.get('destino_id')
            origem_cat = request.POST.get('origem_cat', '')
            if conteudo_ids and destino_id:
                destino = get_object_or_404(Categoria, pk=destino_id)
                count = Conteudo.objects.filter(pk__in=conteudo_ids).update(categoria=destino)
                messages.success(request, f'{count} conteúdo(s) movido(s) para "{destino.nome}".')
            return redirect(f'/admin/organizar/?cat={origem_cat}')

        elif action == 'adicionar_aqui':
            conteudo_ids = request.POST.getlist('conteudo_ids')
            cat_destino = request.POST.get('cat_destino')
            if conteudo_ids and cat_destino:
                destino = get_object_or_404(Categoria, pk=cat_destino)
                count = Conteudo.objects.filter(pk__in=conteudo_ids).update(categoria=destino)
                messages.success(request, f'{count} conteúdo(s) adicionado(s) a "{destino.nome}".')
            return redirect(f'/admin/organizar/?cat={cat_destino}')

        elif action == 'excluir_conteudo':
            conteudo_id = request.POST.get('conteudo_id')
            origem_cat = request.POST.get('origem_cat', '')
            if conteudo_id:
                deleted, _ = Conteudo.objects.filter(pk=conteudo_id).delete()
                if deleted:
                    messages.success(request, 'Conteúdo excluído com sucesso.')
            return redirect(f'/admin/organizar/?cat={origem_cat}')

        elif action == 'excluir_anexo':
            anexo_id = request.POST.get('anexo_id')
            origem_cat = request.POST.get('origem_cat', '')
            if anexo_id:
                deleted, _ = Anexo.objects.filter(pk=anexo_id, categoria_id=origem_cat).delete()
                if deleted:
                    messages.success(request, 'Arquivo excluído com sucesso.')
            return redirect(f'/admin/organizar/?cat={origem_cat}')

        elif action == 'salvar_ordem':
            origem_cat = request.POST.get('origem_cat', '')
            for key, value in request.POST.items():
                if key.startswith('ordem_'):
                    pk = key.replace('ordem_', '')
                    try:
                        Conteudo.objects.filter(pk=int(pk)).update(ordem=int(value))
                    except (ValueError, TypeError):
                        pass
            messages.success(request, 'Ordem salva com sucesso!')
            return redirect(f'/admin/organizar/?cat={origem_cat}')

        elif action == 'criar_conteudo_aqui':
            # Adiciona arquivos e/ou URL diretamente à categoria selecionada.
            cat_destino = request.POST.get('cat_destino')
            titulo = request.POST.get('novo_titulo', '').strip()
            url_ext = request.POST.get('novo_url', '').strip()
            arquivos = request.FILES.getlist('novo_arquivos')
            tem_links_extra = any((u or '').strip() for u in request.POST.getlist('aqui_link_url'))
            tem_anexolinks = any((u or '').strip() for u in request.POST.getlist('aqui_anexolink_url'))
            if not cat_destino:
                messages.error(request, 'Categoria destino não informada.')
                return redirect('/admin/organizar/')
            destino = get_object_or_404(Categoria, pk=cat_destino)
            if not (arquivos or url_ext or tem_links_extra or tem_anexolinks):
                messages.error(request, 'Envie pelo menos um arquivo ou informe uma URL.')
                return redirect(f'/admin/organizar/?cat={cat_destino}')

            criados = 0
            if url_ext:
                nome_link = titulo or url_ext
                slug_link = slugify(nome_link)[:50] or 'link'
                original = slug_link
                n = 1
                while Conteudo.objects.filter(slug=slug_link).exists():
                    slug_link = f'{original}-{n}'
                    n += 1
                Conteudo.objects.create(
                    titulo=nome_link,
                    slug=slug_link,
                    tipo='link',
                    url_externa=url_ext,
                    categoria=destino,
                    status='publicado',
                )
                criados += 1

            for arq in arquivos:
                Anexo.objects.create(categoria=destino, arquivo=arq, nome=arq.name)
                criados += 1

            criados += _criar_links_extra(request.POST, 'aqui', destino, titulo or destino.nome)
            criados += _criar_anexos_link(request.POST, 'aqui', categoria=destino)

            messages.success(
                request,
                f'{criados} item(ns) adicionado(s) a "{destino.nome}".'
            )
            return redirect(f'/admin/organizar/?cat={cat_destino}')

        elif action == 'criar_destaque':
            titulo = request.POST.get('dest_titulo', '').strip()
            url_ext = request.POST.get('dest_url', '').strip()
            arquivo = request.FILES.get('dest_arquivo')
            if not titulo and not arquivo and not url_ext:
                messages.error(request, 'Preencha pelo menos um campo (titulo, arquivo ou URL).')
                return redirect('/admin/organizar/')
            slug = slugify(titulo or 'destaque')
            original_slug = slug
            n = 1
            while Conteudo.objects.filter(slug=slug).exists():
                slug = f'{original_slug}-{n}'
                n += 1
            tipo = 'link' if url_ext else ('documento' if arquivo else 'post')
            # Se o arquivo enviado for uma imagem, vai para imagem_destaque
            # (campo usado pelo card da home) em vez de arquivo genérico —
            # senão o card mostrava só um ícone cinza, mesmo com imagem.
            extensoes_imagem = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'}
            eh_imagem = False
            if arquivo and '.' in arquivo.name:
                eh_imagem = arquivo.name.rsplit('.', 1)[-1].lower() in extensoes_imagem
            c = Conteudo.objects.create(
                titulo=titulo or 'Destaque',
                slug=slug,
                tipo=tipo,
                url_externa=url_ext,
                arquivo=arquivo if (arquivo and not eh_imagem) else '',
                imagem_destaque=arquivo if eh_imagem else None,
                status='publicado',
                destaque=True,
                destaque_gerenciado=True,
                ordem=0,
            )
            messages.success(request, f'Destaque "{c.titulo}" criado com sucesso!')
            return redirect('/admin/organizar/')

        elif action == 'toggle_destaque':
            dest_id = request.POST.get('dest_id')
            if dest_id:
                try:
                    c = Conteudo.objects.get(pk=dest_id)
                    c.destaque = not c.destaque
                    c.save(update_fields=['destaque'])
                    estado = 'ativado' if c.destaque else 'desativado'
                    messages.success(request, f'Destaque "{c.titulo}" {estado}.')
                except Conteudo.DoesNotExist:
                    pass
            return redirect('/admin/organizar/')

        elif action == 'excluir_destaque':
            dest_id = request.POST.get('dest_id')
            if dest_id:
                deleted, _ = Conteudo.objects.filter(pk=dest_id, destaque_gerenciado=True).delete()
                if deleted:
                    messages.success(request, 'Destaque excluido.')
            return redirect('/admin/organizar/')

    if cat_id:
        categoria = get_object_or_404(Categoria, pk=cat_id)
        subcategorias = categoria.subcategorias.filter(ativa=True).order_by('ordem', 'nome')
        conteudos = Conteudo.objects.filter(categoria=categoria).order_by('ordem', 'titulo')
        anexos_categoria = categoria.anexos.all().order_by('ordem', 'nome')

        sub_data = []
        for sub in subcategorias:
            count = Conteudo.objects.filter(categoria=sub).count()
            sub_data.append({'cat': sub, 'count': count})

        todas_subcategorias = list(subcategorias)
        if categoria.categoria_pai:
            irmas = categoria.categoria_pai.subcategorias.filter(ativa=True).exclude(pk=categoria.pk)
            destinos = [categoria.categoria_pai] + list(irmas)
        else:
            destinos = list(subcategorias)

        arvore_destinos = _arvore_flat_categorias(excluir_pk=categoria.pk)

        todos_conteudos = Conteudo.objects.exclude(
            categoria=categoria
        ).select_related('categoria').order_by('titulo')
        if busca:
            # Busca tolerante: ignora acentos e maiúsculas/minúsculas
            from .busca_utils import filtrar_por_texto
            todos_conteudos = filtrar_por_texto(
                todos_conteudos, busca, ('titulo', 'resumo')
            )

        context = {
            'title': f'Organizador — {categoria.nome}',
            'categoria': categoria,
            'subcategorias': sub_data,
            'conteudos': conteudos,
            'anexos_categoria': anexos_categoria,
            'destinos': destinos,
            'todas_subcategorias': todas_subcategorias,
            'arvore_destinos': arvore_destinos,
            'todos_conteudos': todos_conteudos,
            'busca': busca,
            'is_app_index': True,
            'has_permission': True,
        }
    else:
        categorias_pai = Categoria.objects.filter(
            ativa=True, categoria_pai__isnull=True
        ).order_by('ordem', 'nome')

        cat_data = []
        for cat in categorias_pai:
            subs = list(cat.subcategorias.filter(ativa=True))
            total = Conteudo.objects.filter(
                categoria__in=[cat] + subs
            ).count()
            cat_data.append({
                'cat': cat,
                'total': total,
                'sub_count': len(subs),
            })

        # Lista TODOS os itens desta área de gerenciamento, mesmo os ocultos
        # (destaque=False) — senão o item some da lista ao ser ocultado, sem
        # jeito de reativar depois.
        destaques = Conteudo.objects.filter(destaque_gerenciado=True).order_by('-data_publicacao')

        context = {
            'title': 'Organizador de Conteúdo',
            'categorias': cat_data,
            'destaques': destaques,
            'categoria': None,
            'is_app_index': True,
            'has_permission': True,
        }

    return render(request, 'admin/organizar.html', context)


@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_adicionar_arquivos')
def adicionar_arquivos_view(request):
    """Painel para adicionar arquivos a uma categoria do site.
    Fluxo: escolher categoria → dar nome ao grupo (subcategoria) → subir arquivos."""

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        subcategoria_id = request.POST.get('subcategoria_id', '').strip()
        nome_grupo = request.POST.get('nome_grupo', '').strip()

        if not categoria_id:
            messages.error(request, 'Selecione uma categoria (botão).')
            return redirect('/admin/adicionar-arquivos/')

        categoria_pai = get_object_or_404(Categoria, pk=categoria_id)

        if subcategoria_id:
            subcategoria = get_object_or_404(Categoria, pk=subcategoria_id)
            created = False
        elif nome_grupo:
            slug = slugify(nome_grupo)
            if not slug:
                slug = 'grupo'
            original_slug = slug
            counter = 1
            while Categoria.objects.filter(slug=slug).exclude(
                nome=nome_grupo, categoria_pai=categoria_pai
            ).exists():
                slug = f'{original_slug}-{counter}'
                counter += 1

            subcategoria, created = Categoria.objects.get_or_create(
                slug=slug,
                defaults={
                    'nome': nome_grupo,
                    'categoria_pai': categoria_pai,
                    'icone': 'fas fa-folder-open',
                    'ativa': True,
                }
            )
            if not created:
                subcategoria.nome = nome_grupo
                subcategoria.categoria_pai = categoria_pai
                subcategoria.save()
        else:
            # Sem grupo: anexa direto ao botão selecionado
            subcategoria = categoria_pai
            created = False

        file_count = 0
        link_count = 0
        for i in range(50):
            file_key = f'arquivo_{i}'
            url_key = f'url_{i}'
            nome_key = f'nome_{i}'
            nome = request.POST.get(nome_key, '').strip()

            if file_key in request.FILES:
                f = request.FILES[file_key]
                Anexo.objects.create(
                    categoria=subcategoria,
                    arquivo=f,
                    nome=nome,
                    ordem=file_count + link_count + 1,
                )
                file_count += 1
            elif request.POST.get(url_key, '').strip():
                url = request.POST[url_key].strip()
                titulo = nome or url
                slug_link = slugify(titulo)[:50] or 'link'
                original_slug_link = slug_link
                c = 1
                while Conteudo.objects.filter(slug=slug_link).exists():
                    slug_link = f'{original_slug_link}-{c}'
                    c += 1
                Conteudo.objects.create(
                    titulo=titulo,
                    slug=slug_link,
                    tipo='link',
                    url_externa=url,
                    categoria=subcategoria,
                    status='publicado',
                    ordem=file_count + link_count + 1,
                )
                link_count += 1

        total = file_count + link_count
        direto_no_botao = (subcategoria.pk == categoria_pai.pk)
        if total:
            parts = []
            if file_count:
                parts.append(f'{file_count} arquivo(s)')
            if link_count:
                parts.append(f'{link_count} link(s)')
            if direto_no_botao:
                messages.success(
                    request,
                    f'✅ {" e ".join(parts)} adicionado(s) diretamente a "{categoria_pai.nome}"!'
                )
            else:
                messages.success(
                    request,
                    f'✅ {" e ".join(parts)} adicionado(s) a "{subcategoria.nome}" '
                    f'(dentro de "{categoria_pai.nome}")!'
                )
        elif created:
            messages.success(
                request,
                f'✅ Grupo "{subcategoria.nome}" criado dentro de '
                f'"{categoria_pai.nome}" (sem itens por enquanto).'
            )
        elif direto_no_botao:
            messages.warning(
                request,
                'Nenhum arquivo ou link enviado.'
            )
        else:
            messages.info(
                request,
                f'O grupo "{subcategoria.nome}" já existe em '
                f'"{categoria_pai.nome}". Nenhum item novo enviado.'
            )

        return redirect('/admin/adicionar-arquivos/')

    from .widgets import CategoriaPicker
    picker = CategoriaPicker(include_home=False)
    picker_html = picker.render('categoria', None)

    context = {
        'title': 'Adicionar Arquivos',
        'picker_html': picker_html,
        'has_permission': True,
    }
    return render(request, 'admin/adicionar_arquivos.html', context)


@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_adicionar_arquivos')
def api_subcategorias_itens(request):
    """API JSON para listar subcategorias e seus itens, excluir itens,
    excluir grupos e duplicar itens."""

    if request.method == 'GET':
        cat_id = request.GET.get('cat_id')
        if not cat_id:
            return JsonResponse({'subcategorias': []})

        try:
            categoria = Categoria.objects.get(pk=cat_id)
        except Categoria.DoesNotExist:
            return JsonResponse({'subcategorias': []})

        subcats = categoria.subcategorias.filter(ativa=True).order_by('ordem', 'nome')
        data = []
        for sub in subcats:
            anexos = Anexo.objects.filter(categoria=sub).order_by('ordem')
            conteudos = Conteudo.objects.filter(categoria=sub).order_by('ordem')

            items = []
            for a in anexos:
                items.append({
                    'id': a.pk,
                    'tipo_item': 'anexo',
                    'nome': a.nome_exibicao,
                    'extensao': a.extensao,
                    'ordem': a.ordem,
                })
            for c in conteudos:
                items.append({
                    'id': c.pk,
                    'tipo_item': 'conteudo',
                    'nome': c.titulo,
                    'tipo': c.tipo,
                    'url': c.url_externa or '',
                    'ordem': c.ordem,
                    'edit_url': f'/admin/conteudo/conteudo/{c.pk}/change/',
                })
            items.sort(key=lambda x: x['ordem'])

            data.append({
                'id': sub.pk,
                'nome': sub.nome,
                'count': len(items),
                'items': items,
            })

        return JsonResponse({'subcategorias': data})

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        action = body.get('action')
        item_id = body.get('id')

        if action == 'delete_anexo' and item_id:
            deleted, _ = Anexo.objects.filter(pk=item_id).delete()
            return JsonResponse({'ok': True, 'deleted': deleted})
        elif action == 'delete_conteudo' and item_id:
            deleted, _ = Conteudo.objects.filter(pk=item_id).delete()
            return JsonResponse({'ok': True, 'deleted': deleted})
        elif action == 'delete_grupo' and item_id:
            try:
                grupo = Categoria.objects.get(pk=item_id)
            except Categoria.DoesNotExist:
                return JsonResponse({'error': 'Grupo não encontrado'}, status=404)
            n_conteudos = Conteudo.objects.filter(categoria=grupo).count()
            n_anexos = Anexo.objects.filter(categoria=grupo).count()
            n_sub = grupo.subcategorias.count()
            if n_conteudos > 0 or n_anexos > 0 or n_sub > 0:
                Conteudo.objects.filter(categoria=grupo).update(categoria=None)
                Anexo.objects.filter(categoria=grupo).delete()
            grupo.delete()
            return JsonResponse({
                'ok': True,
                'conteudos_orfaos': n_conteudos,
                'anexos_excluidos': n_anexos,
            })
        elif action == 'duplicar_conteudo' and item_id:
            try:
                orig = Conteudo.objects.get(pk=item_id)
            except Conteudo.DoesNotExist:
                return JsonResponse({'error': 'Conteúdo não encontrado'}, status=404)
            orig.pk = None
            orig.slug = ''
            orig.titulo = f'{orig.titulo} (cópia)'
            orig.save()
            for anexo in Anexo.objects.filter(conteudo_id=item_id):
                Anexo.objects.create(
                    conteudo=orig,
                    arquivo=anexo.arquivo,
                    nome=anexo.nome,
                    ordem=anexo.ordem,
                )
            return JsonResponse({'ok': True, 'new_id': orig.pk})
        elif action == 'duplicar_anexo' and item_id:
            try:
                orig = Anexo.objects.get(pk=item_id)
            except Anexo.DoesNotExist:
                return JsonResponse({'error': 'Anexo não encontrado'}, status=404)
            Anexo.objects.create(
                conteudo=orig.conteudo,
                categoria=orig.categoria,
                arquivo=orig.arquivo,
                nome=f'{orig.nome} (cópia)' if orig.nome else '',
                ordem=orig.ordem,
            )
            return JsonResponse({'ok': True})

        return JsonResponse({'error': 'ação desconhecida'}, status=400)

    return JsonResponse({'error': 'método não permitido'}, status=405)


# ── Gestão dos botões da BARRA SUPERIOR da home (pedido 2026-07-11) ────
# Tela simples: marcar/desmarcar quais botões principais aparecem na barra
# azul do topo, mudar a ordem, e atalhos para criar/editar/excluir botões.

@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_barra_superior')
def barra_superior_view(request):
    principais = Categoria.objects.filter(
        categoria_pai__isnull=True).order_by('ordem', 'nome')

    if request.method == 'POST':
        marcados_barra = set(request.POST.getlist('na_barra'))
        marcados_central = set(request.POST.getlist('na_central'))
        alterados = 0
        for cat in principais:
            novo_barra = str(cat.pk) in marcados_barra
            novo_central = str(cat.pk) in marcados_central
            try:
                nova_ordem = int(request.POST.get(f'ordem_{cat.pk}', cat.ordem))
            except (TypeError, ValueError):
                nova_ordem = cat.ordem
            if (cat.mostrar_menu_superior != novo_barra
                    or cat.mostrar_area_central != novo_central
                    or cat.ordem != nova_ordem):
                cat.mostrar_menu_superior = novo_barra
                cat.mostrar_area_central = novo_central
                cat.ordem = nova_ordem
                cat.save(update_fields=['mostrar_menu_superior', 'mostrar_area_central', 'ordem'])
                alterados += 1
        if alterados:
            messages.success(
                request,
                f'{alterados} botão(ões) atualizado(s). A barra superior e a '
                'área central do site já refletem a mudança.')
        else:
            messages.info(request, 'Nada mudou.')
        return redirect('admin_barra_superior')

    return render(request, 'admin/barra_superior.html', {
        'title': 'Botões da barra superior',
        'principais': principais,
        'has_permission': True,
        'is_app_index': True,
    })


@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_editor_rodape')
def editor_rodape_view(request):
    config = ConfiguracaoSite.get_config()

    if request.method == 'POST':
        secao = request.POST.get('secao', 'textos')

        if secao == 'imagem_nova':
            arquivo = request.FILES.get('nova_imagem')
            if not arquivo:
                messages.error(request, 'Selecione um arquivo de imagem.')
                return redirect('admin_editor_rodape')
            largura = request.POST.get('nova_largura', '').strip()
            altura = request.POST.get('nova_altura', '').strip()
            RodapeImagem.objects.create(
                imagem=arquivo,
                largura=int(largura) if largura.isdigit() else None,
                altura=int(altura) if altura.isdigit() else None,
                alinhamento=request.POST.get('nova_alinhamento', 'esquerda'),
                url=request.POST.get('nova_url', '').strip(),
                ordem=RodapeImagem.objects.count(),
            )
            messages.success(request, 'Imagem adicionada ao rodapé.')
            return redirect('admin_editor_rodape')

        if secao == 'imagem_excluir':
            RodapeImagem.objects.filter(pk=request.POST.get('imagem_id')).delete()
            messages.success(request, 'Imagem removida do rodapé.')
            return redirect('admin_editor_rodape')

        config.rodape_col1_titulo = request.POST.get('col1_titulo', '').strip()
        config.rodape_col1_html = request.POST.get('col1_html', '').strip()
        config.rodape_col2_titulo = request.POST.get('col2_titulo', '').strip()
        config.rodape_col2_html = request.POST.get('col2_html', '').strip()
        config.rodape_col3_titulo = request.POST.get('col3_titulo', '').strip()
        config.rodape_col3_html = request.POST.get('col3_html', '').strip()
        config.rodape_copyright = request.POST.get('copyright', '').strip()
        config.email_contato = request.POST.get('email', '').strip() or config.email_contato
        config.telefone = request.POST.get('telefone', '').strip() or config.telefone
        config.endereco = request.POST.get('endereco', '').strip() or config.endereco
        if 'rodape_imagem' in request.FILES:
            config.rodape_imagem = request.FILES['rodape_imagem']
        if request.POST.get('limpar_imagem'):
            config.rodape_imagem = None
        config.save()
        messages.success(request, 'Rodape atualizado com sucesso!')
        return redirect('admin_editor_rodape')

    return render(request, 'admin/editor_rodape.html', {
        'title': 'Editor do Rodape',
        'config': config,
        'imagens_rodape': RodapeImagem.objects.all(),
        'has_permission': True,
        'is_app_index': True,
    })


# ── Painel "Área do Site" ──────────────────────────────────────────
# Gerencia (1) o texto/formatação dos títulos das 3 seções da home
# (Destaques, Conteúdos recentes, Navegue por área) e (2) colunas extras
# opcionais à esquerda/direita da faixa "Recentes + Navegue por área",
# com botões personalizados dentro (link para categoria ou URL externa).

@staff_member_required
@exige_permissao_painel('conteudo.pode_acessar_area_do_site')
def area_do_site_view(request):
    from .forms import TituloSecoesForm

    config = ConfiguracaoSite.get_config()

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'salvar_titulos':
            form = TituloSecoesForm(request.POST, instance=config)
            if form.is_valid():
                obj = form.save(commit=False)
                for campo in ('icone_destaques_imagem', 'icone_recentes_imagem', 'icone_areas_imagem'):
                    if campo in request.FILES:
                        setattr(obj, campo, request.FILES[campo])
                    elif request.POST.get(f'limpar_{campo}'):
                        setattr(obj, campo, None)
                obj.save()
                messages.success(request, 'Títulos e ícones das seções atualizados com sucesso!')
            else:
                messages.error(request, 'Não foi possível salvar os títulos.')
            return redirect('admin_area_do_site')

        elif action == 'criar_coluna':
            titulo = request.POST.get('coluna_titulo', '').strip()
            lado = request.POST.get('coluna_lado', 'direita')
            if lado not in ('esquerda', 'direita'):
                lado = 'direita'
            coluna = ColunaExtra.objects.create(
                titulo=titulo or 'Nova coluna',
                lado=lado,
                icone=request.POST.get('coluna_icone', '').strip(),
            )
            if 'coluna_icone_imagem' in request.FILES:
                coluna.icone_imagem = request.FILES['coluna_icone_imagem']
                coluna.save(update_fields=['icone_imagem'])
            messages.success(request, 'Coluna criada com sucesso! Agora adicione botões dentro dela.')
            return redirect('admin_area_do_site')

        elif action == 'editar_coluna':
            coluna_id = request.POST.get('coluna_id')
            coluna = get_object_or_404(ColunaExtra, pk=coluna_id)
            coluna.titulo = request.POST.get('coluna_titulo', '').strip()
            coluna.icone = request.POST.get('coluna_icone', '').strip()
            lado = request.POST.get('coluna_lado', coluna.lado)
            if lado in ('esquerda', 'direita'):
                coluna.lado = lado
            coluna.ativa = bool(request.POST.get('coluna_ativa'))
            try:
                coluna.ordem = int(request.POST.get('coluna_ordem', coluna.ordem))
            except (TypeError, ValueError):
                pass
            if 'coluna_icone_imagem' in request.FILES:
                coluna.icone_imagem = request.FILES['coluna_icone_imagem']
            elif request.POST.get('limpar_coluna_icone_imagem'):
                coluna.icone_imagem = None
            coluna.save()
            messages.success(request, f'Coluna "{coluna.titulo}" atualizada.')
            return redirect('admin_area_do_site')

        elif action == 'excluir_coluna':
            coluna_id = request.POST.get('coluna_id')
            deleted, _ = ColunaExtra.objects.filter(pk=coluna_id).delete()
            if deleted:
                messages.success(request, 'Coluna excluída com sucesso.')
            return redirect('admin_area_do_site')

        elif action == 'criar_botao':
            coluna_id = request.POST.get('coluna_id')
            coluna = get_object_or_404(ColunaExtra, pk=coluna_id)
            nome = request.POST.get('botao_nome', '').strip()
            if not nome:
                messages.error(request, 'Informe um nome para o botão.')
                return redirect('admin_area_do_site')
            categoria_id = request.POST.get('botao_categoria') or None
            categoria = Categoria.objects.filter(pk=categoria_id).first() if categoria_id else None
            criar_botao_completo = bool(request.POST.get('botao_criar_arvore'))
            icone_texto = request.POST.get('botao_icone', '').strip()
            icone_img = request.FILES.get('botao_icone_imagem')

            # "Criar um botão completo do site": sem escolher uma categoria já
            # existente, cria uma categoria RAIZ de verdade (categoria_pai=None,
            # igual a "Currículo Atual" e qualquer outro botão principal) — a
            # partir daí o botão aparece em TODAS as árvores (Estrutura de
            # Árvores, Painel Central, Organizador, Barra Superior) como raiz
            # e aceita tudo que os outros botões aceitam (conteúdos,
            # subbotões, anexos, etc.).
            if not categoria and criar_botao_completo:
                slug = slugify(nome)
                original_slug = slug
                counter = 1
                while Categoria.objects.filter(slug=slug).exists():
                    slug = f'{original_slug}-{counter}'
                    counter += 1
                categoria = Categoria.objects.create(
                    nome=nome,
                    slug=slug,
                    categoria_pai=None,
                    icone=icone_texto or 'fas fa-folder-open',
                    ativa=True,
                    mostrar_menu_superior=False,
                    mostrar_navegue_area=False,
                )
                if icone_img:
                    icone_img.seek(0)
                    categoria.icone_imagem.save(icone_img.name, icone_img, save=True)

            # URL / anexos rápidos — preenchem o botão (novo ou já existente)
            # sem precisar abrir a árvore de botões separadamente.
            url_rapida = request.POST.get('botao_url_rapida', '').strip()
            if categoria and url_rapida:
                slug_link = slugify(nome)[:50] or 'link'
                original_link = slug_link
                n = 1
                while Conteudo.objects.filter(slug=slug_link).exists():
                    slug_link = f'{original_link}-{n}'
                    n += 1
                Conteudo.objects.create(
                    titulo=nome,
                    slug=slug_link,
                    tipo='link',
                    url_externa=url_rapida,
                    categoria=categoria,
                    status='publicado',
                )
            if categoria:
                for arq in request.FILES.getlist('botao_anexos_rapidos'):
                    Anexo.objects.create(categoria=categoria, arquivo=arq, nome=arq.name)
                _criar_links_extra(request.POST, 'botao', categoria, nome)
                _criar_anexos_link(request.POST, 'botao', categoria=categoria)

            botao = ColunaExtraBotao.objects.create(
                coluna=coluna,
                nome=nome,
                categoria=categoria,
                link_externo=request.POST.get('botao_link', '').strip() if not categoria else '',
                icone=icone_texto or 'fas fa-link',
            )
            if icone_img:
                icone_img.seek(0)
                botao.icone_imagem = icone_img
                botao.save(update_fields=['icone_imagem'])
            messages.success(request, f'Botão "{nome}" adicionado à coluna "{coluna.titulo}".')
            return redirect('admin_area_do_site')

        elif action == 'excluir_botao':
            botao_id = request.POST.get('botao_id')
            deleted, _ = ColunaExtraBotao.objects.filter(pk=botao_id).delete()
            if deleted:
                messages.success(request, 'Botão excluído com sucesso.')
            return redirect('admin_area_do_site')

        return redirect('admin_area_do_site')

    from .widgets import RichTextWidget

    form = TituloSecoesForm(instance=config)
    colunas = list(ColunaExtra.objects.all().prefetch_related('botoes'))
    categorias = Categoria.objects.filter(ativa=True).order_by('nome')

    titulo_widget = RichTextWidget()
    for coluna in colunas:
        coluna.titulo_editor_html = titulo_widget.render(
            'coluna_titulo', coluna.titulo, attrs={'id': f'id_coluna_titulo_{coluna.pk}'}
        )
    titulo_editor_novo_html = titulo_widget.render(
        'coluna_titulo', '', attrs={'id': 'id_coluna_titulo_nova'}
    )

    return render(request, 'admin/area_do_site.html', {
        'title': 'Área do Site',
        'form': form,
        'colunas': colunas,
        'categorias': categorias,
        'titulo_editor_novo_html': titulo_editor_novo_html,
        'has_permission': True,
        'is_app_index': True,
    })
