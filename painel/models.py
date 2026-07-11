"""
Modelos do Painel Central Administrativo.

Princípio (Especificação, Partes 3 e 4): o conteúdo é uma entidade
independente e a publicação em múltiplos locais acontece por VÍNCULOS.
A "árvore de nós" da especificação é a hierarquia de Categoria que já
existe no app conteudo (self-FK categoria_pai = adjacency list, sem
limite de níveis). Nada do sistema antigo é alterado: a FK
Conteudo.categoria continua sendo o vínculo primário; os vínculos
adicionais criados aqui apenas SOMAM locais de exibição.
"""
from django.db import models


class Vinculo(models.Model):
    """Vínculo extra entre um conteúdo e uma categoria (botão/subbotão/subárea).

    Permite que o mesmo conteúdo apareça em vários locais do site sem
    duplicação. Remover um vínculo nunca exclui o conteúdo — apenas
    interrompe a exibição naquele local."""
    conteudo = models.ForeignKey(
        'conteudo.Conteudo', on_delete=models.CASCADE,
        related_name='vinculos', verbose_name='Conteúdo'
    )
    categoria = models.ForeignKey(
        'conteudo.Categoria', on_delete=models.CASCADE,
        related_name='vinculos', verbose_name='Categoria (local de exibição)'
    )
    ordem = models.PositiveIntegerField('Ordem de exibição', default=0)
    pulsante = models.BooleanField(
        'Botão vibrante/pulsante', default=False,
        help_text='O card deste conteúdo pulsa suavemente neste local do site.'
    )
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Vínculo de publicação'
        verbose_name_plural = 'Vínculos de publicação'
        unique_together = [('conteudo', 'categoria')]
        ordering = ['categoria', 'ordem']

    def __str__(self):
        return f'{self.conteudo.titulo[:40]} → {self.categoria.nome}'


class EstiloBotao(models.Model):
    """Aparência personalizada de um botão do site (categoria/subcategoria).

    Se não existir registro para a categoria, o site usa a aparência
    automática de sempre. Todos os campos são opcionais."""
    ALINHAMENTO_CHOICES = [
        ('', 'Automático'),
        ('left', 'Esquerda'),
        ('center', 'Centralizado'),
        ('right', 'Direita'),
    ]
    categoria = models.OneToOneField(
        'conteudo.Categoria', on_delete=models.CASCADE,
        related_name='estilo', verbose_name='Categoria (botão)'
    )
    cor_fundo = models.CharField(
        'Cor de fundo', max_length=20, blank=True,
        help_text='Ex.: #2d5a8e. Vazio = automático.'
    )
    cor_texto = models.CharField('Cor do texto', max_length=20, blank=True)
    fonte = models.CharField(
        'Fonte', max_length=100, blank=True,
        help_text='Ex.: Inter, Georgia, Arial. Vazio = fonte do site.'
    )
    tamanho_fonte = models.PositiveIntegerField(
        'Tamanho da letra (px)', null=True, blank=True
    )
    alinhamento = models.CharField(
        'Alinhamento do texto', max_length=10, blank=True,
        choices=ALINHAMENTO_CHOICES
    )
    pulsante = models.BooleanField(
        'Botão vibrante/pulsante', default=False,
        help_text='O botão desta categoria pulsa suavemente no site.'
    )
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Estilo de botão'
        verbose_name_plural = 'Estilos de botões'

    def __str__(self):
        return f'Estilo de "{self.categoria.nome}"'

    @property
    def css_inline(self):
        """Estilo inline pronto para o template do site."""
        partes = []
        if self.cor_fundo:
            partes.append(f'background:{self.cor_fundo};border-color:{self.cor_fundo};')
        if self.cor_texto:
            partes.append(f'color:{self.cor_texto};')
        if self.fonte:
            partes.append(f"font-family:'{self.fonte}',Inter,sans-serif;")
        if self.tamanho_fonte:
            partes.append(f'font-size:{self.tamanho_fonte}px;')
        if self.alinhamento:
            partes.append(f'text-align:{self.alinhamento};justify-content:{ {"left":"flex-start","center":"center","right":"flex-end"}[self.alinhamento] };')
        return ''.join(partes)
