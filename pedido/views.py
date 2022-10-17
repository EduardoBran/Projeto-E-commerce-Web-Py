import datetime

from categoria.models import Categoria
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from produto.models import Variacao
from utils import utils

from .models import ItemPedido, Pedido


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['categoria'] = self.kwargs.get('categoria', None)
        context['termo'] = self.request.GET.get('termo')
        context['carrinho'] = self.request.session.get('carrinho', {})
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs


class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class ResumoPagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/resumopagamento.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class GerarBoleto(DispatchLoginRequiredMixin, ListView):
    template_name = 'pedido/gerarBoleto.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedidos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        valor_total = Pedido.objects.values('total').last()
        valor_total = valor_total['total']
        valor_total = str(valor_total)

        # print('\n**************\n')
        # print(valor_total)
        # print('\n**************\n')

        context['valor_total'] = valor_total

        current_time = datetime.datetime.now()

        dia = current_time.day
        mes = current_time.month
        ano = current_time.year

        dia = str(dia)
        mes = str(mes)
        ano = str(ano)

        data_hoje = dia + '/' + mes + '/' + ano

        context['data_hoje'] = data_hoje

        return context


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer o login.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]

        # bd_variacoes = list(
        #     Variacao.objects.filter(id__in=carrinho_variacao_ids)
        # )

        # eliminando duas consultas no bd
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unitario = carrinho[vid]['preco_unitario']
            preco_unitario_promocional = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unitario
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unitario_promocional

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, verifique '\
                    'quais produtos foram afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = utils.qtd_total_carrinho(carrinho)
        valor_total_carrinho = utils.total_carrinho(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )

        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']

        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/detalhe.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 5
    ordering = ['-id']
