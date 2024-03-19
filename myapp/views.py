from django.shortcuts import render
from .models import Cobertura, Embalagem, TipoSabor

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def cardapio(request):
    embalagens = Embalagem.objects.filter(ativo=True)
    tipo_sabor = TipoSabor.objects.filter(ativo=True)
    coberturas = Cobertura.objects.filter(ativo=True)
    context = {
        'embalagens': embalagens,
        'tipo_sabor': tipo_sabor,
        'coberturas': coberturas
    }
    return render(request, 'cardapio.html', context)
