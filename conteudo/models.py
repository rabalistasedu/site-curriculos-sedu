import re
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
    icone_imagem = models.FileField(
        'Ícone personalizado (imagem)', upload_to='icones_categoria/', blank=True, null=True,
        help_text='Envie uma imagem para usar como ícone deste botão, no lugar do ícone '
                  'automático/Font Awesome. Aceita qualquer formato (PNG, JPG, SVG, ICO, '
                  'WEBP...). Use uma imagem com fundo transparente para não prejudicar a '
                  'estética do botão. A imagem é ajustada automaticamente ao espaço do '
                  'ícone (sem cortar) tanto no botão principal quanto em subbotões. Se '
                  'preenchido, tem prioridade sobre o ícone escolhido.'
    )
    icone_largura = models.PositiveIntegerField(
        'Largura do ícone (px)', null=True, blank=True,
        help_text='Opcional. Controla o tamanho do ícone deste botão em pixels '
                  '(Font Awesome ou imagem personalizada). Deixe em branco para '
                  'usar o tamanho padrão do site.'
    )
    icone_altura = models.PositiveIntegerField(
        'Altura do ícone (px)', null=True, blank=True,
        help_text='Opcional. Se vazio e a largura estiver preenchida, usa o mesmo '
                  'valor da largura (ícone quadrado).'
    )
    imagem = models.ImageField('Imagem de capa', upload_to='categorias/', blank=True, null=True)
    ordem = models.PositiveIntegerField('Ordem no menu', default=0)
    ativa = models.BooleanField('Ativa', default=True)
    categoria_pai = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subcategorias', verbose_name='Categoria pai'
    )
    mostrar_menu_superior = models.BooleanField(
        'Aparecer na barra superior do site', default=False,
        help_text='Se marcado, o botão aparece na barra azul do topo da página '
                  'inicial e na lista "Navegação" do rodapé. Se desmarcado, some '
                  'dessas duas barras (mas a página da categoria continua existindo). '
                  'Vale apenas para botões do nível principal.'
    )
    mostrar_navegue_area = models.BooleanField(
        'Aparecer no "Navegue por área"', default=False,
        help_text='Se marcado, o botão aparece na seção "Navegue por área" da '
                  'página inicial. Se desmarcado, não aparece lá. '
                  'Vale apenas para botões do nível principal.'
    )
    mostrar_area_central = models.BooleanField(
        'Aparecer na área central (ao lado do Currículo Atual)', default=False,
        help_text='Se marcado, o botão aparece centralizado na página inicial, '
                  'ao lado do botão "Currículo Atual". Independente da barra '
                  'superior — pode marcar um, outro, os dois ou nenhum. A ordem '
                  'de exibição usa o mesmo campo "Ordem no menu". '
                  'Vale apenas para botões do nível principal.'
    )
    url_externa = models.URLField(
        'URL / Link de acesso externo', max_length=1000, blank=True,
        help_text='Opcional. Se preenchido, ao clicar neste botão o visitante '
                  'será direcionado para este endereço externo em vez de abrir '
                  'a página interna da categoria.'
    )
    mostrar_conteudos_recentes = models.BooleanField(
        'Aparecer em Conteúdos Recentes', default=False,
        help_text='Se marcado, os conteúdos desta categoria poderão aparecer '
                  'automaticamente na área "Conteúdos Recentes" da página inicial.'
    )
    mostrar_como_card = models.BooleanField(
        'Mostrar como card grande na página do pai', default=True,
        help_text='Vale apenas para subcategorias (botões dentro de outro botão). '
                  'Se marcado, aparece como chip no topo E como card grande clicável '
                  'no meio da página do pai. Se desmarcado, aparece SOMENTE como chip '
                  'no topo (sem duplicar). Subáreas criadas pela função "Criar subárea '
                  'nos botões marcados" já nascem desmarcadas, por padrão.'
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

    @property
    def link_externo(self):
        """URL externa pronta para uso no href, com schema garantido."""
        url = (self.url_externa or '').strip()
        if not url:
            return ''
        if '://' in url or url.startswith(('mailto:', 'tel:', '//', '#', '/')):
            return url
        return 'https://' + url

    @property
    def icone_estilo_inline(self):
        """CSS inline (width/height/font-size) quando o tamanho do ícone é personalizado."""
        if not self.icone_largura and not self.icone_altura:
            return ''
        largura = self.icone_largura or self.icone_altura
        altura = self.icone_altura or self.icone_largura
        fonte = max(10, int(altura * 0.45))
        return f'width:{largura}px;height:{altura}px;font-size:{fonte}px;'


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

    titulo = models.CharField(
        'Título', max_length=300, blank=True,
        help_text='Opcional. Deixe em branco para postar só uma imagem/vídeo, '
                  'sem nenhum texto aparecendo sobre ela.'
    )
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
        'URL do vídeo', max_length=1000, blank=True,
        help_text='Cole o link do YouTube ou Vimeo'
    )

    # Link externo
    url_externa = models.URLField('Link externo', max_length=1000, blank=True)

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
    # Ícone personalizado enviado como imagem — tem prioridade sobre icone_manual
    icone_imagem = models.FileField(
        'Ícone personalizado (imagem)', upload_to='icones/', blank=True, null=True,
        help_text='Envie uma imagem para usar como ícone do card, no lugar do ícone '
                  'automático. Aceita qualquer formato (PNG, JPG, SVG, ICO, WEBP...). '
                  'Use uma imagem com fundo transparente para não prejudicar a '
                  'estética do botão. Se preenchido, tem prioridade sobre o ícone escolhido.'
    )

    # Estilo do TÍTULO do card (opcional) — mesmo espírito do EstiloBotao das
    # categorias, mas aqui vive direto no Conteudo (cada conteúdo é único)
    TEXTO_ALINHAMENTO_CHOICES = [
        ('', 'Automático (padrão do site)'),
        ('left', 'Esquerda'),
        ('center', 'Centralizado'),
        ('right', 'Direita'),
    ]
    texto_alinhamento = models.CharField(
        'Alinhamento do texto', max_length=10, blank=True,
        choices=TEXTO_ALINHAMENTO_CHOICES,
        help_text='Alinhamento do título do card no site.'
    )
    texto_fonte = models.CharField(
        'Fonte do texto', max_length=100, blank=True,
        help_text='Ex.: Georgia, Arial, Times New Roman. Vazio = fonte do site (Inter).'
    )
    texto_tamanho_fonte = models.PositiveIntegerField(
        'Tamanho da letra (px)', null=True, blank=True,
        help_text='Vazio = tamanho automático do card.'
    )

    @property
    def texto_estilo_inline(self):
        """CSS inline pronto para o título do card, se algum estilo foi definido."""
        partes = []
        if self.texto_alinhamento:
            partes.append(f'text-align:{self.texto_alinhamento};')
        if self.texto_fonte:
            partes.append(f"font-family:'{self.texto_fonte}',Inter,sans-serif;")
        if self.texto_tamanho_fonte:
            partes.append(f'font-size:{self.texto_tamanho_fonte}px;')
        return ''.join(partes)

    # Publicação
    status = models.CharField(
        'Status', max_length=20,
        choices=StatusPublicacao.choices, default=StatusPublicacao.RASCUNHO
    )
    destaque = models.BooleanField(
        'Destaque na home', default=False,
        help_text='Marque para exibir este conteúdo na página principal'
    )
    destaque_gerenciado = models.BooleanField(
        'Cadastrado pela área "Destaques do Site" (Organizador)', default=False,
        help_text='Marcado automaticamente para itens criados na área "Destaques do '
                  'Site" do Organizador de Conteúdo. Mantém o item visível na lista '
                  'de gerenciamento mesmo quando ocultado (destaque=False), para '
                  'poder reativar depois.'
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
            # Sem título (ex.: destaque só com imagem/vídeo), usa o tipo como
            # base do endereço — nunca gera um slug vazio.
            base = self.titulo or self.get_tipo_display() or 'conteudo'
            self.slug = slugify(base) or 'conteudo'
            original_slug = self.slug
            counter = 1
            while Conteudo.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo or f'{self.get_tipo_display()} #{self.pk}'

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
        """Converte URL do YouTube/Vimeo para embed. Reconhece as variações
        mais comuns (watch, youtu.be, shorts, live, mobile m.youtube.com,
        já embed) via regex — extrai o ID de forma confiável, ignorando
        parâmetros extras (ex.: si=, t=, list=) em qualquer ordem.
        Se a URL não for de um provedor de vídeo reconhecido (ex.: o usuário
        colou por engano o link de um site comum), devolve '' em vez de
        tentar embutir algo que não é um vídeo — evita o erro "153/erro de
        configuração do player" do YouTube, que aparecia sempre que a URL
        não era de fato um vídeo do YouTube/Vimeo."""
        url = (self.url_video or '').strip()
        if not url:
            return ''

        padroes_youtube = [
            r'(?:youtube\.com|m\.youtube\.com)/watch\?(?:.*&)?v=([A-Za-z0-9_-]{6,})',
            r'youtu\.be/([A-Za-z0-9_-]{6,})',
            r'(?:youtube\.com|m\.youtube\.com)/shorts/([A-Za-z0-9_-]{6,})',
            r'(?:youtube\.com|m\.youtube\.com)/live/([A-Za-z0-9_-]{6,})',
            r'(?:youtube\.com|m\.youtube\.com)/embed/([A-Za-z0-9_-]{6,})',
        ]
        for padrao in padroes_youtube:
            m = re.search(padrao, url)
            if m:
                return f'https://www.youtube.com/embed/{m.group(1)}'

        m = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
        if m:
            return f'https://player.vimeo.com/video/{m.group(1)}'

        # Não é uma URL reconhecida de vídeo — não tenta embutir (o template
        # mostra um botão "Assistir/abrir" apontando direto para a URL).
        return ''

    @property
    def video_embed_valido(self):
        """True quando url_video é de um provedor reconhecido (YouTube/Vimeo)
        e pode ser embutido num iframe. Usado no template para decidir entre
        mostrar o player embutido ou um botão de link direto."""
        return bool(self.get_video_embed_url())

    @property
    def link_externo(self):
        """URL externa pronta para uso no href. Garante que sempre tenha
        um schema (http:// ou https://) na frente — sem isso o navegador
        interpreta 'uol.com.br' como caminho interno do próprio site
        (=> tenta abrir /uol.com.br dentro do site atual, o que dá o erro
        "recusou a se conectar"). Aceita URLs coladas sem o https://."""
        url = (self.url_externa or '').strip()
        if not url:
            return ''
        # Já tem schema (http://, https://, mailto:, tel:, ftp://, //)?
        if '://' in url or url.startswith(('mailto:', 'tel:', '//', '#', '/')):
            return url
        # Sem schema: assume https:// (mais seguro e mais comum hoje)
        return 'https://' + url

    @property
    def video_thumbnail_url(self):
        """Miniatura do vídeo (só YouTube tem endereço de miniatura público
        e previsível; Vimeo exige chamada de API, então fica sem miniatura)."""
        url = self.url_video
        if not url:
            return ''
        video_id = ''
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        if video_id:
            return f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
        return ''


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
        'Arquivo', upload_to='anexos/%Y/%m/', blank=True,
        help_text='PDF, Word, Excel, PowerPoint, vídeo, imagem ou outro arquivo.'
    )
    url = models.URLField(
        'Link (URL)', max_length=1000, blank=True,
        help_text='Em vez de um arquivo, aponta para um link externo. Aparece no site '
                   'exatamente como um anexo de arquivo, só que abre a URL. Preencha '
                   'OU o arquivo OU o link — nunca os dois.'
    )
    nome = models.CharField(
        'Nome de exibição', max_length=200, blank=True,
        help_text='Nome exibido no site. Se vazio, usa o nome do arquivo (ou o link, se for um anexo de URL).'
    )
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome_exibicao

    @property
    def eh_link(self):
        """True quando este anexo é um link de URL, não um arquivo enviado."""
        return bool(self.url) and not self.arquivo

    @property
    def link_href(self):
        """URL de destino do anexo — do link externo ou do arquivo enviado."""
        if self.url:
            return self.url
        if self.arquivo:
            return self.arquivo.url
        return ''

    @property
    def extensao(self):
        if self.eh_link:
            return 'LINK'
        if self.arquivo:
            return self.arquivo.name.split('.')[-1].upper()
        return ''

    @property
    def nome_exibicao(self):
        if self.nome:
            return self.nome
        if self.arquivo:
            return self.arquivo.name.split('/')[-1]
        if self.url:
            return self.url
        return '(anexo vazio)'


