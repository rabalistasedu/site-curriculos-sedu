"""
Views do Painel Central Administrativo (/admin/painel-central/).

Tela 1 — Painel Administrativo Completo: árvore de botões com checkboxes
(lado esquerdo) + painel de composição e publicação (lado direito).
Publica o mesmo conteúdo em vários locais de uma vez, via Vinculo.

Tela 2 — Conteúdo para modificar ou configurar: listagem geral de todos
os conteúdos com seleção múltipla, edição de destaque/recentes/ordem e
remoção de vínculos.
"""
from datetime import datetime

from django.http import JsonResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify

from conteudo.models import Categoria, Conteudo, Anexo
from conteudo.widgets import IconPicker
from .models import Vinculo, EstiloBotao


# ── Helpers ───────────────────────────────────────────────────────────

def _slug_unico(modelo, base):
    slug = slugify(base) or 'item'
    original = slug
    n = 1
    while modelo.objects.filter(slug=slug).exists():
        slug = f'{original}-{n}'
        n += 1
    return slug


def _montar_arvore():
    """Árvore completa de categorias (todos os níveis), com contagem de
    conteúdos. Uma única consulta por tabela — sem N+1."""
    cats = list(Categoria.objects.filter(ativa=True).order_by('ordem', 'nome'))
    contagens = dict(
        Conteudo.objects.values_list('categoria').annotate(n=Count('id'))
    )
    filhos_map = {}
    for c in cats:
        filhos_map.setdefault(c.categoria_pai_id, []).append(c)

    def no(cat):
        return {
            'cat': cat,
            'n_conteudos': contagens.get(cat.pk, 0),
            'filhos': [no(f) for f in filhos_map.get(cat.pk, [])],
        }

    return [no(c) for c in filhos_map.get(None, [])]


def _arvore_flat(arvore):
    """Lista achatada da árvore (todos os níveis, com profundidade) — usada
    no select "criar botão dentro de outro botão"."""
    itens = []

    def caminhar(nos, nivel):
        for n in nos:
            itens.append({'cat': n['cat'], 'nivel': nivel, 'recuo': ' ' * (nivel * 4)})
            caminhar(n['filhos'], nivel + 1)

    caminhar(arvore, 0)
    return itens


def _data_publicacao(post):
    """Combina os campos data + hora do formulário; vazio = agora."""
    data = post.get('pub_data', '').strip()
    hora = post.get('pub_hora', '').strip() or '00:00'
    if not data:
        return timezone.now()
    try:
        dt = datetime.strptime(f'{data} {hora}'[:16], '%Y-%m-%d %H:%M')
        return timezone.make_aware(dt)
    except ValueError:
        return timezone.now()


CAMPOS_ESTILO = ('cor_fundo', 'cor_texto', 'fonte', 'tamanho_fonte', 'alinhamento', 'tamanho')


# ── Tela 1: Painel Administrativo Completo ────────────────────────────

@staff_member_required
def painel_central_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'criar_no':
            return _criar_no(request)

        if action == 'publicar':
            return _publicar(request)

        if action == 'excluir_nos':
            return _excluir_nos(request)

        if action == 'criar_subareas':
            return _criar_subareas(request)

        if action == 'editar_botao':
            return _editar_botao(request)

    if request.GET.get('action') == 'dados_botao' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return _dados_botao(request)

    arvore = _montar_arvore()
    context = {
        'title': 'Painel Administrativo Completo',
        'arvore': arvore,
        'arvore_flat': _arvore_flat(arvore),
        'icon_picker_html': IconPicker().render('icone_manual', None),
        'has_permission': True,
        'is_app_index': True,
    }
    return render(request, 'admin/painel_central.html', context)


