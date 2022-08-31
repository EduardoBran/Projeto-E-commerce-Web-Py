from categoria.models import Categoria
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from produto.models import Produto


class Privacidade(TemplateView):
    model = Produto
    template_name = 'suporte/privacidade.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['categoria'] = self.kwargs.get('categoria', None)
        context['termo'] = self.request.GET.get('termo')
        return context


class Termos(Privacidade):
    template_name = 'suporte/termos.html'


class Sobre(Privacidade):
    template_name = 'suporte/sobre.html'


def ContatoView(request):
    categorias = Categoria.objects.all()

    context = {
        'categorias': categorias
    }
    return render(request, 'suporte/contato.html', context)
