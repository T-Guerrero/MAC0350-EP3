from django.db import models

# Create your models here.


class Paciente(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome + ' - ' + self.cpf


class Exame(models.Model):
    EXAM_TYPES = (
        ('PCR', 'PCR'),
        ('Anticorpos', 'Anticorpos'),
    )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    virus = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=EXAM_TYPES)
    data_solicitacao = models.DateTimeField('Data de Solicitação')
    data_execucao = models.DateTimeField('Data de Execução')

    def __str__(self):
        return self.paciente.cpf + ' - ' + self.virus + ' | ' + str(self.data_solicitacao) + ' - ' + str(self.data_execucao)


class Amostra(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE)
    data_coleta = models.DateTimeField('Data de Coleta')
    tipo_material = models.CharField(max_length=30)

    def __str__(self):
        return self.paciente.cpf + ' - ' + self.exame.tipo + '/' + self.exame.virus + ' | ' + str(self.data_coleta)
