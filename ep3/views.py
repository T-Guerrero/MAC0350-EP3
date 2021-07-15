from django.shortcuts import get_object_or_404, render
from django.db import connection

from .models import Paciente, Exame, Amostra
# Create your views here.

cursor = connection.cursor()


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
    exames_query = ' \
                    SELECT E.id, E.data_solicitacao, E.data_execucao, E.tipo, E.virus \
                    FROM ep3_exame as E  \
                    WHERE E.paciente_id = %s \
                    '
    amostras_query = ' \
                    SELECT A.id, A.exame_id, A.data_coleta, A.tipo_material \
                    FROM ep3_amostra as A \
                    WHERE A.paciente_id = %s \
                    '
    paciente = get_object_or_404(Paciente, id=id)
    exames = runSQLQuery(exames_query, (id,))
    amostras = runSQLQuery(amostras_query, (id,))
    context = {
        'paciente': paciente,
        'exames': exames,
        'amostras': amostras
    }
    return render(req, 'paciente.html', context)


def exames(req):
    exames = Exame.objects.all()
    return render(req, 'exames.html', {'exames': exames})


def exame(req, id):
    amostras_query = ' \
                    SELECT A.id, A.data_coleta, A.tipo_material \
                    FROM ep3_amostra as A \
                    WHERE A.exame_id = %s; \
                    '
    exame = get_object_or_404(Exame, id=id)
    amostras = runSQLQuery(amostras_query, (id,))
    context = {
        'exame': exame,
        'amostras': amostras
    }
    return render(req, 'exame.html', context)


def amostras(req):
    amostras = Amostra.objects.all()
    return render(req, 'amostras.html', {'amostras': amostras})


def amostra(req, id):
    amostra = get_object_or_404(Amostra, id=id)
    return render(req, 'amostra.html', {'amostra': amostra})

# Funções auxiliares


def runSQLQuery(query, args):
    cursor.execute(query, args)
    return cursor.fetchall()
