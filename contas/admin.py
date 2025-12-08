from django.contrib import admin
from .models import Cliente

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['email', 'telefone', 'endereco', 'date_joined', 'first_name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'username', 'password']
    search_fields = ['username', 'email']

admin.site.register(Cliente, ClienteAdmin)