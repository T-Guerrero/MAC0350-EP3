from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db import connection
from django.urls import reverse
import datetime

from .models import Paciente, Exame, Amostra
# Create your views here.

cursor = connection.cursor()


def home(req):
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
    return render(req, 'home.html', context)


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


def new_paciente(req):
    return render(req, 'inserir_paciente.html')


def create_paciente(req):
    cpf = req.POST['cpf']
    nome = req.POST['nome']
    data_nascimento = req.POST['data_nascimento']
    endereco = req.POST['endereco']

    try:
        paciente = Paciente(cpf=cpf, nome=nome,
                            data_nascimento=data_nascimento, endereco=endereco)
        paciente.save()
        return HttpResponseRedirect(reverse('pacientes'))
    except:
        return render(req, 'inserir_paciente.html', {
            'error_message': "Paciente inválido",
        })


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


def new_exame(req):
    pacientes = Paciente.objects.all()
    tipos = ['PCR', 'Anticorpos']

    context = {
        'pacientes': pacientes,
        'tipos': tipos
    }

    return render(req, 'inserir_exame.html', context)


def create_exame(req):
    try:
        paciente = req.POST['paciente']
        virus = req.POST['virus']
        tipo = req.POST['tipo']
        data_solicitacao = req.POST['data_solicitacao']
        tempo_solicitacao = req.POST['tempo_solicitacao']
        data_execucao = req.POST['data_execucao']
        tempo_execucao = req.POST['tempo_execucao']

        data_solicitacao = stringToDatetime(
            data_solicitacao, tempo_solicitacao)
        data_execucao = stringToDatetime(data_execucao, tempo_execucao)

        exame = Exame(
            paciente_id=paciente,
            virus=virus,
            tipo=tipo,
            data_solicitacao=data_solicitacao,
            data_execucao=data_execucao
        )
        exame.save()
        return HttpResponseRedirect(reverse('exames'))
    except Exception as e:
        pacientes = Paciente.objects.all()
        tipos = ['PCR', 'Anticorpos']
        return render(req, 'inserir_exame.html', {
            'pacientes': pacientes,
            'tipos': tipos,
            'error_message': "Exame inválido",
        })


def amostras(req):
    amostras = Amostra.objects.all()
    return render(req, 'amostras.html', {'amostras': amostras})


def amostra(req, id):
    amostra = get_object_or_404(Amostra, id=id)
    return render(req, 'amostra.html', {'amostra': amostra})


def new_amostra(req):
    pacientes = Paciente.objects.all()
    exames = Exame.objects.all()

    context = {
        'pacientes': pacientes,
        'exames': exames
    }

    return render(req, 'inserir_amostra.html', context)


def create_amostra(req):
    try:
        paciente = req.POST['paciente']
        exame = req.POST['exame']
        data_coleta = req.POST['data_coleta']
        tempo_coleta = req.POST['tempo_coleta']
        tipo_material = req.POST['tipo_material']

        data_coleta = stringToDatetime(data_coleta, tempo_coleta)

        if (Exame.objects.get(id=exame).paciente_id != int(paciente)):
            raise Exception('Exame não corresponde ao paciente selecionado')

        amostra = Amostra(
            paciente_id=paciente,
            exame_id=exame,
            data_coleta=data_coleta,
            tipo_material=tipo_material
        )
        amostra.save()
        return HttpResponseRedirect(reverse('amostras'))
    except Exception as e:
        pacientes = Paciente.objects.all()
        exames = Exame.objects.all()
        return render(req, 'inserir_amostra.html', {
            'pacientes': pacientes,
            'exames': exames,
            'error_message': "Amostra inválida",
        })

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
