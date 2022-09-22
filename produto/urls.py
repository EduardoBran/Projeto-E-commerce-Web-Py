from django.urls import path

from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('produtos/', views.ListaProdutos.as_view(), name='lista'),
    path('produto/<slug>', views.DetalheProduto.as_view(), name='detalhe'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(),
         name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(),
         name='removerdocarrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name='resumodacompra'),
    path('busca/', views.Busca.as_view(), name='busca'),
    path('categoria/<str:categoria>',
         views.ProdutoCategoria.as_view(), name='categoria'),
    path('produtos/ord_nome',
         views.ListaProdutosOrdernarNome.as_view(), name='ord_nome'),
    path('produtos/ord_nome/<str:categoria>',
         views.ListaProdutosCategoriaOrdernarNome.as_view(), name='categoria_ord_nome'),

]
