from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('pacientes', views.pacientes, name="pacientes"),
    path('pacientes/<int:id>', views.paciente, name="paciente"),
    path('exames', views.exames, name="exames"),
    path('exames/<int:id>', views.exame, name="exame"),
    path('amostras', views.amostras, name="amostras"),
    path('amostras/<int:id>', views.amostra, name="amostra"),
]
