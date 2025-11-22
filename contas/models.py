from django.db import models
from produtos.models import Produto
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Cliente(AbstractUser):
    telefone = models.CharField(max_length=11)
    endereco = models.CharField()


class Favorito(models.Model):
    id_produto = models.ForeignKey(to=Produto, on_delete=models.CASCADE, related_name='produto_favorito')
    id_cliente = models.ForeignKey(to=Cliente, on_delete=models.CASCADE, related_name='cliente_favorito')