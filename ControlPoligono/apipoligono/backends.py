from django.contrib.auth.backends import BaseBackend
from .models import Usuario

class RUTAuthBackend(BaseBackend):
    def authenticate(self, request, rut=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(rut=rut)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
        
#------------------------------------------------------------
# Este archivo maneja la lógica de autenticación de la aplicación. (por rut)