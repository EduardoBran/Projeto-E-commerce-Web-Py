from django.contrib import admin

from . import models


class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'criado', 'usuario',
                    'valor_total', 'status', 'modificado']

    list_filter = ['criado', 'usuario', 'status']

    list_editable = ['status']

    list_display_links = ['id', 'criado', 'usuario']

    list_per_page = 20

    search_fields = ['usuario']

    def valor_total(self, obj):
        return 'R$ %.2f' % obj.total

    inlines = [
        ItemPedidoInline
    ]


admin.site.register(models.Pedido, PedidoAdmin)
