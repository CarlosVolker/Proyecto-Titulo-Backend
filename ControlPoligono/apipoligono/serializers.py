from rest_framework import serializers
from .models import Usuario, Tirador, Arma, TiradorArma, PoligonoTiro, LeccionTiro, FraccionTiro, Carril, ResultadoTiro

# Serializer para Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    grado = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre', 'apellido_paterno','apellido_materno', 'rut','correo', 'rol', 'unidad_regimental', 'unidad_combate', 'unidad_fundamental', 'grado']
        
    def get_grado(self, obj):
        return obj.perfil_tirador.grado if hasattr(obj, 'perfil_tirador') else None


# Serializer para Tirador
class TiradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tirador
        fields = ['id_tirador','grado' ]

# Serializer para Arma
class ArmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arma
        fields = ['id_arma', 'tipo_arma', 'modelo_arma', 'numero_serie']

# Serializer para TiradorArma
class TiradorArmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiradorArma
        fields = ['id_arma', 'id_tirador']

# Serializer para PoligonoTiro
class PoligonoTiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoligonoTiro
        fields = ['id_poligono', 'nombre', 'ciudad', 'carriles_maximos', 'distancia_maxima']

# Serializer para LeccionTiro
class LeccionTiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeccionTiro
        fields = ['id_leccion', 'id_poligono', 'fecha_tiro', 'numero_orden', 'fecha_orden', 'tipo_tiro', 'cant_tiros_cereo', 'cant_tiros_leccion', 'distancia']

# Serializer para FraccionTiro
class FraccionTiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraccionTiro
        fields = ['id_fraccion', 'id_leccion', 'numero_fraccion']

# Serializer para Carril
class CarrilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carril
        fields = ['id_carril', 'id_fraccion', 'id_tirador', 'id_arma', 'numero_carril']

# Serializer para ResultadoTiro
class ResultadoTiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoTiro
        fields = ['id_resultado', 'id_carril', 'id_tirador', 'id_arma', 'tiros_acertados', 'total_tiros']
