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
from produtos.views import ListViewProdutos, DetailViewProduto, adicionar_cesta, retirar_cesta, adicionar_favorito, remover_favorito, ListViewFavorito, ListViewPedidos, confirmar_pedido, DetalhesPedidoView
from gestao.views import ViewCesta, criar_pedido, gerar_comprovante_pdf, dashboard_view, GestaoPedidosView, GestaoProdutosListView, GestaoUpdateProduto, DetalhesProduto, DeleteProduto, GestaoDetalhesPedido, confirmar_entrega
from contas.views import login_view, logout_view, register_view, perfil_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ListViewProdutos.as_view(), name='pagina_principal'),
    path('<int:pk>/', DetailViewProduto.as_view(), name='pagina_produto'),
    path('pedidos', ListViewPedidos.as_view(), name='pedidos'),
    path('pedidos/confirmar-pedido', confirmar_pedido, name='confirmar_pedido'),
    path('pedidos/criar-pedido', criar_pedido, name='criar_pedido'),
    path('pedidos/detalhes-pedido/<int:pk>', DetalhesPedidoView.as_view(), name='detalhes_pedido'),
    path('pedidos/detalhes_pedido/<int:pk>/comprovante', gerar_comprovante_pdf, name='comprovante'),
    path('cesta', ViewCesta.as_view(), name='cesta'),
    path('cesta/adicionar', adicionar_cesta, name="adicionar_cesta"),
    path('cesta/remover', retirar_cesta, name='remover_cesta'),
    path('favoritos', ListViewFavorito.as_view(), name='favoritos'),
    path('favorito/adicionar', adicionar_favorito, name='adicionar_favorito'),
    path('favorito/remover', remover_favorito, name='remover_favorito'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('registrar', register_view, name='registrar'),
    path('perfil', perfil_view, name='perfil'),
    path('gestao/dashboard', dashboard_view, name='dashboard'),
    path('gestao/pedidos', GestaoPedidosView.as_view(), name='gestao_pedidos'),
    path('gestao/pedidos/<int:pk>', GestaoDetalhesPedido.as_view(), name='gestao_detalhes_pedido'),
    path('gestao/pedidos/<int:pk>/confirmar-entrega', confirmar_entrega, name='alterar_status'),
    path('gestao/produtos', GestaoProdutosListView.as_view(), name='gestao_produtos'),
    path('gestao/produtos/<int:pk>', DetalhesProduto.as_view(), name='gestao_detalhes_produto'),
    path('gestao/produtos/<int:pk>/delete', DeleteProduto.as_view(), name='delete_produto'),
    path('gestao/produtos/<int:pk>/update', GestaoUpdateProduto.as_view(), name='edicao_produto')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)