class Banner(models.Model):
    """Banners rotativos — aparecem na home ou em uma categoria específica."""
    TAMANHO_CHOICES = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio (padrão)'),
        ('grande', 'Grande'),
    ]
    titulo = models.CharField(
        'Título', max_length=200, blank=True,
        help_text='Opcional. Deixe em branco se não quiser nenhum texto sobre o banner.'
    )
    subtitulo = models.CharField('Subtítulo', max_length=300, blank=True)
    imagem = models.ImageField('Imagem do banner', upload_to='banners/', blank=True, null=True)
    url_imagem = models.URLField(
        'Imagem por URL (opcional)', max_length=1000, blank=True,
        help_text='Cole aqui o endereço de uma imagem da internet para usá-la '
                  'no lugar do arquivo enviado. Se os dois estiverem preenchidos, '
                  'a URL tem prioridade.'
    )
    link = models.URLField('Link ao clicar', max_length=1000, blank=True)
    tamanho = models.CharField(
        'Tamanho da imagem', max_length=10, choices=TAMANHO_CHOICES, default='medio',
        help_text='Campo legado — hoje o banner se ajusta AUTOMATICAMENTE à imagem '
                  '(ocupa a largura toda e a altura acompanha a proporção, sem cortar). '
                  'Só tem efeito se você NÃO usar o ajuste automático via "Altura personalizada".'
    )
    altura_personalizada = models.PositiveIntegerField(
        'Altura fixa em pixels (opcional)', null=True, blank=True,
        help_text='VAZIO: o banner se ajusta sozinho à imagem (ocupa a largura toda e a altura '
                  'acompanha a proporção, sem cortar). PREENCHA um número para deixar o banner com '
                  'uma altura fixa — ótimo para uma FAIXA FINA E DISCRETA (ex.: 120, 150). Nesse '
                  'caso a imagem PREENCHE a faixa (pode recortar um pouco o topo/base para caber), '
                  'sem barras nem desfoque. Quanto menor o número, mais fina a faixa.'
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
        return self.titulo or f'Banner #{self.pk} (sem título)'

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
        'Imagem por URL (opcional)', max_length=1000, blank=True,
        help_text='Cole aqui o endereço de uma imagem da internet para usá-la '
                  'como cartaz, no lugar do arquivo enviado. Se os dois estiverem '
                  'preenchidos, a URL tem prioridade.'
    )
    link = models.URLField('Link do evento', max_length=1000, blank=True, help_text='URL para inscrição ou página do evento')
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
    """Um item do carrossel — imagem OU vídeo, enviado como arquivo ou
    puxado de uma URL. O conteúdo se ajusta sozinho ao espaço do carrossel."""
    EXTENSOES_VIDEO = ('.mp4', '.webm', '.ogg', '.ogv', '.mov', '.m4v')

    carrossel = models.ForeignKey(
        Carrossel, on_delete=models.CASCADE,
        related_name='imagens', verbose_name='Carrossel'
    )
    imagem = models.FileField(
        'Imagem ou vídeo (arquivo)', upload_to='carrossel/', blank=True, null=True,
        help_text='Aceita imagem (JPG, PNG, GIF, WEBP...) ou vídeo (MP4, WEBM...).'
    )
    url_imagem = models.URLField(
        'Imagem/vídeo por URL', max_length=1000, blank=True,
        help_text='Cole o endereço de uma imagem ou vídeo da internet. Se os '
                  'dois estiverem preenchidos, a URL tem prioridade.'
    )
    link = models.URLField('Link ao clicar (opcional)', max_length=1000, blank=True)
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

    @property
    def eh_video(self):
        """True quando o arquivo/URL é um vídeo (pela extensão)."""
        src = self.imagem_src.split('?')[0].lower()
        return src.endswith(self.EXTENSOES_VIDEO)


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
    rodape_col1_titulo = models.CharField('Rodape: titulo coluna 1', max_length=200, blank=True, default='GERENCIA DE CURRICULO DA EDUCACAO BASICA (GECEB)')
    rodape_col1_html = models.TextField('Rodape: conteudo coluna 1 (HTML)', blank=True)
    rodape_col2_titulo = models.CharField('Rodape: titulo coluna 2', max_length=200, blank=True, default='SECRETARIA DA EDUCACAO (SEDU)')
    rodape_col2_html = models.TextField('Rodape: conteudo coluna 2 (HTML)', blank=True)
    rodape_col3_titulo = models.CharField('Rodape: titulo coluna 3', max_length=200, blank=True, default='Navegacao')
    rodape_col3_html = models.TextField('Rodape: conteudo coluna 3 (HTML)', blank=True, help_text='Se vazio, exibe links automaticos das categorias do menu.')
    rodape_copyright = models.CharField('Rodape: texto copyright', max_length=300, blank=True)
    rodape_imagem = models.ImageField('Rodape: imagem/logo', upload_to='config/', blank=True, null=True)

    # Títulos das 3 seções da home (área "Destaques", "Conteúdos recentes" e
    # "Navegue por área") — HTML rico (negrito/itálico/sublinhado/alinhamento/
    # lista) via RichTextWidget, editável no painel "Área do Site".
    titulo_destaques = models.TextField('Título da seção "Destaques"', blank=True, default='Destaques')
    titulo_recentes = models.TextField('Título da seção "Conteúdos recentes"', blank=True, default='Conteúdos recentes')
    titulo_areas = models.TextField('Título da seção "Navegue por área"', blank=True, default='Navegue por área')

    # Ícones das 3 seções — Font Awesome (padrões do site, via IconPicker) OU
    # imagem enviada em qualquer formato (a imagem tem prioridade e é exibida
    # sempre com fundo transparente, via classe "sem-fundo" + object-fit:contain,
    # para não atrapalhar a estética do site).
    icone_destaques = models.CharField('Ícone de "Destaques" (padrão do site)', max_length=100, blank=True)
    icone_destaques_imagem = models.FileField('Ícone de "Destaques" (imagem)', upload_to='icones_secao/', blank=True, null=True)
    icone_recentes = models.CharField('Ícone de "Conteúdos recentes" (padrão do site)', max_length=100, blank=True, default='fas fa-wand-magic-sparkles')
    icone_recentes_imagem = models.FileField('Ícone de "Conteúdos recentes" (imagem)', upload_to='icones_secao/', blank=True, null=True)
    icone_areas = models.CharField('Ícone de "Navegue por área" (padrão do site)', max_length=100, blank=True, default='fas fa-compass')
    icone_areas_imagem = models.FileField('Ícone de "Navegue por área" (imagem)', upload_to='icones_secao/', blank=True, null=True)

    # Nome do botão "Currículo Atual" (pílula central da home) — editável.
    nome_curriculo_atual = models.CharField(
        'Nome do botão "Currículo Atual"', max_length=100, blank=True,
        default='Currículo Atual',
        help_text='Texto exibido na pílula central da página inicial. Deixe vazio '
                  'para usar "Currículo Atual" (padrão).'
    )

    # ── Identidade Visual (cabeçalho) ──────────────────────────────────
    ALINHAMENTO_LOGO_CHOICES = [
        ('esquerda', 'Esquerda'),
        ('centro', 'Centro'),
        ('direita', 'Direita'),
    ]
    brasao_imagem = models.FileField(
        'Brasão personalizado (opcional)', upload_to='identidade/', blank=True, null=True,
        help_text='Se vazio, usa o brasão padrão do Espírito Santo. Envie uma imagem '
                  'para substituí-lo (fundo transparente recomendado).'
    )
    brasao_alinhamento = models.CharField(
        'Alinhamento do brasão', max_length=10, choices=ALINHAMENTO_LOGO_CHOICES, default='esquerda'
    )
    brasao_largura = models.PositiveIntegerField('Largura do brasão (px)', null=True, blank=True)
    brasao_altura = models.PositiveIntegerField('Altura do brasão (px)', null=True, blank=True)

    logo2_imagem = models.FileField(
        'Segundo logotipo (opcional)', upload_to='identidade/', blank=True, null=True,
        help_text='Ex.: logo do Currículo. Aparece na barra superior ao lado do brasão. '
                  'Deixe vazio para não exibir nenhum segundo logotipo.'
    )
    logo2_alinhamento = models.CharField(
        'Alinhamento do segundo logotipo', max_length=10, choices=ALINHAMENTO_LOGO_CHOICES, default='esquerda'
    )
    logo2_largura = models.PositiveIntegerField('Largura do segundo logotipo (px)', null=True, blank=True)
    logo2_altura = models.PositiveIntegerField('Altura do segundo logotipo (px)', null=True, blank=True)

    class Meta:
        verbose_name = 'Configuração do site'
        verbose_name_plural = 'Configuração do site'
        permissions = [
            ('pode_acessar_organizador', 'Pode acessar: Organizador de Conteúdo'),
            ('pode_acessar_adicionar_arquivos', 'Pode acessar: Adicionar Arquivos'),
            ('pode_acessar_barra_superior', 'Pode acessar: Botões da Barra Superior'),
            ('pode_acessar_editor_rodape', 'Pode acessar: Editor do Rodapé'),
            ('pode_acessar_area_do_site', 'Pode acessar: Área do Site'),
            ('pode_acessar_estrutura_arvores', 'Pode acessar: Estrutura de Árvores'),
        ]

    def __str__(self):
        return self.nome_site

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        config, _ = cls.objects.get_or_create(pk=1)
        return config


