from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Cliente

class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Ops! Nome de usuário ou senha incorretos.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilizando o campo de usuário
        self.fields['username'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Digite seu nome de usuário'
        })
        
        # Estilizando o campo de senha
        self.fields['password'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': '••••••••'
        })


class CustomUserCreationForm(UserCreationForm):
    # Estilizando o campo de usuário
    class Meta:
        model = Cliente
        # Inclui os campos padrão + os seus personalizados
        fields = ('username', 'email', 'telefone', 'endereco')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilização automática para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-field'
            
            # Placeholders específicos (opcional)
            if field_name == 'username':
                field.label = 'Nome de usuário'
            elif field_name == 'email':
                field.label = 'E-mail'
            elif field_name == 'telefone':
                field.widget.attrs['placeholder'] = '(XX) XXXXX-XXXX'
            elif field_name == 'endereco':
                field.widget.attrs['placeholder'] = 'Rua, Número, Bairro...'
                field.widget.attrs['rows'] = 3 # Se for Textarea
            elif field_name == 'password1':
                field.label = 'Senha'
            elif field_name == 'password2':
                field.label = 'Confirme sua senha'