
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Usuario,
                     Arma, 
                     PoligonoTiro, 
                     LeccionTiro,
                     FraccionTiro,
                     ResultadoTiro)



class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['nombre', 'rut', 'grado', 'apellido_paterno']
    list_filter = ['rol']
    search_fields = ['rut', 'nombre', 'apellido_paterno', 'apellido_materno']
    
    fieldsets = (
        (None, {'fields': ('rut', 'password')}),
        ('Información Personal', {'fields': ('grado','nombre', 'apellido_paterno', 'apellido_materno', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

# Personalizo la vista de PoligonoTiro en el panel de administración  
# Puedo hacerlo a cualquier modelo que haya creado
class PoligonoTiroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'carriles_maximos', 'distancia_maxima']
    search_fields = ['ciudad']


# Registrar el modelo Usuario con el UserAdmin personalizado
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Arma)
admin.site.register(PoligonoTiro, PoligonoTiroAdmin)
admin.site.register(LeccionTiro)
admin.site.register(FraccionTiro)
admin.site.register(ResultadoTiro)


# Registrar el modelo Group
#admin.site.register(Group)