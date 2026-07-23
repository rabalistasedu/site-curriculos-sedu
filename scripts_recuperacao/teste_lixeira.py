"""Teste ponta a ponta do sistema de lixeira — roda via exec() no shell."""
from datetime import timedelta
from django.test import Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from conteudo.models import Categoria, Conteudo, Anexo
from conteudo.admin_views import _purgar_lixeira_expirada

User = get_user_model()
u = User.objects.filter(is_superuser=True).first()
c = Client()
c.force_login(u)

resultados = []


def check(nome, condicao):
    resultados.append((nome, bool(condicao)))


# ============ SETUP ============
pai = Categoria.objects.create(nome='TESTE LIXEIRA Pai', slug='teste-lixeira-pai', ativa=True)
filho = Categoria.objects.create(nome='TESTE LIXEIRA Filho', slug='teste-lixeira-filho', categoria_pai=pai, ativa=True)
neto = Categoria.objects.create(nome='TESTE LIXEIRA Neto', slug='teste-lixeira-neto', categoria_pai=filho, ativa=True)
cont = Conteudo.objects.create(titulo='TESTE LIXEIRA Conteudo', slug='teste-lixeira-conteudo', categoria=filho, status='publicado', tipo='pagina')
anexo = Anexo.objects.create(categoria=filho, url='https://exemplo.com/teste', nome='anexo teste')

# ============ TESTE 1: Model.delete() em Categoria trashea subarvore inteira ============
pai.delete()
check('Pai sumiu de Categoria.objects (filtrado)', not Categoria.objects.filter(pk=pai.pk).exists())
check('Pai continua em todos_objetos', Categoria.todos_objetos.filter(pk=pai.pk).exists())
check('Filho tambem foi trashado (cascata)', not Categoria.objects.filter(pk=filho.pk).exists())
check('Neto tambem foi trashado (cascata)', not Categoria.objects.filter(pk=neto.pk).exists())
pai.refresh_from_db()
check('excluido_em preenchido no pai', pai.excluido_em is not None)

# Conteudo NAO deve ter sido orfanado (fica ligado, diferente do SET_NULL de verdade)
cont.refresh_from_db()
check('Conteudo continua com categoria_id apontando pro filho (nao orfanado)', cont.categoria_id == filho.pk)
check('Conteudo continua visivel em Conteudo.objects (nao foi trashado junto)', Conteudo.objects.filter(pk=cont.pk).exists())

# Anexo tambem nao deve ter sido tocado
check('Anexo continua existindo', Anexo.objects.filter(pk=anexo.pk).exists())

# ============ TESTE 2: pagina de categoria trashada retorna 404 no site ============
resp = c.get('/categoria/teste-lixeira-pai/')
check('Pagina da categoria trashada retorna 404', resp.status_code == 404)

# ============ TESTE 3: Lixeira lista o item (so o topo da subarvore) ============
resp = c.get('/admin/lixeira/')
check('Tela da lixeira carrega (200)', resp.status_code == 200)
html = resp.content.decode('utf-8')
check('Categoria trashada aparece na lixeira', 'TESTE LIXEIRA Pai' in html)
check('Filho NAO aparece separado na lixeira (so o topo)', html.count('TESTE LIXEIRA Filho') == 0 or 'subbot' in html.lower())

# ============ TESTE 4: Restaurar via view ============
resp = c.post('/admin/lixeira/', {'action': 'restaurar', 'tipo': 'categoria', 'id': str(pai.pk)})
check('POST restaurar redireciona (302)', resp.status_code == 302)
check('Pai restaurado, aparece em Categoria.objects de novo', Categoria.objects.filter(pk=pai.pk).exists())
check('Filho tambem restaurado junto', Categoria.objects.filter(pk=filho.pk).exists())
check('Neto tambem restaurado junto', Categoria.objects.filter(pk=neto.pk).exists())

resp2 = c.get('/categoria/teste-lixeira-pai/')
check('Pagina da categoria volta a funcionar (200) apos restaurar', resp2.status_code == 200)

