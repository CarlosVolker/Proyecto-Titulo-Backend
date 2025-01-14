from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apipoligono.models import ResultadoTiro, FraccionTiro


# Se ejecuta cada vez que se guarda un resultado de tiro
# lo que hace es actualizar la cantidad de tiradores totales en la fraccion
@receiver(post_save, sender=ResultadoTiro)
def actualizar_tiradores_totales(sender, instance, **kwargs):
    fraccion = instance.id_fraccion
    tiradores_totaltes = ResultadoTiro.objects.filter(id_fraccion=fraccion).values('id_usuario').distinct().count()
    fraccion.tiradores_totales = tiradores_totaltes
    fraccion.save()
    
# Se ejecuta cada vez que se elimina un resultado de tiro
# Actualiza la cantidad de tiradores en la fraccion
@receiver(post_delete, sender=ResultadoTiro)
def actualizar_tiradores_totales_eliminacion(sender, instance, **kwargs):
    fraccion = instance.id_fraccion
    tiradores_totaltes = ResultadoTiro.objects.filter(id_fraccion=fraccion).values('id_usuario').distinct().count()
    fraccion.tiradores_totales = tiradores_totaltes
    fraccion.save()