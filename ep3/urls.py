from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('pacientes', views.pacientes, name="pacientes"),
    path('pacientes/new', views.new_paciente, name="new_paciente"),
    path('pacientes/create', views.create_paciente, name="create_paciente"),
    path('pacientes/<int:id>', views.paciente, name="paciente"),
    path('exames', views.exames, name="exames"),
    path('exames/<int:id>', views.exame, name="exame"),
    path('exames/new', views.new_exame, name="new_exame"),
    path('exames/create', views.create_exame, name="create_exame"),
    path('amostras', views.amostras, name="amostras"),
    path('amostras/<int:id>', views.amostra, name="amostra"),
    path('amostras/new', views.new_amostra, name="new_amostra"),
    path('amostras/create', views.create_amostra, name="create_amostra"),
]
