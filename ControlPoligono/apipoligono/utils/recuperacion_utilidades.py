import random
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Usuario, CodigoRecuperacion
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.decorators import api_view
from ..serializers import RecuperacionSerializer



#Genera código de longitud 6
def generar_codigo_verificador():
    return str(random.randint(100000, 999999))

# Censura el correo perteneciente al rut consultado
def censurar_codigo(correo):
    nombre, dominio = correo.split('@')
    return f"{nombre[0]}{'*' * (len(nombre) - 1)}@{'*' * (len(dominio) - 2)}{dominio[-1]}"

# Obtiene el usuario por el rut o lanza error 404 si no existe
def obtener_usuario_por_rut(rut):
    return get_object_or_404(Usuario, rut=rut)

# Envía un correo con el código de verificación
def enviar_codigo_verificador(correo, codigo):
    send_mail(
        'Código de verificación',
        f'Su código de verificación es: {codigo}',
        'carlos_volkerdev@gmail.com',
        [correo],
        fail_silently=False
    )

# Creacion de funcion solo para que devuelva el correo censurado.
# Lo hice en el backend y no en el fontend, para que no se pueda capturar el correo real.
@api_view(['POST'])
def iniciar_recuperacion(request):
    # Recibe el rut del usuario
    serializer = RecuperacionSerializer(data=request.data)
    # si el rut es valido, devuelve el correo censurado perteneciente al rut
    if serializer.is_valid():
        rut = serializer.validated_data['rut']
        usuario = obtener_usuario_por_rut(rut)
        correo_censurado = censurar_codigo(usuario.correo)              
        return JsonResponse({'correo_censurado': correo_censurado})
    return JsonResponse({'mensaje': 'Datos inválidos', 'errores': serializer.errors}, status=400)

      
# Funcion que crea el codigo de verificacion y lo envia al correo del usuario
@api_view(['POST'])  
def crea_codigo(request):
    rut = request.data.get('rut')
    correo = request.data.get('correo')
    usuario = obtener_usuario_por_rut(rut)

    # Verifica si el correo coincide con el usuario(rut)
    if usuario.correo != correo:
        return JsonResponse({'mensaje': 'El correo no coincide con el RUT'}, status=400)
    # Elimina codigos de recuperacion anteriores si es q ya existen para este usuario
    CodigoRecuperacion.objects.filter(usuario=usuario).delete()
    # Genera nuevo código de verificacón
    codigo = generar_codigo_verificador()
    # Busca el codigo mas reciente
    CodigoRecuperacion.objects.create(usuario=usuario, codigo=codigo)
    
    # Enviar correo con el código
    enviar_codigo_verificador(usuario.correo, codigo)
    return JsonResponse({'mensaje': 'Código enviado correctamente.'})
 
# Verifica si el codigo es correcto o a expirado
@api_view(['POST'])
def comprobar_codigo(request):
    #if request.method == 'POST':
    rut = request.data.get('rut')
    codigo = request.data.get('codigo')
    # Obtengo el usuario con el rut
    usuario = obtener_usuario_por_rut(rut)
    
    # Busca codigo de recuperacion en la BD
    codigo_obj = CodigoRecuperacion.objects.filter(
        usuario=usuario,
        codigo=codigo,
        creado_en__gte=now() - timedelta(minutes=5)
    ).first()
    
    if not codigo_obj:
        return JsonResponse({'mensaje': 'Código incorrecto o expirado'}, status=400)
    
    return JsonResponse({'mensaje': 'Código correcto'})
 
# Cambia la contraseña del usuario despues de verificar el RUT y la existencia
#del codigo de recuperacion
@api_view(['POST'])    
def cambiar_contrasena(request):
    # Recibe el rut, el digito verificador y la nueva contraseña
    rut = request.data.get('rut')
    nueva_contrasena = request.data.get('nueva_contrasena')
    # Busca el usuario por el rut
    usuario = obtener_usuario_por_rut(rut)
    
    codigo_obj = CodigoRecuperacion.objects.filter(usuario=usuario).first()
    if not codigo_obj:
        return JsonResponse({'mensaje': 'No existe un código de verificación válido para este usuario'}, status=400)
    
    # Actualiza la contraseña del usuario con ciffrado
    usuario.password = make_password(nueva_contrasena)
    usuario.save()
    # Elimina codigos de recuperacion anteriores si es q ya existen para este usuario
    CodigoRecuperacion.objects.filter(usuario=usuario).delete()
    
    return JsonResponse({'mensaje': 'Contraseña actualizada correctamente.'})