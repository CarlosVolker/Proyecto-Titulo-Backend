from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Usuario,Arma,PoligonoTiro,LeccionTiro,FraccionTiro,ResultadoTiro)
from .serializers import (UsuarioSerializer,ArmaSerializer,PoligonoTiroSerializer,LeccionTiroSerializer,FraccionTiroSerializer,ResultadoTiroSerializer, RUTAuthTokenSerializer)
from .utils.recuperacion_utilidades import iniciar_recuperacion, crea_codigo, cambiar_contrasena, comprobar_codigo


# ModelViewSet para cada modelo

#Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'], url_path='cambiar-contrasena')
    def cambiar_contrasena(self, request, pk=None):
        user = self.get_object()
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password')
        
        #Validar que la nueva contraseña esté presente
        if not new_password:
            return Response({'error': 'La nueva contraseña es requerida'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar nueva contraseña (opcional: longitud, 6 minimo)
        if len(new_password) < 6:
            return Response({'error': 'La contraseña debe tener al menos 6 caracteres'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validad contraseña actual
        if old_password is not None:
            if not user.check_password(old_password):
                return Response({'error': 'Contraseña actual incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Cifrar y actualizar la contraseña
        user.password = make_password(new_password)
        user.save()
        
        return Response({'detail': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)

class ArmaViewSet(viewsets.ModelViewSet):
    queryset = Arma.objects.all()
    serializer_class = ArmaSerializer
    permission_classes = [IsAuthenticated]
 
    def crear_arma(request):
        numero_serie = request.data.get('numero_serie')
        
        #Verificar si el arma ya existe
        arma_existente = Arma.objects.filter(numero_serie=numero_serie).first()
        
        if arma_existente:
            #Retornar arma existente
            serializer = ArmaSerializer(arma_existente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Si no existe, crea un arma
        serializer = ArmaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class PoligonoTiroViewSet(viewsets.ModelViewSet):
    queryset = PoligonoTiro.objects.all()
    serializer_class = PoligonoTiroSerializer
    permission_classes = [IsAuthenticated]
 
    @action(detail=True, methods=['get'])
    def lecciones(self, request, pk=None):
        poligono = self.get_object()
        lecciones = LeccionTiro.objects.filter(id_poligono=poligono)
        serializer = LeccionTiroSerializer(lecciones, many=True)
        return Response(serializer.data)

class LeccionTiroViewSet(viewsets.ModelViewSet):
    queryset = LeccionTiro.objects.all()
    serializer_class = LeccionTiroSerializer
    permission_classes = [IsAuthenticated]
     
    @action(detail=True, methods=['get'])
    def fracciones(self, request, pk=None):
        leccion = self.get_object()
        fracciones = FraccionTiro.objects.filter(id_leccion=leccion)
        serializer = FraccionTiroSerializer(fracciones, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='usuarios')
    def usuarios_listar(self, request, pk=None):
        #Obtener leccion
        leccion = self.get_object()
        
        # Obtener todas las fracciones asociadas a la leccion
        fracciones = FraccionTiro.objects.filter(id_leccion=leccion)
        
        # Obtener los tiradores/usuarios en esas fracciones
        resultados = ResultadoTiro.objects.filter(id_fraccion__in=fracciones)
        usuarios = Usuario.objects.filter(id_usuario__in=resultados.values('id_usuario'))
        
        # Serializar los usuarios
        serializer = UsuarioSerializer(usuarios, many=True)
        
        # Retorna la lista de usuarios
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='resultados')
    def resultados(self, request, pk=None):
        #Obtener leccion
        leccion = self.get_object()
        
        # Obtener todas las fracciones asociadas a la leccion
        fracciones = FraccionTiro.objects.filter(id_leccion=leccion)
        
        # Filtrar los resultados de tiro asociados a las fracciones
        resultados = ResultadoTiro.objects.filter(id_fraccion__in=fracciones)
        
        # Realizar los JOINs con los usuario, Arma y FraccionTiro
        data = []
        for resultado in resultados:
            usuario = Usuario.objects.get(id_usuario=resultado.id_usuario.id_usuario)
            arma = Arma.objects.get(id_arma=resultado.id_arma.id_arma)
            fraccion = FraccionTiro.objects.get(id_fraccion=resultado.id_fraccion.id_fraccion)
            
            # Diccionario de datos
            data.append({
                'RUT': usuario.rut,
                'Grado': usuario.grado,
                'Apellido_paterno': usuario.apellido_paterno,
                'Apellido_materno': usuario.apellido_materno,
                'Nombre': usuario.nombre,
                'Unidad Regimentaria': usuario.unidad_regimentaria,
                'Unidad de Combate': usuario.unidad_combate,
                'Unidad Fundamental': usuario.unidad_fundamental,
                'Tipo Arma': arma.tipo_arma,
                'Modelo de Arma': arma.modelo_arma,
                'Número de Serie': arma.numero_serie,
                'Carril': resultado.numero_carril,
                'Tiros Acertados': resultado.tiros_acertados,
                'Total Tiros': resultado.total_tiros,
            })
            
        # Retornar la lista de resultados
        return Response(data, status=status.HTTP_200_OK)
    
    
    
class FraccionTiroViewSet(viewsets.ModelViewSet):
    queryset = FraccionTiro.objects.all()
    serializer_class = FraccionTiroSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def tiradores(self, request, pk=None):
        fraccion = self.get_object()
        resultados = ResultadoTiro.objects.filter(id_fraccion=fraccion)
        usuarios = Usuario.objects.filter(id_usuario__in=resultados.values('id_usuario'))
        armas = Arma.objects.filter(id_arma__in=resultados.values('id_arma'))
        
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        armas_serializer = ArmaSerializer(armas, many=True)
        
        response_data = {
            'usuarios': usuarios_serializer.data,
            'armas': armas_serializer.data
        }
        return Response(response_data)
    
    @action(detail=True, methods=['get'])
    def resultados(self, request, pk=None):
        fraccion = self.get_object()
        resultados = ResultadoTiro.objects.filter(id_fraccion=fraccion)
        response_data = []
        
        for resultado in resultados:
            usuario = resultado.id_usuario
            arma = resultado.id_arma
            resultado_data = ResultadoTiroSerializer(resultado).data
            usuario_data = UsuarioSerializer(usuario).data
            arma_data = ArmaSerializer(arma).data
            
            response_data.append({
                'resultado' : resultado_data,
                'usuario': usuario_data,
                'arma': arma_data
            })
            
            
        return Response(response_data)
   
class ResultadoTiroViewSet(viewsets.ModelViewSet):
    queryset = ResultadoTiro.objects.all()
    serializer_class = ResultadoTiroSerializer
    permission_classes = [IsAuthenticated]
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({'Detalle: Esta es una vista protegida'})
    

class RUTAuthTokenView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = RUTAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id_usuario': user.pk,
            'rol': user.rol
            }, status=status.HTTP_200_OK)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'detail': 'Desconectado satisfactoriamente.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'detail': 'Token Invalido.'}, status=status.HTTP_400_BAD_REQUEST)
        