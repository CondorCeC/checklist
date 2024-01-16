from django.contrib import admin
from .models import UserChecklist, Questao, Resposta, Avaliacao, Subtopico, TipoAvaliacao

@admin.register(UserChecklist)
class UserChecklistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_grupos')
    def get_grupos(self, obj):
        return ", ".join([grupo.name for grupo in obj.grupos.all()])
    get_grupos.short_description = 'Grupos' 

class RespostaInline(admin.TabularInline): 
    model = Resposta
    extra = 1 

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto', 'subtopico')
    list_editable = ('texto', 'subtopico')

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_av', 'loja', 'obs')
    list_editable = ('loja',)
    inlines = [RespostaInline]

@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('id', 'resposta', 'avaliacao', 'questao')
class QuestaoInline(admin.StackedInline): 
    model = Questao
    extra = 10

@admin.register(Subtopico)
class SubtopicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_avaliacao')
    list_editable = ('tipo_avaliacao',)
    inlines = [QuestaoInline]  

class SubtopicoInline(admin.StackedInline):
    model = Subtopico
    extra = 1

@admin.register(TipoAvaliacao)
class TipoAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', )
    list_editable = ('titulo',)
    inlines = [SubtopicoInline]
