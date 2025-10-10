"""
Script para verificar y crear permisos de dashboard faltantes
"""
import os
import django
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import PermisoRol
from api.choices import Rol

print("=" * 80)
print("VERIFICACION DE PERMISOS DE DASHBOARD")
print("=" * 80)

# Verificar permisos actuales de dashboard
print("\nPERMISOS ACTUALES DE DASHBOARD EN BASE DE DATOS:")
print("-" * 80)

permisos_dashboard = PermisoRol.objects.filter(modulo='dashboard')
if permisos_dashboard.exists():
    for permiso in permisos_dashboard:
        print(f"[OK] Rol: {permiso.rol:<20} | Modulo: {permiso.modulo:<15} | Permisos: {permiso.permisos}")
else:
    print("[ERROR] NO HAY PERMISOS DE DASHBOARD EN LA BASE DE DATOS")

# Verificar todos los módulos para administrador
print("\nTODOS LOS MODULOS PARA ADMINISTRADOR:")
print("-" * 80)
permisos_admin = PermisoRol.objects.filter(rol=Rol.ADMINISTRADOR)
for permiso in permisos_admin:
    print(f"  * {permiso.modulo:<20} | {permiso.permisos}")

print(f"\nTotal modulos configurados para administrador: {permisos_admin.count()}")

# Crear permisos de dashboard si no existen
print("\n" + "=" * 80)
print("CREANDO PERMISOS DE DASHBOARD FALTANTES...")
print("=" * 80)

roles_permisos = {
    Rol.ADMINISTRADOR: {'ver': True},
    Rol.VETERINARIO: {'ver': True},  # Veterinarios tambien necesitan dashboard
    Rol.RECEPCIONISTA: {'ver': True},  # Recepcionistas tambien necesitan dashboard
    Rol.INVENTARIO: {'ver': True},  # Inventario tambien necesita dashboard
}

created_count = 0
updated_count = 0

for rol, permisos in roles_permisos.items():
    permiso_obj, created = PermisoRol.objects.get_or_create(
        rol=rol,
        modulo='dashboard',
        defaults={
            'permisos': permisos,
            'descripcion_modulo': 'Panel principal del sistema'
        }
    )

    if created:
        print(f"[CREADO] {rol:<20} | dashboard | {permisos}")
        created_count += 1
    else:
        # Actualizar si existe pero tiene permisos incorrectos
        if permiso_obj.permisos != permisos:
            permiso_obj.permisos = permisos
            permiso_obj.save()
            print(f"[ACTUALIZADO] {rol:<20} | dashboard | {permisos}")
            updated_count += 1
        else:
            print(f"[YA EXISTE] {rol:<20} | dashboard | {permisos}")

print("\n" + "=" * 80)
print("RESUMEN:")
print("=" * 80)
print(f"Permisos creados: {created_count}")
print(f"Permisos actualizados: {updated_count}")
print(f"Permisos sin cambios: {len(roles_permisos) - created_count - updated_count}")

# Verificar resultado final
print("\n" + "=" * 80)
print("VERIFICACION FINAL - PERMISOS DE DASHBOARD:")
print("=" * 80)

permisos_dashboard_final = PermisoRol.objects.filter(modulo='dashboard').order_by('rol')
for permiso in permisos_dashboard_final:
    print(f"  [OK] {permiso.rol:<20} | {permiso.permisos}")

print("\nSCRIPT COMPLETADO")
print("=" * 80)
