import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from .models import Categoria, Conteudo, Anexo


@staff_member_required
def organizar_view(request):
    cat_id = request.GET.get('cat')
    busca = request.GET.get('busca', '').strip()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'criar_subcategoria':
            nome = request.POST.get('nome', '').strip()
            pai_id = request.POST.get('categoria_pai_id')
            icone = request.POST.get('icone', '').strip()
            if nome and pai_id:
                pai = get_object_or_404(Categoria, pk=pai_id)
                slug = slugify(nome)
                original_slug = slug
                counter = 1
                while Categoria.objects.filter(slug=slug).exists():
                    slug = f'{original_slug}-{counter}'
                    counter += 1
                Categoria.objects.create(
                    nome=nome,
                    slug=slug,
                    categoria_pai=pai,
                    icone=icone or 'fas fa-folder',
                    ativa=True,
                )
                messages.success(request, f'Subcategoria "{nome}" criada com sucesso!')
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

    if cat_id:
        categoria = get_object_or_404(Categoria, pk=cat_id)
        subcategorias = categoria.subcategorias.filter(ativa=True).order_by('ordem', 'nome')
        conteudos = Conteudo.objects.filter(categoria=categoria).order_by('ordem', 'titulo')

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

        todos_conteudos = Conteudo.objects.exclude(
            categoria=categoria
        ).select_related('categoria').order_by('titulo')
        if busca:
            todos_conteudos = todos_conteudos.filter(
                Q(titulo__icontains=busca) | Q(resumo__icontains=busca)
            )

        context = {
            'title': f'Organizador — {categoria.nome}',
            'categoria': categoria,
            'subcategorias': sub_data,
            'conteudos': conteudos,
            'destinos': destinos,
            'todas_subcategorias': todas_subcategorias,
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

        context = {
            'title': 'Organizador de Conteúdo',
            'categorias': cat_data,
            'categoria': None,
            'is_app_index': True,
            'has_permission': True,
        }

    return render(request, 'admin/organizar.html', context)


@staff_member_required
def adicionar_arquivos_view(request):
    """Painel para adicionar arquivos a uma categoria do site.
    Fluxo: escolher categoria → dar nome ao grupo (subcategoria) → subir arquivos."""

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        subcategoria_id = request.POST.get('subcategoria_id', '').strip()
        nome_grupo = request.POST.get('nome_grupo', '').strip()

        if not categoria_id or (not nome_grupo and not subcategoria_id):
            messages.error(request, 'Selecione uma categoria e escolha ou crie um grupo.')
            return redirect('/admin/adicionar-arquivos/')

        categoria_pai = get_object_or_404(Categoria, pk=categoria_id)

        if subcategoria_id:
            subcategoria = get_object_or_404(Categoria, pk=subcategoria_id)
            created = False
        else:
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
        if total:
            parts = []
            if file_count:
                parts.append(f'{file_count} arquivo(s)')
            if link_count:
                parts.append(f'{link_count} link(s)')
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
def api_subcategorias_itens(request):
    """API JSON para listar subcategorias e seus itens, e excluir itens."""

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

        return JsonResponse({'error': 'ação desconhecida'}, status=400)

    return JsonResponse({'error': 'método não permitido'}, status=405)
