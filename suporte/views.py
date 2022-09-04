from categoria.models import Categoria
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from produto.models import Produto

from .forms import *


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
    if str(request.method) == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.send_email()
            messages.success(request, 'Email enviado com sucesso.')
            form = ContatoForm()
        else:
            messages.error(request, 'Email NÃO FOI enviado com sucesso.')
    else:
        form = ContatoForm()

    categorias = Categoria.objects.all()

    context = {
        'categorias': categorias,
        'form': form
    }
    return render(request, 'suporte/contato.html', context)
