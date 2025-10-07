import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Usuario

print('=== USUARIOS EN BASE DE DATOS ===')
usuarios = Usuario.objects.all()
print(f'Total usuarios: {usuarios.count()}\n')

for u in usuarios:
    print(f'Email: {u.email}')
    print(f'Rol: {u.rol}')
    print(f'ID: {u.id}')
    print('---')
