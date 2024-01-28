from django.shortcuts import render, redirect


def sugerencia(request):
    return render(request, 'sugerencia.html')


def contacto(request):
    return render(request, 'contacto.html')
