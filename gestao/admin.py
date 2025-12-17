from django.contrib import admin
from .models import Cupom, Pedido, Cesta, ItemCesta, ItemPedido

# Register your models here.
class CupomAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'tipo', 'valor', 'ativo', 'data_inicio', 'data_expiracao', 'uso_maximo_usuario', 'uso_maximo', 'valor_minimo']
    search_fields = ['codigo', 'ativo', 'data_inicio', 'data_expiracao', 'categoria']


class PedidoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'valor_compra', 'data_compra', 'status']
    search_fields = ['cliente']


class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'pedido', 'quantidade', 'preco_unico']
    search_fields = ['produto', 'pedido', 'quantidade', 'preco_unico']

    
class CestaAdmin(admin.ModelAdmin):
    list_display = ['usuario']
    search_fields = ['usuario']


class ItemCestaAdmin(admin.ModelAdmin):
    list_display = ['cesta', 'produto', 'quantidade']
    search_fields = ['cesta', 'produto', 'quantidade']


admin.site.register(Cupom, CupomAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido, ItemPedidoAdmin)
admin.site.register(Cesta, CestaAdmin)
admin.site.register(ItemCesta, ItemCestaAdmin)