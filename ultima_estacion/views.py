from django.shortcuts import render


def inicio(request):
    return render(request, "app1/index.html")


def mecanicas(request):
    return render(request, "app1/mecanicas.html")


def pagina(request):
    return render(request, "app1/pagina.html")


def contacto(request):
    return render(request, "app1/contacto.html")
