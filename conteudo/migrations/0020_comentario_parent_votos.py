import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0019_comentario_status_resposta'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='parent',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='respostas',
                to='conteudo.comentario',
                verbose_name='Em resposta a',
            ),
        ),
        migrations.AddField(
            model_name='comentario',
            name='votos_positivos',
            field=models.PositiveIntegerField(default=0, verbose_name='👍 Curtidas'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='votos_negativos',
            field=models.PositiveIntegerField(default=0, verbose_name='👎 Não curtidas'),
        ),
    ]
