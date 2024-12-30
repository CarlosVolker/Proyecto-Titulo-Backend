from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomAuthToken, recover_account
from .views import (
    UsuarioViewSet,
    TiradorViewSet, 
    ArmaViewSet, 
    TiradorArmaViewSet,
    PoligonoTiroViewSet,
    LeccionTiroViewSet, 
    FraccionTiroViewSet,
    CarrilViewSet, 
    ResultadoTiroViewSet
)

# Crear un router para los ViewSets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'tiradores', TiradorViewSet)
router.register(r'armas', ArmaViewSet)
router.register(r'tiradores-armas', TiradorArmaViewSet)
router.register(r'poligonos-tiro', PoligonoTiroViewSet)
router.register(r'lecciones-tiro', LeccionTiroViewSet)
router.register(r'fracciones-tiro', FraccionTiroViewSet)
router.register(r'carriles', CarrilViewSet)
router.register(r'resultados-tiro', ResultadoTiroViewSet)

# URLs de la aplicación apipoligono
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('recover/', recover_account, name='recover_account'),
]