def _criar_no(request):
    """Cria um novo botão (categoria raiz), subbotão ou subárea.
    Se nenhum pai for escolhido, o botão vai para a categoria especial
    "Botões novos criados" (criada automaticamente se não existir)."""
    nome = request.POST.get('novo_nome', '').strip()
    pai_id = request.POST.get('novo_pai', '').strip()
    if not nome:
        messages.error(request, 'Digite o nome do novo botão.')
        return redirect('painel:central')
    pai = None
    if pai_id:
        pai = get_object_or_404(Categoria, pk=pai_id)
    else:
        pai, _criada = Categoria.objects.get_or_create(
            slug='botoes-novos-criados',
            defaults={
                'nome': 'Botões novos criados',
                'icone': 'fas fa-plus-circle',
                'ativa': True,
                'mostrar_menu_superior': False,
                'mostrar_navegue_area': False,
            },
        )
    Categoria.objects.create(
        nome=nome,
        slug=_slug_unico(Categoria, nome),
        categoria_pai=pai,
        icone=request.POST.get('novo_icone', '').strip() or 'fas fa-folder-open',
        ativa=True,
    )
    onde = f'dentro de "{pai.nome}"'
    messages.success(request, f'Botão "{nome}" criado {onde}.')
    return redirect('painel:central')


def _excluir_nos(request):
    """Exclui os botões (categorias) marcados na árvore. Os conteúdos
    publicados neles NÃO são excluídos — apenas ficam sem local (a FK
    Conteudo.categoria é SET_NULL); podem ser vinculados de novo depois.
    Subbotões dos botões excluídos são excluídos junto (fazem parte dele)."""
    ids = request.POST.getlist('destinos')
    cats = list(Categoria.objects.filter(pk__in=ids))
    if not cats:
        messages.error(request, 'Marque na árvore o(s) botão(ões) que deseja excluir.')
        return redirect('painel:central')
    nomes = ', '.join(c.nome for c in cats)
    n = len(cats)
    Categoria.objects.filter(pk__in=ids).delete()
    messages.success(
        request,
        f'{n} botão(ões) excluído(s): {nomes}. Os conteúdos que estavam '
        'neles continuam salvos (sem local de exibição) e podem ser '
        'vinculados novamente em "Conteúdo para modificar ou configurar".'
    )
    return redirect('painel:central')


def _criar_subareas(request):
    """Cria uma nova subárea (subbotão) DENTRO de cada botão marcado na
    árvore. Atalho: em vez de ir no formulário "Criar novo botão" e
    escolher pai um a um, marca os pais na árvore e cria de uma vez."""
    nome = request.POST.get('subarea_nome', '').strip()
    if not nome:
        messages.error(request, 'Digite o nome da subárea.')
        return redirect('painel:central')
    ids = request.POST.getlist('destinos')
    pais = list(Categoria.objects.filter(pk__in=ids))
    if not pais:
        messages.error(
            request,
            'Marque na árvore o(s) botão(ões) dentro dos quais a subárea será criada.'
        )
        return redirect('painel:central')
    criados = []
    for pai in pais:
        nova = Categoria.objects.create(
            nome=nome,
            slug=_slug_unico(Categoria, nome),
            categoria_pai=pai,
            icone='fas fa-folder-open',
            ativa=True,
        )
        criados.append(f'"{nome}" dentro de "{pai.nome}"')
    messages.success(
        request,
        f'{len(criados)} subárea(s) criada(s): ' + '; '.join(criados)
    )
    return redirect('painel:central')


def _dados_botao(request):
    """Endpoint AJAX: retorna dados de uma categoria para edição inline."""
    cat_id = request.GET.get('id')
    cat = get_object_or_404(Categoria, pk=cat_id)
    return JsonResponse({
        'nome': cat.nome,
        'descricao': cat.descricao or '',
        'icone': cat.icone or '',
        'n_anexos': cat.anexos.count(),
        'n_conteudos': Conteudo.objects.filter(categoria=cat).count(),
    })


def _editar_botao(request):
    """Salva edições no botão (categoria) selecionado: nome, descrição,
    ícone (FA ou imagem) e anexo opcional."""
    cat_id = request.POST.get('editar_id')
    cat = get_object_or_404(Categoria, pk=cat_id)

    nome = request.POST.get('editar_nome', '').strip()
    if nome and nome != cat.nome:
        cat.nome = nome
        cat.slug = _slug_unico(Categoria, nome)

    descricao = request.POST.get('editar_descricao', '').strip()
    cat.descricao = descricao

    icone = request.POST.get('editar_icone', '').strip()
    if icone:
        cat.icone = icone

    icone_img = request.FILES.get('editar_icone_imagem')
    if icone_img:
        cat.icone_imagem.save(icone_img.name, icone_img, save=False)

    cat.save()

    anexo_file = request.FILES.get('editar_anexo')
    if anexo_file:
        Anexo.objects.create(
            categoria=cat,
            arquivo=anexo_file,
            nome=anexo_file.name,
        )

    messages.success(request, f'Botão "{cat.nome}" atualizado com sucesso.')
    return redirect('painel:central')


