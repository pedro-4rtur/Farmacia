from django.contrib import admin
from .models import Cupom, Pedido

# Register your models here.
class CupomAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'tipo', 'valor', 'ativo', 'data_inicio', 'data_expiracao', 'uso_maximo_usuario', 'uso_maximo', 'valor_minimo']
    search_fields = ['codigo', 'ativo', 'data_inicio', 'data_expiracao', 'categoria']


class PedidoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'valor_compra', 'data_compra']
    search_fields = ['cliente']


admin.site.register(Cupom, CupomAdmin)
admin.site.register(Pedido, PedidoAdmin)