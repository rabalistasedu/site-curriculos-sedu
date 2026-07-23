from django.test import Client
from django.contrib.auth import get_user_model
from conteudo.models import Categoria, Conteudo

User = get_user_model()
u = User.objects.filter(is_superuser=True).first()
c = Client()
c.force_login(u)

cat_ea = Categoria.objects.create(nome='TESTE EA Categoria', slug='teste-ea-categoria', ativa=True)
c.post('/admin/estrutura-arvores/api/', {'action': 'excluir', 'id': str(cat_ea.pk)})

cat_org = Categoria.objects.create(nome='TESTE ORG Categoria', slug='teste-org-categoria', ativa=True)

cat_dj = Categoria.objects.create(nome='TESTE DJ Categoria', slug='teste-dj-categoria', ativa=True)
resp_delete = c.post(f'/admin/conteudo/categoria/{cat_dj.pk}/delete/', {'post': 'yes'})

cat_dj.refresh_from_db()
with open('scripts_recuperacao/debug_dj_resultado.txt', 'w', encoding='utf-8') as f:
    f.write(f'excluido_em de cat_dj apos delete: {cat_dj.excluido_em}\n')
    f.write(f'Em Categoria.objects (filtrado)? {Categoria.objects.filter(pk=cat_dj.pk).exists()}\n')
    f.write(f'Em Categoria.todos_objetos? {Categoria.todos_objetos.filter(pk=cat_dj.pk).exists()}\n')

    resp_cl = c.get('/admin/conteudo/categoria/')
    html_cl = resp_cl.content.decode('utf-8')
    f.write(f'Changelist status: {resp_cl.status_code}\n')
    f.write(f'"TESTE DJ Categoria" no html? {"TESTE DJ Categoria" in html_cl}\n')

    idx = html_cl.find('TESTE DJ')
    if idx != -1:
        f.write('--- CONTEXTO ao redor da ocorrencia ---\n')
        f.write(html_cl[max(0, idx-300):idx+300])
        f.write('\n')
    else:
        f.write('Nao encontrado no html (delete funcionou corretamente neste script isolado)\n')

# limpeza
Categoria.todos_objetos.filter(slug__in=['teste-ea-categoria', 'teste-org-categoria', 'teste-dj-categoria']).hard_delete()
print('feito, ver debug_dj_resultado.txt')
