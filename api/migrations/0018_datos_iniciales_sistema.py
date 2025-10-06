# Generated manually for initial system data

from django.db import migrations
from django.contrib.auth.hashers import make_password
import uuid


def crear_datos_iniciales(apps, schema_editor):
    """
    Crea los datos iniciales del sistema:
    1. Usuario Administrador por defecto
    2. TipoDocumento DNI (para Trabajador)
    3. Trabajador asociado al admin
    4. Veterinario Externo (para registros históricos)
    """
    Usuario = apps.get_model('api', 'Usuario')
    TipoDocumento = apps.get_model('api', 'TipoDocumento')
    Trabajador = apps.get_model('api', 'Trabajador')
    Veterinario = apps.get_model('api', 'Veterinario')

    # 1. Crear TipoDocumento DNI si no existe
    tipo_dni, _ = TipoDocumento.objects.get_or_create(
        nombre='DNI',
        defaults={'descripcion': 'Documento Nacional de Identidad'}
    )

    # 2. Crear Usuario Administrador por defecto
    admin_email = 'admin@huellitas.com'
    if not Usuario.objects.filter(email=admin_email).exists():
        admin_user = Usuario.objects.create(
            id=uuid.uuid4(),
            email=admin_email,
            password=make_password('admin123'),  # Contraseña por defecto
            rol='administrador',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        print(f"[OK] Usuario administrador creado: {admin_email}")

        # 3. Crear Trabajador asociado al admin
        trabajador_admin = Trabajador.objects.create(
            id=uuid.uuid4(),
            nombres='Administrador',
            apellidos='Sistema',
            email=admin_email,
            telefono='000000000',
            tipodocumento=tipo_dni,
            documento='00000000',
            usuario=admin_user,
            estado='Activo'
        )
        print(f"[OK] Trabajador admin creado: {trabajador_admin.nombres}")

    # 4. Crear Veterinario Externo (para registros históricos)
    vet_externo_email = 'veterinario.externo@sistema.com'
    if not Usuario.objects.filter(email=vet_externo_email).exists():
        # Obtener o crear especialidad "Externa"
        Especialidad = apps.get_model('api', 'Especialidad')
        especialidad_externa, _ = Especialidad.objects.get_or_create(
            nombre='Externa',
            defaults={'estado': 'Activo'}
        )

        # Crear usuario para veterinario externo
        vet_externo_user = Usuario.objects.create(
            id=uuid.uuid4(),
            email=vet_externo_email,
            password=make_password('externo_no_login'),  # No se usa para login
            rol='veterinario_externo',
            is_staff=False,
            is_superuser=False,
            is_active=False  # Inactivo, solo para referencia
        )
        print(f"[OK] Usuario veterinario externo creado: {vet_externo_email}")

        # Crear trabajador para veterinario externo
        trabajador_externo = Trabajador.objects.create(
            id=uuid.uuid4(),
            nombres='Veterinario',
            apellidos='Externo',
            email=vet_externo_email,
            telefono='000000000',
            tipodocumento=tipo_dni,
            documento='99999999',
            usuario=vet_externo_user,
            estado='Activo'
        )
        print(f"[OK] Trabajador externo creado: {trabajador_externo.nombres}")

        # Crear registro de veterinario externo
        veterinario_externo = Veterinario.objects.create(
            id=uuid.uuid4(),
            trabajador=trabajador_externo,
            especialidad=especialidad_externa
        )
        print(f"[OK] Veterinario externo creado: ID {veterinario_externo.id}")
        print(f"  - Usar este veterinario para registros de vacunas externas")

    print("\n" + "="*60)
    print("DATOS INICIALES CREADOS EXITOSAMENTE")
    print("="*60)
    print("\nCREDENCIALES DE ACCESO:")
    print(f"  Email:    admin@huellitas.com")
    print(f"  Password: admin123")
    print("\n[!] IMPORTANTE: Cambia la contrasena del admin despues del primer login")
    print("="*60)


def eliminar_datos_iniciales(apps, schema_editor):
    """
    Revierte la migración eliminando los datos creados
    """
    Usuario = apps.get_model('api', 'Usuario')

    # Eliminar usuarios creados
    Usuario.objects.filter(email='admin@huellitas.com').delete()
    Usuario.objects.filter(email='veterinario.externo@sistema.com').delete()

    print("[OK] Datos iniciales eliminados")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_mejorar_sistema_slots'),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales, eliminar_datos_iniciales),
    ]
