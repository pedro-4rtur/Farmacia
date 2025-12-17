from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, Categoria, Comentario, Favorito
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from gestao.models import Cesta, ItemCesta, Pedido, ItemPedido
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class ListViewProdutos(ListView):
    model = Produto
    template_name = 'lista_produtos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qtd_por_pagina = 24

        context["categorias"] = Categoria.objects.all()
        paginator = Paginator(Produto.objects.all().order_by('id'), qtd_por_pagina)
        page_number = self.request.GET.get("page")

        categoria = self.request.GET.get('categoria')

        if categoria:
            produtosPorCategoria = Produto.objects.filter(categoria__nome=categoria).order_by('id')
            paginator = Paginator(produtosPorCategoria, qtd_por_pagina)

        context["page_obj"] = paginator.get_page(page_number)
        
        if self.request.user.is_authenticated:
            cesta = Cesta.objects.filter(usuario=self.request.user)
            context['itens_cesta'] = 0
            if cesta:
                qtd_itens_cesta = ItemCesta.objects.filter(cesta=cesta[0]).count()
                context['itens_cesta'] = qtd_itens_cesta

            favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
            context['favoritos'] = len(list(favoritos)) if favoritos else 0

        return context
    

class DetailViewProduto(DetailView):
    model = Produto
    template_name = 'detalhes_produto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['comentarios'] = Comentario.objects.filter(produto__nome=context['object'].nome)
        context['adicionado_cesta'] = False

        if self.request.user.is_authenticated:
            cesta = Cesta.objects.filter(usuario=self.request.user)
            context['itens_cesta'] = 0
            if cesta:
                qtd_itens_cesta = ItemCesta.objects.filter(cesta=cesta[0]).count()
                context['itens_cesta'] = qtd_itens_cesta

            favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
            context['favoritos'] = len(list(favoritos)) if favoritos else 0

            if ItemCesta.objects.filter(produto__nome=context['object']):
                context['adicionado_cesta'] = True


        return context
    

def adicionar_cesta(request):
    # 1. Verifica se é POST e se o usuário está logado
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'sucesso': False, 'erro': 'Você precisa fazer login para adicionar itens.'}, status=403)

        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')
            
            # 2. Busca o produto
            produto = get_object_or_404(Produto, id=produto_id)
            
            # 3. Pega (ou cria) a cesta do usuário logado
            # O campo no model cesta é 'usuario', que é um OneToOneField com Cliente (seu user model)
            cesta, _ = Cesta.objects.get_or_create(usuario=request.user)
            
            # 4. Verifica se este produto já existe nesta Cesta (ItemCesta)
            item, created = ItemCesta.objects.get_or_create(
                cesta=cesta,
                produto=produto
            )
            
            # 5. Se já existia (não foi criado agora), incrementa a quantidade
            if not created:
                item.quantidade += 1
                item.save()
                
            # 6. Calcula o total de itens para atualizar o ícone
            # Aqui somamos as quantidades de todos os itens (ex: 2 dipironas + 1 fralda = 3 itens)
            # O related_name definido em ItemCesta é 'items'
            total_itens = cesta.items.count()
            
            return JsonResponse({
                'sucesso': True, 
                'novo_total_itens': total_itens
            })
            
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)
    
    return JsonResponse({'sucesso': False, 'erro': 'Método inválido'}, status=400)


def retirar_cesta(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'sucesso': False, 'erro': 'Você precisa fazer login para adicionar itens.'}, status=403)
        
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')
            delete = data.get('delete')

            print(delete)
            
            cesta, _ = Cesta.objects.get_or_create(usuario=request.user)
            
            item = get_object_or_404(ItemCesta, cesta=cesta, produto_id=produto_id)

            if item.quantidade > 1 and not delete:
                item.quantidade -= 1
                item.save()
            else:
                item.delete()
        
            total_itens = cesta.items.count()
            
            return JsonResponse({
                'sucesso': True, 
                'novo_total_itens': total_itens
            })
            
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)
    
    return JsonResponse({'sucesso': False, 'erro': 'Método inválido'}, status=400)


