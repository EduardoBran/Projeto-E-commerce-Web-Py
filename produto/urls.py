from django.urls import path

from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('busca/', views.Busca.as_view(), name='busca'),

    path('produtos/', views.ListaProdutos.as_view(), name='lista'),
    path('produto/<slug>', views.DetalheProduto.as_view(), name='detalhe'),

    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(),
         name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(),
         name='removerdocarrinho'),

    path('adicionaraocarrinhomodal/', views.AdicionarAoCarrinhoModal.as_view(),
         name='adicionaraocarrinhomodal'),
    path('removerdocarrinhomodal/', views.RemoverDoCarrinhoModal.as_view(),
         name='removerdocarrinhomodal'),

    path('adicionarfavorito/<slug>',  views.AdicionarAoFavorito.as_view(),
         name='adicionarfavorito'),
    path('removerfavorito/<slug>',  views.RemoverFavorito.as_view(),
         name='removerfavorito'),

    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name='resumodacompra'),

    path('categoria/<str:categoria>',
         views.ProdutoCategoria.as_view(), name='categoria'),

    path('produtos/ord_nome',
         views.ListaProdutosOrdernarNome.as_view(), name='ord_nome'),
    path('produtos/ord_preco_maior',
         views.ListaProdutosOrdernarPrecoMaior.as_view(), name='ord_preco_maior'),
    path('produtos/ord_preco_menor',
         views.ListaProdutosOrdernarPrecoMenor.as_view(), name='ord_preco_menor'),
    path('produtos/ord_destaque',
         views.ListaProdutosOrdernarDestaque.as_view(), name='ord_destaque'),

    path('produtos/<str:categoria>/ord_nome',
         views.ListaProdutosCategoriaOrdernarNome.as_view(), name='categoria_ord_nome'),
    path('produtos/<str:categoria>/ord_preco_maior',
         views.ListaProdutosCategoriaOrdernarPrecoMaior.as_view(), name='categoria_ord_preco_maior'),
    path('produtos/<str:categoria>/ord_preco_menor',
         views.ListaProdutosCategoriaOrdernarPrecoMenor.as_view(), name='categoria_ord_preco_menor'),
    path('produtos/<str:categoria>/ord_destaque',
         views.ListaProdutosCategoriaOrdernarDestaque.as_view(), name='categoria_ord_destaque'),
]
