from django import forms
from gestao.models import ItemPedido

class ProdutoModelForm(forms.ModelForm):

    class Meta():
        model = ItemPedido
        fields = '__all__'