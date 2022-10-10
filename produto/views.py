from categoria.models import Categoria
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from perfil.models import Perfil

from . import models
from .models import Produto


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['categoria'] = self.kwargs.get('categoria', None)
        context['termo'] = self.request.GET.get('termo')
        context['carrinho'] = self.request.session.get('carrinho', {})
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id')
        return qs


class ListaProdutosOrdernarNome(ListaProdutos):
    template_name = 'produto/lista_ordernar_nome.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('nome')
        return qs


class ListaProdutosOrdernarPrecoMaior(ListaProdutos):
    template_name = 'produto/lista_ordernar_precoMaior.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-preco_marketing')
        return qs


class ListaProdutosOrdernarPrecoMenor(ListaProdutos):
    template_name = 'produto/lista_ordernar_precoMenor.html'
    condicao = False

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('preco_marketing')

        # for v in qs.values('preco_marketing_promocional'):
        #     if v['preco_marketing_promocional'] == 0:
        #         self.condicao = True

        # if self.condicao:
        #     qs = qs.order_by('preco_marketing')
        # else:
        #     qs = qs.order_by('preco_marketing_promocional')

        return qs


class ListaProdutosOrdernarDestaque(ListaProdutos):
    template_name = 'produto/lista_ordernar_destaque.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(tipo='D').order_by('?')
        return qs


class Home(ListaProdutos):
    template_name = 'produto/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['produtos1'] = Produto.objects.all()[:3]
        # context['produtos2'] = Produto.objects.all()[3:6]
        # context['produtos3'] = Produto.objects.all()[6:9]

        context['produtoDestaque'] = Produto.objects.filter(
            tipo='D').order_by('?')
        context['produtoLancamento'] = Produto.objects.filter(
            tipo='L').order_by('?')
        context['produtoMaisVendidos'] = Produto.objects.filter(
            tipo='V').order_by('?')

        return context


class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        self.request.session.save()

        return qs


class ProdutoCategoria(ListaProdutos):
    template_name = 'produto/lista_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categoria_produto__nome_cat__iexact=categoria)
        qs = qs.order_by('-id')  # lançamento

        return qs


class ListaProdutosCategoriaOrdernarNome(ProdutoCategoria):
    template_name = 'produto/lista_cat_ordernar_nome.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('nome')
        return qs


class ListaProdutosCategoriaOrdernarPrecoMaior(ProdutoCategoria):
    template_name = 'produto/lista_cat_ordernar_precoMaior.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-preco_marketing')
        return qs


class ListaProdutosCategoriaOrdernarPrecoMenor(ProdutoCategoria):
    template_name = 'produto/lista_cat_ordernar_precoMenor.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('preco_marketing')
        return qs


class ListaProdutosCategoriaOrdernarDestaque(ProdutoCategoria):
    template_name = 'produto/lista_cat_ordernar_destaque.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(tipo='D').order_by('?')
        return qs


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'  # o slug vem da urls.py

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['categoria'] = self.kwargs.get('categoria', None)
        context['produtoDestaque'] = Produto.objects.filter(
            tipo='D').order_by('?')

        context['carrinho'] = self.request.session.get('carrinho', {})

        # recuperando slug do produto via URL
        # slug = self.request.get_full_path()
        # slug = slug.split('/')
        # slug = slug.pop()

        # # filtrando produto através do slug recuperado
        # contexto = Produto.objects.filter(
        #     slug=slug)

        # # percorrendo contexto para virar um dicionario
        # for c in contexto:
        #     precoFor = c

        # # recuperando valor do preco
        # preco = precoFor['preco_marketing_promocional']

        # # condicao pra verificar valor de preço
        # if preco >= 100:
        #     preco = preco / 4
        # else:
        #     preco = preco / 2

        # context['preco'] = preco

        return context


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        # última pág do usuário
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get(
            'select-variacoes')  # valor vindo do form

        if not variacao_id:  # vid=?
            messages.error(
                self.request,
                'Produto não existe.'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        # valor da qtd vindo do form
        valor_quantidade = self.request.GET.get('valor')

        if valor_quantidade == '':
            valor_quantidade = 1

        valor_quantidade = int(valor_quantidade)

        if valor_quantidade <= 0 or valor_quantidade > 10:
            messages.error(
                self.request,
                f'O Produto não foi adicionado.'
                f'O valor deve ser maior ou igual a 1 e menor ou igual a 10.'
            )
            return redirect(http_referer)

        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = valor_quantidade
        slug = produto.slug
        imagem = produto.imagem

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente.'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += quantidade

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no produto "{produto_nome}". '
                    f'Adicionamos {variacao_estoque}x no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                quantidade_carrinho

        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario * quantidade,
                'preco_quantitativo_promocional': preco_unitario_promocional * quantidade,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} (Tam: {variacao_nome}) adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        # valor vindo de _carrinho.html
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:  # vid=?
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]

        messages.warning(
            self.request,
            f'Produto {carrinho["produto_nome"]} (Tam: {carrinho["variacao_nome"]}) '
            f'removido do seu carrinho.'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {}),
            'categorias': Categoria.objects.all(),
            'categoria': self.kwargs.get('categoria', None),
            'produtoMaisVendidos': Produto.objects.filter(
                tipo='V').order_by('?')

        }
        return render(self.request, 'produto/carrinho.html', contexto)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
            'categorias': Categoria.objects.all(),
            'categoria': self.kwargs.get('categoria', None),
            'produtoLancamento': Produto.objects.filter(
                tipo='L').order_by('?')
        }

        return render(self.request, 'produto/resumodacompra.html', contexto)
