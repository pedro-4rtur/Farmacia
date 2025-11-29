from django.db import models

# Create your models here.
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=250)
    quantidade = models.IntegerField()
    valor = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='categoria_produto')
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    comentario = models.TextField(blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='comentario_produto')

    def __str__(self):
        return f'comentario no produto ${self.produto}'