"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from produtos.views import ListViewProdutos, DetailViewProduto, adicionar_cesta, retirar_cesta, adicionar_favorito, remover_favorito

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ListViewProdutos.as_view(), name='pagina_principal'),
    path('<int:pk>/', DetailViewProduto.as_view(), name='pagina_produto'),
    path('cesta/adicionar', adicionar_cesta, name="adicionar_cesta"),
    path('cesta/remover', retirar_cesta, name='remover_cesta'),
    path('favorito/adicionar', adicionar_favorito, name='adicionar_favorito'),
    path('favorito/remover', remover_favorito, name='remover_favorito'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)