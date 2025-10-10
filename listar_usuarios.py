"""
Listar usuarios del sistema para encontrar credenciales de admin
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Usuario

print("=" * 80)
print("USUARIOS REGISTRADOS EN EL SISTEMA")
print("=" * 80)

usuarios = Usuario.objects.all()
for usuario in usuarios:
    print(f"\nEmail: {usuario.email}")
    print(f"Rol: {usuario.rol}")
    print(f"Is Staff: {usuario.is_staff}")
    print(f"Is Superuser: {usuario.is_superuser}")
    print(f"Is Active: {usuario.is_active}")
    print("-" * 80)

print(f"\nTotal usuarios: {usuarios.count()}")
