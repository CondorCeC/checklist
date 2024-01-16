from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserChecklist(models.Model):
    class Meta:
        verbose_name = 'Usuário Checklist'
        verbose_name_plural  = 'Usuários Checklist'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupos = models.ManyToManyField(Group, blank=True, related_name="usuarios_grupos")
    
  

    def __str__(self) -> str:
        return f'{self.user}'
    

class TipoAvaliacao(models.Model):
    class Meta:
        verbose_name = 'Tipo Avaliação'
        verbose_name_plural = 'Tipo Avaliações'
    titulo = models.CharField(max_length=255)


    def __str__(self):
        return self.titulo

class Subtopico(models.Model):
    TOPICOS = (
        ('Separação', 'Separação'),
        ('Operação de loja', 'Operação de loja'),
        ('Processos', 'Processos'),
        ('Equipamentos', 'Equipamentos'),
   

    )
    tipo_avaliacao = models.ForeignKey(TipoAvaliacao, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, choices=TOPICOS, null=True, blank=True)
    

    def __str__(self):
        return self.nome
    

class Questao(models.Model):
    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural  = 'Questões'
    subtopico = models.ForeignKey(Subtopico, on_delete=models.CASCADE, null=True, blank=True)
    texto = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.texto

class Avaliacao(models.Model):
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural  = 'Avaliações'
    data_av = models.DateTimeField(verbose_name='Data da Avaliação', null=True, blank=True)
    loja = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Loja', null=True, blank=True)
    obs = models.CharField(max_length=255, null=True, blank=True, verbose_name='Observação')
    media_geral = models.CharField(max_length=255, null=True, blank=True, verbose_name='Média')
    medias_subtopicos = models.JSONField(default=dict, blank=True, null=True, verbose_name='Médias por Subtópico')

    def __str__(self):
        return f"Avaliação {self.id} - {self.data_av.strftime('%d/%m/%Y %H:%M')}"

class Resposta(models.Model):
    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural  = 'Respostas'
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='resposta_set', null=True, blank=True)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    resposta = models.FloatField(null=True, blank=True)
    