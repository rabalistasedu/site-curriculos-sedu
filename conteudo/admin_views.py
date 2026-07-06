from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from .models import Categoria, Conteudo


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
