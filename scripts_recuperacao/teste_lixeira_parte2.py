"""Parte 2: testa Estrutura de Arvores, Organizador, Django Admin UI completo,
e confirma que o site existente (132 categorias, 588+ conteudos) nao foi afetado."""
from django.test import Client
from django.contrib.auth import get_user_model
from conteudo.models import Categoria, Conteudo

User = get_user_model()
u = User.objects.filter(is_superuser=True).first()
c = Client()
c.force_login(u)

resultados = []


def check(nome, condicao):
    resultados.append((nome, bool(condicao)))


# ============ BASELINE: contagens atuais do site real (nao deve ter mudado) ============
total_cat_antes = Categoria.objects.count()
total_cont_antes = Conteudo.objects.count()
check('Total de categorias ativas parece razoavel (>100)', total_cat_antes > 100)
check('Total de conteudos ativos parece razoavel (>500)', total_cont_antes > 500)

resp_home = c.get('/')
check('Home carrega normalmente (200)', resp_home.status_code == 200)
resp_busca = c.get('/busca/?q=curriculo')
check('Busca carrega normalmente (200)', resp_busca.status_code == 200)

# ============ TESTE: Estrutura de Arvores _api_excluir (categoria) ============
cat_ea = Categoria.objects.create(nome='TESTE EA Categoria', slug='teste-ea-categoria', ativa=True)
resp = c.post('/admin/estrutura-arvores/api/', {'action': 'excluir', 'id': str(cat_ea.pk)})
check('Estrutura Arvores excluir categoria responde 200', resp.status_code == 200)
check('Categoria sumiu de objects (foi pra lixeira)', not Categoria.objects.filter(pk=cat_ea.pk).exists())
check('Categoria continua em todos_objetos (recuperavel)', Categoria.todos_objetos.filter(pk=cat_ea.pk).exists())

# ============ TESTE: Estrutura de Arvores _api_excluir_conteudo ============
cont_ea = Conteudo.objects.create(titulo='TESTE EA Conteudo', slug='teste-ea-conteudo', status='publicado', tipo='pagina')
resp2 = c.post('/admin/estrutura-arvores/api/', {'action': 'excluir_conteudo', 'conteudo_id': str(cont_ea.pk)})
check('Estrutura Arvores excluir conteudo responde 200', resp2.status_code == 200)
check('Conteudo sumiu de objects (foi pra lixeira)', not Conteudo.objects.filter(pk=cont_ea.pk).exists())
check('Conteudo continua em todos_objetos (recuperavel)', Conteudo.todos_objetos.filter(pk=cont_ea.pk).exists())

# ============ TESTE: Organizador excluir_conteudo ============
cat_org = Categoria.objects.create(nome='TESTE ORG Categoria', slug='teste-org-categoria', ativa=True)
cont_org = Conteudo.objects.create(titulo='TESTE ORG Conteudo', slug='teste-org-conteudo', categoria=cat_org, status='publicado', tipo='pagina')
resp3 = c.post('/admin/organizar/', {'action': 'excluir_conteudo', 'conteudo_id': str(cont_org.pk), 'origem_cat': str(cat_org.pk)})
check('Organizador excluir_conteudo redireciona (302)', resp3.status_code == 302)
check('Conteudo do Organizador sumiu de objects (foi pra lixeira)', not Conteudo.objects.filter(pk=cont_org.pk).exists())
check('Conteudo do Organizador continua em todos_objetos', Conteudo.todos_objetos.filter(pk=cont_org.pk).exists())

# ============ TESTE: Django Admin - delete confirmation (single object) ============
cat_dj = Categoria.objects.create(nome='TESTE DJ Categoria', slug='teste-dj-categoria', ativa=True)
resp_confirm = c.get(f'/admin/conteudo/categoria/{cat_dj.pk}/delete/')
check('Pagina de confirmacao de exclusao (Django Admin) carrega 200', resp_confirm.status_code == 200)
resp_delete = c.post(f'/admin/conteudo/categoria/{cat_dj.pk}/delete/', {'post': 'yes'})
check('POST confirmar exclusao redireciona (302)', resp_delete.status_code == 302)
check('Categoria sumiu de objects apos delete via Admin UI', not Categoria.objects.filter(pk=cat_dj.pk).exists())
check('Categoria continua em todos_objetos (recuperavel)', Categoria.todos_objetos.filter(pk=cat_dj.pk).exists())

