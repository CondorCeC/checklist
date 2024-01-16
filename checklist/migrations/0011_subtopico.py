# Generated by Django 4.2.7 on 2023-12-18 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0010_avaliacao_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtopico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tópico')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='checklist.questao')),
            ],
            options={
                'verbose_name': 'Subtópico',
                'verbose_name_plural': 'Subtópicos',
            },
        ),
    ]