
from django import forms
from .models import Catalogo, Producto

class CatalogoForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        fields = ["titulo"]

class ProductoForm(forms.ModelForm):
    imagen = forms.ImageField(required=False)

    class Meta:
        model = Producto
        fields = ["nombre", "precio", "categoria", "imagen"]
