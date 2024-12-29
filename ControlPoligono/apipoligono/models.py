from django.db import models
from django.contrib.auth.models import AbstractUser

# Extensión del modelo de Usuario de Django
class Usuario(AbstractUser):
    rut = models.CharField(max_length=20,)
    ROLES = [
        ('admin', 'Administrador'),
        ('limitado', 'Limitado'),
        ('tirador', 'Tirador'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES)
    nombre = models.CharField(max_length=50, default="")
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    unidad_regimental = models.CharField(max_length=100, null=True, blank=True)
    unidad_combate = models.CharField(max_length=100, null=True, blank=True)
    unidad_fundamental = models.CharField(max_length=100, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    
    def es_tirador(self):
        return self.rol == 'tirador'

# Modelo Tiradores
class Tirador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_tirador')
    grado = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido_paterno} (Tirador)"

# Modelo Armas
class Arma(models.Model):
    id_arma = models.AutoField(primary_key=True)
    tipo_arma = models.IntegerField()
    modelo_arma = models.CharField(max_length=50)
    numero_serie = models.CharField(max_length=50)

# Relación Tiradores_Armas
class TiradorArma(models.Model):
    id_arma = models.ForeignKey(Arma, on_delete=models.CASCADE)
    id_tirador = models.ForeignKey(Tirador, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_tirador', 'id_arma')

# Modelo PoligonoTiro
class PoligonoTiro(models.Model):
    id_poligono = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=30)
    carriles_maximos = models.IntegerField()
    distancia_maxima = models.IntegerField()

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

# Modelo FraccionesTiro
class FraccionTiro(models.Model):
    id_fraccion = models.AutoField(primary_key=True)
    id_leccion = models.ForeignKey(LeccionTiro, on_delete=models.CASCADE)
    numero_fraccion = models.IntegerField()

# Modelo Carriles
class Carril(models.Model):
    id_carril = models.AutoField(primary_key=True)
    id_fraccion = models.ForeignKey(FraccionTiro, on_delete=models.CASCADE)
    id_tirador = models.ForeignKey(Tirador, on_delete=models.CASCADE)
    id_arma = models.ForeignKey(Arma, on_delete=models.CASCADE)
    numero_carril = models.IntegerField()

# Modelo ResultadoTiro
class ResultadoTiro(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    id_carril = models.ForeignKey(Carril, on_delete=models.CASCADE)
    id_tirador = models.ForeignKey(Tirador, on_delete=models.CASCADE)
    id_arma = models.ForeignKey(Arma, on_delete=models.CASCADE)
    tiros_acertados = models.IntegerField()
    total_tiros = models.IntegerField()
