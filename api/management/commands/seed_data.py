"""
Comando de inicialización del sistema Veterinaria Huellitas.

Uso:
    python manage.py seed_data
    python manage.py seed_data --admin-email admin@huellitas.com --admin-password admin1234

Siembra todos los datos indispensables para que el sistema funcione en cualquier entorno:
    1. TipoDocumento  → requerido para crear trabajadores
    2. Especialidad   → requerido para crear veterinarios
    3. Servicio       → requerido para crear citas (campo NOT NULL en Cita)
    4. PermisoRol     → requerido para el sistema de permisos por rol
    5. Usuario admin  → opcional, solo si no existe ningún administrador
"""

from django.core.management.base import BaseCommand
from django.db import transaction


TIPOS_DOCUMENTO = [
    'DNI',
    'Carnet de Extranjería',
    'Pasaporte',
    'RUC',
]

ESPECIALIDADES = [
    'Medicina General',
    'Cirugía',
    'Dermatología',
    'Cardiología',
    'Nutrición y Dietética',
    'Odontología Veterinaria',
    'Traumatología',
    'Oftalmología',
]

SERVICIOS = [
    {'nombre': 'Consulta General',        'categoria': 'consulta',     'precio': 50.00},
    {'nombre': 'Consulta de Emergencia',  'categoria': 'emergencia',   'precio': 120.00},
    {'nombre': 'Vacunación',              'categoria': 'vacunacion',   'precio': 35.00},
    {'nombre': 'Desparasitación',         'categoria': 'tratamiento',  'precio': 30.00},
    {'nombre': 'Cirugía Menor',           'categoria': 'cirugia',      'precio': 200.00},
    {'nombre': 'Cirugía Mayor',           'categoria': 'cirugia',      'precio': 500.00},
    {'nombre': 'Baño y Peluquería',       'categoria': 'estetica',     'precio': 40.00},
    {'nombre': 'Radiografía',             'categoria': 'diagnostico',  'precio': 80.00},
    {'nombre': 'Análisis de Laboratorio', 'categoria': 'diagnostico',  'precio': 60.00},
    {'nombre': 'Hospitalización (día)',   'categoria': 'hospitaliz',   'precio': 100.00},
]