class RodapeImagem(models.Model):
    """Imagem configurável do rodapé (logo parceiro, selo, etc.) — gerenciada
    pelo painel "Editor do Rodapé". A faixa de imagens tem altura fixa: cada
    imagem se ajusta ao espaço disponível (object-fit:contain), nunca aumenta
    a altura do rodapé, seja qual for a largura/altura configurada."""
    ALINHAMENTO_CHOICES = [
        ('esquerda', 'Esquerda'),
        ('centro', 'Centralizado'),
        ('direita', 'Direita'),
    ]
    imagem = models.FileField(
        'Imagem', upload_to='rodape_imagens/',
        help_text='Qualquer formato de imagem (PNG, JPG, SVG, WEBP...).'
    )
    largura = models.PositiveIntegerField(
        'Largura (px)', null=True, blank=True,
        help_text='Vazio = largura automática, proporcional à altura.'
    )
    altura = models.PositiveIntegerField(
        'Altura (px)', null=True, blank=True,
        help_text='Vazio = altura automática. A imagem nunca aumenta a altura do rodapé — '
                  'ela sempre se ajusta ao espaço fixo já reservado.'
    )
    alinhamento = models.CharField(
        'Alinhamento', max_length=10, choices=ALINHAMENTO_CHOICES, default='esquerda'
    )
    url = models.URLField(
        'URL (opcional)', max_length=1000, blank=True,
        help_text='Se preenchida, a imagem funciona como link. Se vazia, é exibida sem link.'
    )
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Imagem do rodapé'
        verbose_name_plural = 'Imagens do rodapé'
        ordering = ['ordem', 'pk']

    def __str__(self):
        return self.imagem.name.split('/')[-1] if self.imagem else f'Imagem {self.pk}'

    @property
    def link_externo(self):
        u = (self.url or '').strip()
        if not u:
            return ''
        if '://' in u or u.startswith(('mailto:', 'tel:', '//', '#', '/')):
            return u
        return 'https://' + u


