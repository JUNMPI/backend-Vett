"""
Actualizar password del admin
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Usuario

# Buscar admin
admin = Usuario.objects.get(email='admin@huellitas.com')
admin.set_password('admin123')
admin.save()

print("[OK] Password actualizado para admin@huellitas.com")
print("Email: admin@huellitas.com")
print("Password: admin123")
