# Generated by Django 4.2.7 on 2023-12-04 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0007_resposta_obs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resposta',
            name='obs',
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='obs',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Observação'),
        ),
    ]