# ============ TESTE 5: Conteudo individual vai pra lixeira e volta ============
cont.delete()
check('Conteudo sumiu de Conteudo.objects apos delete()', not Conteudo.objects.filter(pk=cont.pk).exists())
cont.refresh_from_db()
check('Conteudo tem excluido_em preenchido', cont.excluido_em is not None)

resp3 = c.post('/admin/lixeira/', {'action': 'restaurar', 'tipo': 'conteudo', 'id': str(cont.pk)})
check('Restaurar conteudo redireciona (302)', resp3.status_code == 302)
check('Conteudo restaurado', Conteudo.objects.filter(pk=cont.pk).exists())

# ============ TESTE 6: Excluir definitivo pela tela (hard delete de verdade) ============
cont.delete()  # vai pra lixeira de novo
resp4 = c.post('/admin/lixeira/', {'action': 'excluir_definitivo', 'tipo': 'conteudo', 'id': str(cont.pk)})
check('Excluir definitivo redireciona (302)', resp4.status_code == 302)
check('Conteudo NAO existe nem em todos_objetos (excluido de verdade)', not Conteudo.todos_objetos.filter(pk=cont.pk).exists())

# ============ TESTE 7: Purga automatica (30+ dias) ============
pai.delete()
Categoria.todos_objetos.filter(pk__in=[pai.pk, filho.pk, neto.pk]).update(
    excluido_em=timezone.now() - timedelta(days=35)
)
n_cats, n_conts = _purgar_lixeira_expirada()
check(f'Purga contou 3 categorias expiradas (contou {n_cats})', n_cats == 3)
check('Pai nao existe mais nem em todos_objetos (purgado de verdade)', not Categoria.todos_objetos.filter(pk=pai.pk).exists())
check('Filho nao existe mais', not Categoria.todos_objetos.filter(pk=filho.pk).exists())
check('Neto nao existe mais', not Categoria.todos_objetos.filter(pk=neto.pk).exists())

# ============ TESTE 8: item recem-trashado NAO e purgado (dentro do prazo) ============
c2 = Categoria.objects.create(nome='TESTE LIXEIRA Recente', slug='teste-lixeira-recente', ativa=True)
c2.delete()
n_cats2, n_conts2 = _purgar_lixeira_expirada()
check('Item recente NAO foi purgado (ainda dentro do prazo)', Categoria.todos_objetos.filter(pk=c2.pk, excluido_em__isnull=False).exists())

# ============ TESTE 9: Excluir permanentemente (Painel Central Tela 2) continua de verdade ============
cont_perm = Conteudo.objects.create(titulo='TESTE LIXEIRA Perm', slug='teste-lixeira-perm', status='publicado', tipo='pagina')
resp5 = c.post('/admin/painel-central/conteudos/', {'action': 'excluir', 'sel': [str(cont_perm.pk)]})
check('Painel Central excluir permanente responde (302 ou 200)', resp5.status_code in (200, 302))
check('Conteudo NAO existe nem em todos_objetos (hard delete de verdade)', not Conteudo.todos_objetos.filter(pk=cont_perm.pk).exists())

# ============ LIMPEZA ============
Categoria.todos_objetos.filter(slug__in=['teste-lixeira-pai', 'teste-lixeira-filho', 'teste-lixeira-neto', 'teste-lixeira-recente']).delete()
Categoria.todos_objetos.filter(pk__in=[c2.pk]).hard_delete()
Conteudo.todos_objetos.filter(slug__in=['teste-lixeira-conteudo', 'teste-lixeira-perm']).hard_delete()
Anexo.objects.filter(pk=anexo.pk).delete()

# ============ RESULTADO ============
with open('scripts_recuperacao/resultado_teste_lixeira.txt', 'w', encoding='utf-8') as f:
    falhas = 0
    for nome, ok in resultados:
        status = 'OK' if ok else 'FALHOU'
        if not ok:
            falhas += 1
        f.write(f'[{status}] {nome}\n')
    f.write(f'\nTotal: {len(resultados)} testes, {falhas} falha(s)\n')
print(f'Total: {len(resultados)} testes, {falhas} falha(s) - ver resultado_teste_lixeira.txt')
