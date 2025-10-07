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

# 🚀 URLs del sistema profesional de citas
router.register(r'horarios-trabajo', HorarioTrabajoViewSet)
router.register(r'slots-tiempo', SlotTiempoViewSet)
router.register(r'citas-profesional', CitaProfesionalViewSet, basename='cita-profesional')

# URLs del sistema de vacunación
router.register(r'vacunas', VacunaViewSet)
router.register(r'historial-vacunacion', HistorialVacunacionViewSet)
router.register(r'historial-medico', HistorialMedicoViewSet)

# 🔐 URLs del sistema de gestión de permisos
router.register(r'permisos-rol', PermisoRolViewSet)

urlpatterns = router.urls + [
    # Autenticación
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('trabajadores/registro/', RegistrarTrabajadorView.as_view(), name='registro_trabajador'),

    # Permisos y usuario autenticado
    path('auth/permisos/', obtener_permisos_usuario, name='obtener_permisos'),
    path('auth/me/', obtener_info_usuario, name='info_usuario'),

    # Endpoints de alertas y dashboard
    path('alertas/', alertas_dashboard, name='alertas'),
    path('dashboard/alertas-vacunacion/', alertas_dashboard, name='alertas_dashboard'),

    # Endpoint para obtener veterinario externo
    path('veterinario-externo/', get_veterinario_externo, name='veterinario-externo'),
]
