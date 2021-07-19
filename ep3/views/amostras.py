from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .general import *


def amostras(req):
    amostras = Amostra.objects.all()
    keys = ['ID', 'Paciente', 'Exame', 'Tipo de Material', 'Data de coleta']
    return render(req, 'amostras.html', {'amostras': amostras, 'keys': keys})


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
        paciente = int(req.POST['paciente']) or None
        exame = int(req.POST['exame']) or None
        data_coleta = req.POST['data_coleta'] or None
        tempo_coleta = req.POST['tempo_coleta'] or None
        tipo_material = req.POST['tipo_material'] or None

        data_coleta = stringToDatetime(data_coleta, tempo_coleta)

        if (Exame.objects.get(id=exame).paciente_id != paciente):
            raise Exception('Exame não corresponde ao paciente selecionado')

        amostra = Amostra.objects.create(
            paciente_id=paciente,
            exame_id=exame,
            data_coleta=data_coleta,
            tipo_material=tipo_material
        )
        return HttpResponseRedirect(reverse('amostras'))
    except Exception as e:
        pacientes = Paciente.objects.all()
        exames = Exame.objects.all()
        return render(req, 'inserir_amostra.html', {
            'pacientes': pacientes,
            'exames': exames,
            'error_message': 'Erros:' + str(e),
        })


def delete_amostra(_, id):
    amostra = get_object_or_404(Amostra, id=id)
    amostra.delete()
    return HttpResponseRedirect(reverse('amostras'))


def edit_amostra(req, id):
    amostra = get_object_or_404(Amostra, id=id)
    amostra.tempo_coleta = str(amostra.data_coleta.time())
    amostra.data_coleta = str(amostra.data_coleta.date())
    pacientes = Paciente.objects.all()
    exames = Exame.objects.all()
    context = {
        'amostra': amostra,
        'pacientes': pacientes,
        'exames': exames
    }
    return render(req, 'atualizar_amostra.html', context)


def update_amostra(req, id):
    amostra = get_object_or_404(Amostra, id=id)
    amostra.tempo_coleta = str(amostra.data_coleta.time())
    amostra.data_coleta = str(amostra.data_coleta.date())
    try:
        paciente = req.POST['paciente'] or None
        exame = req.POST['exame'] or None
        data_coleta = req.POST['data_coleta'] or None
        tempo_coleta = req.POST['tempo_coleta'] or None
        tipo_material = req.POST['tipo_material'] or None

        data_coleta = stringToDatetime(data_coleta, tempo_coleta)

        if (Exame.objects.get(id=exame).paciente_id != int(paciente)):
            raise Exception('Exame não corresponde ao paciente selecionado')

        Amostra.objects.filter(id=id).update(
            paciente_id=paciente,
            exame_id=exame,
            data_coleta=data_coleta,
            tipo_material=tipo_material
        )
        return HttpResponseRedirect(reverse('amostra', kwargs={'id': id}))
    except Exception as e:
        pacientes = Paciente.objects.all()
        exames = Exame.objects.all()
        context = {
            'amostra': amostra,
            'pacientes': pacientes,
            'exames': exames,
            'error_message': 'Erros:' + str(e),
        }
        return render(req, 'atualizar_amostra.html', context)
