from django.shortcuts import render
from .models import Produto, Categoria
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

# Create your views here.
class ListViewProdutos(ListView):
    model = Produto
    template_name = 'lista_produtos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qtd_por_pagina = 24

        context["categorias"] = Categoria.objects.all()
        paginator = Paginator(Produto.objects.all(), qtd_por_pagina)
        page_number = self.request.GET.get("page")

        categoria = self.request.GET.get('categoria')

        if categoria:
            paginator = Paginator(Produto.objects.filter(categoria__nome=categoria), qtd_por_pagina)

        context["page_obj"] = paginator.get_page(page_number)

        return context
    

class DetailViewProduto(DetailView):
    model = Produto
    template_name = 'detalhes_produto.html'