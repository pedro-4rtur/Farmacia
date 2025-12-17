from django.db import models
from produtos.models import Produto, Categoria
from contas.models import Cliente

# Create your models here.
class Cupom(models.Model):
    tipo_desconto = [
        ('Percentual', '%'),
        ('Fixo', 'R$')
    ]

    codigo = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(choices=tipo_desconto)
    valor = models.FloatField()
    ativo = models.BooleanField()
    data_inicio = models.DateTimeField()
    data_expiracao = models.DateTimeField()
    uso_maximo_usuario = models.IntegerField(default=1) 
    uso_maximo = models.IntegerField(null=True)
    valor_minimo = models.FloatField(null=True)
    categoria = models.ManyToManyField(Categoria)


class Cesta(models.Model):
    usuario = models.OneToOneField(Cliente, on_delete=models.CASCADE)


class ItemCesta(models.Model):
    cesta = models.ForeignKey(Cesta, on_delete=models.CASCADE, related_name='items')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def get_total(self):
        return round(self.produto.valor * self.quantidade, 2)


class Pedido(models.Model):
    escolhas = (
        ('P', 'Pendente'),
        ('E', 'Enviado'),
        ('C', 'Cancelado'),
    )
    status = models.CharField(choices=escolhas, default='P')
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, related_name='pedido_cliente')
    data_compra = models.DateTimeField(auto_now_add=True)
    valor_compra = models.FloatField(blank=True, null=True)


class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto_pedido')
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pedido_pedido')
    quantidade = models.IntegerField(default=1)
    preco_unico = models.FloatField()

    def __str__(self):
        return f'Produto: {self.produto.nome} \nPedido: {self.pedido} \nQuantidade = {self.quantidade} \nPreço único: {self.preco_unico}'
    
    def get_total(self):
        return round(self.preco_unico * self.quantidade, 2)