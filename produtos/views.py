from django.shortcuts import get_object_or_404
from .models import Produto, Categoria, Comentario, Favorito
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from gestao.models import Sacola, ItemSacola

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
        
        sacola = Sacola.objects.filter(usuario=self.request.user)
        if sacola:
            qtd_itens_sacola = ItemSacola.objects.filter(sacola=sacola[0]).count()
            context['itens_sacola'] = qtd_itens_sacola

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
        context['favoritos'] = list(favoritos)

        return context
    

class DetailViewProduto(DetailView):
    model = Produto
    template_name = 'detalhes_produto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['comentarios'] = Comentario.objects.filter(produto__nome=context['object'].nome)

        sacola = Sacola.objects.filter(usuario=self.request.user)
        if sacola:
            qtd_itens_sacola = ItemSacola.objects.filter(sacola=sacola[0]).count()
            context['itens_sacola'] = qtd_itens_sacola

        context['adicionado_cesta'] = False
        if ItemSacola.objects.filter(produto__nome=context['object']):
            context['adicionado_cesta'] = True

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
        context['favoritos'] = len(list(favoritos))

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
            
            # 3. Pega (ou cria) a Sacola do usuário logado
            # O campo no model Sacola é 'usuario', que é um OneToOneField com Cliente (seu user model)
            sacola, _ = Sacola.objects.get_or_create(usuario=request.user)
            
            # 4. Verifica se este produto já existe nesta Sacola (ItemSacola)
            item, created = ItemSacola.objects.get_or_create(
                sacola=sacola,
                produto=produto
            )
            
            # 5. Se já existia (não foi criado agora), incrementa a quantidade
            if not created:
                item.save()
                
            # 6. Calcula o total de itens para atualizar o ícone
            # Aqui somamos as quantidades de todos os itens (ex: 2 dipironas + 1 fralda = 3 itens)
            # O related_name definido em ItemSacola é 'items'
            total_itens = sacola.items.count()
            
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
            
            sacola, _ = Sacola.objects.get_or_create(usuario=request.user)
            
            item = get_object_or_404(ItemSacola, sacola=sacola, produto_id=produto_id)

            item.delete()
            
            total_itens = sacola.items.count()
            
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


class ListViewFavorito(ListView):
    model = Favorito
    template_name = 'lista_favoritos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categorias"] = Categoria.objects.all()
        
        sacola = Sacola.objects.filter(usuario=self.request.user)
        if sacola:
            qtd_itens_sacola = ItemSacola.objects.filter(sacola=sacola[0]).count()
            context['itens_sacola'] = qtd_itens_sacola

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)

        produtos_favoritos = Produto.objects.filter(id__in=list(favoritos))

        context['produtos_favoritos'] = produtos_favoritos
        context['favoritos'] = list(favoritos)

        return context