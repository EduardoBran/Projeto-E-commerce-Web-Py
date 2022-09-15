from categoria.models import Categoria
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
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


class Pergunta(Privacidade):
    template_name = 'suporte/perguntas.html'


class Contato(Privacidade, FormView):
    template_name = 'suporte/contato.html'
    form_class = ContatoForm
    success_url = reverse_lazy('suporte:contato')

    def form_valid(self, form, *args, **kwargs):
        form.send_email()
        messages.success(self.request, 'E-mail enviado com sucesso.')
        return super(Contato, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail.')
        return super(Contato, self).form_valid(form, *args, **kwargs)


# def ContatoView(request):
#     if str(request.method) == 'POST':
#         form = ContatoForm(request.POST)
#         if form.is_valid():
#             form.send_email()
#             messages.success(request, 'E-mail enviado com sucesso.')
#             form = ContatoForm()
#         else:
#             messages.error(request, 'Email NÃO FOI enviado com sucesso.')
#     else:
#         form = ContatoForm()

#     categorias = Categoria.objects.all()

#     context = {
#         'categorias': categorias,
#         'form': form
#     }
#     return render(request, 'suporte/contato.html', context)
