from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from produtos.models import Produto, Categoria, Favorito
from .models import Cesta, ItemCesta, Pedido, ItemPedido
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse, HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

# Create your views here.
@method_decorator(login_required(login_url='login'), name='dispatch')
class ViewCesta(View):
    def get(self, request, *args, **kwargs):
        context = {}

        context["categorias"] = Categoria.objects.all()

        cesta = Cesta.objects.get_or_create(usuario=self.request.user)
        itensCesta = ItemCesta.objects.filter(cesta=cesta[0])
        context['produtos'] = itensCesta

        qtd_itens_cesta = itensCesta.count()
        context['qtd_itens_cesta'] = qtd_itens_cesta

        favoritos = Favorito.objects.filter(id_cliente=self.request.user).values_list('id_produto', flat=True)
        context['favoritos'] = list(favoritos)

        subtotal = 0
        for i in itensCesta:
            subtotal += i.get_total()
        
        context['subtotal'] = round(subtotal, 2)

        return render(request, 'cesta.html', context=context)
    

login_required(login_url='login')
def cancelarPedido(request):
    try:
        data = json.loads(request.body)
        pedido_id = data.get('pedido_id')
        
        # 2. Busca o produto
        pedido = get_object_or_404(Pedido, id=pedido_id)

        pedido.status = 'C'
        pedido.save()
        
        return JsonResponse({
            'sucesso': True, 
        })
        
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)
    

login_required(login_url='login')
def criar_pedido(request):
    try:
        cesta = Cesta.objects.filter(usuario=request.user).first()
        pedido = Pedido(cliente=request.user)

        pedido.save()

        valor_total_pedido = 0

        for item in cesta.items.all():
            valor_total_pedido += item.get_total()
            item_pedido = ItemPedido()

            item_pedido.produto = item.produto
            item_pedido.pedido = pedido
            item_pedido.quantidade = item.quantidade
            item_pedido.preco_unico = item.produto.valor
            item_pedido.produto.quantidade -= item_pedido.quantidade
            item_pedido.produto.save()

            item_pedido.save()

        pedido.valor_compra = valor_total_pedido
        pedido.save()

        cesta.delete()
        
        return JsonResponse({
            'sucesso': True, 
        })
        
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)
    

def gerar_comprovante_pdf(request, pk):
    # 1. Busca o pedido (garante que existe e pertence ao usuário se necessário)
    pedido = get_object_or_404(Pedido, id=pk)

    # Segurança opcional: verificar se o usuário é dono do pedido
    if pedido.cliente != request.user:
        return HttpResponse("Não autorizado", status=403)

    # 2. Contexto de dados para o template
    contexto = {
        'pedido': pedido,
        'itens': pedido.pedido_pedido.all(),
        'farmacia': {
            'nome': 'GreenMed+',
            'telefone': '(87) 99999-9999'
        }
    }

    # 3. Renderiza o HTML como string
    html_string = render_to_string('comprovantes/comprovante_venda.html', contexto)

    # 4. Converte para PDF
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # 5. Prepara a resposta HTTP para download
    response = HttpResponse(pdf_file, content_type='application/pdf')
    filename = f"comprovante_pedido_{pedido.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


def dashboard_view(request):
    return render(request, template_name='dashboard.html')