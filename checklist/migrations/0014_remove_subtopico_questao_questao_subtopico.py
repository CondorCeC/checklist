# Generated by Django 4.2.7 on 2023-12-18 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0013_subtopico_nome_topico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtopico',
            name='questao',
        ),
        migrations.AddField(
            model_name='questao',
            name='subtopico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='questoes', to='checklist.subtopico'),
        ),
    ]