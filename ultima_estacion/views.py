from django.shortcuts import render


def inicio(request):
    return render(request, "index.html")


def mecanicas(request):
    return render(request, "mecanicas.html")