def _publicar(request):
    """Distribui o que foi composto no painel direito para todos os
    destinos marcados na árvore."""
    destino_ids = request.POST.getlist('destinos')
    destinos = list(Categoria.objects.filter(pk__in=destino_ids))
    if not destinos:
        messages.error(request, 'Marque pelo menos um botão de destino na árvore à esquerda.')
        return redirect('painel:central')

    titulo = request.POST.get('titulo', '').strip()
    url_externa = request.POST.get('url_externa', '').strip()
    url_video = request.POST.get('url_video', '').strip()
    nome_url = request.POST.get('nome_url', '').strip()
    tipo_manual = request.POST.get('tipo_conteudo', '').strip()
    icone_imagem = request.FILES.get('icone_imagem')
    imagem_destaque = request.FILES.get('imagem_destaque')
    resumo = request.POST.get('resumo', '').strip()
    corpo = request.POST.get('corpo', '').strip()
    texto_area = request.POST.get('texto_area', '').strip()
    status = request.POST.get('status', 'publicado')
    destaque = bool(request.POST.get('destaque'))
    recente = bool(request.POST.get('recente'))
    pulsante = bool(request.POST.get('pulsante'))
    botao_pulsante = bool(request.POST.get('botao_pulsante'))
    try:
        ordem = int(request.POST.get('ordem', '0') or 0)
    except ValueError:
        ordem = 0

    feitos = []
    conteudo_criado = False

    # 1. Conteúdo: cria uma única vez e vincula a todos os destinos.
    # Título é OPCIONAL — uma imagem de destaque, vídeo ou link já bastam
    # para criar o conteúdo (ex.: postar só uma imagem no "Destaque").
    tem_arquivos = any(k.startswith('arquivo_') for k in request.FILES)
    if titulo or url_externa or url_video or imagem_destaque:
        titulo_final = titulo or nome_url or url_externa
        if url_externa and not titulo:
            titulo_final = nome_url or url_externa
        # Tipo escolhido manualmente tem prioridade; sem escolha, o site deduz
        # pelo que foi preenchido (comportamento automático de sempre)
        tipo = tipo_manual or (
            'video' if url_video else
            'link' if url_externa else
            'documento' if tem_arquivos else 'post'
        )
        conteudo = Conteudo.objects.create(
            titulo=titulo_final,
            slug=_slug_unico(Conteudo, titulo_final),
            tipo=tipo,
            categoria=destinos[0],
            resumo=resumo,
            corpo=corpo,
            url_externa=url_externa,
            url_video=url_video,
            imagem_destaque=imagem_destaque,
            icone_manual=request.POST.get('icone_manual', '').strip(),
            icone_imagem=icone_imagem,
            texto_alinhamento=request.POST.get('texto_alinhamento', '').strip(),
            texto_fonte=request.POST.get('texto_fonte', '').strip(),
            texto_tamanho_fonte=(
                int(request.POST.get('texto_tamanho_fonte'))
                if request.POST.get('texto_tamanho_fonte', '').strip().isdigit() else None
            ),
            status=status,
            destaque=destaque,
            recente=recente,
            ordem=ordem,
            data_publicacao=_data_publicacao(request.POST),
        )
        # Anexos do conteúdo
        n_anexos = 0
        for i in range(50):
            f = request.FILES.get(f'arquivo_{i}')
            if f:
                Anexo.objects.create(
                    conteudo=conteudo,
                    arquivo=f,
                    nome=request.POST.get(f'nome_{i}', '').strip(),
                    ordem=n_anexos + 1,
                )
                n_anexos += 1
        # Vínculos em TODOS os destinos (o primeiro já é a categoria primária;
        # o vínculo registra ordem/pulsante por local)
        for d in destinos:
            Vinculo.objects.get_or_create(
                conteudo=conteudo, categoria=d,
                defaults={'ordem': ordem, 'pulsante': pulsante},
            )
        locais = ', '.join(d.nome for d in destinos)
        extra = f' com {n_anexos} anexo(s)' if n_anexos else ''
        nome_exibicao = conteudo.titulo or conteudo.get_tipo_display()
        feitos.append(f'Conteúdo "{nome_exibicao}"{extra} publicado em: {locais}')
        conteudo_criado = True

    # 2. Sem título: arquivos soltos viram anexos de cada categoria destino
    elif tem_arquivos:
        n = 0
        for i in range(50):
            f = request.FILES.get(f'arquivo_{i}')
            if not f:
                continue
            for d in destinos:
                f.seek(0)
                Anexo.objects.create(
                    categoria=d,
                    arquivo=f,
                    nome=request.POST.get(f'nome_{i}', '').strip(),
                    ordem=n + 1,
                )
            n += 1
        if n:
            feitos.append(f'{n} arquivo(s) anexado(s) em {len(destinos)} local(is)')

    # 3. Texto da área (Post acima dos botões) → descrição das categorias
    if texto_area:
        for d in destinos:
            d.descricao = texto_area
            d.save(update_fields=['descricao'])
        feitos.append(f'Texto da área atualizado em {len(destinos)} local(is)')

    # 4. Aparência dos botões marcados
    estilo_valores = {c: request.POST.get(f'estilo_{c}', '').strip() for c in CAMPOS_ESTILO}
    if any(estilo_valores.values()) or botao_pulsante:
        for d in destinos:
            estilo, _ = EstiloBotao.objects.get_or_create(categoria=d)
            for campo, valor in estilo_valores.items():
                if campo == 'tamanho_fonte':
                    estilo.tamanho_fonte = int(valor) if valor.isdigit() else None
                elif valor:
                    setattr(estilo, campo, valor)
            estilo.pulsante = botao_pulsante
            estilo.save()
        feitos.append(f'Aparência aplicada a {len(destinos)} botão(ões)')

    # 4b. Ícone dos BOTÕES/subbotões marcados (só quando NÃO foi criado um
    #     conteúdo — se um conteúdo foi criado, a imagem/ícone escolhido já
    #     virou o ícone DELE, no bloco 1). Assim, o MESMO campo "Ícone" do
    #     painel serve para o conteúdo (quando há título) ou para o botão
    #     (quando você só marcou botões, sem título) — nunca é desperdiçado,
    #     e por isso salvar só o ícone já é uma alteração válida.
    #     Aceita `icone_imagem` (campo principal) e `botao_icone_imagem`
    #     (compatibilidade com submissões antigas).
    icone_botao = icone_imagem or request.FILES.get('botao_icone_imagem')
    icone_manual_val = request.POST.get('icone_manual', '').strip()
    if not conteudo_criado and (icone_botao or icone_manual_val):
        for d in destinos:
            if icone_botao:
                # Reposiciona o cursor do arquivo a cada botão — o mesmo upload
                # é reaproveitado em todos os destinos e o cursor fica no fim
                # depois de cada gravação (senão os próximos gravariam vazio)
                icone_botao.seek(0)
                d.icone_imagem = icone_botao
            if icone_manual_val:
                d.icone = icone_manual_val
            d.save(update_fields=['icone_imagem', 'icone'])
        feitos.append(f'Ícone aplicado a {len(destinos)} botão(ões)')

    # 5. Visibilidade dos botões marcados na página inicial
    #    (barra superior do site / seção "Navegue por área")
    vis_menu = request.POST.get('vis_menu', '')
    vis_area = request.POST.get('vis_area', '')
    if vis_menu in ('sim', 'nao') or vis_area in ('sim', 'nao'):
        for d in destinos:
            if vis_menu in ('sim', 'nao'):
                d.mostrar_menu_superior = (vis_menu == 'sim')
            if vis_area in ('sim', 'nao'):
                d.mostrar_navegue_area = (vis_area == 'sim')
            d.save(update_fields=['mostrar_menu_superior', 'mostrar_navegue_area'])
        partes = []
        if vis_menu in ('sim', 'nao'):
            partes.append('barra superior: ' + ('aparece' if vis_menu == 'sim' else 'não aparece'))
        if vis_area in ('sim', 'nao'):
            partes.append('Navegue por área: ' + ('aparece' if vis_area == 'sim' else 'não aparece'))
        feitos.append(f'Visibilidade de {len(destinos)} botão(ões) atualizada ({"; ".join(partes)})')

    if feitos:
        messages.success(request, ' • '.join(feitos))
    else:
        messages.warning(
            request,
            'Nada para salvar: escolha pelo menos uma coisa para alterar nos '
            'botões marcados — um título/link/arquivo (novo conteúdo), um ícone, '
            'uma cor/tamanho, o texto da área ou a visibilidade.'
        )
    return redirect('painel:central')


