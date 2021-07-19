from django.shortcuts import render
from django.db import connection
import datetime

from ..models import Paciente, Exame, Amostra

cursor = connection.cursor()


def home(req):
    pacientes = Paciente.objects.all()[:5]
    exames = Exame.objects.all()[:5]
    amostras = Amostra.objects.all()[:5]
    context = {
        'dados': {
            "pacientes": {
                "quantidade": len(Paciente.objects.all()),
                "valores": pacientes,
            },
            "exames": {
                "quantidade": len(Exame.objects.all()),
                "valores": exames,
            },
            "amostras": {
                "quantidade": len(Amostra.objects.all()),
                "valores": amostras,
            }
        }
    }
    return render(req, 'home.html', context)

# Funções auxiliares


def runSQLQuery(query, args):
    cursor.execute(query, args)
    return cursor.fetchall()


def stringToDatetime(date, time):
    date = list(
        map(lambda x: int(x), date.split('-')))
    time = list(
        map(lambda x: int(x), time.split(':')))

    return datetime.datetime(
        date[0], date[1], date[2],
        time[0], time[1]
    )
