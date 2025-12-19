from django import forms
from gestao.models import ItemPedido
from .models import Produto

class ItemPedidoModelForm(forms.ModelForm):

    class Meta():
        model = ItemPedido
        fields = '__all__'


class ProdutoModelForm(forms.ModelForm):
    class Meta():
        model = Produto
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilização automática para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-field'