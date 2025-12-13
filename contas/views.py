from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm, CustomUserCreationForm

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