from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Usuario, Tirador, Arma, TiradorArma, PoligonoTiro, LeccionTiro, FraccionTiro, Carril, ResultadoTiro
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import authenticate
import random
import string
import json
from .serializers import (
    UsuarioSerializer,
    TiradorSerializer,
    ArmaSerializer,
    TiradorArmaSerializer,
    PoligonoTiroSerializer,
    LeccionTiroSerializer,
    FraccionTiroSerializer,
    CarrilSerializer,
    ResultadoTiroSerializer
)
# Config para autenticación con Token personalizado
@method_decorator(csrf_exempt, name='dispatch')
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        rut = request.data.get('rut')
        password = request.data.get('password')
        user = authenticate(request, rut=rut, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'rol' : user.rol,
                'id' : user.id
            })
        else:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        
        
# ViewSet para Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# ViewSet para Tirador
class TiradorViewSet(viewsets.ModelViewSet):
    queryset = Tirador.objects.all()
    serializer_class = TiradorSerializer

# ViewSet para Arma
class ArmaViewSet(viewsets.ModelViewSet):
    queryset = Arma.objects.all()
    serializer_class = ArmaSerializer

# ViewSet para TiradorArma
class TiradorArmaViewSet(viewsets.ModelViewSet):
    queryset = TiradorArma.objects.all()
    serializer_class = TiradorArmaSerializer

# ViewSet para PoligonoTiro
class PoligonoTiroViewSet(viewsets.ModelViewSet):
    queryset = PoligonoTiro.objects.all()
    serializer_class = PoligonoTiroSerializer

# ViewSet para LeccionTiro
class LeccionTiroViewSet(viewsets.ModelViewSet):
    queryset = LeccionTiro.objects.all()
    serializer_class = LeccionTiroSerializer

# ViewSet para FraccionTiro
class FraccionTiroViewSet(viewsets.ModelViewSet):
    queryset = FraccionTiro.objects.all()
    serializer_class = FraccionTiroSerializer

# ViewSet para Carril
class CarrilViewSet(viewsets.ModelViewSet):
    queryset = Carril.objects.all()
    serializer_class = CarrilSerializer

# ViewSet para ResultadoTiro
class ResultadoTiroViewSet(viewsets.ModelViewSet):
    queryset = ResultadoTiro.objects.all()
    serializer_class = ResultadoTiroSerializer
    
    
@csrf_exempt
def recover_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rut = data.get('rut')
        correo = data.get('correo')

        try:
            user = Usuario.objects.get(correo=correo, rut=rut)
            # Generar una nueva contraseña
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.set_password(new_password)
            user.save()

            # Enviar la nueva contraseña por correo electrónico
            send_mail(
                'Recuperación de cuenta',
                f'Su nueva contraseña es: {new_password}',
                'tu-email@gmail.com',
                [correo],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Correo enviado'}, status=200)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)