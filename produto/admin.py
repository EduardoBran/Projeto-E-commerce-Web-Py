from django.contrib import admin

from . import models


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria_produto', 'descricao_curta', 'get_preco_formatado',
                    'get_preco_promocional_formatado', 'tipo']

    list_filter = ['categoria_produto', 'tipo']

    list_editable = ['tipo']

    search_fields = ['nome']

    inlines = [
        VariacaoInline
    ]


admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
