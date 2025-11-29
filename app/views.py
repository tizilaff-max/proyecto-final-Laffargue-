from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Catalogo, Producto
from .forms import CatalogoForm, ProductoForm
from django.contrib.auth import login
from django.db.models import Q



def lista_productos(request):
    query = request.GET.get('q', '')
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(categoria__nombre__icontains=query) |
            Q(color__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    return render(request, 'app/lista_productos.html', {
        'productos': productos,
        'query': query
    })


def iniciar_sesion(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect("inicio")
    else:
        formulario = AuthenticationForm()
    return render(request, 'appfinal/iniciar_sesion.html', {'formulario': formulario})



def inicio(request):
    categorias = Catalogo.objects.all()
    categorias_con_productos = []

    for categoria in categorias:
        productos = Producto.objects.filter(categoria=categoria)[:3]
        categorias_con_productos.append({
            'categoria': categoria,
            'productos': productos
        })

    return render(request, 'app/inicio.html', {
        'categorias_con_productos': categorias_con_productos
    })


def categorias(request):
    categorias = Catalogo.objects.all()
    return render(request, 'app/categorias.html', {'categorias': categorias})

from django.shortcuts import get_object_or_404, render
from .models import Catalogo, Producto

def productos_por_categoria(request, nombre_categoria):
    categoria = get_object_or_404(Catalogo, titulo=nombre_categoria)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'app/productos_por_categoria.html', {'categoria': categoria, 'productos': productos})


@login_required(login_url="iniciar_sesion")
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("detalle_producto", pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, "app/crear_producto.html", {"form": form, "editar": True})

@login_required(login_url="iniciar_sesion")
def borrar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect("lista_productos")
    return render(request, "app/borrar_producto.html", {"producto": producto})


@login_required(login_url="iniciar_sesion")
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "app/detalle_producto.html", {"producto": producto})

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def registro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("inicio")
    else:
        form = UserCreationForm()
    return render(request, "app/registro.html", {"formulario": form})

class ProductoListView(ListView):
    model = Producto
    template_name = "app/lista_productos.html"
    context_object_name = "productos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['productos']:
            context['mensaje'] = "No hay productos cargados en la base."
        return context


class CatalogoCreateView(LoginRequiredMixin, CreateView):
    model = Catalogo
    form_class = CatalogoForm
    template_name = "app/crear_catalogo.html"
    success_url = reverse_lazy("inicio")
    login_url = "iniciar_sesion"



@login_required(login_url="iniciar_sesion")
def crear_catalogo(request):
    if request.method == "POST":
        form = CatalogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("inicio")
    else:
        form = CatalogoForm()
    return render(request, "app/crear_catalogo.html", {"form": form})


@login_required(login_url="iniciar_sesion")
def crear_producto(request, producto):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm(request.POST, request.FILES, instance=producto)
    return render(request, "app/crear_producto.html", {"form": form})


def about(request):
    return render(request, 'app/about.html')

def cerrar_sesion(request, logout):
    logout(request)
    return redirect("inicio")
