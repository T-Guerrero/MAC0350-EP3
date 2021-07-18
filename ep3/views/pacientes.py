from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .general import *


def pacientes(req):
    pacientes = Paciente.objects.all()
    keys = ['ID', 'CPF', 'Nome', 'Data de Nascimento', 'Endereço']
    return render(req, 'pacientes.html', {'pacientes': pacientes, 'keys': keys})


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
    try:
        cpf = req.POST['cpf'] or None
        nome = req.POST['nome'] or None
        data_nascimento = req.POST['data_nascimento'] or None
        endereco = req.POST['endereco'] or None
        paciente = Paciente.objects.create(
            cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
        return HttpResponseRedirect(reverse('pacientes'))
    except Exception as e:
        return render(req, 'inserir_paciente.html', {
            'paciente': paciente,
            'error_message': "Erros: " + str(e),
        })


def delete_paciente(_, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    return HttpResponseRedirect(reverse('pacientes'))


def edit_paciente(req, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.data_nascimento = str(paciente.data_nascimento)
    return render(req, 'atualizar_paciente.html', {'paciente': paciente})


def update_paciente(req, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.data_nascimento = str(paciente.data_nascimento)
    try:
        cpf = req.POST['cpf'] or None
        nome = req.POST['nome'] or None
        data_nascimento = req.POST['data_nascimento'] or None
        endereco = req.POST['endereco'] or None
        Paciente.objects.filter(id=id).update(cpf=cpf, nome=nome,
                                              data_nascimento=data_nascimento, endereco=endereco)
        return HttpResponseRedirect(reverse('paciente', kwargs={'id': id}))
    except Exception as e:
        return render(req, 'atualizar_paciente.html', {
            'paciente': paciente,
            'error_message': "Erros: " + str(e),
        })
