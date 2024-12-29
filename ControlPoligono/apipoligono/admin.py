
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, PoligonoTiro, LeccionTiro, FraccionTiro, Tirador, Arma, Carril, ResultadoTiro

class TiradorInline(admin.StackedInline):
    model = Tirador
    can_delete = False
    verbose_name_plural = 'Tirador'
    fk_name = 'usuario'
    
# Define un UserAdmin personalizado
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('nombre','rut', 'apellido_paterno', 'apellido_materno', 'correo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Additional info', {'fields': ('rol', 'unidad_regimental', 'unidad_combate', 'unidad_fundamental')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','rut','nombre','apellido_paterno','apellido_materno','correo', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'correo', 'nombre', 'apellido_paterno','get_grado', 'is_staff')
    search_fields = ('username', 'nombre', 'apellido_paterno', 'correo')
    ordering = ('username',)
    
    def get_grado(self, obj):
        return obj.perfil_tirador.grado if hasattr(obj, 'perfil_tirador') else None
    get_grado.short_description = 'Grado'
    

    inlines = [TiradorInline]

# Registrar el modelo Usuario con el UserAdmin personalizado
admin.site.register(Usuario, UserAdmin)

# Registrar otros modelos
admin.site.register(PoligonoTiro)
admin.site.register(LeccionTiro)
admin.site.register(FraccionTiro)
admin.site.register(Tirador)
admin.site.register(Arma)
admin.site.register(Carril)
admin.site.register(ResultadoTiro)

# Registrar el modelo Group
#admin.site.register(Group)