from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Usuario,Arma,PoligonoTiro,LeccionTiro,FraccionTiro,ResultadoTiro)
from .serializers import (UsuarioSerializer,ArmaSerializer,PoligonoTiroSerializer,LeccionTiroSerializer,FraccionTiroSerializer,ResultadoTiroSerializer, RUTAuthTokenSerializer)


# ModelViewSet para cada modelo

#Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
"""     permission_classes = [IsAuthenticated]
 """
class ArmaViewSet(viewsets.ModelViewSet):
    queryset = Arma.objects.all()
    serializer_class = ArmaSerializer
"""     permission_classes = [IsAuthenticated]
 """
    
class PoligonoTiroViewSet(viewsets.ModelViewSet):
    queryset = PoligonoTiro.objects.all()
    serializer_class = PoligonoTiroSerializer
    #permission_classes = [IsAuthenticated]
 
    @action(detail=True, methods=['get'])
    def lecciones(self, request, pk=None):
        poligono = self.get_object()
        lecciones = LeccionTiro.objects.filter(id_poligono=poligono)
        serializer = LeccionTiroSerializer(lecciones, many=True)
        return Response(serializer.data)

class LeccionTiroViewSet(viewsets.ModelViewSet):
    queryset = LeccionTiro.objects.all()
    serializer_class = LeccionTiroSerializer
    #permission_classes = [IsAuthenticated]
     
    @action(detail=True, methods=['get'])
    def fracciones(self, request, pk=None):
        leccion = self.get_object()
        fracciones = FraccionTiro.objects.filter(id_leccion=leccion)
        serializer = FraccionTiroSerializer(fracciones, many=True)
        return Response(serializer.data)
    
class FraccionTiroViewSet(viewsets.ModelViewSet):
    queryset = FraccionTiro.objects.all()
    serializer_class = FraccionTiroSerializer
    #permission_classes = [IsAuthenticated]
    
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
"""     permission_classes = [IsAuthenticated]
 """    
    
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