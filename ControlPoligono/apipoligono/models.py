from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

# Extensión del modelo de Usuario de Django
class Usuario(AbstractUser):
    id_usuario = models.BigAutoField(primary_key=True)
    rut = models.CharField(max_length=20, unique=True)
    ROLES = [
        ('admin', 'Administrador'),
        ('limitado', 'Limitado'),
        ('tirador', 'Tirador'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES)
    nombre = models.CharField(max_length=50, default="")
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    unidad_regimentaria = models.CharField(max_length=100, null=True, blank=True)
    unidad_combate = models.CharField(max_length=100, null=True, blank=True)
    unidad_fundamental = models.CharField(max_length=100, null=True, blank=True)
    correo = models.EmailField(max_length=100, null=True, blank=True)
    grado = models.CharField(max_length=50, null=True, blank=True) 
    
    def tiene_rol(self, rol):
        return self.rol == rol
    
    def __str__(self):
        return f"{self.grado} {self.apellido_paterno} {self.apellido_materno}, {self.nombre}"

# Modelo Armas
class Arma(models.Model):
    id_arma = models.AutoField(primary_key=True)
    tipo_arma = models.CharField(max_length=50)
    modelo_arma = models.CharField(max_length=50)
    numero_serie = models.CharField(max_length=50)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['modelo_arma', 'numero_serie'], name='unique_modelo_numeroserie')
        ]
        
    def __str__(self):
        return f"{self.tipo_arma} - {self.modelo_arma} - {self.numero_serie}" 

        
# Modelo PoligonoTiro
class PoligonoTiro(models.Model):
    id_poligono = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=30)
    carriles_maximos = models.IntegerField()
    distancia_maxima = models.IntegerField()
    
    def __str__(self):
        return f"Polígono: {self.nombre} - Ciudad: {self.ciudad}"

# Modelo LeccionesTiro
class LeccionTiro(models.Model):
    id_leccion = models.AutoField(primary_key=True)
    id_poligono = models.ForeignKey(PoligonoTiro, on_delete=models.CASCADE)
    fecha_tiro = models.DateField()
    numero_orden = models.CharField(max_length=15, null=True, blank=True)
    fecha_orden = models.DateField(null=True, blank=True)
    TIPOS_TIRO = [
        ('evaluacion', 'Evaluación'),
        ('entrenamiento', 'Entrenamiento'),
    ]
    tipo_tiro = models.CharField(max_length=20, choices=TIPOS_TIRO, null=True, blank=True)
    cant_tiros_cereo = models.IntegerField()
    cant_tiros_leccion = models.IntegerField()
    distancia = models.IntegerField()
    
    def __str__(self):
        return f"Fecha Tiro: {self.fecha_tiro} - Polígono: {self.id_poligono.nombre}"
    
# Modelo FraccionesTiro
class FraccionTiro(models.Model):
    id_fraccion = models.AutoField(primary_key=True)
    id_leccion = models.ForeignKey(LeccionTiro, on_delete=models.CASCADE)
    tiradores_totales = models.IntegerField()
    numero_fraccion = models.IntegerField()
    
    class Meta:
        constraints = [
            #models.UniqueConstraint(fields=['id_leccion', 'tiradores_totales'], name='unique_leccion_tiradores'),
            models.UniqueConstraint(fields=['id_leccion', 'numero_fraccion'], name='unique_leccion_numero_fraccion')
        ]
        
        
    def __str__(self):
        return f"Lección: {self.id_leccion.id_leccion} - Cantidad Tiradores: {self.tiradores_totales}"

# Modelo ResultadoTiro
class ResultadoTiro(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    id_fraccion = models.ForeignKey(FraccionTiro, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con Usuario
    id_arma = models.ForeignKey(Arma, on_delete=models.CASCADE)
    tiros_acertados = models.IntegerField()
    total_tiros = models.IntegerField()
    numero_carril = models.IntegerField(null=True, blank=True)


Usuario = get_user_model()
# Tabla para recuperar contraseña
class CodigoRecuperacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    #Esta funcion verifica si el código de recuperación ha expirado
    def esta_expirado(self):
        # aqui defino el tiempo de expiración
        tiempo_expiracion = timedelta(minutes=5)
        return timezone.now() > (self.creado_en + tiempo_expiracion)