class ColunaExtra(models.Model):
    """Coluna extra opcional na home, ao lado de "Conteúdos recentes" e
    "Navegue por área" (esquerda ou direita), com botões personalizados
    dentro — gerenciada pelo painel "Área do Site"."""
    LADO_CHOICES = [('esquerda', 'Esquerda'), ('direita', 'Direita')]

    titulo = models.TextField('Título da coluna', blank=True, help_text='Aceita formatação (negrito, itálico, alinhamento, lista) — mesmo editor usado em Destaques/Recentes/Navegue por área.')
    icone = models.CharField('Ícone do título (padrão do site)', max_length=100, blank=True)
    icone_imagem = models.FileField(
        'Ícone do título (imagem)', upload_to='icones_secao/', blank=True, null=True,
        help_text='Qualquer formato. Tem prioridade sobre o ícone padrão e aparece sempre com fundo transparente.'
    )
    icone_largura = models.PositiveIntegerField(
        'Largura do ícone do título (px)', null=True, blank=True,
        help_text='Opcional. Deixe em branco para usar o tamanho padrão.'
    )
    icone_altura = models.PositiveIntegerField(
        'Altura do ícone do título (px)', null=True, blank=True,
        help_text='Opcional. Se vazio e a largura estiver preenchida, usa o mesmo valor (ícone quadrado).'
    )
    lado = models.CharField('Lado', max_length=10, choices=LADO_CHOICES, default='direita')
    ativa = models.BooleanField('Ativa (aparece no site)', default=True)
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Coluna extra da home'
        verbose_name_plural = 'Colunas extras da home'
        ordering = ['ordem', 'pk']

    def __str__(self):
        return self.titulo or f'Coluna {self.pk}'

    @property
    def icone_estilo_inline(self):
        if not self.icone_largura and not self.icone_altura:
            return ''
        largura = self.icone_largura or self.icone_altura
        altura = self.icone_altura or self.icone_largura
        fonte = max(10, int(altura * 0.45))
        return f'width:{largura}px;height:{altura}px;font-size:{fonte}px;'


