"""
Sistema de permisos por rol para Veterinaria Huellitas

Define qué puede ver y hacer cada rol en el sistema.
"""

from rest_framework import permissions
from .choices import Rol


class PermisosPorRol:
    """
    Definición de permisos por rol para el frontend

    Cada permiso indica si el usuario puede:
    - ver: Ver el módulo/opción en el menú
    - crear: Crear nuevos registros
    - editar: Modificar registros existentes
    - eliminar: Eliminar/desactivar registros
    """

    # Módulos reales del sistema (basados en el menú de navegación):
    # dashboard, mascotas, historial_clinico, citas, vacunas,
    # trabajadores (incluye veterinarios), productos, servicios, configuracion

    PERMISOS = {
        Rol.ADMINISTRADOR: {
            'dashboard':        {'ver': True},
            'mascotas':         {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
            'historial_clinico':{'ver': True, 'crear': True, 'editar': True},
            'citas':            {'ver': True, 'crear': True, 'editar': True, 'eliminar': True, 'calendario_general': True, 'mi_calendario': True},
            'vacunas':          {'ver': True, 'crear': True, 'editar': True, 'eliminar': True, 'aplicar': True, 'historial': True},
            'trabajadores':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
            'productos':        {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
            'servicios':        {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
            'configuracion':    {'ver': True, 'editar': True},
        },

        Rol.VETERINARIO: {
            'dashboard':        {'ver': False},
            'mascotas':         {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
            'historial_clinico':{'ver': True,  'crear': True,  'editar': True},
            'citas':            {'ver': True,  'crear': False, 'editar': True,  'eliminar': False, 'calendario_general': False, 'mi_calendario': True},
            'vacunas':          {'ver': True,  'crear': False, 'editar': False, 'eliminar': False, 'aplicar': True, 'historial': True},
            'trabajadores':     {'ver': False},
            'productos':        {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
            'servicios':        {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
            'configuracion':    {'ver': False, 'editar': False},
        },

        Rol.RECEPCIONISTA: {
            'dashboard':        {'ver': False},
            'mascotas':         {'ver': True,  'crear': True,  'editar': True,  'eliminar': True},
            'historial_clinico':{'ver': True,  'crear': False, 'editar': False},
            'citas':            {'ver': True,  'crear': True,  'editar': True,  'eliminar': True,  'calendario_general': True, 'mi_calendario': False},
            'vacunas':          {'ver': True,  'crear': False, 'editar': False, 'eliminar': False, 'aplicar': False, 'historial': True},
            'trabajadores':     {'ver': False},
            'productos':        {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
            'servicios':        {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
            'configuracion':    {'ver': False, 'editar': False},
        },

        Rol.INVENTARIO: {
            'dashboard':        {'ver': False},
            'mascotas':         {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
            'historial_clinico':{'ver': False, 'crear': False, 'editar': False},
            'citas':            {'ver': False, 'crear': False, 'editar': False, 'eliminar': False, 'calendario_general': False, 'mi_calendario': False},
            'vacunas':          {'ver': True,  'crear': False, 'editar': False, 'eliminar': False, 'aplicar': False, 'historial': False},
            'trabajadores':     {'ver': False},
            'productos':        {'ver': True,  'crear': True,  'editar': True,  'eliminar': True},
            'servicios':        {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
            'configuracion':    {'ver': False, 'editar': False},
        },
    }

    @classmethod
    def obtener_permisos(cls, rol):
        """
        Obtiene los permisos de un rol específico.
        PRIORIDAD: Base de datos > Diccionario hardcodeado
        """
        # Primero intentar obtener de la base de datos
        try:
            from .models import PermisoRol as PermisoRolModel
            permisos_db = PermisoRolModel.objects.filter(rol=rol)

            if permisos_db.exists():
                # Convertir QuerySet a diccionario
                permisos_dict = {}
                for permiso in permisos_db:
                    permisos_dict[permiso.modulo] = permiso.permisos
                return permisos_dict
        except Exception as e:
            # Si falla (ej: tabla no existe), usar diccionario hardcodeado
            pass

        # Fallback al diccionario hardcodeado
        return cls.PERMISOS.get(rol, {})

    @classmethod
    def puede(cls, rol, modulo, accion='ver'):
        """
        Verifica si un rol puede realizar una acción en un módulo.
        PRIORIDAD: Base de datos > Diccionario hardcodeado

        Args:
            rol: El rol del usuario (admin, veterinario, recepcionista)
            modulo: El módulo a verificar (citas, mascotas, etc.)
            accion: La acción a verificar (ver, crear, editar, eliminar)

        Returns:
            bool: True si tiene permiso, False si no
        """
        # Primero intentar obtener de la base de datos
        try:
            from .models import PermisoRol as PermisoRolModel
            permiso_db = PermisoRolModel.objects.filter(rol=rol, modulo=modulo).first()

            if permiso_db:
                permisos_modulo = permiso_db.permisos
                if isinstance(permisos_modulo, dict):
                    return permisos_modulo.get(accion, False)
        except Exception as e:
            # Si falla, usar diccionario hardcodeado
            pass

        # Fallback al diccionario hardcodeado
        permisos_rol = cls.PERMISOS.get(rol, {})
        permisos_modulo = permisos_rol.get(modulo, {})

        # Si el módulo no existe en los permisos, no tiene acceso
        if isinstance(permisos_modulo, dict):
            return permisos_modulo.get(accion, False)

        return False


class EsAdministrador(permissions.BasePermission):
    """
    Permiso: Solo administradores
    """
    message = "Solo administradores pueden realizar esta acción"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == Rol.ADMINISTRADOR


class EsVeterinario(permissions.BasePermission):
    """
    Permiso: Solo veterinarios (incluye admin)
    """
    message = "Solo veterinarios pueden realizar esta acción"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol in [Rol.VETERINARIO, Rol.ADMINISTRADOR]


class EsRecepcionista(permissions.BasePermission):
    """
    Permiso: Solo recepcionistas (incluye admin)
    """
    message = "Solo recepcionistas pueden realizar esta acción"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol in [Rol.RECEPCIONISTA, Rol.ADMINISTRADOR]


class PuedeGestionarCitas(permissions.BasePermission):
    """
    Permiso: Puede gestionar citas (recepcionista o admin)
    """
    message = "No tiene permisos para gestionar citas"

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Administrador tiene todos los permisos
        if request.user.rol == Rol.ADMINISTRADOR:
            return True

        # Recepcionista puede gestionar citas
        if request.user.rol == Rol.RECEPCIONISTA:
            # GET siempre permitido
            if request.method in permissions.SAFE_METHODS:
                return True
            # POST, PATCH, DELETE permitidos para recepcionista
            return True

        # Veterinario solo puede ver sus propias citas
        if request.user.rol == Rol.VETERINARIO:
            return request.method in permissions.SAFE_METHODS

        return False


def make_permiso_api(modulo_nombre):
    """
    Fábrica de clases de permiso por módulo.

    Uso: permission_classes = [make_permiso_api('productos')]

    Mapeo HTTP → acción:
      GET    → ver
      POST   → crear
      PUT    → editar
      PATCH  → editar
      DELETE → eliminar
    """
    ACCION_MAP = {
        'GET': 'ver',
        'POST': 'crear',
        'PUT': 'editar',
        'PATCH': 'editar',
        'DELETE': 'eliminar',
    }

    class _PermisoRolAPI(permissions.BasePermission):
        modulo = modulo_nombre
        message = f"No tienes permiso para realizar esta acción en el módulo '{modulo_nombre}'."

        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False

            # Administrador tiene acceso total
            if request.user.rol == Rol.ADMINISTRADOR:
                return True

            accion = ACCION_MAP.get(request.method, 'ver')

            # Consultar PermisoRol en BD (prioridad sobre dict hardcodeado)
            try:
                from .models import PermisoRol as PermisoRolModel
                permiso = PermisoRolModel.objects.filter(
                    rol=request.user.rol,
                    modulo=self.modulo
                ).first()

                if permiso:
                    return permiso.permisos.get(accion, False)
            except Exception:
                pass

            # Fallback al diccionario hardcodeado
            permisos_rol = PermisosPorRol.PERMISOS.get(request.user.rol, {})
            permisos_modulo = permisos_rol.get(self.modulo, {})
            return permisos_modulo.get(accion, False)

    _PermisoRolAPI.__name__ = f'PermisoRolAPI_{modulo_nombre}'
    return _PermisoRolAPI


class EsAdministrador(permissions.BasePermission):
    """Solo el rol administrador puede acceder."""
    message = "Solo los administradores pueden realizar esta acción."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.rol == Rol.ADMINISTRADOR
        )


class PuedeAplicarVacunas(permissions.BasePermission):
    """
    Permiso: Puede aplicar vacunas (veterinario o admin)
    """
    message = "Solo veterinarios pueden aplicar vacunas"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol in [Rol.VETERINARIO, Rol.ADMINISTRADOR]
