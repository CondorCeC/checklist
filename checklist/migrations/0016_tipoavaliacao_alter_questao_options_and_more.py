# Generated by Django 4.2.7 on 2023-12-18 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0015_remove_questao_subtopico_delete_subtopico'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoAvaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Tipo Avaliação',
                'verbose_name_plural': 'Tipo Avaliações',
            },
        ),
        migrations.AlterModelOptions(
            name='questao',
            options={},
        ),
        migrations.RemoveField(
            model_name='avaliacao',
            name='media',
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='media_geral',
            field=models.FloatField(blank=True, null=True, verbose_name='Média Geral'),
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='medias_subtopicos',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='Médias por Subtópico'),
        ),
        migrations.CreateModel(
            name='Subtopico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, choices=[('Operação', 'Operação'), ('Logística', 'Logística'), ('Sistema', 'Sistema'), ('Responsável', 'Responsável')], max_length=255, null=True)),
                ('tipo_avaliacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.tipoavaliacao')),
            ],
        ),
        migrations.AddField(
            model_name='questao',
            name='subtopico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checklist.subtopico'),
        ),
    ]