def adicionar_favorito(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'sucesso': False, 'erro': 'Você precisa fazer login para adicionar itens.'}, status=403)
        
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')

            produto = get_object_or_404(Produto, id=produto_id)
            
            favorito, created = Favorito.objects.get_or_create(id_produto=produto, id_cliente=request.user)
            if not created:
                favorito.save()

            contagem = Favorito.objects.filter(id_cliente=request.user).count()

            return JsonResponse({
                'sucesso': True,
                'contagemFavoritos': contagem,
            })

        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)

    return JsonResponse({'sucesso': False, 'erro': 'Método inválido'}, status=400)


def remover_favorito(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'sucesso': False, 'erro': 'Você precisa fazer login para adicionar itens.'}, status=403)
        
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')

            produto = get_object_or_404(Produto, id=produto_id)
            
            favorito = Favorito.objects.filter(id_produto=produto, id_cliente=request.user)
            favorito.delete()

            contagem = Favorito.objects.filter(id_cliente=request.user).count()

            return JsonResponse({
                'sucesso': True,
                'contagemFavoritos': contagem,
            })

        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)

    return JsonResponse({'sucesso': False, 'erro': 'Método inválido'}, status=400)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ListViewFavorito(ListView):
    model = Favorito
    template_name = 'lista_favoritos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categorias"] = Categoria.objects.all()
        
        cesta = Cesta.objects.filter(usuario=self.request.user)
        context['itens_cesta'] = 0
        if cesta:
            qtd_itens_cesta = ItemCesta.objects.filter(cesta=cesta[0]).count()
            context['itens_cesta'] = qtd_itens_cesta

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)

        produtos_favoritos = Produto.objects.filter(id__in=list(favoritos))

        context['produtos_favoritos'] = produtos_favoritos
        context['favoritos'] = len(list(favoritos)) if favoritos else 0

        return context
    

class ListViewPedidos(ListView):
    model = Produto
    template_name = 'pedidos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Geral
        context["categorias"] = Categoria.objects.all()
        
        cesta = Cesta.objects.filter(usuario=self.request.user)
        context['itens_cesta'] = 0
        if cesta:
            qtd_itens_cesta = ItemCesta.objects.filter(cesta=cesta[0]).count()
            context['itens_cesta'] = qtd_itens_cesta

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
        context['favoritos'] = len(list(favoritos)) if favoritos else 0

        # Lógica dos pedidos
        if Pedido.objects.filter(cliente=self.request.user):
            pedidos = Pedido.objects.filter(cliente=self.request.user).order_by("-data_compra")
            context['pedidos'] = pedidos

        return context


@login_required(login_url='login')
def confirmar_pedido(request):
    context = {}
    context["categorias"] = Categoria.objects.all()
        
    cesta = Cesta.objects.filter(usuario=request.user).first()
    if not cesta or cesta.items.all().count() == 0:
        return redirect('cesta')
    context['cesta'] = cesta
    valor_total = 0
    for item in cesta.items.all():
        valor_total += round(item.get_total(), 2)
    context['valor_total'] = round(valor_total, 2)

    favoritos = Favorito.objects.filter(id_cliente=request.user).values_list('id_produto', flat=True)
    context['favoritos'] = len(list(favoritos)) if favoritos else 0
    
    return render(request, 'confirmar_pedido.html', context=context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DetalhesPedidoView(DetailView):
    model = Pedido
    template_name = 'detalhes_pedido.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Geral
        context["categorias"] = Categoria.objects.all()
        
        cesta = Cesta.objects.filter(usuario=self.request.user)
        context['itens_cesta'] = 0
        if cesta:
            qtd_itens_cesta = ItemCesta.objects.filter(cesta=cesta[0]).count()
            context['itens_cesta'] = qtd_itens_cesta

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
        context['favoritos'] = len(list(favoritos)) if favoritos else 0

        return context