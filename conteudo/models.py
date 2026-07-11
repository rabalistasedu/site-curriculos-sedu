from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# Mapa de palavras-chave → ícone criativo (a primeira correspondência vence).
# Usado tanto por Conteudo quanto por Categoria para escolher um ícone temático
# a partir do texto, em vez de uma seta/pasta genérica.
ICONES_CRIATIVOS = [
    (('computa', 'tecnologia', 'computacional', 'digital', 'robótic', 'robotic'), 'fas fa-microchip'),
    (('vídeo', 'video', 'webinar', 'live', 'aula gravada'), 'fas fa-play-circle'),
    (('revista', 'diálogos', 'dialogos', 'boletim', 'jornal'), 'fas fa-newspaper'),
    (('notícia', 'noticia', 'informe'), 'fas fa-bullhorn'),
    (('leitura', 'leitores', 'literár', 'literar', 'biblioteca'), 'fas fa-book-open-reader'),
    (('caderno',), 'fas fa-book-open'),
    (('ementa',), 'fas fa-clipboard-list'),
    (('mapa', 'progress'), 'fas fa-map'),
    (('itinerári', 'itinerari', 'ifas', 'rota', 'percurso'), 'fas fa-route'),
    (('orientaç', 'orientac', 'diretriz'), 'fas fa-compass'),
    (('guia', 'oportunidade'), 'fas fa-signs-post'),
    (('sequência', 'sequencia', 'plano de curso', 'planos de curso'), 'fas fa-layer-group'),
    (('recomposiç', 'recomposic', 'rotina', 'nivelamento', 'diagnóstic', 'diagnostic', ' ama'), 'fas fa-arrows-rotate'),
    (('prática', 'pratica', 'experiment', 'laborat'), 'fas fa-flask'),
    (('projeto de vida', 'protagonismo'), 'fas fa-seedling'),
    (('interativo',), 'fas fa-hand-pointer'),
    (('material', 'materiais', 'apoio', 'recurso'), 'fas fa-toolbox'),
    (('paz',), 'fas fa-dove'),
    (('música', 'musica'), 'fas fa-music'),
    (('ambient', 'sustentá', 'sustenta', 'ecolog'), 'fas fa-leaf'),
    (('sucesso escolar', 'aprovaç', 'aprovac', 'geepei', 'proeti', 'pipat'), 'fas fa-graduation-cap'),
    (('indígena', 'indigena'), 'fas fa-feather'),
    (('quilombola',), 'fas fa-drum'),
    (('campo', 'rural', 'agrícol', 'agricol'), 'fas fa-tractor'),
    (('étnico', 'etnico', 'racial', 'raciais', 'equidade'), 'fas fa-hands-holding-circle'),
    (('socioeduca',), 'fas fa-scale-balanced'),
    (('busca ativa',), 'fas fa-magnifying-glass'),
    (('eja', 'jovens e adultos'), 'fas fa-user-graduate'),
    (('tempo integral', 'integral'), 'fas fa-clock'),
    (('especial', 'inclus', 'acessib'), 'fas fa-universal-access'),
    (('espaço', 'espaco', 'museu', 'educativos'), 'fas fa-landmark'),
    (('olimpíad', 'olimpiad', 'competi', 'medalh'), 'fas fa-medal'),
    (('física', 'fisica', 'átomo', 'atomo'), 'fas fa-atom'),
    (('matemátic', 'matematic'), 'fas fa-square-root-variable'),
    (('biolog', 'genétic', 'genetic'), 'fas fa-dna'),
    (('financ', 'econom'), 'fas fa-coins'),
    (('empreendedor',), 'fas fa-briefcase'),
    (('pnld', 'livro didático', 'livro didatico', 'catálogo', 'catalogo'), 'fas fa-book'),
    (('geceb', 'sobre', 'institucional', 'quem somos'), 'fas fa-landmark'),
    (('currículo', 'curriculo'), 'fas fa-book-bookmark'),
]


def icone_por_texto(texto, fallback='fas fa-file-lines'):
    """Escolhe um ícone Font Awesome temático a partir de um texto livre."""
    texto = (texto or '').lower()
    for palavras, icone in ICONES_CRIATIVOS:
        if any(p in texto for p in palavras):
            return icone
    return fallback