PERMISOS_POR_ROL = {
    'administrador': {
        'dashboard':         {'ver': True},
        'mascotas':          {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'historial_clinico': {'ver': True, 'crear': True, 'editar': True},
        'citas':             {'ver': True, 'crear': True, 'editar': True, 'eliminar': True,
                              'calendario_general': True, 'mi_calendario': True},
        'vacunas':           {'ver': True, 'crear': True, 'editar': True, 'eliminar': True,
                              'aplicar': True, 'historial': True},
        'trabajadores':      {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'productos':         {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'servicios':         {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'configuracion':     {'ver': True, 'editar': True},
    },
    'veterinario': {
        'dashboard':         {'ver': False},
        'mascotas':          {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
        'historial_clinico': {'ver': True,  'crear': True,  'editar': True},
        'citas':             {'ver': True,  'crear': False, 'editar': True,  'eliminar': False,
                              'calendario_general': False, 'mi_calendario': True},
        'vacunas':           {'ver': True,  'crear': False, 'editar': False, 'eliminar': False,
                              'aplicar': True, 'historial': True},
        'trabajadores':      {'ver': False},
        'productos':         {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
        'servicios':         {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
        'configuracion':     {'ver': False, 'editar': False},
    },
    'recepcionista': {
        'dashboard':         {'ver': False},
        'mascotas':          {'ver': True,  'crear': True,  'editar': True,  'eliminar': True},
        'historial_clinico': {'ver': True,  'crear': False, 'editar': False},
        'citas':             {'ver': True,  'crear': True,  'editar': True,  'eliminar': True,
                              'calendario_general': True, 'mi_calendario': False},
        'vacunas':           {'ver': True,  'crear': False, 'editar': False, 'eliminar': False,
                              'aplicar': False, 'historial': True},
        'trabajadores':      {'ver': False},
        'productos':         {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
        'servicios':         {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
        'configuracion':     {'ver': False, 'editar': False},
    },
    'inventario': {
        'dashboard':         {'ver': False},
        'mascotas':          {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
        'historial_clinico': {'ver': False, 'crear': False, 'editar': False},
        'citas':             {'ver': False, 'crear': False, 'editar': False, 'eliminar': False,
                              'calendario_general': False, 'mi_calendario': False},
        'vacunas':           {'ver': True,  'crear': False, 'editar': False, 'eliminar': False,
                              'aplicar': False, 'historial': False},
        'trabajadores':      {'ver': False},
        'productos':         {'ver': True,  'crear': True,  'editar': True,  'eliminar': True},
        'servicios':         {'ver': True,  'crear': False, 'editar': False, 'eliminar': False},
        'configuracion':     {'ver': False, 'editar': False},
    },
}


class Command(BaseCommand):
    help = 'Inicializa el sistema con datos indispensables para su funcionamiento'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-email',
            default='admin@huellitas.com',
            help='Email del usuario administrador (default: admin@huellitas.com)',
        )
        parser.add_argument(
            '--admin-password',
            default='admin1234',
            help='Contraseña del usuario administrador (default: admin1234)',
        )
        parser.add_argument(
            '--skip-admin',
            action='store_true',
            help='No crear usuario administrador aunque no exista ninguno',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== Veterinaria Huellitas - Seed Data ==='
        ))

        with transaction.atomic():
            self._seed_tipos_documento()
            self._seed_especialidades()
            self._seed_servicios()
            self._seed_permisos_rol()
            if not options['skip_admin']:
                self._seed_admin(options['admin_email'], options['admin_password'])

        self.stdout.write(self.style.SUCCESS('\nSeed completado exitosamente.\n'))

    def _seed_tipos_documento(self):
        from api.models import TipoDocumento
        self.stdout.write('  Tipos de documento...', ending=' ')
        creados = 0
        for nombre in TIPOS_DOCUMENTO:
            _, created = TipoDocumento.objects.get_or_create(nombre=nombre)
            if created:
                creados += 1
        self.stdout.write(self.style.SUCCESS(f'OK ({creados} nuevos, {len(TIPOS_DOCUMENTO) - creados} ya existían)'))

    def _seed_especialidades(self):
        from api.models import Especialidad
        self.stdout.write('  Especialidades...', ending=' ')
        creados = 0
        for nombre in ESPECIALIDADES:
            _, created = Especialidad.objects.get_or_create(nombre=nombre)
            if created:
                creados += 1
        self.stdout.write(self.style.SUCCESS(f'OK ({creados} nuevos, {len(ESPECIALIDADES) - creados} ya existían)'))

    def _seed_servicios(self):
        from api.models import Servicio
        self.stdout.write('  Servicios...', ending=' ')
        creados = 0
        for datos in SERVICIOS:
            _, created = Servicio.objects.get_or_create(
                nombre=datos['nombre'],
                defaults={'categoria': datos['categoria'], 'precio': datos['precio']}
            )
            if created:
                creados += 1
        self.stdout.write(self.style.SUCCESS(f'OK ({creados} nuevos, {len(SERVICIOS) - creados} ya existían)'))

    def _seed_permisos_rol(self):
        from api.models import PermisoRol
        self.stdout.write('  Permisos por rol...', ending=' ')
        creados = 0
        actualizados = 0
        for rol, modulos in PERMISOS_POR_ROL.items():
            for modulo, permisos in modulos.items():
                obj, created = PermisoRol.objects.get_or_create(
                    rol=rol,
                    modulo=modulo,
                    defaults={'permisos': permisos}
                )
                if created:
                    creados += 1
                # Si ya existe pero no tiene todas las claves, actualizar
                elif not all(k in obj.permisos for k in permisos):
                    obj.permisos = permisos
                    obj.save()
                    actualizados += 1
        total = sum(len(m) for m in PERMISOS_POR_ROL.values())
        self.stdout.write(self.style.SUCCESS(
            f'OK ({creados} nuevos, {actualizados} actualizados, {total - creados - actualizados} sin cambios)'
        ))

    def _seed_admin(self, email, password):
        from api.models import Usuario
        self.stdout.write('  Usuario administrador...', ending=' ')

        # Si ya existe algún admin, no crear otro
        if Usuario.objects.filter(rol='administrador').exists():
            self.stdout.write(self.style.WARNING('SKIP (ya existe un administrador)'))
            return

        if Usuario.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'SKIP ({email} ya existe)'))
            return

        u = Usuario(
            email=email,
            rol='administrador',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        u.set_password(password)
        u.save()
        self.stdout.write(self.style.SUCCESS(f'OK → {email} / {password}'))
        self.stdout.write(self.style.WARNING(
            '  ADVERTENCIA: Cambia la contrasena del admin en produccion.'
        ))
