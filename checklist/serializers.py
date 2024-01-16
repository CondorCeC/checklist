from rest_framework import serializers
from .models import  Avaliacao, Resposta


class RespostaSerializer(serializers.ModelSerializer):
    questao_texto = serializers.CharField(source='questao.texto')
    
    class Meta:
        model = Resposta
        fields = ['questao_id', 'questao_texto', 'resposta']

class ChecklistAvSerializer(serializers.ModelSerializer):
    medias_subtopicos = serializers.SerializerMethodField()
    media_geral = serializers.FloatField()
    respostas = RespostaSerializer(many=True, source='resposta_set')
    loja = serializers.CharField(source='loja.name')
    data_av = serializers.DateTimeField()
    
    class Meta:
        model = Avaliacao
        fields = ['id', 'loja', 'data_av', 'medias_subtopicos', 'media_geral', 'respostas', 'obs']
    
    def get_medias_subtopicos(self, obj):
      
        return obj.medias_subtopicos