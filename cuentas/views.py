from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistroForm


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("inicio")
    else:
        form = RegistroForm()
    return render(request, "cuentas/register.html", {"form": form})

def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario:
            login(request, usuario)
            return redirect("inicio")
        else:
            return render(request, "cuentas/login.html", {"error": "Usuario o contraseña incorrectos"})
    return render(request, "cuentas/login.html")

def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")
