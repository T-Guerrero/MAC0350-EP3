from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .general import *


def exames(req):
    exames = Exame.objects.all()
    keys = ['ID', 'Paciente', 'Vírus', 'Tipo',
            'Data de Solicitação', 'Data de Execução']
    return render(req, 'exames.html', {'exames': exames, 'keys': keys})


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
        paciente = req.POST['paciente'] or None
        virus = req.POST['virus'] or None
        tipo = req.POST['tipo'] or None
        data_solicitacao = req.POST['data_solicitacao'] or None
        tempo_solicitacao = req.POST['tempo_solicitacao'] or None
        data_execucao = req.POST['data_execucao'] or None
        tempo_execucao = req.POST['tempo_execucao'] or None

        data_solicitacao = stringToDatetime(
            data_solicitacao, tempo_solicitacao)
        data_execucao = stringToDatetime(data_execucao, tempo_execucao)

        Exame.objects.create(
            paciente_id=paciente,
            virus=virus,
            tipo=tipo,
            data_solicitacao=data_solicitacao,
            data_execucao=data_execucao
        )
        return HttpResponseRedirect(reverse('exames'))
    except Exception as e:
        pacientes = Paciente.objects.all()
        tipos = ['PCR', 'Anticorpos']
        return render(req, 'inserir_exame.html', {
            'pacientes': pacientes,
            'tipos': tipos,
            'error_message': "Erros: " + str(e),
        })


def delete_exame(_, id):
    exame = get_object_or_404(Exame, id=id)
    exame.delete()
    return HttpResponseRedirect(reverse('exames'))


def edit_exame(req, id):
    exame = get_object_or_404(Exame, id=id)
    pacientes = Paciente.objects.all()
    tipos = ['PCR', 'Anticorpos']
    exame.tempo_execucao = str(exame.data_execucao.time())
    exame.data_execucao = str(exame.data_execucao.date())
    exame.tempo_solicitacao = str(exame.data_solicitacao.time())
    exame.data_solicitacao = str(exame.data_solicitacao.date())
    context = {
        'exame': exame,
        'pacientes': pacientes,
        'tipos': tipos
    }
    return render(req, 'atualizar_exame.html', context)


def update_exame(req, id):
    exame = get_object_or_404(Exame, id=id)
    exame.tempo_execucao = str(exame.data_execucao.time())
    exame.data_execucao = str(exame.data_execucao.date())
    exame.tempo_solicitacao = str(exame.data_solicitacao.time())
    exame.data_solicitacao = str(exame.data_solicitacao.date())
    try:
        paciente = req.POST['paciente'] or None
        virus = req.POST['virus'] or None
        tipo = req.POST['tipo'] or None
        data_solicitacao = req.POST['data_solicitacao'] or None
        tempo_solicitacao = req.POST['tempo_solicitacao'] or None
        data_execucao = req.POST['data_execucao'] or None
        tempo_execucao = req.POST['tempo_execucao'] or None

        data_solicitacao = stringToDatetime(
            data_solicitacao, tempo_solicitacao)
        data_execucao = stringToDatetime(data_execucao, tempo_execucao)

        Exame.objects.filter(id=id).update(
            paciente_id=paciente,
            virus=virus,
            tipo=tipo,
            data_solicitacao=data_solicitacao,
            data_execucao=data_execucao
        )
        return HttpResponseRedirect(reverse('exame', kwargs={'id': id}))
    except Exception as e:
        pacientes = Paciente.objects.all()
        tipos = ['PCR', 'Anticorpos']
        return render(req, 'atualizar_exame.html', {
            'exame': exame,
            'pacientes': pacientes,
            'tipos': tipos,
            'error_message': "Erros: " + str(e),
        })
