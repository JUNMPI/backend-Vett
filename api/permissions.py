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

    PERMISOS = {
        Rol.ADMINISTRADOR: {
            # Dashboard
            'dashboard': {'ver': True},

            # Gestión de Citas
            'citas': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
                'calendario_general': True,  # Ve todos los veterinarios
                'mi_calendario': True,
            },

            # Gestión de Mascotas
            'mascotas': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            # Gestión de Responsables
            'responsables': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            # Vacunación
            'vacunas': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
                'aplicar': True,
                'historial': True,
            },

            # Historial Clínico
            'historial_clinico': {
                'ver': True,
                'crear': True,
                'editar': True,
            },

            # Servicios
            'servicios': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            # Inventario/Productos
            'productos': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            # Usuarios y Trabajadores
            'usuarios': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            'trabajadores': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            # Veterinarios
            'veterinarios': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
                'horarios': True,  # Gestionar horarios de trabajo
                'slots': True,     # Generar slots
            },

            # Reportes
            'reportes': {
                'ver': True,
                'generar': True,
            },

            # Configuración
            'configuracion': {
                'ver': True,
                'editar': True,
            },
        },

        Rol.VETERINARIO: {
            # Dashboard (limitado)
            'dashboard': {'ver': True},

            # Gestión de Citas (solo lectura y sus propias citas)
            'citas': {
                'ver': True,
                'crear': False,  # No crea citas directamente
                'editar': True,  # Puede completar sus citas
                'eliminar': False,
                'calendario_general': False,  # NO ve otros veterinarios
                'mi_calendario': True,  # Solo ve SUS citas
            },

            # Gestión de Mascotas (solo lectura)
            'mascotas': {
                'ver': True,
                'crear': False,
                'editar': False,
                'eliminar': False,
            },

            # Gestión de Responsables (solo lectura)
            'responsables': {
                'ver': True,
                'crear': False,
                'editar': False,
                'eliminar': False,
            },

            # Vacunación (COMPLETO)
            'vacunas': {
                'ver': True,
                'crear': False,  # No crea vacunas, solo las aplica
                'editar': False,
                'eliminar': False,
                'aplicar': True,  # SÍ puede aplicar vacunas
                'historial': True,
            },

            # Historial Clínico (COMPLETO)
            'historial_clinico': {
                'ver': True,
                'crear': True,  # Puede agregar registros
                'editar': True,
            },

            # Servicios (solo lectura)
            'servicios': {
                'ver': True,
                'crear': False,
                'editar': False,
                'eliminar': False,
            },

            # Inventario/Productos (solo lectura)
            'productos': {
                'ver': True,
                'crear': False,
                'editar': False,
                'eliminar': False,
            },

            # NO VE: Usuarios, Trabajadores, Veterinarios
            'usuarios': {'ver': False},
            'trabajadores': {'ver': False},
            'veterinarios': {'ver': False},

            # Reportes (limitado)
            'reportes': {
                'ver': True,
                'generar': False,  # Solo ve, no genera
            },

            # NO VE: Configuración
            'configuracion': {'ver': False},
        },

        Rol.RESPONSABLE: {
            # RESPONSABLE NO TIENE ACCESO AL SISTEMA
            # Este rol se usa SOLO para registro interno de dueños de mascotas
            # No tienen login ni acceso a ningún módulo del sistema
            'dashboard': {'ver': False},
            'citas': {'ver': False},
            'mascotas': {'ver': False},
            'responsables': {'ver': False},
            'vacunas': {'ver': False},
            'historial_clinico': {'ver': False},
            'servicios': {'ver': False},
            'productos': {'ver': False},
            'usuarios': {'ver': False},
            'trabajadores': {'ver': False},
            'veterinarios': {'ver': False},
            'reportes': {'ver': False},
            'configuracion': {'ver': False},
        },

        Rol.RECEPCIONISTA: {
            # Dashboard
            'dashboard': {'ver': True},

            # Gestión de Citas (COMPLETO)
            'citas': {
                'ver': True,
                'crear': True,  # SÍ crea citas
                'editar': True,  # Puede reprogramar
                'eliminar': True,  # Puede cancelar
                'calendario_general': True,  # Ve TODOS los veterinarios
                'mi_calendario': False,
            },

            # Gestión de Mascotas (COMPLETO)
            'mascotas': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            # Gestión de Responsables (COMPLETO)
            'responsables': {
                'ver': True,
                'crear': True,
                'editar': True,
                'eliminar': True,
            },

            # Vacunación (solo lectura)
            'vacunas': {
                'ver': True,
                'crear': False,
                'editar': False,
                'eliminar': False,
                'aplicar': False,  # NO aplica vacunas
                'historial': True,  # Puede ver historial
            },

            # Historial Clínico (solo lectura)
            'historial_clinico': {
                'ver': True,
                'crear': False,
                'editar': False,
            },

            # Servicios (solo lectura)
            'servicios': {
                'ver': True,
                'crear': False,
                'editar': False,
                'eliminar': False,
            },

            # Inventario/Productos (solo lectura)
            'productos': {
                'ver': True,
                'crear': False,
                'editar': False,
                'eliminar': False,
            },

            # NO VE: Usuarios, Trabajadores, Veterinarios
            'usuarios': {'ver': False},
            'trabajadores': {'ver': False},
            'veterinarios': {'ver': False},

            # NO VE: Reportes
            'reportes': {'ver': False},

            # NO VE: Configuración
            'configuracion': {'ver': False},
        },
    }

    @classmethod
    def obtener_permisos(cls, rol):
        """
        Obtiene los permisos de un rol específico
        """
        return cls.PERMISOS.get(rol, {})

    @classmethod
    def puede(cls, rol, modulo, accion='ver'):
        """
        Verifica si un rol puede realizar una acción en un módulo

        Args:
            rol: El rol del usuario (admin, veterinario, recepcionista)
            modulo: El módulo a verificar (citas, mascotas, etc.)
            accion: La acción a verificar (ver, crear, editar, eliminar)

        Returns:
            bool: True si tiene permiso, False si no
        """
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


class PuedeAplicarVacunas(permissions.BasePermission):
    """
    Permiso: Puede aplicar vacunas (veterinario o admin)
    """
    message = "Solo veterinarios pueden aplicar vacunas"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol in [Rol.VETERINARIO, Rol.ADMINISTRADOR]
