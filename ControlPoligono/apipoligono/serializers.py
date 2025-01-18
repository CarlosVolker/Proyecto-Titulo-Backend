from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (Usuario,
                     Arma,
                     PoligonoTiro,
                     LeccionTiro,
                     FraccionTiro,
                     ResultadoTiro)

class UsuarioSerializer(serializers.ModelSerializer):
    habilitado = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = ('id_usuario','rut', 'grado', 'nombre', 'apellido_paterno',
                  'apellido_materno', 'unidad_regimentaria', 'unidad_combate',
                  'unidad_fundamental','correo', 'rol', 'habilitado')
        
    def get_habilitado(self, obj):
        # Verificar si el usuario tiene una contraseña asignada
        return bool(obj.password)

    def create(self, validated_data):
        # Asignar rut como username
        validated_data['username'] = validated_data['rut']
        return super().create(validated_data)
    
class ArmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arma
        fields = ('id_arma', 'tipo_arma', 'modelo_arma', 'numero_serie')

class PoligonoTiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoligonoTiro
        fields = ('id_poligono', 'nombre', 'ciudad', 'carriles_maximos', 'distancia_maxima')
        
class LeccionTiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeccionTiro
        fields = ('id_leccion', 'id_poligono', 'fecha_tiro', 'numero_orden','fecha_orden', 'tipo_tiro', 'cant_tiros_cereo', 'cant_tiros_leccion', 'distancia')
         
class FraccionTiroSerializer(serializers.ModelSerializer):
    id_leccion = serializers.PrimaryKeyRelatedField(queryset=LeccionTiro.objects.all())
    
    class Meta:
        model = FraccionTiro
        fields = ('id_fraccion', 'id_leccion', 'tiradores_totales', 'numero_fraccion')
               
class ResultadoTiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoTiro
        fields = ('id_resultado', 'id_fraccion', 'id_usuario', 'id_arma', 'tiros_acertados', 'total_tiros', 'numero_carril')
        
class RUTAuthTokenSerializer(serializers.Serializer):
    rut = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        rut = attrs.get('rut')
        password = attrs.get('password')

        if rut and password:
            user = authenticate(request=self.context.get('request'), rut=rut, password=password)

            if not user:
                msg = f'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "rut" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
class RecuperacionSerializer(serializers.Serializer):
    rut = serializers.CharField(max_length=12)
