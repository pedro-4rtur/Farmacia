from django.contrib import admin
from .models import Cliente, Favorito

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['email', 'telefone', 'endereco', 'date_joined', 'first_name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'username', 'password']
    search_fields = ['username', 'email']


class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['id_produto', 'id_cliente']
    search_fields = ['id_produto', 'id_cliente']


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Favorito, FavoritoAdmin)
