# Generated by Django 4.2.7 on 2023-12-18 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0012_remove_subtopico_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtopico',
            name='nome_topico',
            field=models.CharField(blank=True, choices=[('Operação', 'Operação'), ('Responsável', 'Responsável'), ('Logística', 'Logística'), ('Sistema', 'Sistema')], max_length=255, null=True, verbose_name='Tópico'),
        ),
    ]
