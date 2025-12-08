from django.shortcuts import render
from django.views.generic import ListView
from produtos.models import Favorito

# Create your views here.
class ListViewFavoritos(ListView):
    model = Favorito
    template_name = 'lista_favoritos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favoritos = Favorito.objects.filter(id_cliente=self.request.user)

        return context