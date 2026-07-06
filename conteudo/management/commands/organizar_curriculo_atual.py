"""
Organiza a subcategoria "Currículo Atual" (dentro de Documentos
Curriculares) em sub-botões por etapa de ensino, como os acordeões do
site antigo:

  Currículo Atual
    ├─ Educação Infantil
    ├─ Ensino Fundamental — Anos Iniciais
    ├─ Ensino Fundamental — Anos Finais
    └─ Ensino Médio

Os documentos gerais (Resoluções e Tema Integrador) permanecem
diretamente em "Currículo Atual". Cada volume vai para a etapa
correspondente, identificada pelo título.

Idempotente: pode rodar várias vezes sem duplicar nada.
"""
from django.core.management.base import BaseCommand
from conteudo.models import Categoria, Conteudo

# (slug_fixo, nome, icone, ordem)
ETAPAS = [
    ('ca-educacao-infantil', 'Educação Infantil', 'fas fa-shapes', 1),
    ('ca-ef-anos-iniciais', 'Ensino Fundamental — Anos Iniciais', 'fas fa-child-reaching', 2),
    ('ca-ef-anos-finais', 'Ensino Fundamental — Anos Finais', 'fas fa-user-graduate', 3),
    ('ca-ensino-medio', 'Ensino Médio', 'fas fa-graduation-cap', 4),
]


def etapa_do_titulo(titulo):
    """Decide em qual etapa o documento entra, pelo título.
    Retorna o slug da etapa, ou None se for documento geral."""
    t = titulo.lower()
    # Resoluções e Tema Integrador são documentos gerais (ficam no topo,
    # fora das etapas), como no site antigo — mesmo que citem uma etapa.
    if t.startswith('resolução') or t.startswith('resolucao') or 'tema integrador' in t:
        return None
    if 'anos iniciais' in t:
        return 'ca-ef-anos-iniciais'
    if 'anos finais' in t:
        return 'ca-ef-anos-finais'
    if 'educação infantil' in t or 'educacao infantil' in t:
        return 'ca-educacao-infantil'
    if titulo.startswith('Currículo EM') or 'ensino médio' in t or 'ensino medio' in t:
        return 'ca-ensino-medio'
    # Resoluções e Tema Integrador ficam em "Currículo Atual"
    return None


class Command(BaseCommand):
    help = 'Organiza Currículo Atual em sub-botões por etapa de ensino'

    def handle(self, *args, **options):
        try:
            pai = Categoria.objects.get(slug='curriculo-atual')
        except Categoria.DoesNotExist:
            self.stderr.write('❌ Subcategoria "curriculo-atual" não encontrada. '
                              'Rode "python manage.py migrar_conteudo" primeiro.')
            return

        # Cria as etapas (filhas de Currículo Atual)
        etapas_por_slug = {}
        for slug, nome, icone, ordem in ETAPAS:
            etapa, criada = Categoria.objects.get_or_create(
                slug=slug,
                defaults={
                    'nome': nome,
                    'icone': icone,
                    'categoria_pai': pai,
                    'ordem': ordem,
                    'ativa': True,
                }
            )
            etapas_por_slug[slug] = etapa
            self.stdout.write(('  ✔ criada' if criada else '  — já existe') + f': {nome}')

        # Junta os documentos de "Currículo Atual" e das etapas (para reorganizar
        # mesmo que já tenham sido movidos numa execução anterior)
        docs = list(Conteudo.objects.filter(categoria=pai))
        for etapa in etapas_por_slug.values():
            docs += list(Conteudo.objects.filter(categoria=etapa))

        movidos = 0
        gerais = 0
        for doc in docs:
            slug_destino = etapa_do_titulo(doc.titulo)
            if slug_destino:
                destino = etapas_por_slug[slug_destino]
            else:
                destino = pai  # documento geral
                gerais += 1
            if doc.categoria_id != destino.id:
                doc.categoria = destino
                doc.save()
                movidos += 1
                self.stdout.write(f'      → {doc.titulo[:55]}  ⇒  {destino.nome}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Concluído: {len(ETAPAS)} etapas, {movidos} documentos reorganizados, '
            f'{gerais} documentos gerais mantidos em "Currículo Atual".'
        ))