class ColunaExtraBotao(models.Model):
    """Um botão dentro de uma ColunaExtra — pode apontar para uma categoria
    do site ou para um link externo."""
    coluna = models.ForeignKey(ColunaExtra, on_delete=models.CASCADE, related_name='botoes', verbose_name='Coluna')
    nome = models.CharField('Nome do botão', max_length=200)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='+', verbose_name='Categoria (opcional)',
        help_text='Se escolhida, o botão abre esta categoria do site.'
    )
    link_externo = models.URLField(
        'Link externo (opcional)', max_length=1000, blank=True,
        help_text='Se preenchido, tem prioridade sobre a categoria escolhida.'
    )
    icone = models.CharField('Ícone Font Awesome', max_length=100, blank=True, default='fas fa-link')
    icone_imagem = models.FileField(
        'Ícone personalizado (imagem)', upload_to='icones_coluna_extra/', blank=True, null=True
    )
    icone_largura = models.PositiveIntegerField(
        'Largura do ícone (px)', null=True, blank=True,
        help_text='Opcional. Deixe em branco para usar o tamanho padrão.'
    )
    icone_altura = models.PositiveIntegerField(
        'Altura do ícone (px)', null=True, blank=True,
        help_text='Opcional. Se vazio e a largura estiver preenchida, usa o mesmo valor (ícone quadrado).'
    )
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Botão da coluna extra'
        verbose_name_plural = 'Botões da coluna extra'
        ordering = ['ordem', 'pk']

    def __str__(self):
        return self.nome

    @property
    def url(self):
        if self.link_externo:
            return self.link_externo
        if self.categoria:
            return f'/categoria/{self.categoria.slug}/'
        return '#'

    @property
    def icone_display(self):
        return self.icone or 'fas fa-link'

    @property
    def icone_estilo_inline(self):
        if not self.icone_largura and not self.icone_altura:
            return ''
        largura = self.icone_largura or self.icone_altura
        altura = self.icone_altura or self.icone_largura
        fonte = max(10, int(altura * 0.45))
        return f'width:{largura}px;height:{altura}px;font-size:{fonte}px;'