class Categoria(models.Model):
    """Categorias principais do menu (Documentos Curriculares, Programas, etc.)"""
    nome = models.CharField('Nome', max_length=200)
    slug = models.SlugField('URL amigável', max_length=200, unique=True, blank=True)
    descricao = models.TextField('Descrição', blank=True)
    icone = models.CharField(
        'Ícone', max_length=50, blank=True,
        help_text='Nome do ícone (ex: fas fa-book, fas fa-trophy)'
    )
    imagem = models.ImageField('Imagem de capa', upload_to='categorias/', blank=True, null=True)
    ordem = models.PositiveIntegerField('Ordem no menu', default=0)
    ativa = models.BooleanField('Ativa', default=True)
    categoria_pai = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subcategorias', verbose_name='Categoria pai'
    )
    mostrar_menu_superior = models.BooleanField(
        'Aparecer na barra superior do site', default=True,
        help_text='Se marcado, o botão aparece na barra azul do topo da página '
                  'inicial e na lista "Navegação" do rodapé. Se desmarcado, some '
                  'dessas duas barras (mas a página da categoria continua existindo). '
                  'Vale apenas para botões do nível principal.'
    )
    mostrar_navegue_area = models.BooleanField(
        'Aparecer no "Navegue por área"', default=True,
        help_text='Se marcado, o botão aparece na seção "Navegue por área" da '
                  'página inicial. Se desmarcado, não aparece lá. '
                  'Vale apenas para botões do nível principal.'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['ordem', 'nome']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} → {self.nome}"
        return self.nome

    @property
    def icone_display(self):
        """Ícone da categoria: o cadastrado no admin, ou um escolhido pelo nome."""
        if self.icone:
            return self.icone
        return icone_por_texto(self.nome, fallback='fas fa-folder-open')


class TipoConteudo(models.TextChoices):
    DOCUMENTO = 'documento', 'Documento (PDF, Word, Excel)'
    VIDEO = 'video', 'Vídeo'
    POST = 'post', 'Post / Texto'
    LINK = 'link', 'Link externo'
    PAGINA = 'pagina', 'Página completa'


class StatusPublicacao(models.TextChoices):
    RASCUNHO = 'rascunho', 'Rascunho'
    PUBLICADO = 'publicado', 'Publicado'
    ARQUIVADO = 'arquivado', 'Arquivado'


class ConteudoQuerySet(models.QuerySet):
    def publicados(self):
        """Conteúdos com status 'Publicado' cuja data/hora de publicação já
        chegou. Permite agendar publicações futuras: um conteúdo com status
        Publicado e data no futuro fica invisível no site até aquele momento."""
        return self.filter(
            status=StatusPublicacao.PUBLICADO,
            data_publicacao__lte=timezone.now(),
        )


