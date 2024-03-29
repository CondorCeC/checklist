# Generated by Django 4.2.7 on 2023-12-01 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0004_resposta_data_av'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_av', models.DateTimeField(blank=True, null=True, verbose_name='Data da Avaliação')),
            ],
        ),
        migrations.RemoveField(
            model_name='resposta',
            name='data_av',
        ),
        migrations.AddField(
            model_name='resposta',
            name='avaliacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='checklist.avaliacao'),
        ),
    ]
