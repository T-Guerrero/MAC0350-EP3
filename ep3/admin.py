from django.contrib import admin
from .models import *
# Register your models here.


class AmostraInline(admin.TabularInline):
    model = Amostra
    extra = 1


class ExameWithAmostra(admin.ModelAdmin):
    inlines = (AmostraInline,)


admin.site.register(Paciente)
admin.site.register(Exame, ExameWithAmostra)
admin.site.register(Amostra)
