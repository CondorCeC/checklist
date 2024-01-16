from django.urls import path
from checklist import views


app_name = 'checklist'
urlpatterns = [
    path('', views.home, name='home'),
    path('checklist/user/login', views.login_checklist, name='login_checklist'),
    path('checklist/user/logout', views.logout_checklist, name='logout_checklist'),
    path('checklist/checklistav/<str:loja_name>/', views.checklistav, name='checklistav'),
    path('checklist/lojas/', views.listar_loja, name='listar_loja'),
    path('checklist/avaliar/<str:loja_name>/', views.salvar_avaliacao, name='salvar_avaliacao'),
    path('api/checklistav/', views.ChecklistListAv.as_view(), name='ChecklistList-listav'),

]