# ── Tela 2: Conteúdo para modificar ou configurar ─────────────────────

@staff_member_required
def conteudos_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        ids = request.POST.getlist('sel')

        if action == 'salvar':
            pks = request.POST.getlist('pk')
            n = 0
            for pk in pks:
                try:
                    c = Conteudo.objects.get(pk=pk)
                except Conteudo.DoesNotExist:
                    continue
                c.destaque = bool(request.POST.get(f'destaque_{pk}'))
                c.recente = bool(request.POST.get(f'recente_{pk}'))
                try:
                    c.ordem = int(request.POST.get(f'ordem_{pk}', c.ordem) or 0)
                except ValueError:
                    pass
                c.save(update_fields=['destaque', 'recente', 'ordem'])
                n += 1
            messages.success(request, f'{n} conteúdo(s) atualizado(s). As mudanças já estão no site.')

        elif action == 'remover_vinculos' and ids:
            # Tira o conteúdo de todos os locais do site (vínculos extras
            # e categoria primária), mas NÃO exclui o conteúdo — ele
            # continua no admin e pode ser vinculado de novo depois.
            n_vinc, _ = Vinculo.objects.filter(conteudo_id__in=ids).delete()
            Conteudo.objects.filter(pk__in=ids).update(categoria=None)
            messages.success(
                request,
                f'{len(ids)} conteúdo(s) removido(s) de todos os botões do site '
                f'({n_vinc} vínculo(s) desfeito(s)). Os conteúdos continuam '
                'salvos e podem ser vinculados novamente.'
            )

        elif action == 'excluir' and ids:
            n = Conteudo.objects.filter(pk__in=ids).count()
            Conteudo.objects.filter(pk__in=ids).delete()
            messages.success(request, f'{n} conteúdo(s) excluído(s) permanentemente.')

        elif not ids and action in ('remover_vinculos', 'excluir'):
            messages.error(request, 'Selecione pelo menos um conteúdo.')

        # Preserva busca/página ao voltar
        params = []
        if request.POST.get('busca'):
            params.append(f"busca={request.POST['busca']}")
        if request.POST.get('pagina'):
            params.append(f"page={request.POST['pagina']}")
        sufixo = ('?' + '&'.join(params)) if params else ''
        return redirect(f"/admin/painel-central/conteudos/{sufixo}")

    busca = request.GET.get('busca', '').strip()
    qs = Conteudo.objects.select_related(
        'categoria', 'categoria__categoria_pai'
    ).annotate(n_vinculos=Count('vinculos')).order_by('-data_publicacao')
    if busca:
        # Busca tolerante: ignora acentos e maiúsculas/minúsculas
        from conteudo.busca_utils import filtrar_por_texto
        pks = [c.pk for c in filtrar_por_texto(
            Conteudo.objects.all(), busca, ('titulo', 'resumo'))]
        qs = qs.filter(pk__in=pks)

    paginator = Paginator(qs, 60)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        'title': 'Conteúdo para modificar ou configurar',
        'page': page,
        'busca': busca,
        'total': paginator.count,
        'has_permission': True,
        'is_app_index': True,
    }
    return render(request, 'admin/painel_conteudos.html', context)
