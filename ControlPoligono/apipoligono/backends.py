from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class RUTAuthBackend(BaseBackend):
    def authenticate(self, request, rut=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(rut=rut)
            if user.check_password(password):
                return user
            else:
                print("Contraseña incorrecta para RUT: {rut}")
        except User.DoesNotExist:
            print(f"Usuario con RUT: {rut} no encontrado ")
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None