class Conteudo(models.Model):
    """Modelo principal — qualquer conteúdo do site (documento, vídeo, post, link)"""
    objects = ConteudoQuerySet.as_manager()

    titulo = models.CharField('Título', max_length=300)
    slug = models.SlugField('URL amigável', max_length=300, unique=True, blank=True)
    tipo = models.CharField('Tipo de conteúdo', max_length=20, choices=TipoConteudo.choices, default=TipoConteudo.POST)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='conteudos', verbose_name='Categoria'
    )

    # Conteúdo textual (para posts e páginas)
    resumo = models.TextField('Resumo', blank=True, help_text='Breve descrição exibida nos cards')
    corpo = models.TextField('Conteúdo completo', blank=True, help_text='Texto com formatação HTML')

    # Arquivo (para documentos PDF, Word, Excel)
    arquivo = models.FileField(
        'Arquivo', upload_to='documentos/%Y/%m/', blank=True, null=True,
        help_text='Formatos aceitos: PDF, Word (.doc/.docx), Excel (.xls/.xlsx), PowerPoint (.ppt/.pptx), vídeo (.mp4/.avi), imagem (.jpg/.png) e outros.'
    )

    # Vídeo
    url_video = models.URLField(
        'URL do vídeo', blank=True,
        help_text='Cole o link do YouTube ou Vimeo'
    )

    # Link externo
    url_externa = models.URLField('Link externo', blank=True)

    # Imagem de destaque
    imagem_destaque = models.ImageField(
        'Imagem de destaque', upload_to='destaques/%Y/%m/', blank=True, null=True,
        help_text='Imagem exibida no card e no topo da página'
    )

    # Ícone escolhido manualmente (opcional) — sobrepõe o ícone automático
    icone_manual = models.CharField(
        'Ícone do card', max_length=50, blank=True,
        help_text='Deixe em branco para o site escolher um ícone automaticamente '
                  'com base no título e na categoria.'
    )

    # Publicação
    status = models.CharField(
        'Status', max_length=20,
        choices=StatusPublicacao.choices, default=StatusPublicacao.RASCUNHO
    )
    destaque = models.BooleanField(
        'Destaque na home', default=False,
        help_text='Marque para exibir este conteúdo na página principal'
    )
    recente = models.BooleanField(
        'Aparecer em "Conteúdos recentes"', default=False,
        help_text='Se marcado, este item aparece na seção "Conteúdos recentes" da '
                  'home (abaixo do banner, à esquerda). Se desmarcado, aparece só '
                  'na categoria escolhida.'
    )
    ordem = models.PositiveIntegerField('Ordem de exibição', default=0)

    # Datas
    data_publicacao = models.DateTimeField('Data de publicação', default=timezone.now)
    data_criacao = models.DateTimeField('Criado em', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Atualizado em', auto_now=True)

    # Autor
    autor = models.CharField('Autor / Responsável', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Conteúdo'
        verbose_name_plural = 'Conteúdos'
        ordering = ['-destaque', 'ordem', '-data_publicacao']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
            original_slug = self.slug
            counter = 1
            while Conteudo.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    @property
    def tipo_icone(self):
        icones = {
            'documento': 'fas fa-file-pdf',
            'video': 'fas fa-play-circle',
            'post': 'fas fa-newspaper',
            'link': 'fas fa-external-link-alt',
            'pagina': 'fas fa-file-alt',
        }
        return icones.get(self.tipo, 'fas fa-file')

    @property
    def icone_criativo(self):
        """Ícone exibido no card. Usa o ícone escolhido manualmente no admin,
        se houver; caso contrário, escolhe automaticamente pelo texto do
        título/categoria, substituindo a seta genérica de 'link externo'."""
        if self.icone_manual:
            return self.icone_manual
        texto = self.titulo or ''
        if self.categoria:
            texto += ' ' + (self.categoria.nome or '')
        # Fallback: ícone da categoria, senão um documento genérico.
        fallback = 'fas fa-file-lines'
        if self.categoria and self.categoria.icone:
            fallback = self.categoria.icone
        return icone_por_texto(texto, fallback=fallback)

    @property
    def extensao_arquivo(self):
        if self.arquivo:
            return self.arquivo.name.split('.')[-1].upper()
        return ''

    def get_video_embed_url(self):
        """Converte URL do YouTube/Vimeo para embed"""
        url = self.url_video
        if not url:
            return ''
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        return url


class Anexo(models.Model):
    """Arquivos anexados a um conteúdo ou categoria — PDF, Word, Excel, vídeo, etc."""
    conteudo = models.ForeignKey(
        Conteudo, on_delete=models.CASCADE, null=True, blank=True,
        related_name='anexos', verbose_name='Conteúdo'
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, null=True, blank=True,
        related_name='anexos', verbose_name='Categoria'
    )
    arquivo = models.FileField(
        'Arquivo', upload_to='anexos/%Y/%m/',
        help_text='PDF, Word, Excel, PowerPoint, vídeo, imagem ou outro arquivo.'
    )
    nome = models.CharField(
        'Nome do arquivo', max_length=200, blank=True,
        help_text='Nome exibido no site. Se vazio, usa o nome do arquivo.'
    )
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome or self.arquivo.name.split('/')[-1]

    @property
    def extensao(self):
        if self.arquivo:
            return self.arquivo.name.split('.')[-1].upper()
        return ''

    @property
    def nome_exibicao(self):
        return self.nome or self.arquivo.name.split('/')[-1]


class Banner(models.Model):
    """Banners rotativos — aparecem na home ou em uma categoria específica."""
    TAMANHO_CHOICES = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio (padrão)'),
        ('grande', 'Grande'),
    ]
    titulo = models.CharField('Título', max_length=200)
    subtitulo = models.CharField('Subtítulo', max_length=300, blank=True)
    imagem = models.ImageField('Imagem do banner', upload_to='banners/', blank=True, null=True)
    url_imagem = models.URLField(
        'Imagem por URL (opcional)', blank=True,
        help_text='Cole aqui o endereço de uma imagem da internet para usá-la '
                  'no lugar do arquivo enviado. Se os dois estiverem preenchidos, '
                  'a URL tem prioridade.'
    )
    link = models.URLField('Link ao clicar', blank=True)
    tamanho = models.CharField(
        'Tamanho da imagem', max_length=10, choices=TAMANHO_CHOICES, default='medio',
        help_text='Controla a altura máxima do banner. A imagem nunca é cortada ou distorcida.'
    )
    ordem = models.PositiveIntegerField('Ordem', default=0)
    ativo = models.BooleanField('Ativo', default=True)
    categoria = models.ForeignKey(
        'Categoria', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='banners', verbose_name='Área de exibição',
        help_text='Deixe vazio para aparecer na página inicial. '
                  'Selecione uma área para o banner aparecer dentro daquela seção.'
    )

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['ordem']

    def __str__(self):
        return self.titulo

    @property
    def imagem_src(self):
        """Endereço da imagem exibida: URL externa (se houver) ou arquivo enviado."""
        if self.url_imagem:
            return self.url_imagem
        if self.imagem:
            return self.imagem.url
        return ''


class Cartaz(models.Model):
    """Cartazes de eventos — aparecem discretamente nas laterais da página principal."""
    LADO_CHOICES = [
        ('esquerdo', 'Lado esquerdo'),
        ('direito', 'Lado direito'),
    ]
    TAMANHO_CHOICES = [
        ('pequeno', 'Pequeno (90px)'),
        ('medio', 'Médio (140px)'),
        ('grande', 'Grande (200px)'),
    ]
    titulo = models.CharField('Título do evento', max_length=200)
    imagem = models.ImageField('Imagem do cartaz', upload_to='cartazes/', blank=True, null=True)
    url_imagem = models.URLField(
        'Imagem por URL (opcional)', blank=True,
        help_text='Cole aqui o endereço de uma imagem da internet para usá-la '
                  'como cartaz, no lugar do arquivo enviado. Se os dois estiverem '
                  'preenchidos, a URL tem prioridade.'
    )
    link = models.URLField('Link do evento', blank=True, help_text='URL para inscrição ou página do evento')
    lado = models.CharField('Lado da página', max_length=10, choices=LADO_CHOICES, default='esquerdo')
    tamanho = models.CharField('Tamanho do cartaz', max_length=10, choices=TAMANHO_CHOICES, default='pequeno')
    ordem = models.PositiveIntegerField('Ordem', default=0)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Cartaz'
        verbose_name_plural = 'Cartazes'
        ordering = ['lado', 'ordem']

    def __str__(self):
        return f'{self.titulo} ({self.get_lado_display()})'

    @property
    def imagem_src(self):
        """Endereço da imagem exibida: URL externa (se houver) ou arquivo enviado."""
        if self.url_imagem:
            return self.url_imagem
        if self.imagem:
            return self.imagem.url
        return ''


class Carrossel(models.Model):
    """Carrossel de imagens exibido junto com os cartazes na página inicial.

    As imagens passam automaticamente. Segue as mesmas regras dos cartazes:
    fica preso à área branca de conteúdo e nunca invade banner ou rodapé."""
    LADO_CHOICES = [
        ('esquerdo', 'Lado esquerdo'),
        ('direito', 'Lado direito'),
    ]
    titulo = models.CharField('Nome do carrossel', max_length=200, default='Carrossel')
    ativo = models.BooleanField(
        'Ativar carrossel', default=False,
        help_text='Se marcado, o carrossel aparece na área dos cartazes da '
                  'página inicial. Se desmarcado, não aparece.'
    )
    lado = models.CharField('Lado da página', max_length=10, choices=LADO_CHOICES, default='direito')
    largura = models.PositiveIntegerField(
        'Largura (px)', default=200,
        help_text='Largura do painel do carrossel em pixels. Ex.: 200'
    )
    altura = models.PositiveIntegerField(
        'Altura (px)', default=356,
        help_text='Altura do painel do carrossel em pixels. Ex.: 356'
    )
    intervalo = models.PositiveIntegerField(
        'Tempo entre imagens (segundos)', default=5,
        help_text='As imagens passam sozinhas a cada X segundos.'
    )
    ordem = models.PositiveIntegerField('Ordem entre os cartazes', default=0)
    codigo_html = models.TextField(
        'Código HTML personalizado (opcional)', blank=True,
        help_text='Avançado: cole aqui um código HTML completo para trocar a '
                  'aparência do carrossel. Onde as imagens devem entrar, escreva '
                  'o marcador <!--IMAGENS--> (ele é substituído pelas imagens '
                  'cadastradas abaixo). Deixe em branco para usar o visual padrão.'
    )

    class Meta:
        verbose_name = 'Carrossel'
        verbose_name_plural = 'Carrosséis'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.titulo} ({"ativo" if self.ativo else "inativo"})'


