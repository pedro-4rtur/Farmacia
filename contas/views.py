from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomLoginForm, CustomUserCreationForm, ClienteUpdateForm
from django.contrib.auth.decorators import login_required
from produtos.models import Categoria, Favorito
from gestao.models import Cesta, ItemCesta
from .models import Cliente
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash # Importante para não deslogar
from django.contrib.auth.forms import PasswordChangeForm # Importar o form de senha

# Create your views here.
def register_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            user_form = CustomUserCreationForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return redirect('login')
        else:
            user_form = CustomUserCreationForm()

        return render(request, 'registrar.html', {'user_form': user_form})
    else:
        return redirect('pagina_principal')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            login_form = CustomLoginForm(data=request.POST)

            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('pagina_principal')
            
        else:
            login_form = CustomLoginForm()

        return render(request, 'login.html', {'login_form': login_form})
    else:
        return redirect('pagina_principal')


def logout_view(request):
    logout(request)
    return redirect('pagina_principal')


@login_required(login_url='login')
def perfil_view(request):
    # Inicializa os formulários com o estado padrão (GET)
    profile_form = ClienteUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    
    # Variável para controlar qual aba abre ativa em caso de erro
    active_tab = 'dados'

    # CASO 1: Atualização de Perfil
    if 'btn_update_profile' in request.POST:
        profile_form = ClienteUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Seus dados pessoais foram atualizados!')
            return redirect('perfil')
        else:
            active_tab = 'dados' # Mantém na aba de dados se der erro

    # CASO 2: Alteração de Senha
    elif 'btn_change_password' in request.POST:
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user) # Mantém logado
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('perfil')
        else:
            active_tab = 'senha' # Força a aba de senha abrir se der erro

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'active_tab': active_tab,
        'categorias': Categoria.objects.all(),
    }
    
    cesta = Cesta.objects.filter(usuario=request.user)
    if cesta:
        qtd_itens_cesta = ItemCesta.objects.filter(cesta=cesta[0]).count()
        context['itens_cesta'] = qtd_itens_cesta

    favoritos = Favorito.objects.filter(id_cliente=request.user).values_list('id_produto', flat=True)
    context['favoritos'] = list(favoritos)

    return render(request, 'perfil.html', context=context)