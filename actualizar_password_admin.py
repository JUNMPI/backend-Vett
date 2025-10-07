import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Usuario

# Actualizar contraseña del admin
print('=== ACTUALIZANDO CONTRASENA DEL ADMIN ===\n')

try:
    admin = Usuario.objects.get(email='admin@huellitas.com')
    admin.set_password('admin12345')
    admin.save()

    print('[OK] Contrasena actualizada exitosamente')
    print('\n' + '='*50)
    print('CREDENCIALES ACTUALIZADAS')
    print('='*50)
    print(f'\nEmail: admin@huellitas.com')
    print(f'Contrasena: admin12345')
    print(f'Rol: administrador')
    print('='*50)

except Usuario.DoesNotExist:
    print('[ERROR] Usuario admin no encontrado')
except Exception as e:
    print(f'[ERROR] Error: {e}')
