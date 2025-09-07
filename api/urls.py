from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'productos', ProductoViewSet) 
router.register(r'mascotas', MascotaViewSet)
router.register(r'responsables', ResponsableViewSet)
router.register(r'consultorios', ConsultorioViewSet)
router.register(r'tipos-documento', TipoDocumentoViewSet)
router.register(r'trabajadores', TrabajadorViewSet)
router.register(r'veterinarios', VeterinarioViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'citas', CitaViewSet)
# 🐾 URLs del sistema de vacunación
router.register(r'vacunas', VacunaViewSet)
router.register(r'historial-vacunacion', HistorialVacunacionViewSet)
router.register(r'historial-medico', HistorialMedicoViewSet)

urlpatterns = router.urls + [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('trabajadores/registro/', RegistrarTrabajadorView.as_view(), name='registro_trabajador'),
]