class CarrosselImagem(models.Model):
    """Uma imagem do carrossel — enviada como arquivo ou puxada de uma URL."""
    carrossel = models.ForeignKey(
        Carrossel, on_delete=models.CASCADE,
        related_name='imagens', verbose_name='Carrossel'
    )
    imagem = models.ImageField('Imagem (arquivo)', upload_to='carrossel/', blank=True, null=True)
    url_imagem = models.URLField(
        'Imagem por URL', blank=True,
        help_text='Cole o endereço de uma imagem da internet. Se os dois '
                  'estiverem preenchidos, a URL tem prioridade.'
    )
    link = models.URLField('Link ao clicar (opcional)', blank=True)
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Imagem do carrossel'
        verbose_name_plural = 'Imagens do carrossel'
        ordering = ['ordem', 'pk']

    def __str__(self):
        return f'Imagem {self.ordem} de {self.carrossel.titulo}'

    @property
    def imagem_src(self):
        if self.url_imagem:
            return self.url_imagem
        if self.imagem:
            return self.imagem.url
        return ''


class ConfiguracaoSite(models.Model):
    """Configurações gerais do site (singleton)"""
    nome_site = models.CharField('Nome do site', max_length=200, default='Currículo do Espírito Santo')
    descricao = models.TextField('Descrição', default='Currículo da Educação Básica do Espírito Santo')
    home_titulo = models.CharField(
        'Título da página inicial', max_length=200,
        default='Currículo do Espírito Santo'
    )
    home_texto = models.TextField(
        'Texto da página inicial', blank=True,
        default='<p>Referencial curricular da Educação Básica, elaborado em regime de colaboração entre Estado e municípios.</p>'
    )
    email_contato = models.EmailField('E-mail de contato', default='gerenciadecurriculo@sedu.es.gov.br')
    telefone = models.CharField('Telefone', max_length=50, default='(27) 3636-7838 / 7842')
    endereco = models.TextField(
        'Endereço',
        default='Av. César Hilal, 1111 – Santa Lúcia\nCEP: 29056-085 – Vitória / ES'
    )
    logo = models.ImageField('Logo', upload_to='config/', blank=True, null=True)
    favicon = models.ImageField('Favicon', upload_to='config/', blank=True, null=True)

    class Meta:
        verbose_name = 'Configuração do site'
        verbose_name_plural = 'Configuração do site'

    def __str__(self):
        return self.nome_site

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        config, _ = cls.objects.get_or_create(pk=1)
        return config


class Comentario(models.Model):
    """Comentários dos usuários, com aprovação pelo admin antes de aparecer no site."""
    conteudo = models.ForeignKey(
        Conteudo, on_delete=models.CASCADE,
        related_name='comentarios', verbose_name='Conteúdo'
    )
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', blank=True)
    texto = models.TextField('Comentário')
    aprovado = models.BooleanField(
        'Aprovado', default=False,
        help_text='Marque para publicar o comentário no site'
    )
    data_criacao = models.DateTimeField('Enviado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['data_criacao']

    def __str__(self):
        return f'{self.nome} em "{self.conteudo.titulo[:40]}"'