class Comentario(models.Model):
    """Comentários dos usuários, com moderação (pendente → publicado ou recusado)."""
    PENDENTE = 'pendente'
    PUBLICADO = 'publicado'
    RECUSADO = 'recusado'
    STATUS_CHOICES = [
        (PENDENTE, '⏳ Pendente'),
        (PUBLICADO, '✅ Publicado'),
        (RECUSADO, '❌ Recusado'),
    ]

    conteudo = models.ForeignKey(
        Conteudo, on_delete=models.CASCADE,
        related_name='comentarios', verbose_name='Conteúdo',
        null=True, blank=True,
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE,
        related_name='comentarios', verbose_name='Botão/categoria',
        null=True, blank=True,
        help_text='Preenchido quando o comentário foi feito na página de um botão (categoria) em vez de num conteúdo específico. Mutuamente exclusivo com Conteúdo.'
    )
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name='Em resposta a',
    )
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', blank=True)
    texto = models.TextField('Comentário')
    status = models.CharField(
        'Status', max_length=10, choices=STATUS_CHOICES, default=PENDENTE,
        help_text='Pendente = aguardando moderação; Publicado = visível no site; Recusado = descartado.'
    )
    # Campo legado — mantido para compatibilidade; sincronizado com status na migration
    aprovado = models.BooleanField('Aprovado (legado)', default=False, editable=False)
    resposta = models.TextField(
        'Resposta do administrador', blank=True,
        help_text='Resposta que aparece vinculada ao comentário no site. Deixe vazio se não quiser responder.'
    )
    votos_positivos = models.PositiveIntegerField('👍 Curtidas', default=0)
    votos_negativos = models.PositiveIntegerField('👎 Não curtidas', default=0)
    data_criacao = models.DateTimeField('Enviado em', auto_now_add=True)
    data_resposta = models.DateTimeField('Respondido em', null=True, blank=True)

    # Integração com Microsoft Teams (grupo GECEB) — todos opcionais, não afetam
    # nenhum comentário existente nem o fluxo de moderação já existente.
    TEAMS_NAO_ENVIADO = 'nao_enviado'
    TEAMS_ENVIADO = 'enviado'
    TEAMS_VINCULADO = 'vinculado'
    TEAMS_RESPONDIDO = 'respondido'
    TEAMS_ERRO = 'erro'
    TEAMS_STATUS_CHOICES = [
        (TEAMS_NAO_ENVIADO, '— Não enviado'),
        (TEAMS_ENVIADO, '📤 Enviado ao Teams'),
        (TEAMS_VINCULADO, '🔗 Vinculado (aguardando resposta)'),
        (TEAMS_RESPONDIDO, '✅ Respondido via Teams'),
        (TEAMS_ERRO, '⚠️ Erro ao enviar'),
    ]
    teams_status = models.CharField(
        'Status no Teams', max_length=12, choices=TEAMS_STATUS_CHOICES,
        default=TEAMS_NAO_ENVIADO, blank=True,
        help_text='Controlado automaticamente pela integração com o Microsoft Teams (grupo GECEB).'
    )
    teams_message_id = models.CharField(
        'ID da mensagem no Teams', max_length=255, blank=True,
        help_text='ID da mensagem raiz criada no canal do Teams para este comentário (uso interno).'
    )
    teams_data_envio = models.DateTimeField('Enviado ao Teams em', null=True, blank=True)
    teams_ultima_verificacao = models.DateTimeField(
        'Última verificação de resposta', null=True, blank=True,
        help_text='Usado pela sincronização automática para não reprocessar tudo a cada rodada.'
    )

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['data_criacao']

    def __str__(self):
        alvo = self.conteudo.titulo if self.conteudo else (self.categoria.nome if self.categoria else '?')
        return f'{self.nome} em "{alvo[:40]}"'

    @property
    def publicado(self):
        return self.status == self.PUBLICADO

    @property
    def origem(self):
        """Devolve o Conteudo ou a Categoria a que este comentário pertence."""
        return self.conteudo or self.categoria
