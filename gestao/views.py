from django.shortcuts import render
from django.views.generic import View
from produtos.models import Produto, Categoria, Favorito
from .models import Cesta, ItemCesta

# Create your views here.
class ViewCesta(View):
    def get(self, request, *args, **kwargs):
        context = {}

        context["categorias"] = Categoria.objects.all()

        cesta = Cesta.objects.filter(usuario=self.request.user)
        itensCesta = ItemCesta.objects.filter(cesta=cesta[0])
        context['produtos'] = itensCesta

        if cesta:
            qtd_itens_cesta = itensCesta.count()
            context['qtd_itens_cesta'] = qtd_itens_cesta

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
        context['favoritos'] = list(favoritos)

        subtotal = 0
        for i in itensCesta:
            subtotal += i.get_total()
        
        context['subtotal'] = round(subtotal, 2)

        return render(request, 'cesta.html', context=context)