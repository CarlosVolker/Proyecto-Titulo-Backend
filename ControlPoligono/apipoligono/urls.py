from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UsuarioViewSet,
                    ArmaViewSet,
                    PoligonoTiroViewSet,
                    LeccionTiroViewSet,
                    FraccionTiroViewSet,
                    ResultadoTiroViewSet,
                    RUTAuthTokenView,
                    LogoutView,
                    ProtectedView,
                    iniciar_recuperacion,
                    crea_codigo,
                    comprobar_codigo,
                    cambiar_contrasena
                    )


# Crear un router para los ViewSets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'armas', ArmaViewSet)
router.register(r'poligonos', PoligonoTiroViewSet)
router.register(r'lecciones', LeccionTiroViewSet)
router.register(r'fracciones', FraccionTiroViewSet)
router.register(r'resultados', ResultadoTiroViewSet)


# URLs de la aplicación apipoligono
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', RUTAuthTokenView.as_view(), name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    
    # URLs para recuperación de contraseña
    #Primera solicitud solo con el rut
    path('recuperar/', iniciar_recuperacion, name='iniciar_recuperacion'),
    # Segunda solicitud con el rut y el correo
    path('recuperar/crear/', crea_codigo, name='crea_codigo'),
    # Segunda solicitud con el rut y el correo
    path('recuperar/comprobar/', comprobar_codigo, name='comprobar_codigo'),
    # Tercera solicitud con el digito verificador y la nueva contraseña
    path('recuperar/cambiar/', cambiar_contrasena, name='cambiar_contrasena'),
]
