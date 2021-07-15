from django.shortcuts import render
from .models import Paciente, Exame, Amostra
# Create your views here.


def index(req):
    pacientes = Paciente.objects.all()
    exames = Exame.objects.all()
    amostras = Amostra.objects.all()

    context = {
        'dados': {
            "pacientes": pacientes,
            "exames": exames,
            "amostras": amostras
        }
    }

    return render(req, 'all.html', context)


def pacientes(req):
    return


def paciente(req, id):
    return


def exames(req):
    return


def exame(req, id):
    return


def amostras(req):
    return


def amostra(req, id):
    return
