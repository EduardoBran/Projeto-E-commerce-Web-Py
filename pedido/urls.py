from django.urls import path

from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('resumopagar/<int:pk>', views.ResumoPagar.as_view(), name='resumopagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('account/', views.Conta.as_view(), name='conta'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('favoritos/<int:pk>', views.Favoritos.as_view(), name='favoritos'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
    path('gerarBoleto/<int:pk>', views.GerarBoleto.as_view(), name='gerarboleto'),
]
