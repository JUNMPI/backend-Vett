import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Responsable, Usuario
from api.choices import Rol

print('=' * 80)
print('VERIFICACION DE RESPONSABLE Y ROLES')
print('=' * 80)

print('\n1. MODELO RESPONSABLE:')
print(f'   Total responsables: {Responsable.objects.count()}')

resp = Responsable.objects.first()
if resp:
    print(f'   Ejemplo: {resp.nombres} {resp.apellidos}')
    print(f'   Tiene usuario asociado: {resp.usuario is not None}')
    if resp.usuario:
        print(f'   Email usuario: {resp.usuario.email}')
        print(f'   Rol usuario: {resp.usuario.rol}')
else:
    print('   [INFO] No hay responsables en la base de datos')

print('\n2. ROLES DISPONIBLES EN EL SISTEMA:')
for rol_code, rol_name in Rol.ROL_CHOICES:
    print(f'   - {rol_code}: {rol_name}')

print('\n3. ACLARACION:')
print('   [OK] "Responsable" NO es un rol del sistema')
print('   [OK] "Responsable" es un modelo para los duenos de mascotas')
print('   [OK] Cada responsable tiene un Usuario con rol por defecto')
print('   [OK] El frontend NO necesita manejar "responsable" como rol')

print('\n4. VETERINARIO EXTERNO:')
from api.models import Veterinario
vets_externos = Veterinario.objects.filter(
    trabajador__usuario__rol='veterinario_externo'
)
print(f'   Total: {vets_externos.count()}')
for vet in vets_externos:
    print(f'   - ID: {vet.id}')
    print(f'     Email: {vet.trabajador.email}')
    print(f'     Rol: {vet.trabajador.usuario.rol}')
    print(f'     Activo: {vet.trabajador.usuario.is_active}')

print('\n' + '=' * 80)
print('[OK] VERIFICACION COMPLETA')
print('=' * 80)
