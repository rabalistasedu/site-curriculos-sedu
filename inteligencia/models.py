from django.db import models


class PageView(models.Model):
    url = models.CharField(max_length=500)
    tipo_pagina = models.CharField(max_length=20, choices=[
        ('home', 'Home'),
        ('categoria', 'Categoria'),
        ('conteudo', 'Conteúdo'),
        ('busca', 'Busca'),
        ('outra', 'Outra'),
    ])
    objeto_id = models.PositiveIntegerField(null=True, blank=True)
    objeto_slug = models.SlugField(max_length=300, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    sessao_id = models.CharField(max_length=40, db_index=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    referrer = models.URLField(max_length=500, blank=True)
    dispositivo = models.CharField(max_length=10, choices=[
        ('desktop', 'Desktop'),
        ('tablet', 'Tablet'),
        ('mobile', 'Mobile'),
    ], default='desktop')
    navegador = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Visualização de página'
        verbose_name_plural = 'Visualizações de página'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['tipo_pagina', 'timestamp']),
            models.Index(fields=['objeto_id', 'tipo_pagina']),
        ]

    def __str__(self):
        return f'{self.tipo_pagina}: {self.url} ({self.timestamp:%d/%m/%Y %H:%M})'


class DownloadEvent(models.Model):
    anexo_id = models.PositiveIntegerField(null=True, blank=True)
    conteudo_id = models.PositiveIntegerField(null=True, blank=True)
    nome_arquivo = models.CharField(max_length=300)
    extensao = models.CharField(max_length=10, blank=True)
    url = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    sessao_id = models.CharField(max_length=40, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.nome_arquivo} ({self.timestamp:%d/%m/%Y %H:%M})'


class SearchQuery(models.Model):
    termo = models.CharField(max_length=300)
    termo_normalizado = models.CharField(max_length=300, db_index=True)
    n_resultados = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    sessao_id = models.CharField(max_length=40, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Pesquisa interna'
        verbose_name_plural = 'Pesquisas internas'
        ordering = ['-timestamp']

    def __str__(self):
        return f'"{self.termo}" ({self.n_resultados} resultados)'


class AlertaInteligencia(models.Model):
    TIPOS = [
        ('sem_acesso', 'Documento sem acesso'),
        ('link_quebrado', 'Link quebrado'),
        ('arquivo_ausente', 'Arquivo ausente'),
        ('pico_acesso', 'Pico de acesso'),
        ('erro_pagina', 'Página com erro'),
    ]
    tipo = models.CharField(max_length=30, choices=TIPOS)
    titulo = models.CharField(max_length=300)
    descricao = models.TextField(blank=True)
    objeto_tipo = models.CharField(max_length=20, blank=True)
    objeto_id = models.PositiveIntegerField(null=True, blank=True)
    resolvido = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-criado_em']

    def __str__(self):
        status = '✅' if self.resolvido else '⚠️'
        return f'{status} {self.get_tipo_display()}: {self.titulo}'
