from django.urls import path

from . import views

app_name = 'suporte'

urlpatterns = [
    path('privacidade/', views.Privacidade.as_view(), name='privacidade'),
    path('termos/', views.Termos.as_view(), name='termos'),
    path('sobre/', views.Sobre.as_view(), name='sobre'),
    path('perguntasfrequentes/', views.Pergunta.as_view(), name='perguntas'),
    path('contato/', views.Contato.as_view(), name='contato'),
]
