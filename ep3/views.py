from django.shortcuts import render
from .models import Paciente, Exame, Amostra
# Create your views here.


def index(req):
    pacientes = Paciente.objects.all()[:5]
    exames = Exame.objects.all()[:5]
    amostras = Amostra.objects.all()[:5]
    context = {
        'dados': {
            "pacientes": pacientes,
            "exames": exames,
            "amostras": amostras
        }
    }
    return render(req, 'all.html', context)


def pacientes(req):
    pacientes = Paciente.objects.all()
    return render(req, 'pacientes.html', {'pacientes': pacientes})


def paciente(req, id):
    return


def exames(req):
    exames = Exame.objects.all()
    return render(req, 'exames.html', {'exames': exames})


def exame(req, id):
    return


def amostras(req):
    amostras = Amostra.objects.all()
    return render(req, 'amostras.html', {'amostras': amostras})


def amostra(req, id):
    return
