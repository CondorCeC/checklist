# Generated by Django 4.2.7 on 2023-12-01 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0002_questao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.FloatField(blank=True, null=True)),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.questao')),
            ],
        ),
    ]
