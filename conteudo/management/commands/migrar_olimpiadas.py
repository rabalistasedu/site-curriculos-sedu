"""
Migra a categoria "Olimpíadas" a partir da página:
https://curriculo.sedu.es.gov.br/curriculo/olimpiadas/

A página do WordPress tem apenas 9 accordions descritivos (com imagens
promocionais de cada olimpíada), sem PDFs para download — cada olimpíada
é apresentada como um card informativo com nome e imagem.

Este comando:
- Renomeia a categoria "Olimpíadas e Competições" para "Olimpíadas"
- Adiciona o texto introdutório oficial
- Cria/atualiza 9 subcategorias (uma por olimpíada)
- Cria 1 link por olimpíada apontando para a página oficial no WordPress
  (por enquanto — quando surgirem PDFs ou páginas nativas, é só editar
  aqui e re-rodar, é idempotente)

Idempotente e autossuficiente.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from conteudo.models import Categoria, Conteudo

URL_ORIGEM = 'https://curriculo.sedu.es.gov.br/curriculo/olimpiadas/'

DESCRICAO = (
    '<p>As <strong>Olimpíadas do Conhecimento</strong> são essenciais para o '
    'desenvolvimento educacional e pessoal dos estudantes. Elas incentivam o '
    'aprofundamento do conhecimento além do currículo tradicional, promovendo o '
    'interesse e a paixão por áreas específicas, e desenvolvem habilidades '
    'críticas como pensamento analítico e resolução de problemas.</p>'
    '<p>Além disso, essas competições fomentam disciplina, dedicação e '
    'resiliência, essenciais para o crescimento pessoal. Ao promover um espírito '
    'de competição saudável e colaboração, as Olimpíadas enriquecem o aprendizado '
    'e criam um ambiente educacional dinâmico e inspirador, além de revelarem '
    'verdadeiros talentos para o desenvolvimento do nosso Estado e da nossa Nação.</p>'
)

# (slug_fixo, nome, icone, ordem, titulo_doc, url_saiba_mais)
SUBCATEGORIAS = [
    ('oli-fisica-obf', 'Olimpíada Brasileira de Física (OBF)', 'fas fa-atom', 1,
     'OBF — Olimpíada Brasileira de Física',
     'https://www.sbfisica.org.br/v1/olimpiada/'),
    ('oli-fisica-obfep', 'Olimpíada Brasileira de Física das Escolas Públicas (OBFEP)', 'fas fa-magnet', 2,
     'OBFEP — Olimpíada Brasileira de Física das Escolas Públicas',
     'https://www.sbfisica.org.br/v1/olimpiada/'),
    ('oli-tesouro-direto', 'Olimpíada do Tesouro Direto de Educação Financeira (OLITEF)', 'fas fa-coins', 3,
     'OLITEF — Olimpíada do Tesouro Direto de Educação Financeira',
     'https://olimpiadatesourodireto.com.br/'),
    ('oli-meninas-olimpiadas', 'Movimento Meninas Olímpiadas', 'fas fa-venus', 4,
     'Movimento Meninas Olímpiadas',
     'https://meninasolimpicas.org/'),
    ('oli-empreendedorismo', 'Olimpíada do Empreendedorismo', 'fas fa-lightbulb', 5,
     'Olimpíada do Empreendedorismo',
     'https://www.olimpiadadoempreendedorismo.com.br/'),
    ('oli-biologia-sintetica', 'Olimpíada Brasileira de Biologia Sintética', 'fas fa-dna', 6,
     'Olimpíada Brasileira de Biologia Sintética',
     'https://obbs.org.br/'),
    ('oli-jovem-cientista', 'Prêmio Jovem Cientista', 'fas fa-microscope', 7,
     'Prêmio Jovem Cientista',
     'https://cnpq.br/premio-jovem-cientista'),
    ('oli-bem-publico', 'Olimpíada do Bem Público (FGV)', 'fas fa-handshake', 8,
     'Olimpíada do Bem Público — FGV',
     'https://olimpiadadobempublico.fgv.br/'),
    ('oli-jovem-senador', 'Programa Jovem Senador', 'fas fa-landmark', 9,
     'Programa Jovem Senador',
     'https://www12.senado.leg.br/jovemsenador'),
]

# Mapeia títulos antigos → slug de destino, para MOVER itens que já existiam
TITULOS_ANTIGOS_PARA_SLUG = {
    'Olimpíada Brasileira de Física — OBF': 'oli-fisica-obf',
    'Olimpíada Brasileira de Física das Escolas Públicas — OBFEP': 'oli-fisica-obfep',
    'Olimpíada do Tesouro Direto de Educação Financeira — OLITEF': 'oli-tesouro-direto',
    'Olimpíada do Empreendedorismo': 'oli-empreendedorismo',
    'Olimpíada Brasileira de Biologia Sintética': 'oli-biologia-sintetica',
    'Olimpíada do Bem Público — FGV': 'oli-bem-publico',
    'Movimento Meninas Olímpicas': 'oli-meninas-olimpiadas',
    'Prêmio Jovem Cientista': 'oli-jovem-cientista',
    'Programa Jovem Senador': 'oli-jovem-senador',
}

# Subcategorias ANTIGAS a remover se ficarem vazias
SLUGS_SUBS_ANTIGAS = [
    'olimpiadas-de-fisica',
    'olimpiadas-de-matematica',
    'olimpiadas-de-biologia',
    'educacao-financeira',
    'empreendedorismo',
    'outras-competicoes',
]

# Títulos antigos que devem ser removidos (foram substituídos por novos itens)
TITULOS_DUPLICADOS_ANTIGOS = [
    'Movimento Meninas Olímpicas',  # antigo — o novo tem grafia "Olímpiadas"
]


class Command(BaseCommand):
    help = 'Migra/organiza a categoria "Olimpíadas" do WordPress'

    def handle(self, *args, **options):
        cat_principal = Categoria.objects.filter(slug='olimpiadas-e-competicoes').first()
        if not cat_principal:
            cat_principal, _ = Categoria.objects.get_or_create(
                slug='olimpiadas-e-competicoes',
                defaults={'nome': 'Olimpíadas', 'ordem': 7, 'ativa': True}
            )

        # Renomeia para "Olimpíadas" e atualiza descrição
        mudou_cat = False
        if cat_principal.nome != 'Olimpíadas':
            cat_principal.nome = 'Olimpíadas'
            mudou_cat = True
        if not cat_principal.descricao or 'Olimpíadas do Conhecimento' not in cat_principal.descricao:
            cat_principal.descricao = DESCRICAO
            mudou_cat = True
        if not cat_principal.icone:
            cat_principal.icone = 'fas fa-trophy'
            mudou_cat = True
        if mudou_cat:
            cat_principal.save()
        self.stdout.write(f'  ✔ categoria: {cat_principal.nome}')

        criadas = 0
        movidos = 0
        criados_docs = 0
        subs_por_slug = {}

        # Cria/garante 9 subcategorias
        for slug_sub, nome_sub, icone_sub, ordem_sub, titulo_doc, url_doc in SUBCATEGORIAS:
            sub, criada = Categoria.objects.get_or_create(
                slug=slug_sub,
                defaults={
                    'nome': nome_sub,
                    'icone': icone_sub,
                    'categoria_pai': cat_principal,
                    'ordem': ordem_sub,
                    'ativa': True,
                }
            )
            if not criada:
                # atualiza nome/ícone/ordem se mudaram
                m = False
                if sub.nome != nome_sub: sub.nome = nome_sub; m = True
                if sub.icone != icone_sub: sub.icone = icone_sub; m = True
                if sub.categoria_pai_id != cat_principal.id: sub.categoria_pai = cat_principal; m = True
                if sub.ordem != ordem_sub: sub.ordem = ordem_sub; m = True
                if m: sub.save()
            else:
                criadas += 1
                self.stdout.write(f'    ✔ subcategoria criada: {nome_sub}')
            subs_por_slug[slug_sub] = sub

        # MOVE os itens antigos que já existiam (por título) para a nova subcategoria correta
        for titulo_antigo, slug_destino in TITULOS_ANTIGOS_PARA_SLUG.items():
            doc = Conteudo.objects.filter(titulo=titulo_antigo).first()
            if not doc: continue
            sub = subs_por_slug[slug_destino]
            if doc.categoria_id != sub.id:
                doc.categoria = sub
                doc.save()
                movidos += 1
                self.stdout.write(f'      → movido: {titulo_antigo[:55]} ⇒ {sub.nome[:40]}')

        # Cria 1 link "Saiba mais" por olimpíada, se ainda não houver conteúdo naquela subcategoria
        for slug_sub, nome_sub, icone_sub, ordem_sub, titulo_doc, url_doc in SUBCATEGORIAS:
            sub = subs_por_slug[slug_sub]
            if Conteudo.objects.filter(categoria=sub).exists():
                continue
            # cria link
            base_slug = ('oli-' + slug_sub[4:])[:50]
            slug_final = base_slug
            i = 2
            while Conteudo.objects.filter(slug=slug_final).exists():
                slug_final = f'{base_slug[:46]}-{i}'
                i += 1
            Conteudo.objects.create(
                titulo=titulo_doc,
                slug=slug_final,
                tipo='link',
                status='publicado',
                url_externa=url_doc,
                categoria=sub,
                data_publicacao=timezone.now(),
                resumo='Página oficial da olimpíada.',
            )
            criados_docs += 1
            self.stdout.write(f'      + criado link: {titulo_doc[:55]}')

        # Remove subcategorias antigas vazias
        removidas = 0
        for slug_antigo in SLUGS_SUBS_ANTIGAS:
            sub_antiga = Categoria.objects.filter(slug=slug_antigo, categoria_pai=cat_principal).first()
            if sub_antiga and not Conteudo.objects.filter(categoria=sub_antiga).exists():
                sub_antiga.delete()
                removidas += 1
                self.stdout.write(f'      × removida subcat vazia antiga: {slug_antigo}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: {criadas} subcategorias criadas, '
            f'{movidos} itens movidos, {criados_docs} links criados, '
            f'{removidas} subcats antigas removidas.'
        ))
