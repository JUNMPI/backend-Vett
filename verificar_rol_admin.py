"""
Verificar y corregir el rol del administrador
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Usuario, PermisoRol
from api.choices import Rol

print("=" * 80)
print("VERIFICACION DE ROLES")
print("=" * 80)

# Buscar admin
admin = Usuario.objects.get(email='admin@huellitas.com')
print(f"\nUsuario admin:")
print(f"  Email: {admin.email}")
print(f"  Rol actual: '{admin.rol}'")
print(f"  Rol esperado: '{Rol.ADMINISTRADOR}'")
print(f"  Coinciden: {admin.rol == Rol.ADMINISTRADOR}")

# Verificar permisos con rol actual
print(f"\nPermisos con rol '{admin.rol}':")
permisos_actual = PermisoRol.objects.filter(rol=admin.rol)
print(f"  Total: {permisos_actual.count()}")

# Verificar permisos con rol esperado
print(f"\nPermisos con rol '{Rol.ADMINISTRADOR}':")
permisos_esperado = PermisoRol.objects.filter(rol=Rol.ADMINISTRADOR)
print(f"  Total: {permisos_esperado.count()}")
for permiso in permisos_esperado[:5]:
    print(f"    - {permiso.modulo}")

# Corregir rol si es necesario
if admin.rol != Rol.ADMINISTRADOR:
    print(f"\n[CORRIGIENDO] Cambiando rol de '{admin.rol}' a '{Rol.ADMINISTRADOR}'")
    admin.rol = Rol.ADMINISTRADOR
    admin.save()
    print("[OK] Rol corregido")
else:
    print("\n[OK] Rol ya es correcto")

# Verificar otros usuarios con roles incorrectos
print("\n" + "=" * 80)
print("VERIFICANDO TODOS LOS USUARIOS")
print("=" * 80)

roles_validos = [
    Rol.ADMINISTRADOR,
    Rol.VETERINARIO,
    Rol.RECEPCIONISTA,
    Rol.INVENTARIO,
    Rol.RESPONSABLE,
    Rol.VETERINARIO_EXTERNO
]

usuarios_incorrectos = Usuario.objects.exclude(rol__in=roles_validos)
print(f"\nUsuarios con roles no estandarizados: {usuarios_incorrectos.count()}")

for usuario in usuarios_incorrectos:
    print(f"\n  Email: {usuario.email}")
    print(f"  Rol actual: '{usuario.rol}'")

    # Intentar normalizar
    rol_lower = usuario.rol.lower()
    if 'admin' in rol_lower:
        nuevo_rol = Rol.ADMINISTRADOR
    elif 'veterinario' in rol_lower and 'externo' not in rol_lower:
        nuevo_rol = Rol.VETERINARIO
    elif 'recep' in rol_lower:
        nuevo_rol = Rol.RECEPCIONISTA
    elif 'responsable' in rol_lower:
        nuevo_rol = Rol.RESPONSABLE
    elif 'inventario' in rol_lower:
        nuevo_rol = Rol.INVENTARIO
    elif 'externo' in rol_lower:
        nuevo_rol = Rol.VETERINARIO_EXTERNO
    else:
        nuevo_rol = None

    if nuevo_rol:
        print(f"  [CORRIGIENDO] -> '{nuevo_rol}'")
        usuario.rol = nuevo_rol
        usuario.save()
    else:
        print(f"  [ADVERTENCIA] No se pudo normalizar")

print("\n" + "=" * 80)
print("SCRIPT COMPLETADO")
print("=" * 80)
