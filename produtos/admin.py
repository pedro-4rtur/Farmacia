from django.contrib import admin
from .models import Categoria, Produto, Comentario

# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade', 'valor', 'categoria', 'descricao']
    search_fields = ['nome', 'quantidade', 'valor', 'categoria', 'descricao']

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['comentario', 'produto']
    search_fields = ['produto']


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Comentario, ComentarioAdmin)