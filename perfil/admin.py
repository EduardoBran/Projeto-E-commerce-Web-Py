from django.contrib import admin

from . import models
from .models import Perfil


class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'idade',
        'data_nascimento',
        'cidade',
        'estado'
    )
    list_display_links = (
        'id',
        'usuario'
    )


admin.site.register(Perfil, PerfilAdmin)