# ============ TESTE: Django Admin - bulk delete_selected (Conteudo) via changelist ============
cont_bulk1 = Conteudo.objects.create(titulo='TESTE BULK 1', slug='teste-bulk-1', status='publicado', tipo='pagina')
cont_bulk2 = Conteudo.objects.create(titulo='TESTE BULK 2', slug='teste-bulk-2', status='publicado', tipo='pagina')
resp_bulk = c.post('/admin/conteudo/conteudo/', {
    'action': 'delete_selected',
    '_selected_action': [str(cont_bulk1.pk), str(cont_bulk2.pk)],
})
check('Bulk delete_selected (Conteudo) responde 200/302', resp_bulk.status_code in (200, 302))
check('Bulk 1 sumiu de objects', not Conteudo.objects.filter(pk=cont_bulk1.pk).exists())
check('Bulk 2 sumiu de objects', not Conteudo.objects.filter(pk=cont_bulk2.pk).exists())
check('Bulk 1 continua em todos_objetos (recuperavel)', Conteudo.todos_objetos.filter(pk=cont_bulk1.pk).exists())
check('Bulk 2 continua em todos_objetos (recuperavel)', Conteudo.todos_objetos.filter(pk=cont_bulk2.pk).exists())

# ============ TESTE: Django Admin changelist nao mostra itens da lixeira ============
resp_cl = c.get('/admin/conteudo/categoria/')
html_cl = resp_cl.content.decode('utf-8')
check('Changelist Categoria NAO mostra "TESTE EA Categoria" (esta na lixeira)', 'TESTE EA Categoria' not in html_cl)
check('Changelist Categoria NAO mostra "TESTE DJ Categoria" (esta na lixeira)', 'TESTE DJ Categoria' not in html_cl)

resp_cl2 = c.get('/admin/conteudo/conteudo/')
html_cl2 = resp_cl2.content.decode('utf-8')
check('Changelist Conteudo NAO mostra "TESTE EA Conteudo" (esta na lixeira)', 'TESTE EA Conteudo' not in html_cl2)
check('Changelist Conteudo NAO mostra "TESTE BULK 1" (esta na lixeira)', 'TESTE BULK 1' not in html_cl2)

# ============ CONFIRMACAO FINAL: nada do site real mudou ============
total_cat_depois = Categoria.objects.count()
total_cont_depois = Conteudo.objects.count()
check('Contagem de categorias ativas nao mudou (baseline preservado)', total_cat_antes == total_cat_depois)
check('Contagem de conteudos ativos nao mudou (baseline preservado)', total_cont_antes == total_cont_depois)

resp_home2 = c.get('/')
check('Home ainda carrega normalmente depois de tudo (200)', resp_home2.status_code == 200)

# ============ LIMPEZA (hard delete de tudo criado neste teste) ============
Categoria.todos_objetos.filter(slug__in=[
    'teste-ea-categoria', 'teste-org-categoria', 'teste-dj-categoria',
]).hard_delete()
Conteudo.todos_objetos.filter(slug__in=[
    'teste-ea-conteudo', 'teste-org-conteudo', 'teste-bulk-1', 'teste-bulk-2',
]).hard_delete()

# ============ RESULTADO ============
with open('scripts_recuperacao/resultado_teste_lixeira_parte2.txt', 'w', encoding='utf-8') as f:
    falhas = 0
    for nome, ok in resultados:
        status = 'OK' if ok else 'FALHOU'
        if not ok:
            falhas += 1
        f.write(f'[{status}] {nome}\n')
    f.write(f'\nTotal: {len(resultados)} testes, {falhas} falha(s)\n')
print(f'Total: {len(resultados)} testes, {falhas} falha(s)')
